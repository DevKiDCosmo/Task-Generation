import re
import joblib
import numpy as np

class ExerciseScorer:
    def __init__(self, math_model_path, vectorizer_path):
        self.math_model = joblib.load(math_model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def extract_equations(self, text):
        equations = re.findall(r"\$\$(.*?)\$\$|\$(.*?)\$|\\\[(.*?)\\\]|\[(.*?)\]", text, re.DOTALL)
        equations = ["".join(eq).strip() for eq in equations if any(eq)]
        return equations

    def evaluate_math_levels(self, equations):
        if not equations:
            return "No equations found", None, None, None, None
        levels = []
        for eq in equations:
            X = self.vectorizer.transform([eq])
            levels.append(self.math_model.predict(X)[0])
        min_level = min(levels)
        max_level = max(levels)
        median_level = np.median(levels)
        final_degree = sum(level ** 3 for level in levels) / sum(levels * 2)
        absolute_degree = (final_degree + median_level) / 2
        return levels, min_level, max_level, median_level, final_degree, absolute_degree

if __name__ == "__main__":
    scorer = ExerciseScorer(
        "math_model.pkl",
        "math_vectorizer.pkl"
    )

    exercise_text = """
    Untersuchen Sie ein raumzeitlich abhängiges Wellenphänomen unter dem Einfluss eines stochastischen Rauschens. Die Wellenfunktion sei gegeben durch:

\\[
\\Psi(x,t,\\omega) = \\psi(x,t) + N(x,t,\\omega)
\\]

wobei:
\\begin{itemize}
  \\item $\\psi(x,t) = A \\sin(kx - \\omega t)$ eine deterministische Basiswelle ist,
  \\item $N(x,t,\\omega)$ ein Gauß-Prozess mit Mittelwert $0$ und stationärer Kovarianzfunktion ist.
\\end{itemize}

\\textbf{Gegeben:}

Ein Gauß-Prozess mit Kovarianzfunktion:

\\[
K(x_1, x_2) = \\sigma^2 \\exp(-\\lambda |x_1 - x_2|)
\\]

und bekannter Rauschstärke $\\sigma^2$ sowie Skalenparameter $\\lambda > 0$.

\\subsubsection{Aufgaben}

\\begin{enumerate}
  \\item \\textbf{Modellierung:} Formulieren Sie $N(x,t,\\omega)$ als Gauß-Prozess mit obiger Kovarianzfunktion.

  \\item \\textbf{Simulation:} Simulieren Sie mehrere Realisierungen von $\\Psi(x,t,\\omega)$ auf einem Gitter $(x_i, t_j)$ für verschiedene Parameter $\\sigma^2$ und $k$.

  \\item \\textbf{Statistik:} Berechnen Sie Erwartungswert $E[\\Psi(x,t)]$ und Varianz $Var[\\Psi(x,t)]$ sowohl analytisch als auch aus den simulierten Daten.

  \\item \\textbf{Spektralanalyse:} Führen Sie eine Fourier-Zerlegung von $\\Psi(x,t,\\omega)$ durch und berechnen Sie die spektrale Energiedichte.

  \\item \\textbf{Extremwertstatistik:} Schätzen Sie die Wahrscheinlichkeitsverteilung der Maxima im Intervall $[a, b]$ mithilfe von Maximum-Likelihood oder Bayesianischen Methoden.

  \\item[\\textbf{(Bonus)}] \\textbf{Rekonstruktion:} Trainieren Sie ein neuronales Netz, das aus verrauschten Beobachtungen $\\Psi(x,t,\\omega)$ die Basiswelle $\\psi(x,t)$ rekonstruiert.
\\end{enumerate}
    """

    equations = scorer.extract_equations(exercise_text)
    levels, min_level, max_level, median_level, final_degree, absolute = scorer.evaluate_math_levels(equations)
    print({
        "math_levels": levels,
        "min_level": min_level,
        "max_level": max_level,
        "median_level": median_level,
        "final_degree": final_degree,
        "absolute_degree": absolute
    })