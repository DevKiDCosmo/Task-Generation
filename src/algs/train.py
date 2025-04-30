# Train all
import word_level.train as wl
import sentence.train as st
import math_level.train as mth

def main():
    # Word Level Training
    word_trainer = wl.word_level("word_level/word_data.csv")
    word_trainer.main()

    # Sentence Level Training
    sentence_trainer = st.SentenceLevelTrainer("sentence/language_data.csv")
    sentence_trainer.train()

    # Math Level Training
    math_trainer = mth.MathTrainer("math_level/math.csv")
    math_trainer.train()

if __name__ == "__main__":
    main()