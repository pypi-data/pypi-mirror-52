

# anki_ocr_gui

anki_ocr_gui is a PyQt5 gui for the CLI tool [anki_ocr](https://github.com/madelesi/anki_ocr/)

anki_ocr is a python program that converts physical flashcards into digital [Anki](https://apps.ankiweb.net)(Anki is a flashcard program that sychronizes your flashcards and uses spaced repetition for efficient memorization) decks. It uses [PyTesseract](https://pypi.org/project/pytesseract/) and [genanki](https://github.com/kerrickstaley/genanki) to turn your handwritten flashcards into digital anki ones.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install anki_ocr_gui.

```bash
pip install anki_ocr_gui
```

## Usage
To use anki_ocr, you will need a directory with images of your flashcards. The program will automatically sort the images by date, so you should **capture the question followed by its answer, and ensure the number of images is even**
(i.e question1>answer1>question2>answer2 and so on)

```bash
anki_ocr_gui
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)