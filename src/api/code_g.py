def hash_to_tikz(hash_string, x_size="8pt", y_size="8pt"):
    # 16 Farben für Hex-Ziffern 0–F
    colors = [
        "red", "green", "blue", "yellow",
        "magenta", "cyan", "gray", "orange",
        "violet", "teal", "lime", "brown",
        "purple", "olive", "black", "white"
    ]

    tikz_code = []
    tikz_code.append(f"\\begin{{tikzpicture}}[x={x_size}, y={y_size}]")

    for i, hex_char in enumerate(hash_string.lower()):
        if hex_char in "0123456789abcdef":
            index = int(hex_char, 16)
            color = colors[index]
            tikz_code.append(
                f"  \\fill[{color}] ({i/4},0) rectangle ({(i+1)/4},1);"
            )

    tikz_code.append("\\end{tikzpicture}")
    return "\n".join(tikz_code)


# Beispielaufruf:
hash_value = "Duy Nam Schlitz"
tikz_output = hash_to_tikz(hash_value)

# Ausgabe in Datei oder Konsole
print(tikz_output)

# Optional: In .tex-Datei speichern
with open("hash_tikz_output.tex", "w") as f:
    f.write(tikz_output)
