import sys
from PyQt6.QtWidgets import QApplication
from gui import DialogueEditor

def main():
    app = QApplication(sys.argv)

    # Create the window
    window = DialogueEditor()
    window.show()

    # Run the app
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
