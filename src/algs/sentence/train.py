import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

class SentenceLevelTrainer:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def train(self):
        # CSV-Datei laden
        data = pd.read_csv(self.csv_file, delimiter=";")
        texts = data["text"].tolist()
        levels = data["level"].tolist()
        languages = data["language"].tolist()

        # Merkmale extrahieren
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(texts)

        # Daten aufteilen
        X_train, X_test, y_train_languages, y_test_languages = train_test_split(
            X, languages, test_size=0.25, random_state=42
        )
        _, _, y_train_levels, y_test_levels = train_test_split(
            X, levels, test_size=0.25, random_state=42
        )

        # Modell für Sprachen trainieren
        model_language = GradientBoostingClassifier(
            n_estimators=500, learning_rate=0.1, max_depth=5, random_state=42, verbose=1
        )
        model_language.fit(X_train, y_train_languages)

        # Modell für Sprachniveaus trainieren
        model_level = GradientBoostingClassifier(
            n_estimators=500, learning_rate=0.1, max_depth=5, random_state=42, verbose=1
        )
        model_level.fit(X_train, y_train_levels)

        # Modelle evaluieren
        y_pred_languages = model_language.predict(X_test)
        y_pred_levels = model_level.predict(X_test)

        print("Genauigkeit (Sprache):", accuracy_score(y_test_languages, y_pred_languages))
        print("Klassifikationsbericht (Sprache):\n", classification_report(y_test_languages, y_pred_languages))

        print("Genauigkeit (Level):", accuracy_score(y_test_levels, y_pred_levels))
        print("Klassifikationsbericht (Level):\n", classification_report(y_test_levels, y_pred_levels))

        # Modelle und Vektorisierer speichern
        joblib.dump(model_language, "language_model_by_sentenced.pkl")
        joblib.dump(model_level, "language_level_model_by_sentenced.pkl")
        joblib.dump(vectorizer, "vectorizer_by_sentenced.pkl")

        print("Modelle und Vektorisierer wurden erfolgreich gespeichert.")

if __name__ == "__main__":
    trainer = SentenceLevelTrainer("language_data.csv")
    trainer.train()