class Code_256:
    def __init__(self):
        pass

    def byte_to_html_color(self, index: int) -> str:
        """Wandle Bytewert (0–255) in eine HTML-Hexfarbe (#RRGGBB)"""
        r = (index * 73) % 256
        g = (index * 151) % 256
        b = (index * 199) % 256
        return f"{r:02X}{g:02X}{b:02X}"  # z.B. "3FA2D1"

    def text_to_tikz_html(self, text: str, x_size: str = "8pt", y_size: str = "8pt") -> str:
        tikz_lines = [
            # "\\usepackage[table]{xcolor}",  # TikZ-Farben aus HTML
            f"\\begin{{tikzpicture}}[x={x_size}, y={y_size}]"
        ]

        for i, c in enumerate(text.encode("utf-8")):
            html_color = self.byte_to_html_color(c)
            tikz_lines.append(
                f"  \\definecolor{{col{i / 8}}}{{HTML}}{{{html_color}}}%" +
                f"\n  \\fill[col{i / 8}] ({i / 8},0) rectangle ({(i + 1) / 8},1);"
            )

        tikz_lines.append("\\end{tikzpicture}")
        return "\n".join(tikz_lines)
