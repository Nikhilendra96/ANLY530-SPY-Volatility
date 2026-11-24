# ANLY 530 KA1 Milestone 2 — SPY volatility

## Data preparation

My question is whether information available at the end of a SPY trading day can identify high volatility on the next trading day with enough recall to help monitor risk. The development notebooks downloaded adjusted daily SPY closes from Yahoo Finance through yfinance. The saved exploration run covered January 2, 2020, through December 31, 2025. It had 1,508 trading days and zero missing closing prices. After removing 21 rows with incomplete rolling windows or an unknown next-day outcome, I had 1,487 complete observations, including 279 high-volatility outcomes (18.76%).

I used three predictors that are available after the close on day t. They are the daily percentage return from adjusted closes, the mean of the latest five daily returns, and the sample standard deviation of the latest 20 daily returns. I defined a high-volatility day as one with 20-day rolling volatility strictly above the 75th percentile of valid 2020–2023 values. The saved run gave a cutoff of 1.3905%, which stayed fixed for both evaluation years. I shifted the class back one row so the label on day t describes day t+1. The code drops missing closes before calculating returns, replaces infinite predictor values with missing values, and drops rows with incomplete predictors, labels, or target dates. Both notebooks use a shared download function that reports the number of duplicate trading dates and stops for review if any are found. Both reruns reported zero duplicate trading dates, and all predictors in the complete dataset were finite.

## Models and evaluation

I trained through 2023 to evaluate 2024, then trained through 2024 to evaluate 2025. I split by the date of the outcome and kept the rows in time order. This puts a December feature row with a January outcome in the January evaluation set. The first split had 985 training rows and 252 evaluation rows. The second had 1,237 training rows and 250 evaluation rows. The predictors end on day t, and each pipeline fits its standard scaler using only that split’s training rows. Both notebooks check that the data end before 2026.

I kept the existing default logistic regression and Gaussian naive Bayes, Euclidean kNN with three neighbors, and the decision tree with maximum depth 2 and random seed 42. Among the existing kNN settings, three neighbors gave the highest recall in both years. The depth-2 tree had the highest minimum recall among the existing configurations. The comparison uses recall, precision, and F1 for high volatility. The notebook displays precision as zero when a model makes no positive predictions. [Model comparison](milestone2_model_comparison.md) · [Recall chart](milestone2_recall_by_model.png)

## Preliminary findings

Based on the current results, the depth-2 tree had the most consistent recall across the two development years. It caught 3 of 4 high-volatility days in 2024 and 26 of 28 in 2025. Its recall was 75.00% and 92.86%, respectively, and its precision increased from 60.00% to 92.86%. The deeper trees had lower recall in both years, although depths 3 and 4 had higher precision in 2024. The depth-2 tree remains a candidate for final evaluation.

One thing I noticed was how much performance changed across years. Logistic regression caught none of the positive cases in 2024 and reached 85.71% recall and 96.00% precision in 2025. The three-neighbor model caught one positive case in 2024 and two more than logistic regression in 2025, with lower 2025 precision. Gaussian naive Bayes also caught none in 2024 and reached 89.29% recall in 2025. The 20-day volatility feature accounted for all of the depth-2 tree’s fitted feature importance in both training windows. That describes how the tree made predictions and provides no evidence of a causal relationship.

## Limitations

One limitation is that 2024 had only 4 positives out of 252 observations, compared with 28 out of 250 in 2025. One additional correct or missed positive changes 2024 recall by 25 percentage points. Market conditions can change, and these two reused evaluation years provide development evidence with limited insight into performance on an untouched period.

Today’s and tomorrow’s 20-day volatility windows share 19 of 20 returns. Today’s volatility is already known at prediction time, so the overlap introduces no look-ahead leakage. It does mean that the results partly reflect volatility persistence and give limited evidence about how well the models would flag a sudden new shock.

## Reproducibility

The repository includes a README, pinned requirements, separate exploration and model-development notebooks, reusable download and data preparation code, and an unexecuted final-evaluation template. I installed the requirements in a clean Python 3.11 environment and ran both development notebooks from fresh kernels. The data counts, cutoff, model metrics, and tree feature importances matched the saved outputs used for the comparison table and chart. The 2026 holdout was neither downloaded nor evaluated. Yahoo Finance can revise historical adjusted closes, so future downloads may differ.

## Next steps

I would freeze the three predictors and existing model candidates, finish the development comparison, and document a selection rule before touching 2026. One option is to prioritize minimum annual recall and use precision to weigh false alarms. I would then record the final model settings, prediction rule, and exact 2026 dates in the final-evaluation template. Once those decisions are fixed, I would run one holdout evaluation and report class counts, recall, precision, and F1. I would use those results to make the final tables and figures, write the conference paper, and prepare the five-minute presentation.
