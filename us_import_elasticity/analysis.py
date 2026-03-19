"""
Tests whether higher US tariff rates reduced US monthly imports
from the tariffed country (direct trade suppression effect).
 
Panel OLS with country + time fixed effects.
Dependent Variable:  log(US monthly imports from country, USD millions)
Independent Variable:  Added effective tariff rate (primary) that applies for most of the month corresponding to that of the independent variable
 
Four main specifications:
  A1: No Lag   | Without China
  A2: 1-Mo Lag | Without China
  B1: No Lag   | With China
  B2: 1-Mo Lag | With China
 
Each specification is run as an OLS and WLS on the entire dataset and an OLS on the 50 largest exporters to the U.S. 
 
Source data:
  - US Census Bureau monthly imports by country (USD millions)
  - Center for Global Development US Tariff Tracker snapshots
"""
 
import os
import warnings
warnings.filterwarnings('ignore')
 
import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
from lists_mappings import MONTH_TO_SNAPSHOT, CENSUS_MONTH_COLS, CENSUS_ROWS_TO_DROP, CENSUS_TO_CGDEV
 
# ── 1. CONFIGURATION ──────────────────────────────────────────────────────────
 
_BASE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_BASE, 'datasets')
 
CGDEV_FILES = {
    'apr29': os.path.join(_DATA, 'apr29_2025.csv'),
    'may22': os.path.join(_DATA, 'may22_2025.csv'),
    'june4': os.path.join(_DATA, 'june4_2025.csv'),
    'aug7':  os.path.join(_DATA, 'aug7_2025.csv'),
    'nov6':  os.path.join(_DATA, 'nov6_2025.csv'),
    'nov21': os.path.join(_DATA, 'nov21_2025.csv'),
}

CENSUS_FILE = os.path.join(_DATA, 'us_monthly_imports_by_country.xlsx')
 
 
# ── 2. LOAD AND RESHAPE CENSUS DATA ──────────────────────────────────────────
 
print("=" * 60)
print("STEP 1: Loading and reshaping US Census import data")
print("=" * 60)
 
census_raw = pd.read_excel(CENSUS_FILE)
 
# Drop aggregate rows
census_raw = census_raw[~census_raw['CTYNAME'].isin(CENSUS_ROWS_TO_DROP)].copy()
 
# Harmonize country names to CGDev convention
census_raw['cgdev_country'] = census_raw['CTYNAME'].apply(
    lambda n: CENSUS_TO_CGDEV.get(n, n)   # use mapped name if exists, else keep as-is
)
census_raw = census_raw[census_raw['cgdev_country'].notna()].copy()
 
# Build long-format: one row per country × calendar month
records = []
for _, row in census_raw.iterrows():
    year = int(row['year'])
    country = row['cgdev_country']
    for col, m_suffix in CENSUS_MONTH_COLS.items():
        month_label = f'{year}-{m_suffix}'
        if month_label not in MONTH_TO_SNAPSHOT:
            continue          # outside our tariff-panel window
        val = row[col]
        if pd.notna(val) and val > 0:
            records.append({'cgdev_country': country,
                            'month': month_label,
                            'imports_millions': float(val)})
 
census_long = pd.DataFrame(records)
before = len(census_long)
 
print(f"  Raw long-format rows: {before}")
print(f"  Unique countries:     {census_long['cgdev_country'].nunique()}")
print(f"  Months covered:       {sorted(census_long['month'].unique())}")
 
# ── 3. LOAD CGDev TARIFF SNAPSHOTS ───────────────────────────────────────────
 
print("\n" + "=" * 60)
print("STEP 2: Loading CGDev tariff snapshots")
print("=" * 60)
 
def load_cgdev(filepath, label):
    df = pd.read_csv(filepath)
    df.columns = ['cgdev_country', 'added_tariff_rate', 'export_share_2024', 'exposure']
    # Drop aggregates and self
    # Keep China so it can be included in the 'with China' panel.
    # United States is the tariff imposer; EU is an aggregate; others are missing/non-sovereign.
    drop = {'Kosovo', 'European Union', 'Western Sahara', 'United States of America'}
    dropped = [c for c in df['cgdev_country'] if c in drop]
    df = df[~df['cgdev_country'].isin(drop)].copy()
    print(f"  {label}: {len(df)} countries | Dropped: {dropped}")
    return df[['cgdev_country', 'added_tariff_rate', 'exposure']]
 
