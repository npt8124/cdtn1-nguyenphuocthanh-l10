# MODEL CARD – AUTOMATED WARRANTY CLAIM CLASSIFICATION SYSTEM

## 1. Basic Information

| Field | Information |
| --- | --- |
| **Model Name** | `phan-loai-su-co` |
| **Version** | `v1.0` |
| **Model Type** | ComplementNB (Complement Naive Bayes) |
| **Creation Date** | September 24, 2026 |
| **Author** | Nguyễn Phước Thành - 2374802013578 |
| **Contact** | Via Course Instructor – Dr. Nguyễn Trí Hải |
| **Reproducibility Command** | `python -m src.models.train --config configs/train.yaml` |

---

## 2. Intended Use

This model is designed to assist warranty intake staff in categorizing device fault groups based on issue descriptions provided by users.

* **Intended Users:** Warranty claim intake staff.
* **Workflow:** Upon receiving a device, the staff member enters the issue description into the system to receive a suggested fault classification.
* **Role of the Model:** Analyzes text and recommends the most appropriate fault category.
* **Role of the Human:** Staff review, select, or adjust the suggested result before confirming the warranty claim.

> **Note:** The model serves strictly as a decision-support tool. It does not replace intake staff and does not autonomously decide the final outcome of a warranty claim.

---

## 3. Out-of-Scope / Inappropriate Use Cases

| Inappropriate Use Case | Reason |
| --- | --- |
| **Fully automated classification and confirmation without human review** | The model can still make incorrect predictions, leading to inaccurate classification records. |
| **Automated technician assignment** | Misclassified fault categories may route devices to the wrong technical department. |
| **Determining warranty eligibility** | Eligibility depends on warranty policies, expiration dates, and purchase terms—not the fault description. |
| **Evaluating staff performance or competence** | Training labels may reflect historical staff labeling habits rather than an objective measure of employee performance. |
| **Classifying descriptions in languages other than Vietnamese** | The training dataset and text preprocessing pipeline were built specifically for Vietnamese. |
| **Classifying device types outside the training data scope** | The model has not been thoroughly evaluated on device categories absent from the training set. |

> Additionally, the model's confidence score must not be interpreted as an absolute probability of accuracy.

---

## 4. Training Data

| Field | Information |
| --- | --- |
| **Data Source** | `src/data/mau/issue_descriptions.csv` |
| **Total Raw Samples** | 4,000 |
| **Split Ratio** | Train 70%, Validation 15%, Test 15% |
| **Random Seed** | 42 |
| **Samples After Deduplication** | 2,081 |
| **Training Samples** | 1,456 |
| **Validation Samples** | 312 |
| **Test Samples** | 313 |

### Label Distribution

| Label | Count | Percentage |
| --- | --- | --- |
| `MAN_HINH` (Screen) | 546 | 26.24% |
| `PIN` (Battery) | 470 | 22.59% |
| `SAC` (Charging) | 356 | 17.11% |
| `PHAN_MEM` (Software) | 323 | 15.52% |
| `NUOC_VAO` (Liquid Damage) | 211 | 10.14% |
| `KHAC` (Other) | 175 | 8.41% |
| **Total** | **2,081** | **100%** |

---

## 5. Architecture & Processing Pipeline

The model employs a supervised text classification approach combining **TF-IDF** vectorization with **Complement Naive Bayes (ComplementNB)**.

### Processing Workflow

1. Receive raw issue description from the user.
2. Clean text: convert to lowercase, handle special characters, and normalize whitespace.
3. Mask Personally Identifiable Information (PII):
* Phone numbers $\rightarrow$ `<sdt>`
* Serial numbers $\rightarrow$ `<serial>`
* Email addresses $\rightarrow$ `<email>`


4. Transform cleaned text into numerical feature vectors using TF-IDF.
5. Feed feature vectors into the `ComplementNB` classifier.
6. Return predicted fault category for human review and confirmation.

### Technical Specifications

| Component | Configuration |
| --- | --- |
| **Preprocessing** | Lowercasing, preserving Vietnamese diacritics, text normalization |
| **Vectorization** | TF-IDF |
| **N-gram Range** | 1–2 |
| **min_df** | 2 |
| **max_features** | 20,000 |
| **Classifier** | ComplementNB |

