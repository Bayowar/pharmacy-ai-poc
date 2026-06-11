import streamlit as st
import pandas as pd
import plotly.graph_objects as go
OLLAMA_AVAILABLE = False
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    pass
from prophet import Prophet
from datetime import date, timedelta

MODEL = "llama3.2:3b"

st.set_page_config(page_title="Rx Compound Pharmacy Dashboard", page_icon="Rx", layout="wide")

st.markdown("""
    <style>
    .header-bar {
        background: linear-gradient(90deg, #1a3c5e, #2e86c1);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-bar">
        <h1> Rx Compound Pharmacy</h1>
        <p>AI-Powered Inventory & Compliance Dashboard</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Inventory & Forecast", "Batch Compliance"])
st.sidebar.markdown("---")
st.sidebar.markdown("**Pharmacy AI POC**")
st.sidebar.markdown("Built with Python + Ollama")
st.sidebar.markdown("Running: Llama 3.2 (local)")

def load_batch_data():
    batches = [
        {"id": "B001", "compound": "B12 1000mcg/mL", "made_on": date.today() - timedelta(days=28), "bud_days": 30},
        {"id": "B002", "compound": "B12 500mcg/mL",  "made_on": date.today() - timedelta(days=25), "bud_days": 30},
        {"id": "B003", "compound": "MIC Injection",  "made_on": date.today() - timedelta(days=10), "bud_days": 30},
        {"id": "B004", "compound": "Glutathione IV", "made_on": date.today() - timedelta(days=12), "bud_days": 14},
        {"id": "B005", "compound": "B12 1000mcg/mL", "made_on": date.today() - timedelta(days=2),  "bud_days": 30},
    ]
    results = []
    for b in batches:
        expiry = b["made_on"] + timedelta(days=b["bud_days"])
        days_left = (expiry - date.today()).days
        if days_left <= 0:
            status, color = "EXPIRED", "#dc3545"
        elif days_left <= 3:
            status, color = "URGENT", "#dc3545"
        elif days_left <= 7:
            status, color = "WARNING", "#fd7e14"
        else:
            status, color = "OK", "#28a745"
        results.append({
            "Batch ID": b["id"],
            "Compound": b["compound"],
            "Expires": expiry.strftime("%b %d %Y"),
            "Days Left": days_left,
            "Status": status,
            "Color": color
        })
    return results

if page == "Inventory & Forecast":
    st.subheader("B12 Demand Forecast — Next 12 Weeks")
    st.write("Building forecast model, please wait...")

    data = {
        "ds": pd.date_range(start="2025-01-01", periods=52, freq="W"),
        "y": [120,115,130,140,128,135,150,145,160,155,
              148,162,170,165,158,172,180,175,168,182,
              190,185,178,192,200,195,188,202,210,205,
              198,212,220,215,208,222,230,225,218,232,
              240,235,228,242,250,245,238,252,260,255,248,262]
    }
    df = pd.DataFrame(data)
    m = Prophet(seasonality_mode="multiplicative", weekly_seasonality=False)
    m.fit(df)
    future = m.make_future_dataframe(periods=12, freq="W")
    forecast = m.predict(future)

    st.write(" Forecast complete!")

    current_avg = int(df["y"].tail(4).mean())
    forecast_avg = int(forecast["yhat"].tail(12).mean())
    peak_units = int(forecast["yhat"].tail(12).max())
    growth = round(((forecast_avg - current_avg) / current_avg) * 100, 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Weekly Avg", str(current_avg) + " units")
    col2.metric("Forecasted Weekly Avg", str(forecast_avg) + " units")
    col3.metric("Peak Week Demand", str(peak_units) + " units")
    col4.metric("Expected Growth", str(growth) + "%", delta=str(growth) + "%")

    st.markdown("---")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["ds"], y=df["y"],
        mode="lines+markers",
        name="Actual Sales",
        line=dict(color="#2e86c1", width=2),
        marker=dict(size=4)
    ))
    fig.add_trace(go.Scatter(
        x=forecast["ds"].tail(12),
        y=forecast["yhat"].tail(12),
        mode="lines+markers",
        name="Forecast",
        line=dict(color="#28a745", width=2, dash="dash"),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast["ds"].tail(12), forecast["ds"].tail(12)[::-1]]),
        y=pd.concat([forecast["yhat_upper"].tail(12), forecast["yhat_lower"].tail(12)[::-1]]),
        fill="toself",
        fillcolor="rgba(40,166,69,0.1)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Confidence Range"
    ))
    fig.update_layout(
        title="B12 Shot Weekly Sales — Historical + 12 Week Forecast",
        xaxis_title="Date",
        yaxis_title="Units Sold",
        height=450,
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#1e1e1e",
        font=dict(color="white"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(" 12 Week Forecast Breakdown")
    ft = forecast[["ds","yhat","yhat_lower","yhat_upper"]].tail(12).copy()
    ft.columns = ["Week","Predicted Units","Low Estimate","High Estimate"]
    ft["Week"] = ft["Week"].dt.strftime("%b %d %Y")
    ft["Predicted Units"] = ft["Predicted Units"].astype(int)
    ft["Low Estimate"] = ft["Low Estimate"].astype(int)
    ft["High Estimate"] = ft["High Estimate"].astype(int)
    st.dataframe(ft, use_container_width=True, hide_index=True)

    st.subheader(" Inventory Recommendation")
    if OLLAMA_AVAILABLE:
        if st.button("Generate AI Recommendation"):
            with st.spinner("Asking AI for inventory advice..."):
                prompt = (
                    "You are a pharmacy inventory manager. "
                    "Write a 4 sentence inventory planning recommendation. "
                    "Current weekly B12 average: " + str(current_avg) + " units. "
                    "Forecasted weekly average: " + str(forecast_avg) + " units. "
                    "Expected growth: " + str(growth) + " percent. "
                    "Peak demand: " + str(peak_units) + " units. "
                    "Give specific reorder and stocking advice."
                )
                response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
                st.success(response["message"]["content"])
    else:
        st.info(" AI recommendations available when running locally with Ollama.")

elif page == "Batch Compliance":
    st.subheader(" Batch Expiry & Compliance Tracker")
    batches = load_batch_data()

    expired = sum(1 for b in batches if b["Status"] == "EXPIRED")
    urgent  = sum(1 for b in batches if b["Status"] == "URGENT")
    warning = sum(1 for b in batches if b["Status"] == "WARNING")
    ok      = sum(1 for b in batches if b["Status"] == "OK")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Expired", expired)
    col2.metric("Urgent (3 days)", urgent)
    col3.metric("Warning (7 days)", warning)
    col4.metric("OK", ok)

    st.markdown("---")
    st.subheader(" Current Batch Status")

    for batch in batches:
        col1, col2, col3, col4, col5 = st.columns([1,2,2,1,1])
        col1.write("**" + batch["Batch ID"] + "**")
        col2.write(batch["Compound"])
        col3.write("Expires: " + batch["Expires"])
        col4.write(str(batch["Days Left"]) + " days")
        if batch["Status"] in ["URGENT", "EXPIRED"]:
            col5.error(batch["Status"])
        elif batch["Status"] == "WARNING":
            col5.warning(batch["Status"])
        else:
            col5.success(batch["Status"])

    st.markdown("---")
    st.subheader(" Days Remaining Per Batch")
    batch_df = pd.DataFrame(batches)

    fig2 = go.Figure(go.Bar(
        x=batch_df["Batch ID"],
        y=batch_df["Days Left"],
        marker_color=batch_df["Color"].tolist(),
        text=batch_df["Days Left"],
        textposition="outside"
    ))
    fig2.update_layout(
        title="Days Until Expiry by Batch",
        xaxis_title="Batch ID",
        yaxis_title="Days Remaining",
        height=350,
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#1e1e1e",
        font=dict(color="white"),
        shapes=[
            dict(type="line", x0=-0.5, x1=4.5, y0=7, y1=7,
                 line=dict(color="#fd7e14", dash="dash", width=2)),
            dict(type="line", x0=-0.5, x1=4.5, y0=3, y1=3,
                 line=dict(color="#dc3545", dash="dash", width=2))
        ]
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Compliance Report")
    if OLLAMA_AVAILABLE:
        if st.button("Generate Compliance Report"):
            with st.spinner("Generating USP 797 compliance report..."):
                summary = "\n".join([
                    b["Batch ID"] + " | " + b["Compound"] + " | " +
                    str(b["Days Left"]) + " days left | " + b["Status"]
                    for b in batches
                ])
                prompt = (
                    "You are a USP 797 pharmacy compliance officer. "
                    "Review these batch expiry statuses and write a formal "
                    "action report with clear priorities. Keep it under 150 words: "
                    "\n\n" + summary
                )
                response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
                st.info(response["message"]["content"])
    else:
        st.info("Compliance reports available when running locally with Ollama.")