import pandas as pd
import numpy as np

dataset_a = pd.read_csv('./new_features/features_of_A.csv')
dataset_b = pd.read_csv('./new_features/features_of_B.csv')
dataset_c = pd.read_csv('./new_features/features_of_C.csv')

dataset = pd.concat([dataset_a, dataset_b, dataset_c])

dataset.head()

dataset.shape

dataset = dataset.dropna()



dataset.shape

print(dataset['Label'].tolist().count('A'))
print(dataset['Label'].tolist().count('N'))

dataset.head()

# from sklearn.model_selection import train_test_split

# unique_patients = dataset['Record_ID'].unique()

# # Split patients into Train (80%) and Test (20%)
# train_patients, test_patients = train_test_split(unique_patients, test_size=0.5, random_state=42)

# # Create train & test datasets
# train_data = dataset[dataset['Record_ID'].isin(train_patients)]
# test_data = dataset[dataset['Record_ID'].isin(test_patients)]

# # Save or return the datasets
# train_data.to_csv("train_patient_wise.csv", index=False)
# test_data.to_csv("test_patient_wise.csv", index=False)

# print("Train Data Patients:", len(train_patients))
# print("Test Data Patients:", len(test_patients))
# print("Train Size:", train_data.shape, "Test Size:", test_data.shape)

# Import required libraries
import pandas as pd
import numpy as np
from imblearn.over_sampling import ADASYN
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split


# Extract features and labels
X = dataset.drop(columns=["Label", "Record_ID"])
y = dataset["Label"]


# X_train , X_test , y_train , y_test = train_data.drop(columns=["Label", "Record_ID"]), test_data.drop(columns=["Label", "Record_ID"]), train_data["Label"], test_data["Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Apply ADASYN to balance the dataset
adasyn = ADASYN(random_state=75)
X_train_resampled, y_train_resampled = adasyn.fit_resample(X_train, y_train)
# X_test, y_test = adasyn.fit_resample(X_test, y_test)



X_train_resampled.shape

X_test.head()

y_train_resampled.shape

print(y_train_resampled.tolist().count('A'))
print(y_train_resampled.tolist().count('N'))

from sklearn.preprocessing import LabelEncoder,StandardScaler


# X_train = df_modified.drop(columns=["Label"])
# Y_train = df_modified["Label"]

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train_resampled)

labelEncoder = LabelEncoder()
y_train = labelEncoder.fit_transform(y_train_resampled)



X_test = scaler.transform(X_test)
y_test = labelEncoder.transform(y_test)


X_train.shape

print(y_train.tolist().count(1))
print(y_train.tolist().count(0))
print(y_test.tolist().count(0))
print(y_test.tolist().count(1))

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, matthews_corrcoef
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.metrics import geometric_mean_score

def metricCalculation(y_test, y_pred):
  cm = confusion_matrix(y_test, y_pred)
  TN, FP, FN, TP = cm.ravel()

  accuracy = accuracy_score(y_test, y_pred)
  tpr = recall_score(y_test, y_pred)
  tnr = TN / (TN + FP)
  auc = roc_auc_score(y_test, y_pred)
  g_mean = geometric_mean_score(y_test, y_pred)
  precision = precision_score(y_test, y_pred)
  fscore = f1_score(y_test, y_pred)

  return {
      "Accuracy": accuracy,
      "TPR": tpr,
      "TNR": tnr,
      "AUC": auc,
      "G-Mean": g_mean,
      "Precision": precision,
      "F-Score": fscore
  }



from sklearn.linear_model import LogisticRegression

logreg_classifier = LogisticRegression(random_state=42)
logreg_classifier.fit(X_train, y_train)

Y_pred_logreg = logreg_classifier.predict(X_test)

logistic_metrics = metricCalculation(y_test, Y_pred_logreg)

logistic_metrics

from sklearn.naive_bayes import GaussianNB

nb_classifier = GaussianNB()
nb_classifier.fit(X_train, y_train)
Y_pred_nb = nb_classifier.predict(X_test)

nb_metrics = metricCalculation(y_test, Y_pred_nb)

from sklearn.neighbors import KNeighborsClassifier

knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)
Y_pred_knn = knn_classifier.predict(X_test)

knn_metrics = metricCalculation(y_test, Y_pred_knn)

knn_metrics

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

dt_classifier = DecisionTreeClassifier(random_state=42)

dt_classifier.fit(X_train, y_train)

Y_pred = dt_classifier.predict(X_test)

dt_metrics = metricCalculation(y_test, Y_pred)

from sklearn.svm import SVC

