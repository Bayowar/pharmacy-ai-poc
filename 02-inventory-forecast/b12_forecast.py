import ollama
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

MODEL = "llama3.2:3b"

#Create historical sales data
# This simulates 52 weeks of B12 shot sales (1 year)
# This would come from POS system
data = {
    "ds": pd.date_range(start="2025-01-01", periods=52, freq="W"),
    "y": [
        120,115,130,140,128,135,150,145,160,155,
        148,162,170,165,158,172,180,175,168,182,
        190,185,178,192,200,195,188,202,210,205,
        198,212,220,215,208,222,230,225,218,232,
        240,235,228,242,250,245,238,252,260,255,
        248,262
    ]
}

df = pd.DataFrame(data)
print("Historical data loaded: " + str(len(df)) + " weeks of sales")

#Build and train the forecast model
print("Training forecast model...")
model = Prophet(
    seasonality_mode="multiplicative",
    weekly_seasonality=False,
    yearly_seasonality=True
)
model.fit(df)

#Predict the next 12 weeks
print("Forecasting next 12 weeks...")
future = model.make_future_dataframe(periods=12, freq="W")
forecast = model.predict(future)

#Save the chart as an image
print("Generating chart...")
fig = model.plot(forecast)
plt.title("B12 Shot Demand Forecast - Next 12 Weeks")
plt.xlabel("Date")
plt.ylabel("Units Sold")
plt.tight_layout()
chart_path = "02-inventory-forecast/forecast_chart.png"
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
print("Chart saved to: " + chart_path)

#Pull key numbers for the AI summary
last_4_weeks_avg = int(df["y"].tail(4).mean())
next_12_weeks_avg = int(forecast["yhat"].tail(12).mean())
peak_week = forecast.tail(12).loc[forecast["yhat"].idxmax(), "ds"].strftime("%B %d %Y")
peak_units = int(forecast["yhat"].max())

#Ask AI to write an inventory recommendation 
print("Generating AI inventory recommendation...")
prompt = (
    "You are a pharmacy inventory manager. "
    "Write a 4 sentence inventory planning recommendation based on these numbers: "
    "Current average weekly B12 sales: " + str(last_4_weeks_avg) + " units. "
    "Forecasted average weekly sales next 12 weeks: " + str(next_12_weeks_avg) + " units. "
    "Peak demand week: " + peak_week + " with " + str(peak_units) + " units. "
    "Give specific advice on stock levels and reorder timing."
)

response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": prompt}]
)

print("\n" + "=" * 52)
print("B12 DEMAND FORECAST REPORT")
print("=" * 52)
print("Current weekly average:   " + str(last_4_weeks_avg) + " units")
print("Forecasted weekly average: " + str(next_12_weeks_avg) + " units")
print("Peak demand week:          " + peak_week)
print("Peak units:                " + str(peak_units))
print("\n--- AI Inventory Recommendation ---")
print(response["message"]["content"])
print("\nChart saved to: " + chart_path)