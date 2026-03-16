import streamlit as st
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide", page_title="SMT 60 Monitoring")

# Auto-refresh every 5 seconds to update temperature data
st_autorefresh(interval=5000, key="data_refresh")

# ────────────────────────────────────────────────
#                CSS + JS for live clock
# ────────────────────────────────────────────────
st.markdown("""
<style>
    body { background-color: #ECFOF1; }
    .block-container { padding-top: 1rem !important; }
    .title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: bold;
        color: #2a4075;
        margin-bottom: 0.9rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .card {
        background: #AAB7V8;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .line-title {
        text-align: center;
        font-size: 1.6rem;
        font-weight: bold;
        color: #37559a;
        margin-bottom: 1rem;
    }
    .metrics-row {
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    .metric {
        font-size: 2.8rem;
        font-weight: bold;
        min-width: 160px;
        text-align: center;
    }
    .temp { color: #2ECC71; }
    .hum  { color: #3498DB; }
    .time {
        color: #7D7D7D;
        text-align: right;
        font-size: 1.2rem;
        font-weight: 600;
    }
</style>

<!-- JavaScript live clock -->
<script>
function updateClock() {
    const now = new Date();
    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = now.getFullYear();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const dateStr = `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
    const clockElement = document.getElementById('live-clock');
    if (clockElement) {
        clockElement.innerHTML = `🔴 LIVE <br> ${dateStr}`;
    }
}
setInterval(updateClock, 1000);
window.addEventListener('load', updateClock);
</script>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
#                HEADER
# ────────────────────────────────────────────────
c1, c2, c3 = st.columns([1.0, 4, 0.7])

with c1:
    try:
        st.image("image.png", width=160)
    except:
        st.write("logo")

with c2:
    st.markdown("<div class='title'>SMT 60 | TEMPERATURE & HUMIDITY MONITORING</div>", unsafe_allow_html=True)

with c3:
    # Placeholder that will be filled by JavaScript
    st.markdown('<div id="live-clock" class="time">🔴 LIVE <br> --</div>', unsafe_allow_html=True)

st.markdown("---")

# ────────────────────────────────────────────────
#                DATA (updated every 5 sec via autorefresh)
# ────────────────────────────────────────────────
reference = {
    "Line 1 & 2": (23.4, 49.0),
    "Line 3 & 4": (25.6, 44.2),
    "Line 5 & 6": (24.5, 47.0),
    "Line 7"     : (24.7, 49.0),
}

def vary(v, delta):
    return round(v + random.uniform(-delta, delta), 1)

colA, colB = st.columns(2)
pairs = list(reference.items())

for i in range(0, len(pairs), 2):
    left  = pairs[i]
    right = pairs[i+1] if i+1 < len(pairs) else None

    with colA:
        line, (base_t, base_h) = left
        t = vary(base_t, 0.5)
        h = vary(base_h, 2.0)
        st.markdown(f"""
        <div class="card">
            <div class="line-title">{line}</div>
            <div class="metrics-row">
                <div class="metric temp">🌡 {t} °C</div>
                <div class="metric hum">💧 {h} %</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if right:
        with colB:
            line, (base_t, base_h) = right
            t = vary(base_t, 0.4)
            h = vary(base_h, 2.0)
            st.markdown(f"""
            <div class="card">
                <div class="line-title">{line}</div>
                <div class="metrics-row">
                    <div class="metric temp">🌡 {t} °C</div>
                    <div class="metric hum">💧 {h} %</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
