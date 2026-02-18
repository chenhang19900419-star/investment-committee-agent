import csv
import math
import matplotlib.pyplot as plt

rows = [
    {"year": 2018, "gmv_total_billion_rmb": 515.6, "net_profit_billion_rmb": -115.492695},
    {"year": 2019, "gmv_total_billion_rmb": 682.1, "net_profit_billion_rmb": 2.236165},
    {"year": 2020, "gmv_total_billion_rmb": math.nan, "net_profit_billion_rmb": 4.707612},
    {"year": 2021, "gmv_total_billion_rmb": math.nan, "net_profit_billion_rmb": -23.536198},
    {"year": 2022, "gmv_total_billion_rmb": math.nan, "net_profit_billion_rmb": -6.685323},
    {"year": 2023, "gmv_total_billion_rmb": math.nan, "net_profit_billion_rmb": 13.857331},
    {"year": 2024, "gmv_total_billion_rmb": math.nan, "net_profit_billion_rmb": 35.808322},
]

csv_path = "/Users/chenhang/Desktop/investment_agent/knowledge/docs/meituan_gmv_netprofit_trend_data.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["year", "gmv_total_billion_rmb", "net_profit_billion_rmb"])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

years = [r["year"] for r in rows]
gmv = [r["gmv_total_billion_rmb"] for r in rows]
profit = [r["net_profit_billion_rmb"] for r in rows]

plt.style.use("seaborn-v0_8-whitegrid")

# GMV trend
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, gmv, marker="o", linewidth=2, color="#1f77b4")
for y, v in zip(years, gmv):
    if isinstance(v, float) and math.isnan(v):
        ax.annotate("N/A", (y, 515.6), textcoords="offset points", xytext=(0, -16), ha="center", fontsize=9, color="#666666")
ax.set_title("Meituan Total Platform GMV Trend (Annual Report Disclosure)")
ax.set_xlabel("Year")
ax.set_ylabel("GMV (RMB bn)")
ax.set_xticks(years)
ax.set_ylim(450, 730)
ax.text(0.01, -0.18, "Note: 2020-2024 annual reports did not disclose total platform GMV in absolute value.", transform=ax.transAxes, fontsize=9, color="#444444")
fig.tight_layout()
gmv_png = "/Users/chenhang/Desktop/investment_agent/knowledge/docs/meituan_gmv_trend.png"
fig.savefig(gmv_png, dpi=160)
plt.close(fig)

# Net profit trend
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, profit, marker="o", linewidth=2, color="#d62728")
ax.axhline(0, color="#888888", linewidth=1)
for y, v in zip(years, profit):
    ax.annotate(f"{v:.1f}", (y, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
ax.set_title("Meituan Net Profit Trend")
ax.set_xlabel("Year")
ax.set_ylabel("Net profit (RMB bn)")
ax.set_xticks(years)
fig.tight_layout()
profit_png = "/Users/chenhang/Desktop/investment_agent/knowledge/docs/meituan_net_profit_trend.png"
fig.savefig(profit_png, dpi=160)
plt.close(fig)

print(gmv_png)
print(profit_png)
print(csv_path)
