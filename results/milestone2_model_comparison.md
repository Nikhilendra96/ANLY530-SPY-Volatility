# Development model comparison

The metrics refer to the high-volatility class. The 2024 and 2025 evaluation sets contained 4 and 28 positive outcomes, respectively.

| Model | 2024 Recall | 2024 Precision | 2024 F1 | 2025 Recall | 2025 Precision | 2025 F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.00% | 0.00% | 0.00% | 85.71% | 96.00% | 90.57% |
| kNN (k=3) | 25.00% | 20.00% | 22.22% | 92.86% | 86.67% | 89.66% |
| Gaussian Naive Bayes | 0.00% | 0.00% | 0.00% | 89.29% | 92.59% | 90.91% |
| Decision Tree depth 2 | 75.00% | 60.00% | 66.67% | 92.86% | 92.86% | 92.86% |

Among the tested kNN settings, k = 3 had the highest recall in both years. The depth-2 tree had the highest minimum recall across the two years among all tested configurations. [Executed model-development notebook](../notebooks/02_model_development.ipynb)
