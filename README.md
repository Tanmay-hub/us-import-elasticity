# U.S Import Elasticity to 2025 U.S Tariffs

**Author:** Tanmay Bothra

**How much did US imports fall in response to the 2025 tariff wave?**

An empirical panel OLS and WLS investigation using monthly Census Bureau trade data and the Center for Global Development tariff tracker.

## Introduction

Beginning on April 2, 2025 ("Liberation Day"), the Trump administration imposed sweeping new tariffs on imports from nearly every US trading partner. Unlike earlier rounds of targeted trade action, these tariffs were broad-based and simultaneously applied to most goods from most countries with China facing rates in an entirely separate regime.

This paper estimates the import demand elasticity with respect to the added effective tariff rate: how much did a one-percentage-point increase in the tariff rate reduce US monthly imports from a given country? The answer has several critical economic implications:

**Fiscal revenue vs. trade suppression tradeoff**: Tariffs have been cited by proponents as a welcome revenue-generator, but they only generate revenue if US imports continue. High elasticity means imports collapse and revenue falls short of projections.

**Inflation pass-through**: If imports fall substantially, domestic producers face less competition and prices rise. If imports are inelastic, the tariff functions more like a tax on US consumers.

**Global supply chain reorientation**: Countries whose exports to the US are highly elastic and therefore fall sharply may face strong incentives to strengthen trade ties with China and other partners, with long-run implications for US economic leverage.

**Domestic Supply chain disruption**: US Tariffs on manufacturing inputs may increase costs for American manufacturers that compound across production stages.

This analysis constructs an econometrically valid Two Way Fixed Effects panel regression for estimating that elasticity. The current data - covering April 2025 through January 2026 - does not yet show a discernible import response among major trading partners, but the model is well-positioned to produce precise estimates as 2026 import data becomes available, particularly once tariff variation following the February 2026 SCOTUS IEEPA ruling can be tested.

## Data