cgdev_frames = {}
for label, fpath in CGDEV_FILES.items():
    cgdev_frames[label] = load_cgdev(fpath, label)
 
# Assign snapshots to months
month_tariff_dfs = []
for month, snap_label in MONTH_TO_SNAPSHOT.items():
    df = cgdev_frames[snap_label].copy()
    df['month'] = month
    month_tariff_dfs.append(df)
 
tariff_long = pd.concat(month_tariff_dfs, ignore_index=True)
print(f"\n  Tariff long-format shape: {tariff_long.shape}")
 
# ── 4. MERGE ──────────────────────────────────────────────────────────────────
 
print("\n" + "=" * 60)
print("STEP 3: Merging Census and CGDev data")
print("=" * 60)
 
panel = pd.merge(census_long, tariff_long,
                 on=['cgdev_country', 'month'], how='inner')
print(f"  Panel shape: {panel.shape}")
print(f"  Unique countries: {panel['cgdev_country'].nunique()}")
print(f"  Unique months:    {panel['month'].nunique()} — {sorted(panel['month'].unique())}")
 
# Verify China is present
china_in = 'China' in panel['cgdev_country'].values
print(f"  China in panel: {china_in}")
 
# ── 5. FEATURE ENGINEERING ───────────────────────────────────────────────────
 
print("\n" + "=" * 60)
print("STEP 4: Feature engineering")
print("=" * 60)
 
panel['log_imports'] = np.log(panel['imports_millions'])
panel = panel.sort_values(['cgdev_country', 'month']).reset_index(drop=True)
 
# Lags (within country)
panel['tariff_lag1']   = panel.groupby('cgdev_country')['added_tariff_rate'].shift(1)
 
# Integer month index for linearmodels
month_order = sorted(panel['month'].unique())
panel['month_int'] = panel['month'].map({m: i for i, m in enumerate(month_order)})
 
print(f"  Month range:       {month_order[0]} to {month_order[-1]}")
print(f"  Tariff rate range: {panel['added_tariff_rate'].min():.2f}% "
      f"to {panel['added_tariff_rate'].max():.2f}%")
print(f"  Log imports range: {panel['log_imports'].min():.2f} "
      f"to {panel['log_imports'].max():.2f}")

# Robustness weights: average monthly import value per country across full sample.
# Used in WLS regressions to up-weight large trading partners.
# We use the full-sample average (not a pre-tariff baseline) for simplicity;
# the weight is fixed per country and does not vary with the tariff shocks.
avg_imports_by_country = (
    panel.groupby('cgdev_country')['imports_millions']
    .mean()
    .rename('avg_imports_weight')
)
panel = panel.merge(avg_imports_by_country.reset_index(),
                    on='cgdev_country', how='left')

# Diagnostic: within-variation after two-way demeaning (computed after subset creation below)
 
# ── 6. SAMPLE SUBSETS ────────────────────────────────────────────────────────
 
print("\n" + "=" * 60)
print("STEP 5: Building sample subsets")
print("=" * 60)
 
panel_with_china    = panel.copy()
panel_without_china = panel[panel['cgdev_country'] != 'China'].copy()
 
print(f"  With China:    {panel_with_china['cgdev_country'].nunique()} countries, "
      f"{len(panel_with_china)} obs")
print(f"  Without China: {panel_without_china['cgdev_country'].nunique()} countries, "
      f"{len(panel_without_china)} obs")

# Top-50 subset: restrict to the 50 largest exporters to the US by average monthly imports.
# This guards against the result being driven by large % swings from tiny trading partners.
top50_countries = avg_imports_by_country.nlargest(50).index.tolist()
panel_top50_with_china    = panel[panel['cgdev_country'].isin(top50_countries)].copy()
panel_top50_without_china = panel_top50_with_china[
    panel_top50_with_china['cgdev_country'] != 'China'
].copy()

