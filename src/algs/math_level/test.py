from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

# Daten laden
data = pd.read_csv("math.csv", delimiter=";")
texts = data["math"].tolist()
levels = data["level"].tolist()

# TfidfVectorizer verwenden
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Daten aufteilen
X_train, X_test, y_train, y_test = train_test_split(X, levels, test_size=0.25, random_state=42)

# Grid Search für Hyperparameter-Tuning
param_grid = {
    'n_estimators': [100, 300, 500],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}
model = GradientBoostingClassifier(random_state=42)
grid_search = GridSearchCV(model, param_grid, cv=3, scoring='accuracy', verbose=1)
grid_search.fit(X_train, y_train)

# Bestes Modell evaluieren
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
print("Beste Parameter:", grid_search.best_params_)
print("Genauigkeit:", accuracy_score(y_test, y_pred))
print("Klassifikationsbericht:\n", classification_report(y_test, y_pred))