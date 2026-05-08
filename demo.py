#!/usr/bin/env python3
"""Demo output for AI Revenue Report Narrator — matches real narrator.py output format."""
import time

SEP = "=" * 60

lines = [
    ("Loading CRM data from sample_crm_data.csv...\n", 0.3),
    ("  18 records loaded\n", 0.2),
    ("Computing metrics...\n", 0.4),
    ("\nGenerating revenue narrative for Week of Jan 6, 2025...\n\n", 0.5),
    (SEP + "\n", 0.1),
    ("### This Week's Headline\n", 0.2),
    ("NovaSpark's $155K close carried the week — but a 44% win rate\n", 0.04),
    ("on 16 closed deals is hiding a pipeline problem worth fixing now.\n\n", 0.04),
    ("### Revenue Summary\n", 0.2),
    ("Closed **$336,000** across **7 won deals** this week.\n", 0.04),
    ("Win rate: **43.8%** (7W / 9L on 16 closed). Avg deal size: **$48K**,\n", 0.04),
    ("inflated by one outlier. Strip NovaSpark and avg drops to $30K.\n\n", 0.04),
    ("### Pipeline Health\n", 0.2),
    ("3 deals in Negotiation totaling $92K — none have moved in 5+ days.\n", 0.04),
    ("Discovery stage is thin: 2 deals, $119K. Top of funnel needs attention\n", 0.04),
    ("or next week's close number will feel it.\n\n", 0.04),
    ("### Rep Highlights\n", 0.2),
    ("**Sarah Chen** — 3 wins, $97K. Consistent closer, healthy mix of sources.\n", 0.04),
    ("**Marcus Webb** — 2 wins including the NovaSpark outlier. Strong week.\n", 0.04),
    ("**Carlos Mendez** — 0 wins, 2 deals stalled in Negotiation. Needs coaching.\n\n", 0.04),
    ("### Anomalies & Watch Items\n", 0.2),
    ("- NovaSpark at $155K is **4x average deal size** — validate discount terms\n", 0.04),
    ("  before it hits the books.\n", 0.04),
    ("- Carlos has had 2 deals in Negotiation for 6+ days with no logged activity.\n", 0.04),
    ("- Referral channel win rate: 100% (3/3). Outbound: 33% (1/3). Shift sourcing mix.\n\n", 0.04),
    ("### Next Week's Focus\n", 0.2),
    ("1. Carlos: Get a next-step booked on both stalled Negotiation deals by EOD Mon.\n", 0.04),
    ("2. Validate NovaSpark discount terms before close is reported to leadership.\n", 0.04),
    ("3. Seed top of funnel — Discovery is too thin to hit target in 2 weeks.\n", 0.04),
    ("\n" + SEP + "\n", 0.2),
    ("\nReport saved to: revenue_report_2025-01-10.md\n", 0.3),
]

for text, delay in lines:
    print(text, end="", flush=True)
    time.sleep(delay)
