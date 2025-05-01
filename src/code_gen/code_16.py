class Code_16:
    def __init__(self):
        pass

    def hash_to_tikz(self, hash_string: str, x_size: str = "8pt", y_size: str = "8pt") -> str:
        """
        # 16 Farben für Hex-Ziffern 0–F
        """
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
                    f"  \\fill[{color}] ({i / 4},0) rectangle ({(i + 1) / 4},1);"
                )

        tikz_code.append("\\end{tikzpicture}")
        return "\n".join(tikz_code)
