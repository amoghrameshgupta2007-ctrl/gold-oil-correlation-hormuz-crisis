import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from datetime import datetime

#data loading
gold = yf.download(tickers = "GC=F", interval = "1d", start = "2025-08-01", end = "2026-08-19")
crude = yf.download(tickers = "CL=F", interval = "1d", start = "2025-08-01", end = "2026-08-19")

#changes all the columns from a tuple to just the first word, so it changed to lsuffix and rsuffix in line 15
gold.columns = gold.columns.get_level_values(0)
crude.columns = crude.columns.get_level_values(0)


merged = gold.join(crude, how = "inner", lsuffix = "_gold", rsuffix = "_crude")

merged['Return_gold'] = merged['Close_gold'].pct_change()
merged['Return_crude'] = merged['Close_crude'].pct_change()

merged['type'] = np.where(merged.index < '2026-02-28', 'calm', 'crisis')


calm = merged[merged['type'] == 'calm']
crisis = merged[merged['type'] == 'crisis']
calm_corr = calm['Return_gold'].corr(calm['Return_crude'])
crisis_corr = crisis['Return_gold'].corr(crisis['Return_crude'])

merged['rolling_corr'] = merged['Return_gold'].rolling(window=30).corr(merged['Return_crude'])


# VISUALISATION 1
plt.figure(figsize=(12, 6))
plt.plot(merged.index, merged['rolling_corr'], label='30-day rolling correlation')
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.axvline(pd.Timestamp('2026-02-28'), color='red', linestyle='--', label='Crisis start')
plt.title('30-Day Rolling Correlation: Gold vs. Crude Oil Returns')
plt.xlabel('Date')
plt.ylabel('Correlation')
plt.legend()
plt.savefig('rolling_correlation.png')
plt.show()

# VISUALISATION 2
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharex=True, sharey=True)
ax1.scatter(calm['Return_gold'], calm['Return_crude'], color='steelblue', alpha=0.6)
ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax1.axvline(0, color='gray', linestyle='--', linewidth=0.8)
ax1.set_title('Calm Period')
ax1.set_xlabel('Gold Daily Return')
ax1.set_ylabel('Crude Oil Daily Return')
ax2.scatter(crisis['Return_gold'], crisis['Return_crude'], color='crimson', alpha=0.6)
ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax2.axvline(0, color='gray', linestyle='--', linewidth=0.8)
ax2.set_title('Crisis Period')
ax2.set_xlabel('Gold Daily Return')
plt.suptitle('Gold vs. Crude Oil Daily Returns: Calm vs. Crisis')
plt.savefig('calm_vs_crisis_scatter.png')
plt.show()

# VISUALISATION 3
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(merged.index, merged['Close_gold'], color='goldenrod', label='Gold')
ax1.set_xlabel('Date')
ax1.set_ylabel('Gold Price (USD)', color='goldenrod')
ax2 = ax1.twinx()
ax2.plot(merged.index, merged['Close_crude'], color='black', label='Crude Oil')
ax2.set_ylabel('Crude Oil Price (USD)', color='black')
ax1.axvline(pd.Timestamp('2026-02-28'), color='red', linestyle='--', label='Crisis start')
plt.title('Gold and Crude Oil Prices Over Time')
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.savefig('price_trends.png')
plt.show()

print(calm_corr)
print(crisis_corr)
