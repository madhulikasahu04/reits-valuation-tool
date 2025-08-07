import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Select REIT Ticker (example: Realty Income - O)
ticker = "O"
reit = yf.Ticker(ticker)

# Fetch historical market data
data = reit.history(period="5y")

# Plot stock price
plt.figure(figsize=(12, 6))
sns.lineplot(data=data['Close'], label='Stock Price')
plt.title(f"{ticker} - REIT Stock Price Over 5 Years")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/mnt/data/stock_price_trend.png")

# Get FFO estimation using cash flow (simplified)
cashflow = reit.cashflow
try:
    ffo = (cashflow.loc['Total Cash From Operating Activities'] - cashflow.loc['Capital Expenditures']) / reit.info['sharesOutstanding']
except:
    ffo = 3.20  # Fallback in case data missing

# DCF valuation
discount_rate = 0.08
growth_rate = 0.03
years = 5

dcf = sum([ffo * (1 + growth_rate)**i / (1 + discount_rate)**i for i in range(1, years+1)])
terminal_value = ffo * (1 + growth_rate)**years / (discount_rate - growth_rate)
dcf_valuation = dcf + terminal_value / (1 + discount_rate)**years

print(f"Estimated DCF Valuation per Share: ${dcf_valuation:.2f}")

# Sensitivity analysis
discount_rates = [0.07, 0.08, 0.09]
growth_rates = [0.02, 0.03, 0.04]
valuation_matrix = pd.DataFrame(index=growth_rates, columns=discount_rates)

for g in growth_rates:
    for d in discount_rates:
        dcf_val = sum([ffo * (1 + g)**i / (1 + d)**i for i in range(1, 6)])
        tv = ffo * (1 + g)**5 / (d - g)
        valuation_matrix.loc[g, d] = round(dcf_val + tv / (1 + d)**5, 2)

print("\nDCF Sensitivity Matrix (Growth rate vs Discount rate):")
print(valuation_matrix)