print(f"\n  Top-50 countries by average monthly imports:")
print(f"  With China:    {panel_top50_with_china['cgdev_country'].nunique()} countries, "
      f"{len(panel_top50_with_china)} obs")
print(f"  Without China: {panel_top50_without_china['cgdev_country'].nunique()} countries, "
      f"{len(panel_top50_without_china)} obs")
print(f"  Countries: {', '.join(sorted(top50_countries))}")

# China tariff path for reference
china_tariff = (panel[panel['cgdev_country'] == 'China']
                .sort_values('month')[['month', 'added_tariff_rate', 'imports_millions']]
                .reset_index(drop=True))
print(f"\n  China tariff path:")
print(china_tariff.to_string(index=False))
 
# Within-variation diagnostics per subset
print()
for subset_label, sub in [('Without China', panel_without_china), ('With China', panel_with_china)]:
    for col in ['added_tariff_rate', 'tariff_lag1']:
        tmp = sub.dropna(subset=[col]).copy()
        tmp['e_mean'] = tmp.groupby('cgdev_country')[col].transform('mean')
        tmp['t_mean'] = tmp.groupby('month_int')[col].transform('mean')
        tmp['g_mean'] = tmp[col].mean()
        tmp['demeaned'] = tmp[col] - tmp['e_mean'] - tmp['t_mean'] + tmp['g_mean']
        print(f"  Within-variation ({subset_label} | {col}): std = {tmp['demeaned'].std():.4f}")
 
# ── 7. REGRESSION FUNCTION ───────────────────────────────────────────────────
 
def run_panel_regression(df, iv_col, label, weights_col=None):
    """
    PanelOLS with country + time fixed effects.
    DV: log_imports | Independent Variable: iv_col
    Standard errors clustered at the country level.
    weights_col: optional column name in df to use as observation weights (WLS).
    """
    cols = ['cgdev_country', 'month_int', 'log_imports', iv_col]
    if weights_col:
        cols.append(weights_col)
    df_reg = df[cols].dropna().copy()
    if len(df_reg) == 0:
        print(f"    {label}: No observations — skipping.")
        return None
    df_reg = df_reg.set_index(['cgdev_country', 'month_int'])
    weights = None
    if weights_col:
        weights = df_reg[[weights_col]]
        df_reg = df_reg.drop(columns=[weights_col])
    try:
        mod = PanelOLS.from_formula(
            f'log_imports ~ {iv_col} + EntityEffects + TimeEffects',
            data=df_reg,
            weights=weights
        )
        return mod.fit(cov_type='clustered', cluster_entity=True)
    except Exception as e:
        print(f"    {label}: Regression failed — {e}")
        return None
 
# ── 8. SPECIFICATIONS ────────────────────────────────────────────────────────
 
print("\n" + "=" * 60)
print("STEP 6: Running regressions")
print("=" * 60)
 
specs = [
    # ── PRIMARY: tariff rate as Independent Variable ────────────────────────────────────────────
    # Semi-log model: β = % change in imports per 1pp increase in tariff rate.
    # No-lag is theoretically primary (Liberation Day had near-zero notice;
    # importers responded contemporaneously). 1-Mo Lag is robustness.
    ('Tariff Rate | No Lag   | Without China', panel_without_china, 'added_tariff_rate'),
    ('Tariff Rate | 1-Mo Lag | Without China', panel_without_china, 'tariff_lag1'),
    ('Tariff Rate | No Lag   | With China',    panel_with_china,    'added_tariff_rate'),
    ('Tariff Rate | 1-Mo Lag | With China',    panel_with_china,    'tariff_lag1'),

    # ── ROBUSTNESS 1: WLS weighted by average monthly import value ──────────────
    # Each observation is weighted by the country's average monthly imports over the
    # full sample period, so large trading partners drive the coefficient estimate.
    ('WLS (Avg Imports) | No Lag   | Without China', panel_without_china, 'added_tariff_rate', 'avg_imports_weight'),
    ('WLS (Avg Imports) | 1-Mo Lag | Without China', panel_without_china, 'tariff_lag1',        'avg_imports_weight'),
    ('WLS (Avg Imports) | No Lag   | With China',    panel_with_china,    'added_tariff_rate', 'avg_imports_weight'),
    ('WLS (Avg Imports) | 1-Mo Lag | With China',    panel_with_china,    'tariff_lag1',        'avg_imports_weight'),

    # ── ROBUSTNESS 2: Top-50 exporters to the US ────────────────────────────────
    # Restricts the sample to the 50 largest exporters to the US by average monthly
    # import value, directly excluding the small-country noise concern.
    ('Top-50 Exporters | No Lag   | Without China', panel_top50_without_china, 'added_tariff_rate'),
    ('Top-50 Exporters | 1-Mo Lag | Without China', panel_top50_without_china, 'tariff_lag1'),
    ('Top-50 Exporters | No Lag   | With China',    panel_top50_with_china,    'added_tariff_rate'),
    ('Top-50 Exporters | 1-Mo Lag | With China',    panel_top50_with_china,    'tariff_lag1'),
]
 
