# Malicious Website Detector

## Screenshots

### Training Label Distribution

![Training Labels](labels.png)

### JavaScript Obfuscation Analysis

![Obfuscated JavaScript Analysis](js_obf_len_box.png)

## Project Overview

Malicious Website Detector is a machine learning project built in Python that identifies potentially malicious websites using website metadata and behavioral indicators. The project performs exploratory data analysis, applies business rules, trains classification models, and predicts whether a website is safe or malicious.

Two machine learning models were evaluated: Logistic Regression and Random Forest. The Random Forest model produced the best performance and was selected as the final solution.

## Results

- Best Model: Random Forest
- Optimal Classification Threshold: 0.13
- True Positives: 298
- False Positives: 2
- True Negatives: 7018
- False Negatives: 7
- Total Business Cost: 7100

The final model was optimized using business-driven cost analysis where false negatives carried a significantly higher penalty than false positives.

## Features

- Exploratory data analysis (EDA)
- Data visualization using Matplotlib
- Website feature analysis
- Business rule implementation
- Logistic Regression classification
- Random Forest classification
- Model performance evaluation
- Threshold optimization
- Prediction generation for unlabeled websites
- Automated results reporting

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Random Forest
- Logistic Regression
- Machine Learning
- Data Analysis

## What I Learned

This project helped me gain experience with:

- Machine learning model development
- Data cleaning and preprocessing
- Exploratory data analysis
- Feature engineering
- Classification algorithms
- Model evaluation techniques
- Business-driven decision making
- Cybersecurity risk assessment
- Data visualization and reporting

## How To Run

Install the required packages:

```bash
pip install pandas numpy matplotlib scikit-learn
```

Run the application:

```bash
python malicious_website_detector.py
```

## Project Structure

```text
malicious_website_detector.py
results_summary.txt
labels.png
js_obf_len_box.png
README.md
```

## Dataset Insights

Key findings from the exploratory data analysis included:

- The dataset was highly imbalanced, with significantly more safe websites than malicious websites.
- JavaScript obfuscation length was substantially higher for malicious websites.
- Domain age and website behavior indicators provided useful predictive information.
- Business rules improved model decision-making prior to classification.

## Future Improvements

- Additional feature engineering
- Cross-validation and hyperparameter tuning
- XGBoost implementation
- Real-time website scoring
- Web-based dashboard
- API deployment for live predictions
- Expanded cybersecurity threat indicators
