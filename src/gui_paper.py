
# NOT RECOMMENDED FOR USE

import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QTextEdit
)
from PyQt5.QtGui import QFont


class PaperCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.exercise_data = {}  # Store exercise data

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Paper Creator")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.main_layout = QHBoxLayout()

        # Paper Details Section
        self.add_paper_details_section()

        # Exercise Details Section
        self.add_exercise_details_section()

        # Buttons
        button_layout = QHBoxLayout()

        self.create_button = QPushButton("Create Paper")
        self.create_button.setFont(QFont("Arial", 12))
        self.create_button.clicked.connect(self.create_paper)
        button_layout.addWidget(self.create_button)

        self.clear_button = QPushButton("Clear All Fields")
        self.clear_button.setFont(QFont("Arial", 12))
        self.clear_button.clicked.connect(self.clear_all_fields)
        button_layout.addWidget(self.clear_button)

        self.main_layout.addLayout(button_layout)

        # Set layout
        self.setLayout(self.main_layout)

    def add_paper_details_section(self):
        # Paper Details Grid Layout
        paper_layout = QGridLayout()

        # Paper ID
        self.paper_id_label = QLabel("Paper ID:")
        self.paper_id_label.setFont(QFont("Arial", 12))
        paper_layout.addWidget(self.paper_id_label, 0, 0)

        self.paper_id_input = QLineEdit()
        self.paper_id_input.setPlaceholderText("Enter Paper ID (e.g., P1.0)")
        paper_layout.addWidget(self.paper_id_input, 0, 1)

        # Title
        self.title_label = QLabel("Title:")
        self.title_label.setFont(QFont("Arial", 12))
        paper_layout.addWidget(self.title_label, 1, 0)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter Title (e.g., Paper Title)")
        paper_layout.addWidget(self.title_input, 1, 1)

        # Description
        self.description_label = QLabel("Description:")
        self.description_label.setFont(QFont("Arial", 12))
        paper_layout.addWidget(self.description_label, 2, 0)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter Description of the Paper")
        paper_layout.addWidget(self.description_input, 2, 1, 1, 1)

        # Version
        self.version_label = QLabel("Version:")
        self.version_label.setFont(QFont("Arial", 12))
        paper_layout.addWidget(self.version_label, 3, 0)

        self.version_input = QLineEdit()
        self.version_input.setPlaceholderText("Enter Version (e.g., 1.0)")
        paper_layout.addWidget(self.version_input, 3, 1)

        # Revision
        self.revision_label = QLabel("Revision:")
        self.revision_label.setFont(QFont("Arial", 12))
        paper_layout.addWidget(self.revision_label, 4, 0)

        self.revision_input = QLineEdit()
        self.revision_input.setPlaceholderText("Enter Revision (e.g., 1)")
        paper_layout.addWidget(self.revision_input, 4, 1)

        # Archive
        self.archive_label = QLabel("Archive:")
        self.archive_label.setFont(QFont("Arial", 12))
        paper_layout.addWidget(self.archive_label, 5, 0)

        self.archive_input = QLineEdit()
        self.archive_input.setPlaceholderText("Enter Archive Name (e.g., P1.0-archive)")
        paper_layout.addWidget(self.archive_input, 5, 1)

        # DOI
        self.doi_label = QLabel("DOI:")
        self.doi_label.setFont(QFont("Arial", 12))
        paper_layout.addWidget(self.doi_label, 6, 0)

        self.doi_input = QLineEdit()
        self.doi_input.setPlaceholderText("Enter DOI (optional)")
        paper_layout.addWidget(self.doi_input, 6, 1)

        # Tags
        self.tags_label = QLabel("Tags:")
        self.tags_label.setFont(QFont("Arial", 12))
        paper_layout.addWidget(self.tags_label, 7, 0)

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Enter Tags (comma-separated, e.g., example,paper,template)")
        paper_layout.addWidget(self.tags_input, 7, 1)

        self.main_layout.addLayout(paper_layout)

    def add_exercise_details_section(self):
        # Exercise Details Grid Layout
        exercise_layout = QGridLayout()

        # Exercise ID
        self.exercise_id_label = QLabel("Exercise ID:")
        self.exercise_id_label.setFont(QFont("Arial", 12))
        exercise_layout.addWidget(self.exercise_id_label, 0, 0)

        self.exercise_id_input = QLineEdit()
        self.exercise_id_input.setPlaceholderText("Enter Exercise ID (e.g., n1, n4)")
        exercise_layout.addWidget(self.exercise_id_input, 0, 1)

        # Languages
        self.languages_label = QLabel("Languages:")
        self.languages_label.setFont(QFont("Arial", 12))
        exercise_layout.addWidget(self.languages_label, 1, 0)

        self.languages_input = QLineEdit()
        self.languages_input.setPlaceholderText("Enter Languages (comma-separated, e.g., en,de,fr)")
        exercise_layout.addWidget(self.languages_input, 1, 1)

        # Versions
        self.versions_label = QLabel("Versions:")
        self.versions_label.setFont(QFont("Arial", 12))
        exercise_layout.addWidget(self.versions_label, 2, 0)

        self.versions_input = QLineEdit()
        self.versions_input.setPlaceholderText("Enter Versions (comma-separated, matching languages)")
        exercise_layout.addWidget(self.versions_input, 2, 1)

        # Exercise Numbers
        self.exercise_numbers_label = QLabel("Exercise Numbers:")
        self.exercise_numbers_label.setFont(QFont("Arial", 12))
        exercise_layout.addWidget(self.exercise_numbers_label, 3, 0)

        self.exercise_numbers_input = QLineEdit()
        self.exercise_numbers_input.setPlaceholderText("Enter Exercise Numbers (comma-separated)")
        exercise_layout.addWidget(self.exercise_numbers_input, 3, 1)

        # Exercise Buttons
        exercise_button_layout = QHBoxLayout()

        self.save_exercise_button = QPushButton("Save Exercise")
        self.save_exercise_button.setFont(QFont("Arial", 12))
        self.save_exercise_button.clicked.connect(self.save_exercise)
        exercise_button_layout.addWidget(self.save_exercise_button)

        self.save_add_more_button = QPushButton("Save and Add More")
        self.save_add_more_button.setFont(QFont("Arial", 12))
        self.save_add_more_button.clicked.connect(self.save_and_add_more_exercise)
        exercise_button_layout.addWidget(self.save_add_more_button)

        exercise_layout.addLayout(exercise_button_layout, 4, 0, 1, 2)

        self.main_layout.addLayout(exercise_layout)

    def save_exercise(self):
        self.save_exercise_data()
        QMessageBox.information(self, "Success", "Exercise saved successfully!")

    def save_and_add_more_exercise(self):
        self.save_exercise_data()
        QMessageBox.information(self, "Success", "Exercise saved! Add more exercises.")
        self.clear_exercise_fields()

    def save_exercise_data(self):
        # Get exercise input values
        exercise_id = self.exercise_id_input.text().strip()
        languages = [lang.strip() for lang in self.languages_input.text().strip().split(",") if lang.strip()]
        versions = [ver.strip() for ver in self.versions_input.text().strip().split(",") if ver.strip()]
        exercise_numbers = [int(num.strip()) for num in self.exercise_numbers_input.text().strip().split(",") if num.strip()]

        # Validate inputs
        if not exercise_id or not languages or not versions or not exercise_numbers:
            QMessageBox.warning(self, "Input Error", "All exercise fields must be filled!")
            return

        if len(languages) != len(versions):
            QMessageBox.warning(self, "Input Error", "Languages and versions count must match!")
            return

        # Save exercise data
        self.exercise_data[exercise_id] = {
            "language": languages,
            "version": versions,
            "exercise": exercise_numbers
        }

    def clear_exercise_fields(self):
        # Clear exercise input fields
        self.exercise_id_input.clear()
        self.languages_input.clear()
        self.versions_input.clear()
        self.exercise_numbers_input.clear()

    def create_paper(self):
        # Get paper input values
        paper_id = self.paper_id_input.text().strip()
        if not paper_id:
            QMessageBox.warning(self, "Input Error", "Paper ID is required!")
            return

        # Use defaults if fields are empty
        title = self.title_input.text().strip() or f"Paper {paper_id}"
        description = self.description_input.toPlainText().strip() or f"This is a description of Paper {paper_id}."
        version = self.version_input.text().strip() or "1.0"
        revision = self.revision_input.text().strip() or "1"
        archive = self.archive_input.text().strip() or f"{paper_id}-archive"
        doi = self.doi_input.text().strip()  # Optional field
        tags = [tag.strip() for tag in self.tags_input.text().strip().split(",") if tag.strip()] or ["example", "paper", "template"]

        # Create paper data
        paper_data = {
            "title": title,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "paper": paper_id,
            "description": description,
            "version": version,
            "revision": revision,
            "archive": archive,
            "doi": doi,
            "tags": tags,
            "exercise": self.exercise_data
        }

        # Ensure the output directory exists
        output_dir = "./paper"
        os.makedirs(output_dir, exist_ok=True)

        # Write the JSON file
        output_file = os.path.join(output_dir, f"{paper_id}.json")
        with open(output_file, 'w', encoding="utf-8") as f:
            json.dump(paper_data, f, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Success", f"Paper JSON created successfully at:\n{output_file}")

    def clear_all_fields(self):
        # Clear all input fields
        self.paper_id_input.clear()
        self.title_input.clear()
        self.description_input.clear()
        self.version_input.clear()
        self.revision_input.clear()
        self.archive_input.clear()
        self.doi_input.clear()
        self.tags_input.clear()
        self.clear_exercise_fields()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaperCreator()
    window.show()
    sys.exit(app.exec_())