results = {}
for spec in specs:
    label, df, iv_col = spec[0], spec[1], spec[2]
    weights_col = spec[3] if len(spec) > 3 else None
    print(f"  Running: {label}")
    results[label] = (run_panel_regression(df, iv_col, label, weights_col=weights_col), iv_col)
 
# ── 9. RESULTS TABLE ─────────────────────────────────────────────────────────
 
def print_results_block(title, spec_labels):
    print(f"\n{title}")
    print(f"  {'Specification':<35} {'β₁':>10} {'t-stat':>8} {'p-value':>9} "
          f"{'N':>6} {'R²(within)':>11}")
    print("  " + "-" * 83)
    for label in spec_labels:
        res, iv_col = results[label]
        if res is None:
            print(f"  {label:<35} {'N/A'}")
            continue
        coef  = res.params[iv_col]
        tstat = res.tstats[iv_col]
        pval  = res.pvalues[iv_col]
        nobs  = int(res.nobs)
        r2    = res.rsquared_within if hasattr(res, 'rsquared_within') else np.nan
        sig   = ('***' if pval < 0.001 else '**' if pval < 0.01
                 else '*' if pval < 0.05 else '.' if pval < 0.10 else ' ')
        short = label.split(' | ', 1)[1]
        print(f"  {short:<35} {coef:>+10.4f}{sig:<1} {tstat:>+8.2f} "
              f"{pval:>9.4f} {nobs:>6} {r2:>11.4f}")
 
print("\n" + "=" * 60)
print("RESULTS SUMMARY")
print("=" * 60)
 
tariff_specs = [s[0] for s in specs if s[0].startswith('Tariff Rate')]
wls_specs    = [s[0] for s in specs if s[0].startswith('WLS')]
top50_specs  = [s[0] for s in specs if s[0].startswith('Top-50')]

print_results_block(
    "Baseline: Added effective tariff rate (all countries)\n"
    "  Semi-log: β = % change in US imports per 1 pp increase in tariff rate",
    tariff_specs
)

print_results_block(
    "Robustness 1: WLS weighted by average monthly import value\n"
    "  Up-weights large trading partners; weight = country avg monthly imports over full sample",
    wls_specs
)

print_results_block(
    "Robustness 2: Top-50 exporters to the US (by avg monthly imports)\n"
    "  Excludes small-country noise by restricting to economically significant partners",
    top50_specs
)
 
print(f"""
Significance: *** p<0.001  ** p<0.01  * p<0.05  . p<0.10
 
Notes:
  All regressions include country and time (month) fixed effects.
  Standard errors clustered at the country level.
  DV:  log(US monthly imports from country, USD millions, Census Bureau).
  Panel covers April 2025 – January 2026 (10 months).
  Tariff snapshots: Apr29, May22, Jun4 (Jun+Jul), Aug7 (Aug–Oct),
                    Nov21 (Nov 2025–Jan 2026).
  Lagged specs use prior-month tariff value; April 2025 observations are lost.
  'With China' includes China's tariff path. China's swing dominates within-variation
  in that sample and the result essentially estimates the US-China bilateral
  tariff elasticity rather than the universal tariff effect.
  Hong Kong and Macau are excluded (separate tariff treatment; not in CGDev).
""")