> **Note:** Output confidence scores are not calibrated to true probabilities. For example, a confidence score of `0.7` does not mean the model is correct 70% of the time.

---

## 6. Evaluation Metrics

**Primary Metric:** **Macro F1-score**.

**Justification:** Class distribution is imbalanced, ranging from 8.41% (`KHAC`) to 26.24% (`MAN_HINH`). Relying solely on Accuracy can be skewed by majority classes. Macro F1 computes the unweighted mean of F1-scores across all six classes, ensuring equal evaluation across both frequent and minority fault categories.

### Mandatory Evaluation Conditions

| Parameter | Value |
| --- | --- |
| **Random Seed** | 42 |
| **Data Source** | `src/data/mau/issue_descriptions.csv` (4,000 raw rows; 2,081 after deduplication) |
| **Train / Val / Test Split** | 1,456 / 312 / 313 |
| **Evaluation Set** | Test set (313 samples) |
| **Selected Primary Model** | TF-IDF + Logistic Regression (`C=0.1`) |
| **TF-IDF Configuration** | `ngram_range=(1,2)`, `min_df=2`, `max_features=20000` |

### Overall Results

| Model | Macro F1 (Validation) | Macro F1 (Test) |
| --- | --- | --- |
| Baseline — Majority Class | 0.069374 | — |
| Baseline — TF-IDF + Logistic Regression | 1.000 | — |
| Candidate — `logistic_regression_C=0.1` | 1.000 | — |
| Candidate — `linear_svc_C=0.1` | 1.000 | — |
| Candidate — `logistic_regression_C=1.0` | 1.000 | — |
| Candidate — `linear_svc_C=1.0` | 1.000 | — |
| Candidate — `logistic_regression_C=10.0` | 1.000 | — |
| Candidate — `linear_svc_C=10.0` | 1.000 | — |
| **Selected — `logistic_regression_C=0.1**` | **1.000** | **1.000** |

### Per-Label F1 and Recall (Test Set)

| Label | F1-score | Recall |
| --- | --- | --- |
| `MAN_HINH` | 1.000 | 1.000 |
| `PIN` | 1.000 | 1.000 |
| `SAC` | 1.000 | 1.000 |
| `PHAN_MEM` | 1.000 | 1.000 |
| `NUOC_VAO` | 1.000 | 1.000 |
| `KHAC` | 1.000 | 1.000 |

### Confusion Matrix (Test Set, 313 Samples)

*(Rows = Actual Label, Columns = Predicted Label)*

| Actual ↓ / Predicted → | `MAN_HINH` | `PIN` | `SAC` | `PHAN_MEM` | `NUOC_VAO` | `KHAC` |
| --- | --- | --- | --- | --- | --- | --- |
| **`MAN_HINH`** | **82** | 0 | 0 | 0 | 0 | 0 |
| **`PIN`** | 0 | **71** | 0 | 0 | 0 | 0 |
| **`SAC`** | 0 | 0 | **54** | 0 | 0 | 0 |
| **`PHAN_MEM`** | 0 | 0 | 0 | **49** | 0 | 0 |
| **`NUOC_VAO`** | 0 | 0 | 0 | 0 | **31** | 0 |
| **`KHAC`** | 0 | 0 | 0 | 0 | 0 | **26** |

---

## 7. Baseline Comparison

| Baseline Model | Macro F1 | Significance |
| --- | --- | --- |
| **Majority Class (`MAN_HINH`)** | 0.069374 | Floor benchmark. Predicts only the dominant class without distinguishing between the six fault types. |
| **TF-IDF + Logistic Regression** | 1.000 | Standard benchmark. Achieves a perfect Macro F1 on the current Validation set. |

The selected primary model, `LogisticRegression_C=0.1`, achieved a Macro F1 of `1.000` on both Validation and Test sets. However, this does not demonstrate superiority over the baseline TF-IDF + Logistic Regression model, as both achieved identical scores. Since LinearSVC and Logistic Regression candidates across different `C` values also scored `1.000` on Validation, selecting `LogisticRegression_C=0.1` should be evaluated based on secondary criteria—such as interpretability, stability, and real-world generalization—rather than Macro F1 alone.

---

## 8. Measured Bias & Slice Analysis

Evaluated across two subgrouping criteria with an alert threshold of **0.15**.

