import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

class word_level:
    def __init__(self, word):
        self.word = word

    def main(self):
        # CSV-Datei laden
        data = pd.read_csv(self.word, delimiter=";")
        texts = data["word"].tolist()
        languages = data["language"].tolist()
        levels = data["level"].tolist()

        # Merkmale extrahieren
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(texts)

        # Daten für Sprachen aufteilen
        X_train_lang, X_test_lang, y_train_lang, y_test_lang = train_test_split(X, languages, test_size=0.25,
                                                                                random_state=42)

        # Daten für Sprachniveaus aufteilen
        X_train_level, X_test_level, y_train_level, y_test_level = train_test_split(X, levels, test_size=0.25,
                                                                                    random_state=42)

        # Modell für Sprachen trainieren
        model_language = GradientBoostingClassifier(n_estimators=1000, learning_rate=0.1, max_depth=5, random_state=42,
                                                    verbose=1)
        model_language.fit(X_train_lang, y_train_lang)

        # Modell für Sprachniveaus trainieren
        model_level = GradientBoostingClassifier(n_estimators=1000, learning_rate=0.1, max_depth=5, random_state=42,
                                                 verbose=1)
        model_level.fit(X_train_level, y_train_level)

        # Modelle evaluieren
        y_pred_lang = model_language.predict(X_test_lang)
        y_pred_level = model_level.predict(X_test_level)

        print("Genauigkeit (Sprache):", accuracy_score(y_test_lang, y_pred_lang))
        print("Klassifikationsbericht (Sprache):\n", classification_report(y_test_lang, y_pred_lang))

        print("Genauigkeit (Level):", accuracy_score(y_test_level, y_pred_level))
        print("Klassifikationsbericht (Level):\n", classification_report(y_test_level, y_pred_level))

        # Modelle und Vektorisierer speichern
        joblib.dump(model_language, "language_model_by_words.pkl")
        joblib.dump(model_level, "level_model_by_words.pkl")
        joblib.dump(vectorizer, "word_vectorizer.pkl")

        print("Modelle und Vektorisierer wurden erfolgreich gespeichert.")

if __name__ == "__main__":
    word = word_level("word_data.csv")
    word.main()