# US Import Elasticity to 2025 U.S Tariffs

## Author
Tanmay Bothra

**How much did US imports fall in response to the 2025 tariff wave?**  
An empirical panel OLS investigation using monthly Census Bureau trade data and the Center for Global Development tariff tracker.

---

## Introduction

Beginning on April 2, 2025 ("Liberation Day"), the Trump administration imposed sweeping new tariffs on imports from nearly every US trading partner. Unlike earlier rounds of targeted trade action, these tariffs were broad-based, applying to most goods from most countries simultaneously — with China facing rates in a separate regime entirely.

This project estimates the **import demand elasticity** with respect to the added effective tariff rate: how much did a one-percentage-point increase in the tariff rate reduce US monthly imports from a given country? The answer matters for several reasons:

- **Fiscal revenue vs. trade suppression tradeoff.** Tariffs only generate revenue if trade continues. High elasticity means imports collapse and revenue falls short of projections.
- **Inflation pass-through.** If imports fall substantially, domestic producers face less competition and prices rise. If imports are inelastic, the tariff functions more like a tax on US consumers.
- **Geopolitical reorientation.** Countries whose exports to the US fall sharply face strong incentives to deepen trade ties with China and other partners, with long-run implications for US economic leverage.
- **Supply chain disruption.** US manufacturers relying on imported inputs face cost increases that compound across production stages.

This analysis provides an early empirical estimate of that elasticity. With the panel currently extending to January 2026 and additional tariff variation expected from the February 2026 escalations, results will sharpen considerably as more data becomes available.

---

## Data

### US Import Data — Census Bureau

