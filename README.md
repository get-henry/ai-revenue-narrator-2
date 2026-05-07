# AI Revenue Report Narrator

> Drop in a CRM export. Get a plain-English revenue summary in 30 seconds — with anomaly callouts your team will actually read.

Built for RevOps and Marketing leaders who spend Monday mornings copy-pasting numbers into a narrative nobody finishes writing.

---

## What It Does

1. Loads any CRM CSV export (HubSpot, Salesforce, Pipedrive — any format)
2. Computes deal metrics: closed revenue, win rate, pipeline by stage and rep
3. Runs anomaly detection — flags outlier deals, win rate drops, stalling stages
4. Streams a plain-English narrative brief formatted for a CRO or VP of Sales

---

## Demo

```bash
$ python narrator.py sample_crm_data.csv "Week of Jan 6, 2025"

Loading CRM data from sample_crm_data.csv...
  18 records loaded
Computing metrics...

Generating revenue narrative for Week of Jan 6, 2025...

============================================================
### This Week's Headline
MomentumAI closed at $155K — single-handedly pulling the week to target
despite a win rate that deserves a hard look.

### Revenue Summary
Closed $336,000 across 7 won deals. Win rate sits at 43% on 16 closed deals —
healthy on paper, but that number is propped up by one outlier deal...

### Anomalies & Watch Items
⚠ MomentumAI at $155K is 4x the average deal size — validate this didn't
slip through at a discount. Carlos has 2 deals stalled in Negotiation >7 days.
============================================================

Report saved to: revenue_report_2025-01-10.md
```

---

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

---

## Usage

```bash
# Auto-detects current week
python narrator.py hubspot_export.csv

# Specify period label
python narrator.py crm_data.csv "Week of Jan 6, 2025"
```

**Flexible CSV format** — the script auto-detects common column names:
- Deal value: `amount`, `deal_value`, or `value`
- Stage: `stage` or `status`
- Owner: `owner`, `rep`, or `assigned_to`
- Source: `lead_source` or `source`

---

## Sample Output Structure

```markdown
### This Week's Headline
### Revenue Summary
### Pipeline Health
### Rep Highlights
### Anomalies & Watch Items
### Next Week's Focus
```

Report is streamed live and saved as a dated `.md` file.

---

## Stack

- Python 3.10+
- [Anthropic Claude API](https://docs.anthropic.com) (`claude-sonnet-4-6`) with streaming
- Zero dependencies beyond `anthropic` — no pandas, no heavy data libs

---

## Why This Matters

RevOps teams spend 3–5 hours per week writing revenue narratives that rehash numbers everyone can already see in a dashboard. This agent writes the analysis layer — the *so what* — in under a minute.

*Built by [Henry Tran](https://linkedin.com/in/get-henry) — AI automation for Revenue teams.*
