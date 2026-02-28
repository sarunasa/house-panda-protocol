import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Config ---
st.set_page_config(
    page_title="House Panda — Bonding Curve Explorer",
    page_icon="🐼",
    layout="wide",
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background-color: #0a0a0a;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        font-family: 'Inter', sans-serif !important;
    }
    
    .main-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .main-header .subtitle {
        color: #76b900;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #141414 0%, #1a1a1a 100%);
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
    }
    .metric-card .label {
        color: #888;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .metric-card .value {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
    }
    .metric-card .value.green { color: #76b900; }
    .metric-card .value.amber { color: #f5a623; }
    .metric-card .value.red { color: #e74c3c; }
    .metric-card .value.blue { color: #4a9eff; }
    
    .info-panel {
        background: #111111;
        border-left: 3px solid #76b900;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        font-size: 0.85rem;
        color: #ccc;
        line-height: 1.6;
    }
    .info-panel strong { color: #76b900; }
    
    .scenario-box {
        background: linear-gradient(135deg, #0d1a00 0%, #111a05 100%);
        border: 1px solid #2a3a10;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    .scenario-box .title {
        color: #76b900;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .scenario-box .detail {
        color: #bbb;
        font-size: 0.82rem;
        line-height: 1.5;
    }
    
    .default-box {
        background: linear-gradient(135deg, #1a0a0a 0%, #1a0f0f 100%);
        border: 1px solid #3a1a1a;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    .default-box .title {
        color: #e74c3c;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .default-box .detail {
        color: #bbb;
        font-size: 0.82rem;
        line-height: 1.5;
    }
    
    .inference-box {
        background: linear-gradient(135deg, #0a0a1a 0%, #0f0f1a 100%);
        border: 1px solid #1a1a3a;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    .inference-box .title {
        color: #4a9eff;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .inference-box .detail {
        color: #bbb;
        font-size: 0.82rem;
        line-height: 1.5;
    }
    
    .nvidia-badge {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        color: #555;
        font-size: 0.7rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
    .nvidia-badge strong { color: #76b900; }
    
    .stSlider > div > div { color: #888 !important; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .section-divider {
        border: none;
        border-top: 1px solid #222;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Bonding Curve Math ---
def bonding_curve_price(supply, k, n):
    return k * np.power(supply, n)

def bonding_curve_integral(supply, k, n):
    return k * np.power(supply, n + 1) / (n + 1)

def lending_rate(curve_position, base_rate=0.02, max_rate=0.50):
    return base_rate + (max_rate - base_rate) * (curve_position ** 1.5)

def ai_allocation_pct(curve_position, max_alloc=0.50, min_alloc=0.15):
    return max_alloc - (max_alloc - min_alloc) * curve_position

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>🐼 House Panda — Bonding Curve Explorer</h1>
    <div class="subtitle">AI-Managed Token Lending Protocol &nbsp;·&nbsp; Interactive Model</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

col_controls, col_chart = st.columns([1, 2.2], gap="large")

with col_controls:
    st.markdown("#### ⚙️ Curve Parameters")
    k = st.slider("**k** — Base price coefficient", min_value=0.0001, max_value=0.01, value=0.001, step=0.0001, format="%.4f", help="Starting price factor.")
    n = st.slider("**n** — Curve exponent", min_value=1.0, max_value=3.0, value=1.8, step=0.1, help="Steepness of price growth.")
    total_supply = st.slider("**Total supply** (millions)", min_value=10, max_value=200, value=100, step=10)
    
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("#### 🏦 Market Maker Activity")
    circulating_pct = st.slider("**Circulating supply** (% of total)", min_value=5, max_value=95, value=40, step=5)
    mm_borrow_pct = st.slider("**MM borrow amount** (% of circulating)", min_value=0, max_value=30, value=10, step=1)
    
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("#### 💥 Stress Scenarios")
    default_events = st.slider("**Default events** (MMs who didn't return)", min_value=0, max_value=5, value=0, step=1)
    default_shift = 1.0 + (default_events * 0.08)

# --- Calculations ---
total_supply_tokens = total_supply * 1_000_000
circulating = total_supply_tokens * (circulating_pct / 100)
mm_borrow = circulating * (mm_borrow_pct / 100)
curve_position = circulating_pct / 100

supply_range = np.linspace(1, total_supply_tokens, 500)
prices_base = bonding_curve_price(supply_range, k, n)
prices_shifted = bonding_curve_price(supply_range, k * default_shift, n)
current_price = bonding_curve_price(circulating, k * default_shift, n)
price_after_borrow = bonding_curve_price(circulating - mm_borrow, k * default_shift, n)
current_lending_rate = lending_rate(curve_position)
current_ai_alloc = ai_allocation_pct(curve_position)
income_rate = current_lending_rate * mm_borrow * current_price
ai_spend = current_ai_alloc * income_rate
inference_bank_surplus = income_rate - ai_spend
market_cap = circulating * current_price
collateral_ratio = 0.60 + (0.15 * curve_position)
collateral_required = mm_borrow * current_price * collateral_ratio
default_profit_threshold = current_price / collateral_ratio

# --- Chart ---
with col_chart:
    fig = go.Figure()
    if default_events > 0:
        fig.add_trace(go.Scatter(x=supply_range / 1e6, y=prices_base, mode='lines', name='Original Curve', line=dict(color='rgba(100,100,100,0.3)', width=1, dash='dot')))
    
    curve_color = '#e74c3c' if default_events > 0 else '#76b900'
    curve_name = f'Active Curve (+{default_events} defaults)' if default_events > 0 else 'Bonding Curve'
    fig.add_trace(go.Scatter(x=supply_range / 1e6, y=prices_shifted, mode='lines', name=curve_name, line=dict(color=curve_color, width=2.5)))
    
    if mm_borrow_pct > 0:
        borrow_range = np.linspace(circulating - mm_borrow, circulating, 50)
        borrow_prices = bonding_curve_price(borrow_range, k * default_shift, n)
        fig.add_trace(go.Scatter(x=np.concatenate([borrow_range / 1e6, (borrow_range / 1e6)[::-1]]), y=np.concatenate([borrow_prices, np.zeros(len(borrow_prices))]), fill='toself', fillcolor='rgba(245,166,35,0.12)', line=dict(color='rgba(0,0,0,0)'), name='MM Borrowed Zone', hoverinfo='skip'))
    
    ai_range = np.linspace(1, circulating - mm_borrow, 100)
    ai_prices = bonding_curve_price(ai_range, k * default_shift, n)
    fig.add_trace(go.Scatter(x=np.concatenate([ai_range / 1e6, (ai_range / 1e6)[::-1]]), y=np.concatenate([ai_prices * current_ai_alloc, np.zeros(len(ai_prices))]), fill='toself', fillcolor='rgba(74,158,255,0.06)', line=dict(color='rgba(0,0,0,0)'), name=f'AI Allocation ({current_ai_alloc:.0%})', hoverinfo='skip'))
    
    fig.add_trace(go.Scatter(x=[circulating / 1e6], y=[current_price], mode='markers+text', name='Current Position', marker=dict(color='#ffffff', size=12, symbol='circle', line=dict(color='#76b900', width=2)), text=[f'${current_price:.4f}'], textposition='top center', textfont=dict(color='#ffffff', size=11)))
    
    if mm_borrow_pct > 0:
        fig.add_trace(go.Scatter(x=[(circulating - mm_borrow) / 1e6], y=[price_after_borrow], mode='markers+text', name='Effective Supply (post-borrow)', marker=dict(color='#f5a623', size=10, symbol='diamond', line=dict(color='#f5a623', width=1.5)), text=[f'${price_after_borrow:.4f}'], textposition='bottom center', textfont=dict(color='#f5a623', size=10)))
        fig.add_trace(go.Scatter(x=[circulating / 1e6, (circulating - mm_borrow) / 1e6], y=[current_price, price_after_borrow], mode='lines', line=dict(color='#f5a623', width=1, dash='dash'), showlegend=False, hoverinfo='skip'))
    
    fig.update_layout(template='plotly_dark', paper_bgcolor='#0a0a0a', plot_bgcolor='#0a0a0a', font=dict(family='Inter', color='#888'), title=dict(text=f'HPT Bonding Curve  ·  P = {k * default_shift:.4f} × S<sup>{n}</sup>', font=dict(size=15, color='#aaa'), x=0.5), xaxis=dict(title='Supply (millions)', gridcolor='#1a1a1a', zerolinecolor='#1a1a1a'), yaxis=dict(title='Price (USD)', gridcolor='#1a1a1a', zerolinecolor='#1a1a1a', tickprefix='$'), legend=dict(bgcolor='rgba(20,20,20,0.8)', bordercolor='#2a2a2a', borderwidth=1, font=dict(size=10), x=0.02, y=0.98), margin=dict(l=60, r=30, t=50, b=50), height=480)
    st.plotly_chart(fig, use_container_width=True)

# --- Metrics Row ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
m1, m2, m3, m4, m5, m6 = st.columns(6)
with m1:
    st.markdown(f'<div class="metric-card"><div class="label">Token Price</div><div class="value green">${current_price:.4f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="label">Market Cap</div><div class="value">${market_cap:,.0f}</div></div>', unsafe_allow_html=True)
with m3:
    rate_color = "green" if current_lending_rate < 0.10 else ("amber" if current_lending_rate < 0.25 else "red")
    st.markdown(f'<div class="metric-card"><div class="label">Lending Rate</div><div class="value {rate_color}">{current_lending_rate:.1%}</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="label">AI Allocation</div><div class="value blue">{current_ai_alloc:.0%}</div></div>', unsafe_allow_html=True)
with m5:
    st.markdown(f'<div class="metric-card"><div class="label">MM Borrowed</div><div class="value amber">{mm_borrow/1e6:.1f}M</div></div>', unsafe_allow_html=True)
with m6:
    st.markdown(f'<div class="metric-card"><div class="label">Collateral Req.</div><div class="value">{collateral_ratio:.0%}</div></div>', unsafe_allow_html=True)

# --- Bottom Panels ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
panel1, panel2, panel3 = st.columns(3)

with panel1:
    st.markdown(f'<div class="scenario-box"><div class="title">📐 Curve Economics</div><div class="detail"><strong>Formula:</strong> P = {k * default_shift:.4f} × S<sup>{n}</sup><br><strong>At current supply:</strong> {circulating/1e6:.0f}M → ${current_price:.4f}<br><strong>Post-borrow:</strong> {(circulating-mm_borrow)/1e6:.1f}M → ${price_after_borrow:.4f}<br><strong>Price impact:</strong> {((price_after_borrow - current_price)/current_price)*100:+.1f}%<br><strong>Lending income (ann.):</strong> ${income_rate:,.0f}</div></div>', unsafe_allow_html=True)

with panel2:
    if default_events > 0:
        st.markdown(f'<div class="default-box"><div class="title">💥 Default Response Active</div><div class="detail"><strong>{default_events} default(s)</strong> → curve shifted +{(default_shift-1)*100:.0f}%<br><strong>k shifted:</strong> {k:.4f} → {k * default_shift:.4f}<br><strong>Effect:</strong> All borrowers pay higher rates<br><strong>Self-healing:</strong> No governance vote required</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="scenario-box"><div class="title">🛡️ Default Protection</div><div class="detail"><strong>Dynamic collateral:</strong> {collateral_ratio:.0%} of current value<br><strong>Collateral required:</strong> ${collateral_required:,.0f}<br><strong>Token value borrowed:</strong> ${mm_borrow * current_price:,.0f}<br><strong>Default profitable above:</strong> ${default_profit_threshold:.4f}/token<br><strong>That requires:</strong> {(default_profit_threshold/current_price - 1)*100:+.0f}% price increase</div></div>', unsafe_allow_html=True)

with panel3:
    st.markdown(f'<div class="inference-box"><div class="title">🧠 Inference Bank</div><div class="detail"><strong>Lending income:</strong> ${income_rate:,.0f}/yr<br><strong>AI spend ({current_ai_alloc:.0%}):</strong> ${ai_spend:,.0f}/yr<br><strong>Surplus:</strong> <span style="color: {"#76b900" if inference_bank_surplus > 0 else "#e74c3c"}">${inference_bank_surplus:,.0f}/yr</span><br><strong>Function:</strong> Countercyclical buffer<br><strong>When income drops → AI draws from reserve</strong></div></div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="info-panel"><strong>How it works:</strong> Market makers borrow HPT from the bonding curve to provide liquidity on exchanges. The curve sets both the <strong>price</strong> (deterministic from supply) and the <strong>lending rate</strong> (increases as supply is consumed). Income flows to AI development via the <strong>Inference Bank</strong> — a countercyclical reserve. If an MM defaults, the curve <strong>shifts upward permanently</strong> — the protocol self-heals without governance intervention.<br><br><strong>AI output = GitHub commits</strong> (public, 3-month delay). Every decision produces a verifiable artifact.</div>', unsafe_allow_html=True)
st.markdown('<div class="nvidia-badge"><strong>NVIDIA Inception</strong> — East Asia Cohort &nbsp;·&nbsp; House Panda &nbsp;·&nbsp; 2026</div>', unsafe_allow_html=True)
