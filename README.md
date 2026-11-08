# Predicting Next-Day SPY Volatility

For my project, I am using information available at the end of today's trading session to predict whether the next SPY trading day will have high volatility. This folder organizes my ANLY 530 Week 4–8 work. I kept the same target, three predictors, and chronological evaluation periods.

## Research question and motivation

Can today's return, recent average return, and recent volatility help identify whether the next SPY trading day will be a high-volatility day?

I am interested in this as a risk-management problem. Missing a high-volatility day matters, but too many false alarms would also make the predictions less useful. The goal is to compare that tradeoff, not to build a trading strategy.

## Data source and unit of observation

I use public daily SPY prices from Yahoo Finance through [yfinance](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html). The download starts on January 1, 2020 and ends before January 1, 2026. `auto_adjust=True` keeps the adjusted-price setup from my earlier notebooks. No private or work-related data is used.

One observation is one trading day. The row's date is day t, when the predictors become available after the close. `target_date` is the next observed trading day, t+1, which may follow a weekend or holiday.

## Target definition

I calculate daily percentage returns from adjusted closing prices, then take the sample standard deviation of the latest 20 returns. This is daily volatility, not an annualized measure.

The cutoff is the 75th percentile of valid 20-day volatility values from 2020–2023. I keep it fixed for the later evaluation periods. The target is 1 if the **next trading day's** volatility is strictly above that cutoff, and 0 otherwise.

The code keeps the original rule: `rolling_volatility.loc[:"2023"].quantile(0.75)`, followed by a one-row backward shift of the volatility class. Initial incomplete windows and the final row with an unknown next-day outcome are removed before modeling. The cutoff is calculated before removing those rows, just as in my earlier notebooks.

## Predictors

| Predictor | Definition | Available when? |
|---|---|---|
| `daily_return` | Today's adjusted close divided by the previous trading day's adjusted close, minus 1 | After today's close |
| `average_return_5d` | Mean of the latest 5 daily returns, including today | After today's close |
| `volatility_20d` | Sample standard deviation of the latest 20 daily returns, including today | After today's close |

Returns are stored as decimals, so 0.01 means 1%. `Close`, `target`, and `target_date` are not predictors. Rolling windows use trading observations and do not look forward.

## Evaluation strategy and metrics

I keep the expanding windows used in Weeks 5–8:

| Training outcomes | Evaluation outcomes |
|---|---|
| Through 2023 | 2024 |
| Through 2024 | 2025 |

The split uses `target_date`, not the feature date. This keeps every training outcome before the evaluation year starts. For example, a row on the last trading day of December belongs to the next year's evaluation if its target date is in January. No rows are randomly shuffled.

Recall for high volatility (class 1) is my primary metric. Precision and F1-score give context about false alarms and the balance between precision and recall. When a model makes no positive predictions, precision is undefined; the table displays zero using `zero_division=0`, as in the earlier notebooks.

These 2024 and 2025 periods have already been used to compare models, so they are development periods rather than a new final test. **2026 remains reserved.** Neither exploration nor model development downloads or evaluates 2026 data. Notebook 03 is an unexecuted template with no active download or evaluation code.

## What I kept from each week

| Earlier notebook | What carries into this project |
|---|---|
| Week 4 — Classification | SPY download, fixed historical cutoff, next-day target, and class-distribution check |
| Week 5 — Evaluation | Logistic regression, training-only scaling, 2024/2025 expanding windows, recall, precision, and F1 |
| Week 6 — Representation | The reduced three-predictor set and training-period correlation check |
| Week 7 — Neighbors and Probabilities | kNN with k = 3, 5, and 7 using Euclidean distance, plus Gaussian Naive Bayes |
| Week 8 — Trees | Decision trees with maximum depths 2, 3, 4, and 5, using `random_state=42` |

Week 6 also tried seven predictors with L1 regularization. That experiment stays in the original notebook because this project keeps exactly the three reduced predictors. I did not add new models or search settings. Logistic regression keeps its original defaults, and all classifiers use the same scaling pipeline as before. Scaling is fitted only on the training period; see the [scikit-learn leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage).

Week 8 identified the depth-2 tree as a candidate for a later check. I keep that as a development finding, not a claim about 2026 performance. The original Week 4–8 notebooks are unchanged and are not needed to run this folder.

## Repository structure

```text
ANLY530_SPY_Volatility_Project/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_model_development.ipynb
│   └── 03_final_evaluation.ipynb
└── src/
    └── data_utils.py
```

`src/data_utils.py` contains three small functions for downloading prices, creating predictors, and creating the target. The modeling code stays in notebook 02 so I can follow each step.

## Installation

Use Python 3.11, which matches the environment used for this project. From this project folder, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. The requirements contain the data and modeling packages plus Jupyter Notebook and its Python kernel. No separate CSV download is needed.

## Run the notebooks

In VS Code, open this project folder, select the `.venv` Python kernel, and run notebook 01 from top to bottom. Then run notebook 02. Each notebook downloads the public development data and can run from a fresh kernel without the other notebook's variables.

For the browser interface, run:

```bash
python -m notebook
```

Open `notebooks/01_exploration.ipynb`, then `notebooks/02_model_development.ipynb`, and use **Restart Kernel and Run All Cells**. An internet connection is required. If Yahoo Finance temporarily fails or limits requests, wait and rerun the download cell.

**Do not run notebook 03 until model development and selection are complete.** It records what needs to be fixed before using the 2026 holdout. It contains no final results.

## Reproducibility notes

The date range, cutoff period, feature order, model settings, and evaluation years are explicit. Package versions are pinned to the working environment. The saved notebook outputs come from real executions, not copied scores from earlier weeks.

Yahoo Finance may revise its historical adjusted prices, so a fresh download can differ slightly from an older run even when the code is unchanged. I keep that limitation visible instead of forcing the new outputs to match old numbers. The notebooks print the download date range and cutoff each time they run.

Downloaded data files, virtual environments, notebook checkpoints, and Python cache files are excluded by `.gitignore`. The notebooks work directly with the public download in memory and do not require a saved dataset.

For this saved copy, notebooks 01 and 02 ran from fresh kernels. The download covered January 2, 2020 through December 31, 2025 and produced 1,487 complete observations. The cutoff was 1.3905%, with 279 high-volatility targets. Checks matched the shared data functions to the original Week 8 code and matched the model comparisons to the original Week 7 and Week 8 code using the same downloaded rows. File hashes confirmed that the existing notebooks were unchanged. Notebook 03 was not executed.

## Limitations

Today's and tomorrow's 20-day volatility share 19 returns. This makes persistence useful, but it also means the project is not the same as forecasting a sudden market shock or tomorrow's absolute return.

High-volatility outcomes were rare in the later years of the earlier notebooks. A small number of cases can cause large changes in recall. Two reused evaluation periods are not enough to establish reliable future performance.

The cutoff uses information through 2023, so it cannot support a claim about predictions made before that cutoff was available. The formal evaluations start in 2024. Adjusted historical prices are also not a point-in-time archive, and revised data may differ from what was available live.

All predictions assume today's closing price is available. These are predictive relationships, not evidence that a feature causes future volatility. I would like to check a later untouched period only after the final model and evaluation plan are fixed.
