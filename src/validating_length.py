import re
import os
import sys


def process_file(filepath, already_included=None):
    if already_included is None:
        already_included = set()
    # Prevent circular inclusions
    if filepath in already_included:
        return ""
    already_included.add(filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: File not found:", filepath)
        return ""

    # Pattern to find \input{filename} commands
    pattern = r'\\input\{([^}]+)\}'

    def replacer(match):
        # Get the filename from the \input command
        filename = match.group(1)
        # Append .tex extension if missing
        if not os.path.splitext(filename)[1]:
            filename += ".tex"
        # Build the file path relative to the current file
        subfile_path = os.path.join(os.path.dirname(filepath), filename)
        subfile_path += ".tex" if not subfile_path.endswith(".tex") else ""
        if os.path.exists(subfile_path):
            return process_file(subfile_path, already_included)
        else:
            print("Warning: File not found:", subfile_path)
            return ""

    # Replace each \input occurrence recursively
    new_content = re.sub(pattern, replacer, content)
    return new_content


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <main.tex> <output.tex>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    combined_content = process_file(input_file)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined_content)

    print(f"Combined LaTeX file saved as {output_file}")


if __name__ == "__main__":
    main()
