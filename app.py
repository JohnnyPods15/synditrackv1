import streamlit as st
import pandas as pd
from datetime import date
from data import DEALS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Syndication Tracker| KBCM Loan Syndication",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background-color: #0d1117; color: #e6edf3; }
.main .block-container { padding-top: 1.5rem; max-width: 1400px; }
section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
h1, h2, h3 { color: #e6edf3 !important; }
.stSelectbox label, .stMultiSelect label { color: #8b949e !important; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; }

.kpi-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.kpi-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.1rem 1.4rem; flex: 1; min-width: 140px; }
.kpi-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; color: #8b949e; font-family: 'IBM Plex Mono', monospace; margin-bottom: 0.3rem; }
.kpi-value { font-size: 1.5rem; font-weight: 700; color: #58a6ff; font-family: 'IBM Plex Mono', monospace; }
.kpi-sub { font-size: 0.72rem; color: #8b949e; margin-top: 0.2rem; }

.section-header { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #58a6ff; font-family: 'IBM Plex Mono', monospace; border-bottom: 1px solid #21262d; padding-bottom: 0.4rem; margin: 1.5rem 0 1rem 0; }

.tranche-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.2rem 1.4rem; margin-bottom: 1rem; }
.tranche-title { font-size: 1rem; font-weight: 700; color: #e6edf3; margin-bottom: 0.8rem; }
.tranche-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 0.8rem; }
.tranche-field-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; color: #8b949e; font-family: 'IBM Plex Mono', monospace; }
.tranche-field-value { font-size: 0.9rem; font-weight: 600; color: #e6edf3; font-family: 'IBM Plex Mono', monospace; }

.badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.7rem; font-weight: 600; font-family: 'IBM Plex Mono', monospace; }
.badge-funded { background: #1a4731; color: #3fb950; }
.badge-active { background: #1a3a4a; color: #58a6ff; }
.badge-partial { background: #3d2f00; color: #d29922; }
.badge-undrawn { background: #21262d; color: #8b949e; }
.badge-upcoming { background: #2d1f00; color: #f0883e; }
.badge-complete { background: #1a4731; color: #3fb950; }
.badge-high { background: #4a1515; color: #f85149; }
.badge-medium { background: #3d2f00; color: #d29922; }
.badge-low { background: #21262d; color: #8b949e; }

.styled-table { width: 100%; border-collapse: collapse; font-size: 0.83rem; }
.styled-table th { background: #21262d; color: #8b949e; padding: 0.6rem 0.8rem; text-align: left; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; font-family: 'IBM Plex Mono', monospace; }
.styled-table td { padding: 0.6rem 0.8rem; border-bottom: 1px solid #21262d; color: #e6edf3; vertical-align: top; }
.styled-table tr:hover td { background: #1c2128; }

.progress-container { background: #21262d; border-radius: 4px; height: 6px; margin-top: 0.3rem; }
.progress-bar { background: #58a6ff; border-radius: 4px; height: 6px; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_mm(val):
    if val >= 1_000_000_000:
        return f"${val/1_000_000_000:.2f}B"
    return f"${val/1_000_000:.0f}M"

def status_badge(status):
    s = status.lower()
    if "funded" in s: cls = "badge-funded"
    elif "active" in s or "utilized" in s: cls = "badge-active"
    elif "partial" in s: cls = "badge-partial"
    elif "undrawn" in s: cls = "badge-undrawn"
    elif "upcoming" in s: cls = "badge-upcoming"
    elif "complete" in s: cls = "badge-complete"
    else: cls = "badge-undrawn"
    return f'<span class="badge {cls}">{status}</span>'

def priority_badge(p):
    cls = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}.get(p, "badge-low")
    return f'<span class="badge {cls}">{p}</span>'

def days_until(d):
    delta = (d - date.today()).days
    if delta < 0: return f'<span style="color:#f85149">{abs(delta)}d overdue</span>'
    elif delta <= 7: return f'<span style="color:#f0883e">{delta}d</span>'
    elif delta <= 30: return f'<span style="color:#d29922">{delta}d</span>'
    else: return f'<span style="color:#8b949e">{delta}d</span>'

def pricing_str(p):
    idx = p.get("index", "SOFR")
    spread = p.get("spread_bps")
    if idx == "N/A": return f"Flat fee: {spread}bps"
    parts = [f"{idx} + {spread}bps"]
    if p.get("floor_bps"): parts.append(f"({p['floor_bps']}bps floor)")
    if p.get("oid"): parts.append(f"OID: {p['oid']}")
    return " | ".join(parts)

def milestone_progress(milestones):
    done = sum(1 for m in milestones if m["status"] == "Complete")
    return done, len(milestones)

def go_current_cell(t):
    """Returns formatted go-current date string with alert flag if applicable."""
    gc = t.get("go_current_date")
    if not gc:
        return "—"
    label = gc.strftime("%b %d, %Y")
    if gc <= date.today():
        return f'{label} <span style="color:#f85149;font-size:0.7rem;">● CURRENT</span>'
    elif (gc - date.today()).days <= 365:
        return f'{label} <span style="color:#d29922;font-size:0.7rem;">⚠ &lt;12mo</span>'
    return label

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 SyndiTrack")
    st.markdown('<div style="color:#8b949e;font-size:0.78rem;margin-bottom:1.2rem;">KBCM Loan Syndication Manager</div>', unsafe_allow_html=True)

    deal_options = {
        "USF-2024": "US Fertility – $1.07B",
        "ACE-2025": "Apex Clean Energy – $1.05B",
    }
    selected_id = st.selectbox("Active Deal", list(deal_options.keys()), format_func=lambda x: deal_options[x])
    deal = DEALS[selected_id]

    st.markdown("---")
    view = st.radio("View", ["📊 Deal Overview", "🏗️ Tranches & Pricing", "📋 Milestones", "📞 Follow-Ups", "👥 Lender Allocations"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f'<div style="color:#8b949e;font-size:0.72rem;">Lead Arranger<br><span style="color:#e6edf3;font-weight:600;">KeyBanc Capital Markets</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#8b949e;font-size:0.72rem;margin-top:0.6rem;">Today<br><span style="color:#e6edf3;font-weight:600;">{date.today().strftime("%b %d, %Y")}</span></div>', unsafe_allow_html=True)

# ── Data shortcuts ────────────────────────────────────────────────────────────
tranches = deal["tranches"]
milestones = deal["milestones"]
followups = deal["followups"]
done_ms, total_ms = milestone_progress(milestones)
open_followups = sum(1 for f in followups if not f["done"])
high_priority = sum(1 for f in followups if not f["done"] and f["priority"] == "High")
total_lenders = sum(len(t["lenders"]) for t in tranches.values())

# ═══════════════════════════════════════════════════════════════════════════════
# DEAL OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if view == "📊 Deal Overview":
    st.markdown(f"## {deal['borrower']}")
    st.markdown(f'<div style="color:#8b949e;font-size:0.85rem;margin-bottom:1.5rem;">{deal["industry"]} · Sponsor: {deal["sponsor"]} · {deal["purpose"]}</div>', unsafe_allow_html=True)

    alert_color = "#f85149" if high_priority > 0 else "#58a6ff"
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">Total Facility</div>
            <div class="kpi-value">{fmt_mm(deal["total_facility"])}</div>
            <div class="kpi-sub">{len(tranches)} tranches</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Deal Rating</div>
            <div class="kpi-value" style="font-size:1.2rem;">{deal["deal_rating"]}</div>
            <div class="kpi-sub">Moody's / S&P</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Milestones</div>
            <div class="kpi-value">{done_ms}/{total_ms}</div>
            <div class="kpi-sub">Complete</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Open Follow-Ups</div>
            <div class="kpi-value" style="color:{alert_color}">{open_followups}</div>
            <div class="kpi-sub">{high_priority} high priority</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Lender Count</div>
            <div class="kpi-value">{total_lenders}</div>
            <div class="kpi-sub">Across all tranches</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Close Date</div>
            <div class="kpi-value" style="font-size:1rem;">{deal["close_date"].strftime("%b %Y")}</div>
            <div class="kpi-sub">Announced {deal["announcement_date"].strftime("%b %d")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Parties
    st.markdown('<div class="section-header">Deal Parties</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="tranche-card">
            <div class="tranche-grid">
                <div><div class="tranche-field-label">Lead Arranger</div><div class="tranche-field-value" style="font-size:0.82rem;">{deal["lead_arranger"]}</div></div>
                <div><div class="tranche-field-label">Admin Agent</div><div class="tranche-field-value" style="font-size:0.82rem;">{deal["administrative_agent"]}</div></div>
                <div><div class="tranche-field-label">Sponsor</div><div class="tranche-field-value" style="font-size:0.82rem;">{deal["sponsor"]}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)
    with col2:
        br_html = "<br>".join(f"· {b}" for b in deal["bookrunners"])
        st.markdown(f"""
        <div class="tranche-card">
            <div class="tranche-field-label">Bookrunners</div>
            <div style="margin-top:0.4rem;font-size:0.82rem;color:#e6edf3;line-height:1.8;">{br_html}</div>
        </div>""", unsafe_allow_html=True)

    # Tranche snapshot table — includes Maturity Date and Go-Current Date
    st.markdown('<div class="section-header">Tranche Snapshot</div>', unsafe_allow_html=True)
    rows = []
    for n, t in tranches.items():
        maturity = t["maturity_date"].strftime("%b %d, %Y") if t.get("maturity_date") else "—"
        tenor_maturity = f'{t["tenor"]} · {maturity}'
        rows.append({
            "Tranche": n,
            "Type": t["type"],
            "Amount": fmt_mm(t["amount"]),
            "Pricing": pricing_str(t["pricing"]),
            "Tenor / Maturity": tenor_maturity,
            "Go-Current Date": go_current_cell(t),
            "Status": t["status"],
        })
    df = pd.DataFrame(rows)
    html = '<table class="styled-table"><thead><tr>' + "".join(f"<th>{c}</th>" for c in df.columns) + "</tr></thead><tbody>"
    for _, row in df.iterrows():
        html += "<tr>" + "".join(
            f"<td>{status_badge(str(row[c])) if c == 'Status' else row[c]}</td>"
            for c in df.columns
        ) + "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

    # Progress
    st.markdown('<div class="section-header">Deal Progress</div>', unsafe_allow_html=True)
    pct = int(done_ms / total_ms * 100)
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#8b949e;margin-bottom:0.3rem;">
        <span>Milestone completion</span><span style="color:#58a6ff;font-family:'IBM Plex Mono',monospace;">{pct}%</span>
    </div>
    <div class="progress-container" style="height:8px;"><div class="progress-bar" style="width:{pct}%;height:8px;"></div></div>
    """, unsafe_allow_html=True)
    for ms in milestones[-5:]:
        icon = "✅" if ms["status"] == "Complete" else "🔜"
        st.markdown(f'<div style="font-size:0.8rem;color:#8b949e;margin-top:0.5rem;">{icon} <span style="color:#e6edf3;">{ms["milestone"]}</span> — {ms["due_date"].strftime("%b %d, %Y")} · {ms["owner"]}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TRANCHES & PRICING
# ═══════════════════════════════════════════════════════════════════════════════
elif view == "🏗️ Tranches & Pricing":
    st.markdown("## Tranches & Pricing")
    st.markdown(f'<div style="color:#8b949e;font-size:0.85rem;margin-bottom:1.5rem;">{deal["borrower"]} · {fmt_mm(deal["total_facility"])} total</div>', unsafe_allow_html=True)

    for name, t in tranches.items():
        p = t["pricing"]

        # Maturity and go-current dates for the card subtitle
        maturity_str = t["maturity_date"].strftime("%b %d, %Y") if t.get("maturity_date") else "—"
        gc = t.get("go_current_date")
        if gc:
            gc_str = gc.strftime("%b %d, %Y")
            if gc <= date.today():
                gc_display = f'<span style="color:#f85149;">{gc_str} ● CURRENT</span>'
            elif (gc - date.today()).days <= 365:
                gc_display = f'<span style="color:#d29922;">{gc_str} ⚠ &lt;12mo</span>'
            else:
                gc_display = f'<span style="color:#8b949e;">{gc_str}</span>'
        else:
            gc_display = "—"

        extra_fields = ""
        if p.get("floor_bps"):
            extra_fields += f'<div><div class="tranche-field-label">SOFR Floor</div><div class="tranche-field-value">{p["floor_bps"]}bps</div></div>'
        if p.get("oid"):
            extra_fields += f'<div><div class="tranche-field-label">OID</div><div class="tranche-field-value">{p["oid"]}</div></div>'
        if p.get("commitment_fee_bps"):
            extra_fields += f'<div><div class="tranche-field-label">Commitment Fee</div><div class="tranche-field-value">{p["commitment_fee_bps"]}bps</div></div>'

        st.markdown(f"""
        <div class="tranche-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1rem;">
                <div>
                    <div class="tranche-title">{name}</div>
                    <div style="font-size:0.75rem;color:#8b949e;">
                        {t["type"]} · {t["tenor"]} · Matures <span style="color:#e6edf3;">{maturity_str}</span>
                    </div>
                    <div style="font-size:0.75rem;margin-top:0.3rem;">
                        <span style="color:#8b949e;">Go-Current: </span>{gc_display}
                    </div>
                </div>
                <div style="text-align:right;">
                    {status_badge(t["status"])}
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:1.1rem;font-weight:700;color:#58a6ff;margin-top:0.3rem;">{fmt_mm(t["amount"])}</div>
                </div>
            </div>
            <div class="tranche-grid">
                <div><div class="tranche-field-label">Rate Index</div><div class="tranche-field-value">{p.get("index","SOFR")}</div></div>
                <div><div class="tranche-field-label">Spread</div><div class="tranche-field-value" style="color:#3fb950;">{p.get("spread_bps")}bps</div></div>
                {extra_fields}
            </div>
            <div style="margin-top:0.8rem;padding:0.6rem 0.8rem;background:#0d1117;border-radius:5px;border:1px solid #21262d;">
                <div class="tranche-field-label" style="margin-bottom:0.2rem;">Flex Status</div>
                <div style="font-size:0.8rem;color:#e6edf3;">{t["flex_status"]}</div>
            </div>
            <div style="margin-top:0.6rem;font-size:0.78rem;color:#8b949e;">📝 {t["notes"]}</div>
        </div>
        """, unsafe_allow_html=True)

        if t["type"] == "DDTL" and "drawn_amount" in t:
            dp = int(t["drawn_amount"] / t["amount"] * 100)
            drawn_mm = fmt_mm(t["drawn_amount"])
            total_mm = fmt_mm(t["amount"])
            avail = t["availability_period_end"].strftime("%b %d, %Y")
            st.markdown("**DDTL Draw Status**")
            st.progress(dp / 100)
            st.caption(f"{drawn_mm} drawn of {total_mm} ({dp}%) · Availability window closes: {avail}")


# ═══════════════════════════════════════════════════════════════════════════════
# MILESTONES
# ═══════════════════════════════════════════════════════════════════════════════
elif view == "📋 Milestones":
    st.markdown("## Deal Milestones")
    done, total = milestone_progress(milestones)
    pct = int(done / total * 100)

    col1, col2, col3 = st.columns(3)
    col1.metric("Complete", f"{done}/{total}")
    col2.metric("Progress", f"{pct}%")
    col3.metric("Upcoming", total - done)

    st.markdown(f'<div class="progress-container" style="height:10px;margin:1rem 0;"><div class="progress-bar" style="width:{pct}%;height:10px;"></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Timeline</div>', unsafe_allow_html=True)

    html = '<table class="styled-table"><thead><tr><th>Milestone</th><th>Tranche</th><th>Due Date</th><th>Owner</th><th>Status</th></tr></thead><tbody>'
    for ms in milestones:
        html += f"""<tr>
            <td>{ms["milestone"]}</td>
            <td><span style="font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#8b949e;">{ms["tranche"]}</span></td>
            <td><span style="font-family:'IBM Plex Mono',monospace;">{ms["due_date"].strftime("%b %d, %Y")}</span></td>
            <td>{ms["owner"]}</td>
            <td>{status_badge(ms["status"])}</td>
        </tr>"""
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FOLLOW-UPS
# ═══════════════════════════════════════════════════════════════════════════════
elif view == "📞 Follow-Ups":
    st.markdown("## Follow-Up Tracker")

    open_fu = [f for f in followups if not f["done"]]
    done_fu = [f for f in followups if f["done"]]

    col1, col2, col3 = st.columns(3)
    col1.metric("Open Items", len(open_fu))
    col2.metric("High Priority", sum(1 for f in open_fu if f["priority"] == "High"))
    col3.metric("Completed", len(done_fu))

    st.markdown('<div class="section-header">Open Items</div>', unsafe_allow_html=True)
    html = '<table class="styled-table"><thead><tr><th>Party</th><th>Action Required</th><th>Due Date</th><th>Days Left</th><th>Priority</th></tr></thead><tbody>'
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    for f in sorted(open_fu, key=lambda x: (priority_order[x["priority"]], x["due_date"])):
        html += f"""<tr>
            <td><strong>{f["party"]}</strong></td>
            <td style="max-width:320px;">{f["action"]}</td>
            <td><span style="font-family:'IBM Plex Mono',monospace;">{f["due_date"].strftime("%b %d, %Y")}</span></td>
            <td>{days_until(f["due_date"])}</td>
            <td>{priority_badge(f["priority"])}</td>
        </tr>"""
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

    if done_fu:
        st.markdown('<div class="section-header">Completed</div>', unsafe_allow_html=True)
        for f in done_fu:
            st.markdown(f'<div style="font-size:0.82rem;color:#3fb950;padding:0.4rem 0;border-bottom:1px solid #21262d;">✅ <span style="color:#8b949e;">{f["party"]}</span> — {f["action"]}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# LENDER ALLOCATIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif view == "👥 Lender Allocations":
    st.markdown("## Lender Allocations")
    st.markdown(f'<div style="color:#8b949e;font-size:0.85rem;margin-bottom:1.5rem;">{deal["borrower"]} · {fmt_mm(deal["total_facility"])} total commitment</div>', unsafe_allow_html=True)

    # Aggregate by lender
    lender_totals = {}
    for tname, t in tranches.items():
        for l in t["lenders"]:
            nm = l["name"]
            if nm not in lender_totals:
                lender_totals[nm] = {"total": 0, "tranches": []}
            lender_totals[nm]["total"] += l["hold_mm"]
            lender_totals[nm]["tranches"].append(f'{tname} (${l["hold_mm"]:.0f}M)')

    st.markdown('<div class="section-header">Total Lender Exposure</div>', unsafe_allow_html=True)
    sorted_lenders = sorted(lender_totals.items(), key=lambda x: x[1]["total"], reverse=True)
    max_hold = sorted_lenders[0][1]["total"] if sorted_lenders else 1

    html = '<table class="styled-table"><thead><tr><th>Lender</th><th>Total Hold</th><th>Tranches</th><th>Exposure</th></tr></thead><tbody>'
    for lname, info in sorted_lenders:
        bar_pct = int(info["total"] / max_hold * 100)
        html += f"""<tr>
            <td><strong>{lname}</strong></td>
            <td><span style="font-family:'IBM Plex Mono',monospace;color:#58a6ff;">${info["total"]:.0f}M</span></td>
            <td style="font-size:0.75rem;color:#8b949e;max-width:280px;">{"&nbsp;·&nbsp;".join(info["tranches"])}</td>
            <td style="width:120px;"><div class="progress-container"><div class="progress-bar" style="width:{bar_pct}%"></div></div></td>
        </tr>"""
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

    # Per-tranche breakdown
    st.markdown('<div class="section-header">Breakdown by Tranche</div>', unsafe_allow_html=True)
    for tname, t in tranches.items():
        st.markdown(f'<div style="font-size:0.85rem;font-weight:600;color:#e6edf3;margin:0.8rem 0 0.4rem 0;">{tname} · {fmt_mm(t["amount"])}</div>', unsafe_allow_html=True)
        rows_html = ""
        for l in t["lenders"]:
            pct = int(l["hold_mm"] / (t["amount"] / 1_000_000) * 100)
            rows_html += f"""<tr>
                <td>{l["name"]}</td>
                <td><span style="font-family:'IBM Plex Mono',monospace;color:#58a6ff;">${l["hold_mm"]:.0f}M</span></td>
                <td><span style="font-size:0.75rem;color:#8b949e;">{l["role"]}</span></td>
                <td><span style="font-family:'IBM Plex Mono',monospace;color:#8b949e;">{pct}%</span></td>
            </tr>"""
        st.markdown(f'<table class="styled-table"><thead><tr><th>Lender</th><th>Hold</th><th>Role</th><th>% of Tranche</th></tr></thead><tbody>{rows_html}</tbody></table>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:3rem;padding-top:1rem;border-top:1px solid #21262d;font-size:0.7rem;color:#8b949e;text-align:center;font-family:'IBM Plex Mono',monospace;">
SyndiTrack · KBCM Loan Syndication · Simulated data based on public deal announcements · For demonstration purposes only
</div>
""", unsafe_allow_html=True)