svm_classifier = SVC(probability=True, kernel='rbf', C=1.0, random_state=42)
svm_classifier.fit(X_train, y_train)
Y_pred_svm = svm_classifier.predict(X_test)

svm_metrics = metricCalculation(y_test, Y_pred_svm)
svm_metrics

from sklearn.ensemble import RandomForestClassifier

rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X_train, y_train)
Y_pred_rf = rf_classifier.predict(X_test)

rf_metrics = metricCalculation(y_test, Y_pred_rf)


from sklearn.ensemble import AdaBoostClassifier


ada_classifier = AdaBoostClassifier(random_state=42)
ada_classifier.fit(X_train, y_train)
Y_pred_ada = ada_classifier.predict(X_test)

ada_metrics = metricCalculation(y_test, Y_pred_ada)



from sklearn.ensemble import GradientBoostingClassifier

gb_classifier = GradientBoostingClassifier(random_state=42)
gb_classifier.fit(X_train, y_train)
Y_pred_gb = gb_classifier.predict(X_test)

gb_metrics = metricCalculation(y_test, Y_pred_gb)


from sklearn.ensemble import BaggingClassifier

base_estimator = DecisionTreeClassifier(random_state=42)

bagging_classifier = BaggingClassifier(estimator=base_estimator, n_estimators=10, random_state=42)

bagging_classifier.fit(X_train, y_train)

Y_pred_bagging = bagging_classifier.predict(X_test)

bagging_metrics = metricCalculation(y_test, Y_pred_bagging)


from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

xgb_classifier = XGBClassifier(random_state=42)
xgb_classifier.fit(X_train, y_train)

Y_pred_xgb = xgb_classifier.predict(X_test)

xgb_metrics = metricCalculation(y_test, Y_pred_xgb)


from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

# Hyperparameters for Decision Tree
dt_params = {
    'max_depth': [None, 10, 20, 56],  # Max number of splits
    'criterion': ['gini'],  # Split criterion
}

# Initialize the Decision Tree model
dt = DecisionTreeClassifier(random_state=42)

# Hyperparameter tuning with GridSearchCV
dt_grid = GridSearchCV(dt, dt_params, cv=5, scoring='accuracy')
dt_grid.fit(X_train, y_train)

# Best Parameters and Best Model
dt_best = dt_grid.best_estimator_

Y_pred_dt_best = dt_best.predict(X_test)
optimised_dt_metrics = metricCalculation(y_test, Y_pred_dt_best)

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV

# Define hyperparameters for Naïve Bayes
nb_params = {
    'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6],  # Smoothing parameter for GaussianNB
}

# Initialize Naïve Bayes model
nb_model = GaussianNB()

# Perform Grid Search for hyperparameter tuning
nb_grid = GridSearchCV(nb_model, nb_params, cv=5, scoring='accuracy', n_jobs=-1)
nb_grid.fit(X_train, y_train)

# Best parameters and model
nb_best = nb_grid.best_estimator_

# Evaluate tuned model
Y_pred_nb_best = nb_best.predict(X_test)
optimised_nb_metrics = metricCalculation(y_test, Y_pred_nb_best)



# Store all model metrics in a dictionary
models_metrics = {
    "Logistic Regression": logistic_metrics,
    "Naive Bayes": nb_metrics,
    "KNN": knn_metrics,
    "Decision Tree": dt_metrics,
    "SVM": svm_metrics,
    "Random Forest": rf_metrics,
    "AdaBoost": ada_metrics,
    "Gradient Boosting": gb_metrics,
    "Bagging Classifier": bagging_metrics,
    "XGBoost": xgb_metrics,
    "Optimized Decision Tree": optimised_dt_metrics,
    "Optimized Naive Bayes": optimised_nb_metrics
}

# Convert to DataFrame
metrics_df = pd.DataFrame(models_metrics).T

# Display the DataFrame
print(metrics_df)

# Save to CSV (optional)
metrics_df.to_csv("50_20_split_model_metrics.csv", index=True)


metrics_df

from prettytable import PrettyTable

# Define table headers
table = PrettyTable()
table.field_names = ["Model", "Accuracy", "TPR", "TNR", "AUC", "G-Mean", "Precision", "F-Score"]

# Add rows to the table
for model, metrics in models_metrics.items():
    table.add_row([model] + list(metrics.values()))

# Print the table
print(table)


import joblib

joblib.dump(xgb_classifier, 'xgb_classifier.pkl')

joblib.dump(rf_classifier, 'rf_classifier.pkl')

joblib.dump(knn_classifier, 'knn_classifier.pkl')

joblib.dump(bagging_classifier,'bagging_classifier.pkl')

