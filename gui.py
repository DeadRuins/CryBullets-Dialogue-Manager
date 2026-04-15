from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QToolBar, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QFrame
)
from PyQt6.QtGui import QAction, QDoubleValidator
from PyQt6.QtCore import Qt

import codegen


class DialogueEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Window Setup
        self.resize(1000, 700)
        self.setWindowTitle("CryBullets PyQt Dialogue Manager")
        self.setAcceptDrops(True)

        # 2. Main Layout Structure
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # 3. Setup Components
        self.setup_generator_ui()  # The Dialogue Generating part
        self.setup_editor_ui()     # The Text Editor part
        self.create_toolbars()
        self.create_menu()

    def setup_generator_ui(self):
        """Creates the input fields for generating dialogue code."""
        gen_box = QWidget()
        gen_layout = QVBoxLayout(gen_box)

        # Create a vertical line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setLineWidth(1)

        # Duration Input
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Seconds (e.g. 1.5)")
        self.time_input.setValidator(QDoubleValidator(0.0, 999.0, 2))
        self.time_input.setFixedWidth(120)

        # Frame Name
        self.frame_input = QLineEdit()
        self.frame_input.setPlaceholderText("TNT1")
        self.frame_input.setFixedWidth(150)

        self.nframe_input = QLineEdit()
        self.nframe_input.setPlaceholderText("A")
        self.nframe_input.setFixedWidth(30)

        self.bframe_input = QLineEdit()
        self.bframe_input.setPlaceholderText(" ")
        self.bframe_input.setFixedWidth(30)

        # Goto Input
        self.goto_input = QLineEdit()
        self.goto_input.setPlaceholderText("Goto Label (e.g. Dialogue)")

        # Action Button
        gen_button = QPushButton("Generate to Textbox and Copy it to Clipboard")
        gen_button.setStyleSheet("background-color: #2b5b84; color: white; font-weight: bold; padding: 5px;")
        gen_button.clicked.connect(self.handle_generation)

        # Status Label
        self.status_label = QLabel("Ready")


        # --- ROW 1: Sprite Frames ---
        frame_row = QHBoxLayout()
        frame_row.addWidget(QLabel("Sprite frame name:"))
        frame_row.addWidget(self.frame_input)
        frame_row.addWidget(QLabel("Normal frame:"))
        frame_row.addWidget(self.nframe_input)
        frame_row.addWidget(QLabel("Blink frame:"))
        frame_row.addWidget(self.bframe_input)
        gen_layout.addLayout(frame_row)

        # --- THE HORIZONTAL SEPARATOR ---
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine) # Horizontal Line
        line.setFrameShadow(QFrame.Shadow.Sunken)
        gen_layout.addWidget(line)

        # --- ROW 2: SECONDS ---
        seconds_row = QHBoxLayout()
        seconds_row.addWidget(QLabel("Seconds:"))
        seconds_row.addWidget(self.time_input)
        seconds_row.addWidget(QLabel("Target Label:"))
        seconds_row.addWidget(self.goto_input)
        gen_layout.addLayout(seconds_row)

        # --- THE REST ---
        gen_layout.addWidget(gen_button)
        gen_layout.addWidget(self.status_label)

        self.main_layout.addWidget(gen_box)

    def setup_editor_ui(self):
        """Sets up the main text editing area."""
        self.textEdit = QTextEdit()
        # Set a monospaced font for coding
        self.textEdit.setStyleSheet("font-family: 'Consolas', 'Monospace'; font-size: 13px;")
        self.main_layout.addWidget(self.textEdit)

    def create_toolbars(self):
        file_toolbar = QToolBar("File")
        self.addToolBar(file_toolbar)

        new_action = QAction("New", self)
        new_action.triggered.connect(lambda: self.textEdit.clear())
        file_toolbar.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_toolbar.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_toolbar.addAction(save_action)

    def create_menu(self):
        file_menu = self.menuBar().addMenu("&File")

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "ZScript/Text (*.txt *.zsc);;All Files (*)")
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                self.textEdit.setPlainText(f.read())

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text (*.txt);;ZScript Txt (*.zsc);;All Files (*)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.textEdit.toPlainText())

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            filepath = url.toLocalFile()
            if filepath:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.textEdit.setPlainText(f.read())
                break

    def handle_generation(self):
            """Bridge between GUI and Logic."""
            try:
                # Gather data from GUI
                f_label = self.frame_input.text() or "TNT1"
                target = self.goto_input.text()
                secs = self.time_input.text()

                if not target or not secs:
                    return

                # Call the Logic
                script = codegen.generate_zscript(f_label, "A", "B", target, secs)

                # Update GUI
                self.textEdit.insertPlainText(script)

            except Exception as e:
                self.status_label.setText(f"Error: {str(e)}")
                print(f"Error: {e}")
