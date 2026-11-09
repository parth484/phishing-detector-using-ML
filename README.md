# Phishing URL Detection – ML & Feature Pipeline

## 1. Project Overview

This project focuses on detecting phishing URLs using Machine Learning techniques. The ML pipeline extracts URL-based features, preprocesses the dataset, trains a Random Forest classifier, evaluates its performance, and saves the trained model for future predictions.

**My Role:** ML & Feature Pipeline Lead

**Technologies Used:**
- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- urllib.parse
- tldextract
- IP Address

## 2. Dataset

**Dataset:** PhiUSIIL Phishing URL Dataset

Source: https://www.kaggle.com/datasets/kaggleprollc/phishing-url-websites-dataset-phiusiil

Dataset details:
- Original records: 235,795
- Records after cleaning: 235,370
- Balanced sample selected: 10,000
- Phishing samples: 5,000
- Legitimate samples: 5,000

### Data Preprocessing
- Explored dataset structure and columns.
- Checked missing values.
- Removed duplicate and invalid records during cleaning.
- Handled infinite and missing values.
- Created a balanced dataset for model training.

## 3. URL Feature Extraction

Implemented a URL feature extraction pipeline to convert raw URLs into numerical features suitable for machine learning.

**Total Features Extracted: 17**

| No. | Feature |
|---|---|
| 1 | URLLength |
| 2 | DomainLength |
| 3 | IsDomainIP |
| 4 | TLDLength |
| 5 | NoOfSubDomain |
| 6 | HasObfuscation |
| 7 | NoOfObfuscatedChar |
| 8 | ObfuscationRatio |
| 9 | NoOfLettersInURL |
| 10 | LetterRatioInURL |
| 11 | NoOfDegitsInURL |
| 12 | DegitRatioInURL |
| 13 | NoOfEqualsInURL |
| 14 | NoOfQMarkInURL |
| 15 | NoOfAmpersandInURL |
| 16 | NoOfOtherSpecialCharsInURL |
| 17 | SpacialCharRatioInURL |

These features help identify suspicious URL characteristics such as unusually long URLs, IP-based domains, subdomains, obfuscation, and excessive special characters.

## 4. Model Training

**Algorithm:** Random Forest Classifier

Training configuration:
- Dataset size: 10,000 samples
- Training samples: 8,000
- Testing samples: 2,000
- Model: RandomForestClassifier
- Number of estimators: 100

The dataset was divided into training and testing sets to evaluate the model on unseen samples.

## 5. Model Evaluation

The trained model achieved the following results:

<escape>
</escape>

| Evaluation Metric | Result |
|---|---:|
| Accuracy | 97.45% |
| Precision | ~97% |
| Recall | ~97% |
| F1-Score | ~97% |

### Confusion Matrix

```text
[[974  26]
 [ 25 975]]
```

The model achieved 97.45% accuracy on the 2,000 testing samples.

## 6. Model Persistence

Used Joblib to save the trained model and supporting preprocessing information.

Generated artifacts:

```text
rf_model_v2.pkl
url_medians_v2.pkl
url_features_v2.pkl
```

These files store:
- Trained Random Forest model.
- Feature median values used for preprocessing.
- Expected feature names and ordering.

## 7. Prediction & Inference

Implemented and tested the V3 prediction workflow.

The inference pipeline:
1. Accepts a URL as input.
2. Extracts the required 17 URL features.
3. Applies the required preprocessing.
4. Loads the trained Random Forest model.
5. Generates a prediction.

Tested the prediction workflow using multiple URLs, including legitimate-looking URLs and suspicious IP-based URLs.

## 8. My Contribution

As the ML & Feature Pipeline Lead, my completed responsibilities include:

- Dataset exploration and analysis.
- Dataset cleaning and preprocessing.
- URL feature engineering.
- Extraction of 17 numerical URL features.
- Random Forest model implementation.
- Training and testing the machine learning model.
- Performance evaluation using accuracy, precision, recall, F1-score, and confusion matrix.
- Saving trained model artifacts using Joblib.
- Developing and testing the prediction and inference pipeline.

## 9. Project Status

**Completed Work:**
- Dataset preprocessing.
- 17-feature extraction pipeline.
- Random Forest model training.
- Model evaluation.
- Model artifact generation.
- V3 prediction workflow testing.

---

**Focus:** Machine Learning, URL Feature Engineering, Model Training, Evaluation & Inference.

**Role:** ML & Feature Pipeline Lead
