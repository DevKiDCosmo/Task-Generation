import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

class MathTrainer:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def train(self):
        # CSV-Datei laden
        data = pd.read_csv(self.csv_file, delimiter=";")
        texts = data["math"].tolist()
        levels = data["level"].tolist()

        # Merkmale extrahieren
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(texts)

        # Daten aufteilen
        X_train, X_test, y_train, y_test = train_test_split(X, levels, test_size=0.25, random_state=42)

        # Modell definieren und trainieren
        model = GradientBoostingClassifier(n_estimators=500, learning_rate=0.1, max_depth=5, random_state=42, verbose=1)
        model.fit(X_train, y_train)

        # Modell evaluieren
        y_pred = model.predict(X_test)
        print("Genauigkeit:", accuracy_score(y_test, y_pred))
        print("Klassifikationsbericht:\n", classification_report(y_test, y_pred))

        # Modell und Vektorisierer speichern
        joblib.dump(model, "math_model.pkl")
        joblib.dump(vectorizer, "math_vectorizer.pkl")

        print("Modell und Vektorisierer wurden erfolgreich gespeichert.")

if __name__ == "__main__":
    trainer = MathTrainer("math.csv")
    trainer.train()