Monthly US import values (USD millions, CIF basis) by country of origin, covering April 2025 through January 2026. Source: [US Census Bureau Foreign Trade Division](https://www.census.gov/foreign-trade/statistics/country/index.html).

The raw file includes aggregate rows (World totals, regional aggregates, USMCA groupings) which are dropped prior to analysis. Country names are harmonized to match the CGDev naming convention (e.g. "Burma" → "Myanmar", "Korea, South" → "South Korea"). Hong Kong and Macau are excluded because they receive separate tariff treatment not captured in the CGDev tracker.

### Tariff Data — Center for Global Development

Tariff exposure is measured using the [CGDev US Tariff Tracker](https://www.cgdev.org/media/us-tariff-tracker-measuring-effective-tariff-rates), which publishes the **added effective tariff rate** (ETR) for each country at multiple snapshot dates throughout 2025. The Added ETR at any given snapshot time in 2025 is the difference between the effective tariff rate imposed on a country at that snapshot time and the effective tariff rate facing it in January 2025.

The CGDev rate is more analytically useful than headline tariff rates because it computes a trade-weighted average across tariff categories. Specifically, for each country the tracker disaggregates that country's US-bound exports by product category, looks up the applicable tariff rate for each category, and computes a weighted average using each category's share of the country's total US-bound exports as the weight. The result is an **effective rate** — what a representative dollar of exports from that country actually faces on average at the US border — rather than the statutory rate on any single product. This is especially important in 2025 because different sectors (steel, aluminum, semiconductors, general goods) faced different tariff schedules applied through different legal authorities (Section 232, Section 301, IEEPA), and headline figures often conflate these.

Five tariff snapshots are used:

| Snapshot | Date | Months assigned |
|---|---|---|
| `apr29` | April 29, 2025 | April 2025 |
| `may22` | May 22, 2025 | May 2025 |
| `june4` | June 4, 2025 | June–July 2025 |
| `aug7`  | August 7, 2025 | August–October 2025 |
| `nov21` | November 21, 2025 | November 2025–January 2026 |

Each month is assigned the snapshot that was **in effect for the majority of that month**, following the principle that import flows reflect purchasing and shipping decisions made under the prevailing tariff environment. The `nov6` snapshot (released November 6) is not used for November because goods arriving in November were largely ordered in September–October under the `aug7` schedule; the `nov21` rate better represents the forward tariff environment shaping December and January import decisions.

**Sample coverage:** 186 countries (without China) or 187 countries (with China), 10 months (April 2025 – January 2026), yielding approximately 1,800 observations per specification. Nine countries — Cuba, Iran, Russia, Syria, Eritrea, and four others — are excluded via `dropna()` in the regression because they lack CGDev tariff data (primarily due to pre-existing sanctions regimes unrelated to the 2025 tariff wave).

**China's tariff path** deserves special note given its extreme variation:

| Month | Added ETR | US Imports ($M) |
|---|---|---|
| Apr 2025 | 111.8% | 25,378 |
| May 2025 | 30.2% | 20,494 |
| Jun–Oct 2025 | 32.2% | ~22,000–26,000 |
| Nov 2025–Jan 2026 | 24.0% | ~21,000 |

April's high import figure likely partly reflects **pre-tariff front-running** — orders placed before April 2 clearing customs during the month. The "With China" specifications should be interpreted with caution: China's tariff swing is so large relative to other countries that the estimated coefficient in that sample primarily reflects the US-China bilateral trade war response, rather than the universal tariff effect of interest.

---

## Model

### Specification

The primary model is a **semi-log panel OLS** with two-way fixed effects:

$$\log(\text{Imports}_{it}) = \alpha_i + \gamma_t + \beta_1 \cdot \text{TariffRate}_{it} + \varepsilon_{it}$$

where:

- $\log(\text{Imports}_{it})$ is the natural log of US monthly imports from country $i$ in month $t$, in USD millions
- $\alpha_i$ is a country fixed effect, absorbing all time-invariant differences across countries (e.g. Germany always exports more than Cambodia regardless of tariffs)
- $\gamma_t$ is a time fixed effect, absorbing all shocks common to all countries in a given month (e.g. a global recession, US seasonal demand patterns, or exchange rate movements correlated across all trading partners)
- $\text{TariffRate}_{it}$ is the CGDev added effective tariff rate for country $i$ in month $t$, in percentage points
- $\varepsilon_{it}$ is the error term, clustered at the country level to account for serial correlation within countries over time

### Interpretation

Because the dependent variable is logged and the independent variable is in levels (percentage points), $\beta_1$ has a **semi-elasticity** interpretation:

$$\beta_1 \approx \frac{\Delta \log(\text{Imports})}{\Delta \text{TariffRate}} \approx \% \text{ change in imports per 1 pp increase in tariff rate}$$

### Identification

The country fixed effects remove all cross-sectional variation — the regression does not use the fact that Germany imports more than Cambodia. Identification comes entirely from **within-country, over-time variation**: did imports from country $i$ fall in months when *its specific tariff* rose, relative to what would be expected from common monthly trends? 

After two-way demeaning, the within-country standard deviation of the tariff rate is **2.68 percentage points** (without China), confirming meaningful identifying variation. This compares favorably to prior work using this design on other tariff episodes.

The **no-lag specification** is theoretically primary. Liberation Day tariffs were announced and implemented with near-zero notice (tariffs effective April 2, announced days prior), giving importers no opportunity to front-run the change, so the contemporaneous response is the theoretically expected channel. The **one-month lagged specification** is included as a robustness check, capturing any goods already in transit that could not adjust within the same month.

---

## Results

```
Independent Variable: Added effective tariff rate
Semi-log: β = % change in US imports per 1 pp increase in tariff rate

Specification                           β₁      t-stat   p-value    N    R²(within)
-------------------------------------------------------------------------------------
No Lag   | Without China            -0.0273***   -3.41    0.0007   1788     0.0104
1-Mo Lag | Without China            -0.0271**    -3.14    0.0017   1608     0.0074
No Lag   | With China               -0.0175*     -2.03    0.0424   1798     0.0069
1-Mo Lag | With China               -0.0175*     -2.16    0.0306   1617     0.0050

Significance: *** p<0.001  ** p<0.01  * p<0.05  . p<0.10

All regressions: country + time fixed effects, SEs clustered at country level.
```

### Interpretation

The preferred specification — **No Lag | Without China** — yields β₁ = −0.0273 (p < 0.001). A one-percentage-point increase in the added effective tariff rate is associated with a **2.7% decrease in US monthly imports** from that country. The result is robust across both lag structures and highly consistent (−0.0273 vs −0.0271), indicating the import response is genuinely contemporaneous rather than delayed.

To put this in concrete terms for major trading partners, using the change in each country's tariff rate between the April and November 2025 snapshots:

| Country | Tariff change (pp) | Implied import effect |
|---|---|---|
| India | +24.5 | −48.8% |
| Vietnam | +7.9 | −19.4% |
| Japan | +3.8 | −10.0% |
| Germany | +5.0 | −12.8% |

These are model-implied effects conditional on the fixed effects; actual import changes incorporate other factors. A 10 percentage point tariff increase implies approximately a **24% decline** in imports; a 20 percentage point increase implies approximately a **42% decline**.

**Effect of including China:** Adding China to the sample reduces the estimated coefficient to −0.0175, reflecting that China's enormous tariff swing (from 111.8% to 30.2% between April and May) is accompanied by a relatively modest import decline — consistent with pre-tariff front-running inflating the April baseline and supply-chain inertia in May. The without-China result is more representative of the universal tariff effect on the general population of trading partners.

**Exposure measure as robustness (not shown):** Regressions using the exposure measure (tariff rate × country's US export share) as the independent variable are uniformly insignificant. This is informative: it implies that a country's dependence on the US market does not amplify the import suppression effect *beyond* what the tariff rate already predicts. The tariff rate alone captures the relevant variation.

---

## Limitations and Next Steps

**Short panel.** Ten months is a limited window. The tariff variation across snapshots creates only 3–4 genuinely distinct tariff regimes per country, constraining identification. Results should be treated as preliminary estimates.

**Pre-tariff front-running.** April 2025 import data likely reflect elevated pre-tariff stockpiling, which inflates the April baseline and could bias the no-lag coefficient downward in magnitude (import levels appear higher than they would have been under normal conditions, making the subsequent decline look larger).

**February 2026 escalation.** The panel currently ends January 2026, before the tariff increases that followed the Supreme Court ruling on IEEPA authority in February 2026. Adding data through mid-2026 will substantially expand the identifying variation and allow estimation across a wider tariff range, sharpening the elasticity estimate considerably.

**Additional specifications to explore:**
- Heterogeneous effects by income group, trade bloc membership (USMCA, EU, ASEAN), and export concentration
- Sector-level analysis using HS-code disaggregated import data, where tariff variation is much richer
- Estimating the import-weighted tariff increase absorbed by US consumers and downstream manufacturers
- Comparison with the 2018–19 tariff elasticities to assess whether the speed and breadth of 2025 tariffs produced a different behavioral response
- Dynamic panel specifications to test for adjustment over time (whether the short-run elasticity differs from the medium-run)

---

## Repository Structure

```
├── analysis_us_imports.py        # Main analysis script
├── lists_mappings.py             # Country name mappings, snapshot assignments
├── datasets/
│   ├── us_monthly_imports_by_country.xlsx   # US Census Bureau monthly imports
│   ├── apr29_2025.csv            # CGDev tariff snapshot: April 29, 2025
│   ├── may22_2025.csv            # CGDev tariff snapshot: May 22, 2025
│   ├── june4_2025.csv            # CGDev tariff snapshot: June 4, 2025
│   ├── aug7_2025.csv             # CGDev tariff snapshot: August 7, 2025
│   ├── nov6_2025.csv             # CGDev tariff snapshot: November 6, 2025 (not used; see note)
│   └── nov21_2025.csv            # CGDev tariff snapshot: November 21, 2025
└── README.md
```

## Requirements

```
pandas
numpy
linearmodels
openpyxl
```

Install with: `pip install pandas numpy linearmodels openpyxl`

---
