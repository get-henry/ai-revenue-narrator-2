#!/usr/bin/env python3
"""
AI Revenue Report Narrator
Takes raw CRM/sales CSV data and writes a plain-English weekly revenue summary
with anomaly callouts. No more Monday morning report writing.
"""

import anthropic
import csv
import json
from dotenv import load_dotenv
load_dotenv()
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path


SYSTEM_PROMPT = """You are a sharp revenue analyst writing for a VP of Sales or CRO.
Your job is to translate raw numbers into a clear, confident narrative.
Be direct. Lead with the most important insight. No filler sentences.
Flag anomalies clearly. Use plain English, not jargon."""


def load_csv(filepath: str) -> list[dict]:
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))


def compute_metrics(rows: list[dict]) -> dict:
    """Compute summary metrics from CRM data rows."""
    metrics = {
        "total_deals": len(rows),
        "total_revenue": 0,
        "won": 0,
        "lost": 0,
        "in_progress": 0,
        "by_stage": defaultdict(lambda: {"count": 0, "value": 0}),
        "by_rep": defaultdict(lambda: {"won": 0, "revenue": 0, "pipeline": 0}),
        "by_source": defaultdict(int),
        "avg_deal_size": 0,
        "win_rate": 0,
        "anomalies": [],
    }

    revenues = []
    for row in rows:
        try:
            value = float(row.get("amount", row.get("deal_value", row.get("value", 0))) or 0)
        except (ValueError, TypeError):
            value = 0

        stage = row.get("stage", row.get("status", "Unknown")).strip()
        rep = row.get("owner", row.get("rep", row.get("assigned_to", "Unassigned"))).strip()
        source = row.get("lead_source", row.get("source", "Unknown")).strip()

        metrics["by_stage"][stage]["count"] += 1
        metrics["by_stage"][stage]["value"] += value
        metrics["by_source"][source] += 1

        stage_lower = stage.lower()
        if any(w in stage_lower for w in ["won", "closed won", "closed-won"]):
            metrics["won"] += 1
            metrics["total_revenue"] += value
            metrics["by_rep"][rep]["won"] += 1
            metrics["by_rep"][rep]["revenue"] += value
            revenues.append(value)
        elif any(w in stage_lower for w in ["lost", "closed lost", "closed-lost", "disqualified"]):
            metrics["lost"] += 1
        else:
            metrics["in_progress"] += 1
            metrics["by_rep"][rep]["pipeline"] += value

    closed = metrics["won"] + metrics["lost"]
    metrics["win_rate"] = round(metrics["won"] / closed * 100, 1) if closed > 0 else 0
    metrics["avg_deal_size"] = round(metrics["total_revenue"] / metrics["won"], 0) if metrics["won"] > 0 else 0

    # Anomaly detection
    if revenues:
        avg = sum(revenues) / len(revenues)
        for row in rows:
            try:
                value = float(row.get("amount", row.get("deal_value", row.get("value", 0))) or 0)
            except (ValueError, TypeError):
                value = 0
            if value > avg * 3:
                metrics["anomalies"].append(f"Outlier deal: {row.get('company', row.get('account', 'Unknown'))} at ${value:,.0f} (3x+ avg deal size)")

    if metrics["win_rate"] < 20 and closed > 5:
        metrics["anomalies"].append(f"Win rate at {metrics['win_rate']}% — significantly below healthy range (25–35%)")

    return metrics


def build_prompt(metrics: dict, period: str, raw_row_count: int) -> str:
    return f"""Write a weekly revenue report narrative based on these CRM metrics.

Period: {period}
Total deals in dataset: {raw_row_count}

## Metrics
- Closed Won: {metrics['won']} deals | ${metrics['total_revenue']:,.0f} total revenue
- Closed Lost: {metrics['lost']} deals
- In Progress: {metrics['in_progress']} deals
- Win Rate: {metrics['win_rate']}%
- Avg Deal Size: ${metrics['avg_deal_size']:,.0f}

## By Stage
{json.dumps(dict(metrics['by_stage']), indent=2)}

## By Rep
{json.dumps(dict(metrics['by_rep']), indent=2)}

## Lead Sources
{json.dumps(dict(metrics['by_source']), indent=2)}

## Flagged Anomalies
{json.dumps(metrics['anomalies']) if metrics['anomalies'] else 'None detected'}

---

Write the narrative report with these sections:

### This Week's Headline
One punchy sentence: the single most important thing that happened.

### Revenue Summary
Plain-English summary of closed revenue, win rate, and deal volume.

### Pipeline Health
What's moving, what's stalling, where the risk is.

### Rep Highlights
Who's carrying the number. Who needs attention.

### Anomalies & Watch Items
Flag anything that doesn't look right. Be direct.

### Next Week's Focus
2-3 specific actions the team should prioritize.

Keep the whole thing under 400 words. Write like you're briefing a CRO at 8am Monday.
"""


def narrate(input_csv: str, period: str = None) -> None:
    if period is None:
        end = date.today()
        start = end - timedelta(days=7)
        period = f"{start.strftime('%b %d')} – {end.strftime('%b %d, %Y')}"

    print(f"Loading CRM data from {input_csv}...")
    rows = load_csv(input_csv)
    print(f"  {len(rows)} records loaded")

    print("Computing metrics...")
    metrics = compute_metrics(rows)

    print(f"\nGenerating revenue narrative for {period}...\n")
    print("=" * 60)

    client = anthropic.Anthropic()

    full_text = ""
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(metrics, period, len(rows))}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_text += text

    print("\n" + "=" * 60)

    # Save report
    report_file = f"revenue_report_{date.today().isoformat()}.md"
    with open(report_file, "w") as f:
        f.write(f"# Weekly Revenue Report\n*{period}*\n\n")
        f.write(full_text)
        f.write(f"\n\n---\n*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} from {input_csv}*\n")

    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python narrator.py <crm_data.csv> [\"Week of Jan 6, 2025\"]")
        print("Example: python narrator.py hubspot_export.csv")
        sys.exit(1)

    period = sys.argv[2] if len(sys.argv) > 2 else None
    narrate(sys.argv[1], period)
