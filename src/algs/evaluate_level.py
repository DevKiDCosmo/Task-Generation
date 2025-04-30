import joblib
import numpy as np

class LanguageLevelEvaluator:
    def __init__(self, level_model_path, vectorizer_path):
        self.level_model = joblib.load(level_model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def evaluate_language_level(self, text):
        if not text.strip():
            return "No text provided", None
        X = self.vectorizer.transform([text])
        level = self.level_model.predict(X)[0]
        return level

if __name__ == "__main__":
    evaluator = LanguageLevelEvaluator(
        "language_level_model_by_sentenced.pkl",
        "vectorizer_by_sentenced.pkl"
    )

    sample_text = """
    This is a sample text to evaluate the language level.
    It contains multiple sentences and varying complexity.
    """

    language_level = evaluator.evaluate_language_level(sample_text)
    print({
        "text": sample_text.strip(),
        "language_level": language_level
    })