### Slice 1 — By Description Length

| Subgroup | Sample Count | Macro F1 |
| --- | --- | --- |
| Short (`< 10` words) | 110 | 0.8186 |
| Long (`≥ 10` words) | 248 | 0.8326 |
| **Disparity** | — | **0.0140** |

* **Conclusion:** Below the `0.15` threshold. The gap is minor and follows an expected pattern (shorter descriptions contain less context and perform slightly worse). Mitigation measures in Section 9 still apply because the disparity impacts users with brief descriptions.

### Slice 2 — By Service Center (`center_id`)

| Center ID | Sample Count | Macro F1 |
| --- | --- | --- |
| Center 1 | 72 | 0.7658 |
| Center 2 | 51 | 0.9260 |
| Center 3 | 60 | 0.8479 |
| Center 4 | 57 | 0.8864 |
| Center 5 | 53 | 0.7847 |
| Center 6 | 67 | 0.8052 |
| **Max Disparity (Center 2 vs. Center 1)** | — | **0.1602** |

* **Conclusion:** Do **not** claim that the model exhibits bias across service centers. The sample sizes per subgroup are too small to draw statistically valid conclusions. Reliable subgroup claims require at least ~200 samples per group or bootstrap confidence intervals rather than single point estimates.
* **Key Takeaway:** Disparity measured on small slices may simply reflect sampling noise. Reporting a point difference as definitive proof of bias without statistical power is the inverse equivalent of reporting 89% accuracy on an imbalanced dataset.

---

## 9. Risks and Limitations

### Risk 1 — Evaluation Results May Not Reflect Real-World Performance

* **Issue:** The model achieved `1.000` Accuracy and `1.000` Macro F1 across all six classes on the 313-sample Test set. While high, this does not guarantee similar performance in production.
* **Operational Impact:** Real-world customer phrasing, terminology, or edge-case faults differing from training data may result in inaccurate label suggestions.
* **Mitigation (Implemented):** Separated Validation set (for model selection) and Test set (for final evaluation); fixed random seed (`42`) for reproducibility.
* **Mitigation (Proposed):** Incorporate real-world issue descriptions verified by warranty staff, re-evaluate on independent production data, and monitor pilot deployment performance.

### Risk 2 — Synthetically Generated Training Data

* **Issue:** The dataset (4,000 raw rows; 2,081 deduplicated) was synthetically generated rather than collected from actual customer claims.
* **Operational Impact:** Synthetic text may lack real-world linguistic diversity, including typos, incomplete descriptions, regional dialects, or multi-fault descriptions within a single claim.
* **Mitigation (Implemented):** Deduplicated data prior to splitting; tracked dataset versioning via SHA-256 hashes; documented synthetic data limitations.
* **Mitigation (Proposed):** Collect real warranty claim logs, anonymize PII, have domain experts annotate labels, and retrain/re-evaluate the model.

### Risk 3 — Broad Scope of the `KHAC` (Other) Label

* **Issue:** `KHAC` acts as a catch-all category for faults outside the five primary labels (`MAN_HINH`, `PIN`, `SAC`, `PHAN_MEM`, `NUOC_VAO`), grouping unrelated technical issues together.
* **Operational Impact:** A `KHAC` prediction lacks granular routing information, requiring intake staff to manually inspect the claim before assigning a technician.
* **Mitigation (Implemented):** Retained `KHAC` as a distinct fallback category for out-of-taxonomy descriptions.
* **Mitigation (Proposed):** Review label definitions with warranty operations and split `KHAC` into specific sub-categories once sufficient real-world data is collected, updating the dataset, training pipeline, and UI accordingly.

### Risk 4 — Potential Misinterpretation of Confidence Scores

* **Issue:** The `do_tin_cay` (confidence) score returned by the model is not a calibrated probability (e.g., `0.7` does not mean a 70% likelihood of correctness).
* **Operational Impact:** Staff may treat the score as a true probability, leading to over-reliance on automated suggestions.
* **Mitigation (Implemented):** Named the output field `do_tin_cay` rather than "probability" and documented its interpretation in user guidelines.
* **Mitigation (Proposed):** Apply probability calibration (e.g., Platt scaling or isotonic regression) on a held-out calibration set and evaluate using Brier Score and Reliability Diagrams before exposing probability estimates.

