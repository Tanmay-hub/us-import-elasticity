# US Import Elasticity to 2025 U.S Tariffs
 
## Author
Tanmay Bothra
 
**How much did US imports fall in response to the 2025 tariff wave?**
An empirical panel OLS investigation using monthly Census Bureau trade data and the Center for Global Development tariff tracker.
 
---
 
## Introduction
 
Beginning on April 2, 2025 ("Liberation Day"), the Trump administration imposed sweeping new tariffs on imports from nearly every US trading partner. Unlike earlier rounds of targeted trade action, these tariffs were broad-based and simultaneously applied to most goods from most countries with China facing rates in an entirely separate regime.
 
This project estimates the **import demand elasticity** with respect to the added effective tariff rate: how much did a one-percentage-point increase in the tariff rate reduce US monthly imports from a given country? The answer has several critical economic implications:
 
- **Fiscal revenue vs. trade suppression tradeoff:** Tariffs have been cited by proponents as a welcome revenue-generator, but they only generate revenue if US imports continue. High elasticity means imports collapse and revenue falls short of projections.
- **Inflation pass-through.** If imports fall substantially, domestic producers face less competition and prices rise. If imports are inelastic, the tariff functions more like a tax on US consumers.
- **Global supply chain reorientation:** Countries whose exports to the US are highly elastic and therefore fall sharply may face strong incentives to strengthen trade ties with China and other partners, with long-run implications for US economic leverage.
- **Domestic Supply chain disruption:** US Tariffs on manufacturing inputs may increase costs for American manufacturers that compound across production stages.
 
This analysis constructs an econometrically valid Two Way Fixed Effects panel regression for estimating that elasticity. The current data - covering April 2025 through January 2026 - does not yet show a discernible import response among major trading partners, but the model is well-positioned to produce precise estimates as 2026 import data becomes available, particularly once tariff variation following the February 2026 SCOTUS IEEPA ruling can be tested.
 
---
 
## Data
 
### US Import Data — Census Bureau
 
