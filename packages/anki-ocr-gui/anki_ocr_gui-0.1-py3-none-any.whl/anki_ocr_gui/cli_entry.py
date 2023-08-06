from . import anki_ocr_gui
import sys


def main():
    app = anki_ocr_gui.QApplication(sys.argv)
    Window = anki_ocr_gui.Window()
    app.exec_()