### Risk 5 — Incomplete Subgroup Performance Evaluation

* **Issue:** While overall Test Macro F1 is `1.000`, granular slice evaluations across description length and `center_id` had limited sample sizes.
* **Operational Impact:** Aggregate metrics can mask performance disparities across specific intake channels or locations.
* **Mitigation (Implemented):** Reported per-class Precision, Recall, F1-score, and a full Confusion Matrix on the Test set.
* **Mitigation (Proposed):** Expand subgroup evaluations by description length, intake channel, and service center as metadata becomes available, using bootstrap confidence intervals for small slices.

### Pre-Deployment Readiness Conclusion

While the model meets benchmark expectations on the experimental dataset, there is insufficient evidence to guarantee equivalent performance on live customer data. Prior to production deployment, the team must collect and annotate real-world data, re-evaluate model performance across subgroups, and update Sections 6, 8, and 9 of this Model Card.

---

## 10. Maintenance and Model Updates

### Retraining Triggers

| Indicator | Proposed Threshold | Action |
| --- | --- | --- |
| **Staff override rate on suggested labels** | `> 35%` within a single month | Audit new incoming data and consider retraining |
| **Low-confidence prediction rate** | Abnormal spike during operation | Inspect input data distribution and description quality |
| **Addition of new fault categories** | Whenever label taxonomy changes | Update annotated dataset and retrain model |
| **Introduction of new device types** | Whenever product scope expands | Collect new device data and run dedicated evaluation |
| **`scikit-learn` version upgrade** | Whenever deployment environment changes | Verify compatibility and rebuild model artifacts if needed |

* **Monitoring Strategy:** Continuously log model predictions alongside final staff-confirmed labels to track real-world agreement rates.
* **Maintainer Responsibilities:** System maintainers are responsible for data auditing, performance monitoring, model retraining, and updating the Model Card for each new release. Every model update must log the dataset version, training configuration, and evaluation metrics.

---

## APPENDIX – RESPONSIBLE AI CHECKLIST (7 SELF-ASSESSMENT QUESTIONS)

### 1. Who is impacted by an INCORRECT prediction from this model, and what do they lose?

Customers submitting devices for warranty service are impacted if a misclassified claim routes their device to the wrong technical team, delaying repair turnaround times. Intake staff also lose time reviewing and manually correcting inaccurate suggestions.

### 2. Do affected individuals know an AI system is involved in the decision? If not, why, and should they be informed?

Intake staff must be informed that the system uses a machine learning model to generate classification suggestions. Customers do not necessarily interact directly with the model since human staff review and confirm every claim; however, explicit user disclosure will be necessary if the AI's scope expands to directly affect customer rights or eligibility.

### 3. Do affected individuals have a way to contest or request a review of an outcome?

Yes. Intake staff can review, override, or modify the model's suggested fault category before confirming the warranty claim. This human-in-the-loop mechanism prevents unverified predictions from taking direct effect.

### 4. Does the model perform worse for any specific group of people or data slice? Was this MEASURED or assumed?

It was **measured** across description length and service centers (`center_id`). The Macro F1 disparity between short and long descriptions is `0.0140`, while the maximum disparity between service centers is `0.1602`. However, sample counts per service center are too small to conclusively prove systemic bias.

### 5. Does the model use any ethically inappropriate features (e.g., gender, age, location) irrelevant to the task?

No. The model's input features are derived exclusively from the device issue description text—not personal attributes like gender, age, or address. Phone numbers, serial numbers, and email addresses are masked with placeholder tokens prior to vectorization. Service center IDs (`center_id`) are used strictly for post-hoc fairness auditing, not as model input features.

### 6. Was the training data collected legitimately, and did data providers consent to this use?

The current dataset was synthetically generated for academic and experimental purposes and contains no real customer data; therefore, customer consent issues do not apply to this version. If real operational data is used in the future, the team must establish a lawful basis for collection, define usage scope, enforce access controls, and implement PII protection measures.

### 7. If this model stops working, can the system still operate, and who gets notified?

If the model fails to load or infer, automated classification will be unavailable, and intake staff must seamlessly fall back to manual classification so warranty intake continues uninterrupted. Error handling, Docker container health checks, and application logs must be configured to alert system maintainers. Failover resilience must be verified through live testing before claiming production readiness.