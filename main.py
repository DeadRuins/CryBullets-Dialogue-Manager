import sys
import threading
import keyboard

from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

class LineEditDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        # Labels
        label_top = QLabel("Sets up a dialogue for Crystalled Bullets.")

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Specify the length of voice (Seconds) here...")
        self.text_input.setValidator(QDoubleValidator(0.0, 999.0, 2))
        self.text_input.returnPressed.connect(self.copy_to_clipboard)

        self.goto_input = QLineEdit()
        self.goto_input.setPlaceholderText("Enter your goto (TNT1 A 0 A_JumpIfInTargetInventory('SkipDialogue'), 1, 'This part') here...")

        self.result_label_top = QLabel("Waiting for user input...")


        # The Button
        copy_button = QPushButton("Enter")
        copy_button.clicked.connect(self.copy_to_clipboard)

        # UI Layouts
        layout = QVBoxLayout()
        layout.addWidget(label_top)
        layout.addWidget(self.text_input)
        layout.addWidget(self.goto_input)
        layout.addWidget(copy_button)
        layout.addWidget(self.result_label_top)

        self.setLayout(layout)
        self.setWindowTitle("CryBullets Python Dialogue Manager") # ウィンドウのタイトル
        self.setFixedSize(600,300) # ウィンドウの位置と大きさ


    def copy_to_clipboard(self):
            input_text = self.text_input.text()
            goto_input2 = self.goto_input.text()

            try:
                # Generate the code.
                second_val = float(input_text)
                count = int(second_val * 36)

                preformat_text = ""
                x = 0
                # The first ten lines will be devoted to not dialogue to skip/
                for x in range(0, 10):
                    preformat_text = preformat_text + f'TNT1 A 1 CB_DialogueSkipPrevent;\n'
                    x = x + 1

                # Actually doing stuffs.
                for x in range(10, count):
                    preformat_text = preformat_text + f'TNT1 A 1 A_JumpIfInTargetInventory("SkipDialogue", 1, "' + goto_input2 + f'");\n'
                    x = x + 1

                formatted_text = preformat_text + f'\n' + goto_input2 + ":"

                # Copy to clipboard
                QApplication.clipboard().setText(formatted_text)

                # Update UI
                self.result_label_top.setText(f"Copied script for {count} lines, pasted on clipboard.")
                self.text_input.clear()

            except ValueError:
                # This runs if the user typed letters instead of numbers
                self.result_label_top.setText("Error: Please enter a valid number!")


if __name__ == "__main__":
    app = QApplication([])
    demo = LineEditDemo()
    demo.show()
    app.exec()
