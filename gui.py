from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QToolBar, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QFrame, QMessageBox, QCheckBox
)
from PyQt6.QtGui import QAction, QDoubleValidator, QIntValidator
from PyQt6.QtCore import Qt

from mutagen.oggvorbis import OggVorbis
import codegen
import audio_analyze

ABOUT = """<p>The <b>Crystalled Bullets PyQt Dialogue Manager</b> is a Python and Qt based application, intent to assist development of the game.<br>
While its intent to used on Crystalled Bullets' development, feel free to use it on your ZDoom-based project.<br><br>

If you have encountered any trouble, please contact to DeadRuins(https://deadruins.github.io/).<br>
Preferably submit issues on GitHub.

"""


class DialogueEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Window Setup
        self.resize(1000, 1000)
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

        # CB_SpeakDialgoue setups
        self.dnumber1_input = QLineEdit()
        self.dnumber1_input.setValidator(QIntValidator(0, 99))
        self.dnumber1_input.setFixedWidth(60)

        self.dnumber2_input = QLineEdit()
        self.dnumber2_input.setValidator(QIntValidator(0, 99))
        self.dnumber2_input.setFixedWidth(60)

        self.isplayer_input = QCheckBox('IsPlayer',self)

        # Duration Input
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("e.g. 1.5[seconds]")
        self.time_input.setValidator(QDoubleValidator(0.0, 999.0, 2))
        self.time_input.setFixedWidth(120)

        # Mouth Moving Frame Lists Input1
        self.mouthmove_input = QLineEdit()
        self.mouthmove_input.setPlaceholderText("e.g. 0.3, 0.7, 1.2 (...)")

        # Mouth Moving Frame Lists Input2, Unperiodic
        self.mouthmove_input2 = QLineEdit()
        self.mouthmove_input2.setPlaceholderText("e.g. 0.3, 0.7, 1.2 (...)")

        # variables for audio analysis (analyze_var_row)
        self.threshold_input = QLineEdit()
        self.threshold_input.setPlaceholderText("[db]")
        self.threshold_input.setText("0.3")
        self.threshold_input.setFixedWidth(150)

        self.window_input = QLineEdit()
        self.window_input.setPlaceholderText("[milliseconds]")
        self.window_input.setText("0.05")
        self.window_input.setFixedWidth(150)

        # Goto Input
        self.goto_input = QLineEdit()
        self.goto_input.setPlaceholderText("Goto Label (e.g. Dialogue2)")

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

        #For MouthOpen
        self.oframe_input = QLineEdit()
        self.oframe_input.setPlaceholderText(" ")
        self.oframe_input.setFixedWidth(30)

        #For MouthOpen, Larger
        self.obframe_input = QLineEdit()
        self.obframe_input.setPlaceholderText(" ")
        self.obframe_input.setFixedWidth(30)

        #For MouthOpen - Blink
        self.oc_frame_input = QLineEdit()
        self.oc_frame_input.setPlaceholderText(" ")
        self.oc_frame_input.setFixedWidth(30)

        #For MouthOpen - Blink
        self.obc_frame_input = QLineEdit()
        self.obc_frame_input.setPlaceholderText(" ")
        self.obc_frame_input.setFixedWidth(30)

        # Action Button
        gen_button = QPushButton("Generate to Textbox and Copy it to Clipboard")
        gen_button.setStyleSheet("background-color: #2b5b84; color: white; font-weight: bold; padding: 5px;")
        gen_button.clicked.connect(self.handle_generation)

        # Status Label
        self.status_label = QLabel("Ready")

        # --- ROW 0: CB_SpeakDialgoue Setups ---
        speakdialogue_row = QHBoxLayout()
        speakdialogue_row.addWidget(QLabel("Dialogue Number 1:"))
        speakdialogue_row.addWidget(self.dnumber1_input)
        speakdialogue_row.addWidget(QLabel("Dialogue Number 2:"))
        speakdialogue_row.addWidget(self.dnumber2_input)
        speakdialogue_row.addWidget(self.isplayer_input)
        gen_layout.addLayout(speakdialogue_row)

        # --- THE HORIZONTAL SEPARATOR ---
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine) # Horizontal Line
        line.setFrameShadow(QFrame.Shadow.Sunken)
        gen_layout.addWidget(line)

        # --- ROW 1: Sprite Frames ---
        frame_row = QHBoxLayout()
        frame_row.addWidget(QLabel("Sprite frame name:"))
        frame_row.addWidget(self.frame_input)
        frame_row.addWidget(QLabel("Normal frame:"))
        frame_row.addWidget(self.nframe_input)
        frame_row.addWidget(QLabel("Blink frame:"))
        frame_row.addWidget(self.bframe_input)
        gen_layout.addLayout(frame_row)

        # --- ROW 2: Sprites Frame Part 2 ---
        frame_row2 = QHBoxLayout()
        frame_row2.addWidget(QLabel("Open Mouth frame:"))
        frame_row2.addWidget(self.oframe_input)
        frame_row2.addWidget(QLabel("Larger Open Mouth frame:"))
        frame_row2.addWidget(self.obframe_input)
        gen_layout.addLayout(frame_row2)

        # --- ROW 3: Sprites Frame Part 3 ---
        frame_row3 = QHBoxLayout()
        frame_row3.addWidget(QLabel("Open Mouth frame (Blink):"))
        frame_row3.addWidget(self.oc_frame_input)
        frame_row3.addWidget(QLabel("Larger Open Mouth frame (Blink):"))
        frame_row3.addWidget(self.obc_frame_input)
        gen_layout.addLayout(frame_row3)

        # --- THE HORIZONTAL SEPARATOR ---
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine) # Horizontal Line
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        gen_layout.addWidget(line2)

        # --- ROW 3: SECONDS ---
        seconds_row = QHBoxLayout()
        seconds_row.addWidget(QLabel("Seconds:"))
        seconds_row.addWidget(self.time_input)
        seconds_row.addWidget(QLabel("Target Label:"))
        seconds_row.addWidget(self.goto_input)
        gen_layout.addLayout(seconds_row)

        # --- ROW 4 & 5 & 6: Speaking Seconds ---
        analyze_var_row = QHBoxLayout()
        analyze_var_row.addWidget(QLabel("Audio Threshold [db (decibel)]:"))
        analyze_var_row.addWidget(self.threshold_input)
        analyze_var_row.addWidget(QLabel("Audio Window [milliseconds]:"))
        analyze_var_row.addWidget(self.window_input)
        gen_layout.addLayout(analyze_var_row)

        speaking_row = QHBoxLayout()
        speaking_row.addWidget(QLabel("Mouth Movements (Standard):   "))
        speaking_row.addWidget(self.mouthmove_input)
        gen_layout.addLayout(speaking_row)
        speaking_row2 = QHBoxLayout()
        speaking_row2.addWidget(QLabel("Mouth Movements (Unperiodic):"))
        speaking_row2.addWidget(self.mouthmove_input2)
        gen_layout.addLayout(speaking_row2)


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

        loadaudio_action = QAction("Load Audio File", self)
        loadaudio_action.triggered.connect(self.load_audio)
        file_toolbar.addAction(loadaudio_action)

    def _about(self):
        QMessageBox.about(self, "About", ABOUT)

    def create_menu(self):
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        new_action = QAction("New Document", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(lambda: self.textEdit.clear())
        file_menu.addAction(new_action)

        open_action = QAction("Open Document", self)
        open_action.triggered.connect(self.open_file)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)

        save_action = QAction("Save Document", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        about_act = help_menu.addAction("&About")
        about_act.triggered.connect(self._about)



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

    def load_audio(self):
        self.status_label.setText("Audio analysis for generating lip-sync animation can take times. Please wait!")
        audio_filepath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Ogg Audio File(ogg)(*.ogg);;All Audio Files(mp3, wav, ogg, flac) (*.mp3 *.wav *.ogg *.flac);;All Files (*)")
        try:
            if audio_filepath:
                audio = OggVorbis(audio_filepath)
                duration = float(audio.info.length)
                threshold = float(self.threshold_input.text())
                window = float(self.window_input.text()) * 0.001

                speak_list, unperiodic_list = audio_analyze.analyze_voice_segments(audio_filepath, threshold, window)

                self.mouthmove_input.setText(speak_list)
                self.mouthmove_input2.setText(unperiodic_list)
                self.time_input.setText(f"{duration:.2f}")
                self.status_label.setText("Audio analysis done!")
        except Exception as e:
            print(f"Error reading audio: {e}")
            self.status_label.setText(f"Error: {str(e)}")

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
                n_frame = self.nframe_input.text() or "A"
                b_frame = self.bframe_input.text() or n_frame
                oeframe = self.oframe_input.text() or n_frame
                obframe = self.obframe_input.text() or b_frame
                target = self.goto_input.text()
                secs = self.time_input.text()
                mouthmove = self.mouthmove_input.text()
                mouthmove_unperiodic = self.mouthmove_input2.text()
                isplayer = "false"

                if self.isplayer_input.isChecked():
                    print("isplayer_input is true")
                    isplayer = "true"


                if not target or not secs:
                    self.status_label.setText(f"Error: Fill the Goto Target and Seconds!")
                    print(f"Error: Fill the Goto Target and Seconds!")
                    return

                script = codegen.cb_speakdialogue(self.dnumber1_input.text(), self.dnumber2_input.text(), "Villy", "Very_Angry", isplayer)
                self.textEdit.insertPlainText(script)

                # Call the Logic
                script = codegen.generate_zscript(f_label, n_frame, b_frame, oeframe, obframe, target, secs, mouthmove, mouthmove_unperiodic)

                # Update GUI
                self.textEdit.insertPlainText(script)

            except Exception as e:
                self.status_label.setText(f"Error: {str(e)}")
                print(f"Error: {e}")
