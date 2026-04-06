# Practical Assignment 24.1: Final Report

This project compares the following classification algorithms using [Employmen Scam Aegean Dataset](https://www.kaggle.com/datasets/amruthjithrajvr/recruitment-scam):

- Multilayer Perceptron
- Linear SVM
- XGBoost
- Random Forest
to identify the best model for predicting whether a job posting is fraudulent.

## Business Objective

The Employment Scam Aegean Dataset (EMSCAD) contains 17,880 job postings — 866 fraudulent and 17,014 legitimate — collected from a real-world job aggregator platform. With each observation representing a single job listing composed of structured metadata (company profile, logo presence, required education/experience) and free-text fields (title, description, requirements, benefits), this project engineers features across both domains to:

- Identify structural red flags via missing field counts, company profile completeness, and description length — the most universally predictive fraud signals across all model architectures
- Detect deceptive language patterns through TF-IDF analysis of urgency tactics ("urgent", "hiring immediately"), salary bait ("$100,000"), and suspicious vocabulary ("link", "money", "supply") commonly embedded in fraudulent postings
- Help job-seeking candidates screen postings more effectively by surfacing the specific textual and structural patterns most associated with scams, reducing time wasted on fraudulent listings
- Support legitimate employers and HR firms in benchmarking their own postings against fraud indicators, ensuring authentic job descriptions are structured and detailed enough to distinguish themselves from fraudulent noise on aggregator platforms

## Dataset

The dataset is significantly imbalanced with only ~4.84% fraudulent job postings.

## Data Preparation

The nobebook includes:

- one-hot encoding for categorical variables
- TFIDF feature engineering for text features
- train/test split of the dataset
- correlation heatmaps, numerical and categorical distributions, model comparisons

## Evaluation Metrics

The following metrics were employed to compare the models:

- PR-AUC
- F1 Score
- ROC-AUC
- Precision
- Confusion Matrix

## Repository Structure

```
├── data/
│   ├── fake_job_postings.csv          # Original EMSCAD dataset (17,880 job postings)
│   └── tuned_models.csv               # Pre-saved RandomizedSearchCV results for tuned models (saved to avoid retraining)
│
├── helpers/
│   ├── __init__.py
│   └── salary_features.py             # Shared utility functions used across both EDA and evaluation notebooks
│
├── images/                            # All saved visualizations referenced in notebooks and README
│
├── exploratory_data_analysis.ipynb    # EDA, feature engineering, and baseline modeling (Random Forest classifier)
├── capstone_evaluation.ipynb          # Model comparison, hyperparameter tuning, final model selection, and feature importances
└── README.md
```

## Findings & Insight

![Final Model Comparison](/images/final_tuned_models_model_comparison.png)

### Final Model Recommendation

When using all engineered features, a **Tuned MLP + SMOTE** model provided the best overall scores, balancing fraud detection coverage with precision.

- **Precision:** 92.6% — when the model flags a posting as fraudulent, it is correct over 9 times out of 10
- **Coverage:** Captures 79.2% of all fraudulent postings in the dataset — the highest recall of any tuned model
- **F1 Score:** 0.854 — the strongest harmonic balance between precision and recall
- **Caveat:** ~131 seconds train time and a (512, 256, 128) architecture make this the most computationally expensive option, which could be a latency consideration for real-time screening pipelines

---

### Alternative Model Recommendations

When using all engineered features, a **Tuned MLP + SMOTE** model provided the best overall scores, balancing fraud detection coverage with precision.

- **Precision:** 92.6% — when the model flags a posting as fraudulent, it is correct over 9 times out of 10
- **Coverage:** Captures 79.2% of all fraudulent postings in the dataset — the highest recall of any tuned model
- **F1 Score:** 0.854 — the strongest harmonic balance between precision and recall
- **Caveat:** ~131 seconds train time and a (512, 256, 128) architecture make this the most computationally expensive option, which could be a latency consideration for real-time screening pipelines

---

### Alternative Strategies

**1. Best Balance with Lower Overhead → Use XGBoost**

When the goal is near-MLP performance with a more interpretable, tree-based architecture:

- **Precision:** 95.7% — slightly higher than MLP, with fewer false accusations
- **Coverage:** 77.5% recall — only 1.7 percentage points below MLP
- **F1 Score:** 0.856 — effectively tied with MLP as the top performer
- **Real-world impact:** A strong default choice for production deployment — competitive performance, native feature importance for explainability, and no dependency on over/undersampling techniques at inference time
- **Train time:** ~102 seconds, roughly 22% faster than MLP

**2. High-Confidence Flagging (with caveats) → Use Random Forest**

When incorrectly flagging a legitimate employer's posting is unacceptable (e.g., a job platform risking reputational damage or legal liability):

- **Precision:** 100% on the test set — every flagged posting was genuinely fraudulent, zero false positives
- **Coverage:** 42.2% of fraudulent postings caught — the lowest recall, meaning most scams slip through
- **Real-world impact:** Best suited as a **high-confidence auto-removal layer** where flagged postings are taken down immediately without human review, while unflagged postings proceed to secondary screening
- **Speed advantage:** Trains in 22 seconds — the fastest tuned model, roughly 6× faster than MLP
- **⚠️ Caveat:** 100% test-set precision may reflect overfitting to narrow decision boundaries rather than true generalization — the model likely memorized a small subset of obvious fraud patterns while ignoring subtler ones. Cross-validation PR-AUC (0.895) suggests real-world precision would be lower. This model should be validated on held-out or production data before trusting its zero-false-positive claim.

**3. Lightweight Deployment / Real-Time Screening → Use Linear SVM + SMOTE**

When the model needs to score incoming postings quickly at scale:

- **Precision:** 91.7% — still above 9 in 10 correct fraud flags
- **Coverage:** 69.9% recall — a meaningful trade-off for speed and simplicity
- **Real-world impact:** Linear architecture trains in ~55 seconds (2.4× faster than MLP) and produces directly interpretable coefficients — ideal for integration into a job platform's intake pipeline where new postings need immediate scoring
- **Explainability:** Coefficient magnitudes provide transparent, auditable fraud signals for stakeholders and compliance teams

### Key Insights from Feature Analysis

![Feature Importances and Coefficients](/images/feature_importance_tuned_models.png)

## Key Fraud Indicators

1. **Posting completeness is the single strongest fraud signal.** Missing company profiles, blank fields, and short descriptions appear as top predictors across all four models. Legitimate employers invest effort in detailed, complete listings — fraudulent postings may focus on more high level postings with highly attractive, yet unspecific, language.
2. **Suspicious links are a major red flag.** Postings containing embedded URLs are strongly associated with fraud, typically used to redirect applicants to phishing sites, harvest personal information, or track the user.
3. **Inflated salaries and urgency language are classic bait tactics.** References to large round numbers ("$100,000+") and pressure words ("urgent", "hiring immediately", "cash") are designed to rush applicants into action before they scrutinize the posting.
4. **IT and tech roles are disproportionately targeted.** Scammers exploit the expectation of remote work and high salaries in the tech sector, making IT department postings a higher-risk category.
5. **Vague or minimal requirements signal low-effort fraud.** Postings requiring only a high school diploma with thin job descriptions cast the widest net for potential victims — legitimate roles typically specify detailed qualifications.
6. **Niche industries attract targeted scams.** Biotechnology and Oil & Energy postings show elevated fraud rates, likely because applicants in specialized fields (STEM?) are less familiar with standard hiring norms and more trusting of industry-specific opportunities.

While scam vocabulary and urgency language are important for nuanced detection, **structural completeness features** — company profile presence, missing field counts, and description length — are the most universally predictive across all model architectures and should serve as the **first line of defense** on any job platform screening pipeline.

## Next Steps

**Threshold tuning** offers the most immediate gain. Could lowering the classification threshold below the default 0.5  make models more aggressive in flagging fraud? For some job seekers who can higher false positives, this could prove efficient. A precision-recall curve analysis would allow this trade-off to be set deliberately based on platform tolerance.

**Transformer architectures** like BERT could unlock deeper semantic understanding. Rather than relying on individual TF-IDF tokens, BERT's contextual embeddings could identify recurring phrases, sentence-level deception patterns, and subtle tonal shifts that bag-of-words features cannot capture.

**Feature enrichment** through external datasets could broaden the model's fraud vocabulary:

- The [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) would expose the model to cross-domain deceptive language — urgency cues, financial bait, and data harvesting prompts beyond job-specific vocabulary
- The [LinkedIn Job Postings Dataset](https://huggingface.co/datasets/datastax/linkedin_job_listings), while unlabeled for fraud, would provide contemporary posting norms against which anomalies could be benchmarked

**Temporal validation** is also critical. Fraudulent tactics evolve rapidly, and evaluating current models against more recent postings would test whether learned signals still generalize or have drifted.

A combination of these strategies would advance this baseline toward a deployable, production-grade job scam detection system.