Monthly US import values (USD millions, CIF basis) by country of origin, covering April 2025 through January 2026. Source: [US Census Bureau Foreign Trade Division](https://www.census.gov/foreign-trade/statistics/country/index.html).
 
The raw file includes aggregate rows (World totals, regional aggregates, USMCA groupings) which are dropped prior to analysis. Country names are harmonized to match the CGDev naming convention (e.g. "Burma" becomes "Myanmar", and "Korea, South" becomes "South Korea"). Hong Kong and Macau are excluded because they receive separate tariff treatment not captured in the CGDev tracker.
 
### Tariff Data — Center for Global Development
 
Tariff exposure is measured using the [CGDev US Tariff Tracker](https://www.cgdev.org/media/us-tariff-tracker-measuring-effective-tariff-rates), which publishes the **added effective tariff rate** (ETR) for each country at multiple snapshot dates throughout 2025. The Added ETR at any given snapshot time in 2025 is the difference between the effective tariff rate imposed on a country at that snapshot time and the effective tariff rate facing it in January 2025.
 
The CGDev rate is more analytically useful than headline tariff rates because it computes a trade-weighted average across tariff categories. Specifically, for each country the tracker disaggregates that country's US-bound exports by product category, looks up the applicable tariff rate for each category, and computes a weighted average using each category's share of the country's total US-bound exports as the weight. This is especially important in 2025 because different sectors (steel, aluminum, semiconductors, general goods) faced different tariff schedules applied through different legal authorities (Section 232, Section 301, IEEPA), and headline figures often conflate these.
 
Six tariff snapshots are used:
 
| Snapshot | Date | Months assigned |
|---|---|---|
| `apr29` | April 29, 2025 | April 2025 |
| `may22` | May 22, 2025 | May 2025 |
| `june4` | June 4, 2025 | June–July 2025 |
| `aug7`  | August 7, 2025 | August–October 2025 |
| `nov6`  | November 6, 2025 | November 2025 |
| `nov21` | November 21, 2025 | December 2025–January 2026 |
 
Each month is assigned the snapshot whose rate was in effect for the majority of that month, following the principle that import flows reflect conditions under the prevailing tariff regime. The `june4` snapshot governs July as well as June because the next rate change (`aug7`) did not take effect until August; by the same logic, `nov6` governs November and `nov21` governs December and January.
 
**Sample coverage:** 186 countries (without China) or 187 countries (with China), 10 months (April 2025 – January 2026), yielding approximately 1,800 observations per specification. Nine countries — Cuba, Iran, Russia, Syria, Eritrea, and four others — are excluded via `dropna()` in the regression because they lack CGDev tariff data (primarily due to pre-existing sanctions regimes unrelated to the 2025 tariff wave).
 
The extreme variation in China's tariff path necessitates modeling a dataset that excludes imports from the country. The wide range of tariffs applied to Chinese imports coupled with the large volume of those imports means that a model which includes China in the dataset would largely capture changes in US-China trade rather than a more universally applicable tariff elasticity - China's unique status as the world's second-largest economy, largest trading partner to most countries, and one of America's largest trading partners means that its ability to retaliate against US tariffs or divert exports from the US to other countries cannot easily be replicated by other countries.
 
| Month | Added ETR | US Imports ($M) |
|---|---|---|
| Apr 2025 | 111.8% | 25,378 |
| May 2025 | 30.2% | 20,494 |
| Jun–Oct 2025 | 32.2% | ~22,000–26,000 |
| Nov 2025–Jan 2026 | 24.0% | ~21,000 |
 
April's high import figure amidst the ~111% effective tariff rate that took effect on liberation day likely partly reflects pre-tariff front-running - orders placed before April 2 clearing customs during the month. This concern is more specific to China because actions such as ending the de minimis exemption for Chinese goods in February and imposing a 20% tariff on Chinese goods in March of 2025 had widely raised expectations of much higher tariffs on Chinese imports in a way that did not apply to other countries. The universal baseline 10% tariff on all other countries came as a greater shock to markets than higher tariffs on China.  

The "With China" specifications should therefore be interpreted with caution throughout.
 
---
 
## Model
 
### Specification
 
The primary model is a semi-log panel OLS with two-way fixed effects:
 
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
 
The country and time fixed effects remove all cross-sectional variation, and identification comes entirely from within-country, over-time variation.
 
The no-lag specification is theoretically primary. Liberation Day tariffs were announced and implemented with near-zero notice (tariffs effective April 2, announced days prior), giving importers no opportunity to front-run the change, so the contemporaneous response is the theoretically expected channel. The one-month lagged specification is included as a robustness check, capturing any goods already in transit that could not adjust within the same month. Note that front-running and transit-goods inertia are distinct concerns: the former inflates the April baseline for China specifically, while the latter motivates the lag spec as a check on whether any part of the import response operates through shipments that had already cleared the border before tariffs took effect.
 
---
 
## Results
 
### Baseline (all countries)
 
```
Baseline: Added effective tariff rate (all countries)
Semi-log: β = % change in US imports per 1 pp increase in tariff rate
 
Specification                           β₁      t-stat   p-value    N    R²(within)
-------------------------------------------------------------------------------------
No Lag   | Without China            -0.0269***   -3.43    0.0006   1788     0.0098
1-Mo Lag | Without China            -0.0221**    -3.12    0.0019   1608     0.0037
No Lag   | With China               -0.0170*     -2.00    0.0458   1798     0.0066
1-Mo Lag | With China               -0.0141*     -2.16    0.0309   1617     0.0027
 
Significance: *** p<0.001  ** p<0.01  * p<0.05  . p<0.10
All regressions: country + time fixed effects, SEs clustered at country level.
```
 
The full-sample baseline yields β₁ = −0.0269 (p < 0.001) in the preferred no-lag specification, statistically significant and consistent in sign across lag structures, though the 1-Mo Lag coefficient is somewhat smaller in magnitude (−0.0221). The within-R² of roughly 1% is a warning sign: tariff variation is explaining very little of the total variance in import growth, even where the coefficient is significant. The robustness checks below clarify why.
 
### Robustness checks
 
```
Robustness 1: WLS weighted by average monthly import value
(Up-weights large trading partners)
 
Specification                           β₁      t-stat   p-value    N    R²(within)
-------------------------------------------------------------------------------------
No Lag   | Without China            -0.0010      -0.25    0.8023   1788     0.0011
1-Mo Lag | Without China            +0.0028      +0.73    0.4680   1608     0.0012
No Lag   | With China               +0.0016*     +2.14    0.0326   1798     0.0031
1-Mo Lag | With China               -0.0008.     -1.66    0.0979   1617     0.0005
 
Robustness 2: Top-50 exporters to the US (by avg monthly imports)
(Restricts sample to economically significant trading partners)
 
Specification                           β₁      t-stat   p-value    N    R²(within)
-------------------------------------------------------------------------------------
No Lag   | Without China            -0.0039      -0.93    0.3537    491     0.0092
1-Mo Lag | Without China            -0.0016      -0.41    0.6807    442     0.0004
No Lag   | With China               -0.0003      -0.15    0.8808    501     0.0005
1-Mo Lag | With China               -0.0013      -1.43    0.1543    451     0.0006
```
 
Both robustness checks produce coefficients indistinguishable from zero for large trading partners. The WLS without-China estimate collapses from −0.0269 to essentially zero (−0.0010, p = 0.80), and the Top-50 without-China estimate is similarly flat (−0.0039, p = 0.35). This pattern across two independent approaches indicates that the baseline result is driven by small and volatile trading partners such that a small absolute change in imports translates to a large percentage swing rather than by the economically significant bilateral relationships that dominate US trade.
 
**The +0.0016\* anomaly (WLS, No Lag, With China)** warrants specific explanation. This statistically significant positive coefficient, which implies greater imports when tariffs rise, is an artifact of the April front-running problem interacting with China's dominant weight in the WLS sample. China's within-country variation pairs April (tariff: 111.8%, imports: $25.4B, inflated by pre-tariff stockpiling) with subsequent months (lower tariffs, lower imports), creating a spurious positive correlation between tariffs and import levels when China is heavily weighted. The 1-Mo Lag WLS with China is negative and marginally significant (−0.0008, p = 0.098), consistent with this interpretation: the lag partially decouples the front-running April baseline from the tariff value, partially correcting the sign.
 
**Effect of including China:** In the baseline, adding China reduces the estimated coefficient from −0.0269 to −0.0170, reflecting that China's enormous tariff swing (from 111.8% in April to ~30% subsequently) is accompanied by a smaller-than-expected import decline, consistent with front-running inflating the April baseline. The without-China result is more representative of the universal tariff effect on the general population of trading partners.
 
**Exposure measure (not shown):** Regressions using the exposure measure (tariff rate × country's US export share) as the independent variable are uniformly insignificant. This implies that a country's dependence on the US market does not amplify the import suppression effect beyond what the tariff rate already predicts. The tariff rate alone captures the relevant variation.
 
### Summary
 
The 2025 tariff wave, as measured through January 2026, does not produce a statistically detectable import reduction among major US trading partners. The full-sample negative result appears to be a statistical artifact of small-country noise rather than a genuine behavioral response by economically significant exporters. This does not mean tariffs have had no effect but rather that the current 10-month window, dominated by a single large tariff shock with limited subsequent variation, does not yet provide sufficient identifying variation to precisely estimate the elasticity for large partners. The framework is well-specified and ready to test that elasticity as richer variation from 2026 becomes available.
 
---
 
## Limitations and Next Steps
 
**Small-country heterogeneity:** The baseline estimate is driven by small trading partners with volatile trade flows, where modest absolute changes in imports register as large percentage swings. Among the 50 largest US trading partners — the countries that account for the overwhelming majority of US import value — the estimated effect is statistically indistinguishable from zero in both robustness specifications. Future work should consider explicitly modeling this heterogeneity, or restricting the primary sample to partners above a minimum import threshold.
 
**Short panel with limited tariff variation.:* Ten months is a constrained window. For most non-China countries, the tariff path consists of a step up in April 2025 followed by approximate stability, meaning there are effectively only 2–3 distinct tariff regimes per country over the sample, and the identifying variation comes almost entirely from cross-country differences in how large the April step was. More variation across time within countries would sharpen identification considerably.
 
**Pre-tariff front-running:** April 2025 import data for China likely reflects elevated pre-tariff stockpiling, inflating the April baseline for that country specifically. The concern is most acute for China given the scale of its tariff swing; the uniform 10% Liberation Day rate applied to most other countries is less likely to have generated comparable anticipatory behavior. The consistency of the no-lag and 1-Mo Lag baseline results in the without-China specifications somewhat mitigates concerns about a broader front-running bias, but it cannot be fully resolved without pre-April data extending further back.
 
**February 2026 SCOTUS ruling:** The panel currently ends January 2026, before the tariff changes following the Supreme Court ruling on IEEPA authority in February 2026. This is the most important near-term extension as the ruling introduced renewed tariff variation across a different set of countries that the current panel lacks. Adding data through mid-2026 should substantially sharpen the elasticity estimate for large trading partners.
 
**Additional specifications to explore:**
- Heterogeneous effects by income group, trade bloc membership (USMCA, EU, ASEAN), and export concentration
- Sector-level analysis using HS-code disaggregated import data, where tariff variation is much richer
- Estimating the import-weighted tariff increase absorbed by US consumers and downstream manufacturers
- Comparison with the 2018–19 tariff elasticities to assess whether the speed and breadth of 2025 tariffs produced a different behavioral response
- Dynamic panel specifications to test for adjustment over time (whether the short-run elasticity differs from the medium-run)
 
---
 
## Repository Structure
 
```
├── analysis.py                          # Main analysis script
├── lists_mappings.py                    # Country name mappings, snapshot assignments
├── datasets/
│   ├── us_monthly_imports_by_country.xlsx   # US Census Bureau monthly imports
│   ├── apr29_2025.csv                   # CGDev tariff snapshot: April 29, 2025
│   ├── may22_2025.csv                   # CGDev tariff snapshot: May 22, 2025
│   ├── june4_2025.csv                   # CGDev tariff snapshot: June 4, 2025
│   ├── aug7_2025.csv                    # CGDev tariff snapshot: August 7, 2025
│   ├── nov6_2025.csv                    # CGDev tariff snapshot: November 6, 2025
│   └── nov21_2025.csv                   # CGDev tariff snapshot: November 21, 2025
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