1\) US Import Data - [Census Bureau](https://www.census.gov/foreign-trade/statistics/country/index.html)

Monthly US import values (USD millions, CIF basis) by country of origin, covering April 2025 through January 2026.

The raw file includes aggregate rows (World totals, regional aggregates, USMCA groupings) which are dropped prior to analysis. Country names are harmonized to match the CGDev naming convention (e.g. "Burma" becomes "Myanmar", and "Korea, South" becomes "South Korea"). Hong Kong and Macau are excluded because they receive separate tariff treatment not captured in the CGDev tracker.

2\) Tariff Data - [Center for Global Development](https://www.cgdev.org/media/us-tariff-tracker-measuring-effective-tariff-rates)

Tariff exposure is measured using the CGDev US Tariff Tracker, which publishes the added Effective Tariff Rate (ETR) for each country at multiple snapshot dates throughout 2025. The Added ETR at any given snapshot time in 2025 is the difference between the effective tariff rate imposed on a country at that snapshot time and the effective tariff rate facing it in January 2025.

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

Table 1: Added ETR calculation date and month assignment

Each month is assigned the snapshot whose rate was in effect for the majority of that month, following the principle that import flows reflect conditions under the prevailing tariff regime. June and July are both governed by the `june4` snapshot because CGDev's `july12` snapshot had to do with tariff changes set to take effect in August, which ended up being mostly governed by the `aug7` snapshot. By the same reasoning, `nov6` governs November rather than `nov21`. And `nov21` governs December 2025 and January 2026 because the next tariff snapshot provided by CGDev is as of February 23 2026.

**Sample coverage**: 186 countries (without China) or 187 countries (with China), 10 months (April 2025 – January 2026), yielding approximately 1,800 observations per specification. Nine countries are excluded via `dropna()` in the regression because they lack CGDev tariff data, primarily due to pre-existing sanctions regimes unrelated to the 2025 tariff wave.

The extreme variation in China's tariff path necessitates modeling a dataset that excludes imports from the country. The wide range of tariffs applied to Chinese imports coupled with the large volume of those imports means that a model which includes China in the dataset would largely capture changes in US-China trade rather than a more universally applicable tariff elasticity - China's unique status as the world's second-largest economy, largest trading partner to most countries, and one of America's largest trading partners means that its ability to retaliate against US tariffs or divert exports from the US to other countries cannot easily be replicated by other countries.

| Month | Snapshot | ETR (%) | Imports (USD $M) |
|---|---|---|---|
| Apr 2025 | Apr 29 | 111.80 | 25,378 |
| May 2025 | May 22 | 30.20 | 20,494 |
| Jun 2025 | Jun 4 | 32.19 | 18,949 |
| Jul 2025 | Jun 4 | 32.19 | 26,411 |
| Aug 2025 | Aug 7 | 32.19 | 25,133 |
| Sep 2025 | Aug 7 | 32.19 | 23,415 |
| Oct 2025 | Aug 7 | 32.19 | 23,887 |
| Nov 2025 | Nov 6 | 24.13 | 20,951 |
| Dec 2025 | Nov 21 | 24.01 | 21,104 |
| Jan 2026 | Nov 21 | 24.01 | 21,058 |

*Note: Nov 2025 ETR is from the Nov 6 snapshot (in effect for most of the month).*

Table 2: China's tariff path and monthly imports

April's high import figure amidst the ~111% effective tariff rate that took effect on liberation day likely partly reflects pre-tariff front-running - orders placed before April 2 clearing customs during the month. This concern is more specific to China because actions such as ending the de minimis exemption for Chinese goods in February and imposing a 20% tariff on Chinese goods in March of 2025 had widely raised expectations of much higher tariffs on Chinese imports in a way that did not apply to other countries. The universal baseline 10% tariff on all other countries came as a greater shock to markets than higher tariffs on China.

The "With China" specifications should therefore be interpreted with caution throughout.

## Model

### Specification

The primary model is a semi-log panel OLS with two-way fixed effects

$$\log(\text{Imports}_{it}) = \alpha_i + \gamma_t + \beta_1 \cdot \text{TariffRate}_{it} + \varepsilon_{it}$$

*Equation 1: Regressing the log of imports from country i in month t on the ETR facing i during t*

where:

- **log(Importsᵢₜ)** is the natural log of US monthly imports in USD millions from country i in month t
- **αᵢ** is a country fixed effect, absorbing all time-invariant differences across countries
- **γₜ** is a time fixed effect, absorbing all shocks common to all countries in a given month
- **TariffRateᵢₜ** is the CGDev added effective tariff rate in percentage points for country i in month t
- **εᵢₜ** is the error term clustered at the country level to account for serial correlation within countries over time

The country and time fixed effects remove all cross-sectional variation, and identification comes entirely from within-country variation over time.

Equation 1, as a no-lag specification, is theoretically primary as Liberation Day tariffs were announced and implemented with near-zero notice and gave importers no opportunity to front-run the change. The one-month lagged specification in Equation 2 below is included as a robustness check to capture any goods already in transit that could not adjust within the same month. Front-running and transit-goods inertia are distinct concerns as the former inflates the April baseline specifically for China, while the latter motivates the lag spec as a check on whether any part of the import response operates through shipments that had already cleared the border before tariffs took effect.

$$\log(\text{Imports}_{it}) = \alpha_i + \gamma_t + \beta_1 \cdot \text{TariffRate}_{it-1} + \varepsilon_{it}$$

*Equation 2: Regressing the log of imports from country i in month t on the ETR facing i during t - 1*

### Interpretation

Because the dependent variable is logged and the independent variable is in levels (percentage points), $\beta_1$ has the following interpretation:

$$\beta_1 \approx \frac{\Delta\log(\text{Imports})}{\Delta\text{TariffRate}} \approx \text{percentage change in monthly imports for a 1 percentage-point increase in the ETR}$$

## Results

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

Table 3: Baseline OLS regression results

The full-sample baseline yields β₁ = −0.0269 (p < 0.001) in the preferred no-lag specification, statistically significant and consistent in sign across lag structures, though the 1-Mo Lag coefficient is somewhat smaller in magnitude (−0.0221). The within-R² of roughly 1% is a warning sign that tariff variation is explaining very little of the total variance in import growth even where the coefficient is significant, and the robustness checks demonstrate why.

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

Table 4: Robustness checks with a WLS model weighted by import value and an OLS regression on the top-50 exporters to the U.S

Both robustness checks produce statistically insignificant coefficients of much smaller magnitudes for large trading partners. The WLS without-China estimate collapses from −0.0269 to essentially zero (−0.0010, p = 0.80), and the Top-50 without-China estimate is similarly flat (−0.0039, p = 0.35). This pattern across two independent approaches indicates that the baseline result is driven by small and volatile trading partners such that a small absolute change in imports translates to a large percentage swing rather than by the economically significant bilateral relationships that dominate US trade.

The robustness checks include a surprisingly statistically significant result, namely the +0.0016* coefficient in the no-lag WLS regression on a dataset including China. This statistically significant positive coefficient, which implies greater imports when tariffs rise, is likely an artifact of the previously described April 2025 front-running problem interacting with China's dominant weight in the WLS sample. China's within-country variation pairs April's higher imports and extraordinarily high ETR of around 111% (see Table #1) with the lower tariffs and lower imports of subsequent months to create a spurious positive correlation between tariffs and import levels when China is heavily weighted. The 1-Mo Lag WLS with China being negative and marginally significant (−0.0008, p = 0.098) is consistent with this interpretation as the lag partially decouples the front-running April baseline from the tariff value and corrects the sign.

**Effect of including China:** China's addition the baseline no-lag reduces the estimated coefficient from −0.0269 to −0.0170, which shows that China's enormous tariff swing (from 111.8% in April to ~30% during later months) is accompanied by a smaller-than-expected import decline and is consistent with front-running inflating the April baseline. The without-China result is more representative of the universal tariff effect on the general population of trading partners.

## Conclusion

The 2025 tariff wave, as measured from April 2025 to January 2026, does not produce a statistically detectable import reduction among major US trading partners. The full-sample negative result appears to be a statistical artifact of small-country noise rather than large-scale export diversion by economically significant partners. This does not mean tariffs have had no effect but rather that the current 10-month window, which is dominated by a single large tariff shock with limited subsequent variation, does not yet provide sufficient identifying variation to precisely estimate the elasticity for large partners. The model is well-positioned to test that elasticity as richer variation from 2026 becomes available, particularly following tariff changes from SCOTUS's February 2026 ruling on the IEEPA's invalidity as grounds for a U.S President to impose tariffs.

## Limitations and Next Steps

**Small-country heterogeneity**: The baseline estimate is driven by small trading partners with volatile trade flows, where modest absolute changes in imports register as large percentage swings. Among the 50 largest US trading partners, which account for the overwhelming majority of US import value, the estimated effect is statistically indistinguishable from zero in both robustness specifications. Recommendable modifications could include modeling this heterogeneity or restricting the primary sample to partners above a minimum import threshold.

**Pre-tariff front-running**: April 2025 import data for China likely reflects elevated pre-tariff stockpiling, inflating the April baseline for that country specifically. The concern is most acute for China given the scale of its tariff swing; the uniform 10% Liberation Day rate applied to most other countries is less likely to have generated comparable anticipatory behavior. The consistency of the no-lag and 1-Mo Lag baseline results in the without-China specifications somewhat mitigates concerns about a broader front-running bias, but it cannot be fully resolved without pre-April data extending further back.

**Short panel with limited tariff variation**: The panel dataset includes 10 months of import data (April 2025 - January 2026). The tariff path of most countries consists of a step up in April 2025 followed by approximate stability, meaning there are effectively only 2–3 distinct tariff regimes per country over the sample, and the identifying variation comes almost entirely from cross-country differences in how large the April step was. More variation across time within countries would sharpen identification considerably, and post-January-2026 import data, coupled with tariff changes following the February 2026 Supreme Court IEEPA ruling that invalidated many of them, will bring us much closer to that goal.

**Additional specifications to explore**:
- Estimating elasticity by income group, trade bloc membership (USMCA, EU, ASEAN), and export concentration
- Estimating elasticity by country and product category, for which there will be greater tariff variation
- Comparing import elasticity to 2025 tariffs to the elasticity of previous rounds of tariffs (such as 2018-2019)
