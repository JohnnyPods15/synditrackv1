"""
Simulated deal data based on real KBCM transactions.
US Fertility Enterprises - $1.07B Senior Secured Credit Facilities (Dec 2025)
Apex Clean Energy - $1.05B Senior Secured Credit Facilities (Nov 2025)
Source: key.com/businesses-institutions/our-transactions

Corrections applied vs. prior version:
USF: TLB lender roster updated to reflect broadly syndicated CLO/institutional buyers
USF: DDTL commitment fee corrected from 212bps to 63bps (market standard ~50% of margin floor)
ACE: Close date corrected to Nov 3, 2025
ACE: Sponsor removed - not publicly confirmed
ACE: Deal rating revised from BB-/Ba3 to B+/B1 (more appropriate for developer credit)
"""

from datetime import date

DEALS = {
    "USF-2024": {
        "deal_id": "USF-2024",
        "borrower": "US Fertility Enterprises",
        "industry": "Healthcare - Fertility Services",
        "sponsor": "Amulet Capital Partners & L Catterton",
        "purpose": "Recapitalization & Acquisition of Genetics & IVF Institute",
        "total_facility": 1_070_000_000,
        "lead_arranger": "KeyBanc Capital Markets (KBCM)",
        "bookrunners": ["KeyBanc Capital Markets", "Cain Brothers"],
        "administrative_agent": "KeyBank National Association",
        "deal_rating": "B2 / B",
        "announcement_date": date(2025, 12, 1),
        "close_date": date(2025, 12, 31),
        "tranches": {
            "Revolving Credit Facility": {
                "type": "Revolver",
                "amount": 120_000_000,
                "currency": "USD",
                "tenor": "5 years",
                "maturity_date": date(2030, 12, 31),
                "pricing": {
                    "index": "SOFR",
                    "spread_bps": 400,
                    "floor_bps": 0,
                    "oid": None,
                    "commitment_fee_bps": 50,
                    "drawn_margin_bps": 400,
                },
                "status": "Funded",
                "lenders": [
                    # Revolvers on broadly syndicated healthcare deals are typically
                    # held by relationship banks, not CLO funds
                    {"name": "KeyBank National Association", "hold_mm": 35.0, "role": "Agent / Lender"},
                    {"name": "Truist Bank", "hold_mm": 25.0, "role": "Lender"},
                    {"name": "Regions Bank", "hold_mm": 20.0, "role": "Lender"},
                    {"name": "Fifth Third Bank", "hold_mm": 20.0, "role": "Lender"},
                    {"name": "BMO Bank", "hold_mm": 20.0, "role": "Lender"},
                ],
                "flex_status": "Priced tight - spread flexed in 25bps from initial talk",
                "notes": "Subject to springing maturity if TLB outstanding 91 days prior to TLB maturity.",
            },
            "Term Loan B": {
                "type": "TLB",
                "amount": 825_000_000,
                "currency": "USD",
                "tenor": "7 years",
                "maturity_date": date(2032, 12, 31),
                "pricing": {
                    "index": "SOFR",
                    "spread_bps": 425,
                    "floor_bps": 100,
                    "oid": 99.0,
                    "commitment_fee_bps": None,
                    "drawn_margin_bps": 425,
                },
                "status": "Funded",
                "lenders": [
                    # Broadly syndicated TLB - institutional investors and CLO managers
                    # are the correct buyer base, not private credit direct lenders
                    {"name": "Carlyle CLO Management", "hold_mm": 80.0, "role": "CLO Anchor"},
                    {"name": "PGIM Fixed Income", "hold_mm": 75.0, "role": "Institutional Lender"},
                    {"name": "Blackstone CLO Management", "hold_mm": 70.0, "role": "CLO Lender"},
                    {"name": "Voya Investment Management", "hold_mm": 65.0, "role": "CLO Lender"},
                    {"name": "Benefit Street Partners", "hold_mm": 60.0, "role": "CLO Lender"},
                    {"name": "Owl Rock / Blue Owl CLO", "hold_mm": 55.0, "role": "CLO Lender"},
                    {"name": "Barings LLC", "hold_mm": 50.0, "role": "Institutional Lender"},
                    {"name": "Medalist Partners", "hold_mm": 45.0, "role": "Institutional Lender"},
                    {"name": "Various CLOs / Loan Funds", "hold_mm": 325.0, "role": "Syndicate"},
                ],
                "flex_status": "No flex - priced at initial talk (SOFR+425, OID 99)",
                "notes": "101 soft call protection for 6 months. 1% annual amortization.",
            },
            "Delayed Draw Term Loan": {
                "type": "DDTL",
                "amount": 125_000_000,
                "currency": "USD",
                "tenor": "7 years",
                "maturity_date": date(2032, 12, 31),
                "pricing": {
                    "index": "SOFR",
                    "spread_bps": 425,
                    "floor_bps": 100,
                    "oid": 99.0,
                    # Corrected: market standard DDTL commitment fee is ~50% of spread
                    # 50% of 425bps = ~213bps is mathematically correct BUT
                    # in practice DDTL commitment fees are negotiated lower, typically
                    # 50-75bps, as borrowers push back on holding cost of undrawn capital.
                    # Using 63bps as a realistic market rate for a healthcare services TLB DDTL.
                    "commitment_fee_bps": 63,
                    "drawn_margin_bps": 425,
                },
                "status": "Partially Drawn",
                "availability_period_end": date(2027, 6, 30),
                "drawn_amount": 60_000_000,
                "lenders": [
                    # DDTL lenders typically mirror the TLB syndicate
                    {"name": "Carlyle CLO Management", "hold_mm": 30.0, "role": "CLO Anchor"},
                    {"name": "PGIM Fixed Income", "hold_mm": 25.0, "role": "Institutional Lender"},
                    {"name": "Blackstone CLO Management", "hold_mm": 25.0, "role": "CLO Lender"},
                    {"name": "Voya Investment Management", "hold_mm": 25.0, "role": "CLO Lender"},
                    {"name": "Benefit Street Partners", "hold_mm": 20.0, "role": "CLO Lender"},
                ],
                "flex_status": "Same as TLB - priced in line",
                "notes": "18-month availability window for bolt-on fertility clinic acquisitions. Commitment fee on undrawn balance. Must comply with permitted acquisition criteria per credit agreement.",
            },
        },
        "milestones": [
            {"milestone": "Mandate Awarded", "tranche": "All", "due_date": date(2025, 10, 1), "status": "Complete", "owner": "KBCM Origination"},
            {"milestone": "CIM / Bank Book Distributed", "tranche": "All", "due_date": date(2025, 10, 10), "status": "Complete", "owner": "KBCM Syndicate"},
            {"milestone": "Lender Meetings", "tranche": "TLB / DDTL", "due_date": date(2025, 10, 20), "status": "Complete", "owner": "KBCM Syndicate"},
            {"milestone": "Commitments Due", "tranche": "Revolver", "due_date": date(2025, 11, 1), "status": "Complete", "owner": "KBCM Agency"},
            {"milestone": "Allocations Finalized", "tranche": "TLB", "due_date": date(2025, 11, 15), "status": "Complete", "owner": "KBCM Syndicate"},
            {"milestone": "Credit Agreement Executed", "tranche": "All", "due_date": date(2025, 12, 20), "status": "Complete", "owner": "Legal - Latham & Watkins"},
            {"milestone": "Closing & Funding", "tranche": "All", "due_date": date(2025, 12, 31), "status": "Complete", "owner": "KBCM Agency"},
            {"milestone": "DDTL Draw #1", "tranche": "DDTL", "due_date": date(2026, 3, 15), "status": "Upcoming", "owner": "US Fertility / Agent"},
            {"milestone": "DDTL Availability Period End", "tranche": "DDTL", "due_date": date(2027, 6, 30), "status": "Upcoming", "owner": "KBCM Agency"},
            {"milestone": "Annual Compliance Certificate", "tranche": "All", "due_date": date(2026, 3, 31), "status": "Upcoming", "owner": "Borrower / Agent"},
        ],
        "followups": [
            {"party": "US Fertility CFO", "action": "Deliver Q1 2026 Compliance Certificate", "due_date": date(2026, 4, 15), "priority": "High", "done": False},
            {"party": "KBCM Agency Desk", "action": "Confirm DDTL availability period notice sent to all lenders", "due_date": date(2026, 3, 30), "priority": "High", "done": False},
            {"party": "Latham & Watkins", "action": "Confirm permitted acquisition criteria met for DDTL Draw #1 target", "due_date": date(2026, 3, 1), "priority": "High", "done": False},
            {"party": "KeyBank National Association", "action": "Confirm springing maturity watch on revolver vs TLB maturity date", "due_date": date(2026, 6, 1), "priority": "Medium", "done": False},
            {"party": "Truist Bank", "action": "Updated KYC / AML refresh for revolver lender records", "due_date": date(2026, 6, 1), "priority": "Low", "done": False},
        ],
    },

    "ACE-2025": {
        "deal_id": "ACE-2025",
        "borrower": "Apex Clean Energy",
        "industry": "Renewable Energy - Wind & Solar Development",
        # Sponsor removed - not publicly confirmed on KeyBanc tombstone.
        # Apex is described as an independent developer, not a confirmed PE-backed portfolio co.
        "sponsor": "Not Publicly Disclosed",
        # Revised from "Project Finance" - this is a corporate credit facility at the
        # developer level, not a project finance structure (which would be asset-level, non-recourse)
        "purpose": "Corporate Credit Facility - Portfolio Expansion & Growth Capital",
        "total_facility": 1_050_000_000,
        "lead_arranger": "KeyBanc Capital Markets (KBCM)",
        # KBCM listed as Coordinating Lead Arranger per tombstone - other bookrunners simulated
        "bookrunners": ["KeyBanc Capital Markets"],
        "administrative_agent": "KeyBank National Association",
        # Revised from BB-/Ba3 - a renewable energy developer without fully contracted
        # cash flows is more consistent with a single-B rating. BB- implies near investment
        # grade stability which overstates the credit quality of a development-stage platform.
        "deal_rating": "B+ / B1",
        "announcement_date": date(2025, 9, 10),
        # Corrected: actual close date per KeyBanc tombstone was November 3, 2025
        "close_date": date(2025, 11, 3),
        "tranches": {
            "Term Loan Facility": {
                # Corrected type from TLA to TLB - infrastructure/energy corporate facilities
                # of this size at this rating are more typically institutional TLBs or
                # hybrid bank/institutional deals, not classic TLAs
                "type": "TLB",
                "amount": 500_000_000,
                "currency": "USD",
                "tenor": "5 years",
                "maturity_date": date(2030, 11, 3),
                "pricing": {
                    "index": "SOFR",
                    "spread_bps": 275,
                    "floor_bps": 0,
                    "oid": 99.5,
                    "commitment_fee_bps": None,
                    "drawn_margin_bps": 275,
                },
                "status": "Funded",
                "lenders": [
                    {"name": "KeyBank National Association", "hold_mm": 100.0, "role": "Agent / Lender"},
                    {"name": "BMO Bank", "hold_mm": 90.0, "role": "Lender"},
                    {"name": "MUFG Bank", "hold_mm": 90.0, "role": "Lender"},
                    {"name": "ING Capital", "hold_mm": 75.0, "role": "Lender"},
                    {"name": "Societe Generale", "hold_mm": 70.0, "role": "Lender"},
                    {"name": "Other Banks / Institutional", "hold_mm": 75.0, "role": "Syndicate"},
                ],
                "flex_status": "Spread flexed wide 25bps - energy market volatility at launch",
                # Added placeholder MW target to make ESG ratchet feel complete and realistic
                "notes": "ESG-linked margin ratchet: -10bps if Apex adds >= 500MW of contracted renewable capacity in trailing 12 months. Assessed annually at compliance certificate delivery.",
            },
            "Letter of Credit Facility": {
                "type": "LC Facility",
                "amount": 400_000_000,
                "currency": "USD",
                "tenor": "5 years",
                "maturity_date": date(2030, 11, 3),
                "pricing": {
                    "index": "N/A",
                    "spread_bps": 200,
                    "floor_bps": None,
                    "oid": None,
                    "commitment_fee_bps": 40,
                    "drawn_margin_bps": 200,
                },
                "status": "Active - Partially Utilized",
                "lenders": [
                    {"name": "KeyBank National Association", "hold_mm": 120.0, "role": "LC Issuer / Agent"},
                    {"name": "BMO Bank", "hold_mm": 100.0, "role": "LC Participant"},
                    {"name": "MUFG Bank", "hold_mm": 100.0, "role": "LC Participant"},
                    {"name": "ING Capital", "hold_mm": 80.0, "role": "LC Participant"},
                ],
                "flex_status": "Priced at initial talk",
                "notes": "Supports PPA performance guarantees, interconnection queue deposits, and land lease obligations across development pipeline. Fronting fee 12.5bps. LCs are contingent obligations - no cash drawn unless Apex defaults on underlying obligation.",
            },
            "Revolving Credit Facility": {
                "type": "Revolver",
                "amount": 150_000_000,
                "currency": "USD",
                "tenor": "5 years",
                "maturity_date": date(2030, 11, 3),
                "pricing": {
                    "index": "SOFR",
                    "spread_bps": 250,
                    "floor_bps": 0,
                    "oid": None,
                    "commitment_fee_bps": 37,
                    "drawn_margin_bps": 250,
                },
                "status": "Undrawn",
                "lenders": [
                    {"name": "KeyBank National Association", "hold_mm": 60.0, "role": "Agent / Lender"},
                    {"name": "BMO Bank", "hold_mm": 45.0, "role": "Lender"},
                    {"name": "MUFG Bank", "hold_mm": 45.0, "role": "Lender"},
                ],
                "flex_status": "Priced at initial talk",
                "notes": "Working capital facility for development operations. Clean-down requirement: 30 consecutive days undrawn per year. Cannot be used for project-level capital expenditures.",
            },
        },
        "milestones": [
            {"milestone": "Mandate Awarded", "tranche": "All", "due_date": date(2025, 9, 10), "status": "Complete", "owner": "KBCM Origination"},
            {"milestone": "Bank Book Distributed", "tranche": "All", "due_date": date(2025, 9, 18), "status": "Complete", "owner": "KBCM Syndicate"},
            {"milestone": "Lender Meetings", "tranche": "TL / Revolver", "due_date": date(2025, 9, 25), "status": "Complete", "owner": "KBCM Syndicate"},
            {"milestone": "Commitments Received", "tranche": "All", "due_date": date(2025, 10, 10), "status": "Complete", "owner": "KBCM Agency"},
            {"milestone": "Allocations Finalized", "tranche": "All", "due_date": date(2025, 10, 20), "status": "Complete", "owner": "KBCM Syndicate"},
            {"milestone": "Credit Agreement Signed", "tranche": "All", "due_date": date(2025, 10, 28), "status": "Complete", "owner": "Legal - Simpson Thacher"},
            {"milestone": "Closing & Funding", "tranche": "All", "due_date": date(2025, 11, 3), "status": "Complete", "owner": "KBCM Agency"},
            {"milestone": "First ESG Reporting Period", "tranche": "TL", "due_date": date(2026, 5, 1), "status": "Upcoming", "owner": "Apex / Agent"},
            {"milestone": "Annual Lender Call", "tranche": "All", "due_date": date(2026, 6, 1), "status": "Upcoming", "owner": "KBCM Agency"},
        ],
        "followups": [
            {"party": "Apex Clean Energy IR", "action": "Provide MW capacity build-out update for ESG margin ratchet assessment (500MW threshold)", "due_date": date(2026, 4, 1), "priority": "High", "done": False},
            {"party": "ING Capital", "action": "Confirm LC participation renewal terms ahead of Year 1 anniversary", "due_date": date(2026, 3, 15), "priority": "Medium", "done": False},
            {"party": "Simpson Thacher", "action": "Send annual covenant compliance summary to syndicate", "due_date": date(2026, 3, 30), "priority": "Medium", "done": False},
            {"party": "KBCM Agency Desk", "action": "Schedule annual lender update call with Apex management", "due_date": date(2026, 5, 15), "priority": "Low", "done": False},
            {"party": "KeyBank National Association", "action": "Confirm clean-down period tracking on revolver - 30 consecutive days undrawn required", "due_date": date(2026, 4, 30), "priority": "Medium", "done": False},
        ],
    },
}
