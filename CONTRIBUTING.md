# Contributing to OpenSAK

Thank you for your interest in contributing! Here is how to get involved.

---

## Reporting Bugs

Please use [GitHub Issues](https://github.com/AgreeDK/opensak/issues) and include:

- Platform and version (e.g. "Linux Mint 21.3" or "Windows 11")
- Python version (`python3 --version`)
- What you were trying to do
- The error message from the terminal (if any)

Issues in Danish are also welcome — the project was created in Denmark and Danish bug reports are perfectly fine.

---

## Suggesting Features

Open a GitHub Issue with the label **enhancement** and describe what you would like and why. Screenshots or mockups are very helpful.

---

## Contributing Code

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run the test suite: `pytest -v tests/`
5. Commit with a clear message: `git commit -m "Add: description of change"`
6. Push: `git push origin feature/my-feature`
7. Open a Pull Request

Please keep pull requests focused — one feature or fix per PR makes review much easier.

---

## Development Setup

```bash
git clone https://github.com/AgreeDK/opensak.git
cd opensak
python3 -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows
pip install -r requirements.txt
pytest -v tests/                   # run tests
python run.py                      # start the application
```

---

## Adding a Translation

Want to translate OpenSAK into a new language? It only takes one file:

1. Copy `src/opensak/lang/en.py` to e.g. `src/opensak/lang/de.py`
2. Translate the string values on the right-hand side — **do not change the keys**
3. Register the language in `src/opensak/lang/__init__.py`:
   ```python
   AVAILABLE_LANGUAGES = {
       "da": "Dansk",
       "en": "English",
       "de": "Deutsch",   # ← add this line
   }
   ```
4. Test by selecting the new language in **Tools → Settings** and restarting
5. Open a Pull Request — all translations are warmly welcomed!

The language files contain around 220 strings. A rough machine translation that a native speaker then reviews is a perfectly good starting point.

---

## Code Style

- Python 3.10+, PySide6 for the GUI
- Use `pathlib.Path` for all file paths (cross-platform)
- Background work runs in `QThread` subclasses — never block the main thread
- All user-visible strings go through `tr("key")` from `opensak.lang`
- New UI strings need a matching key in both `lang/da.py` and `lang/en.py`

---

## Running the Tests

```bash
pytest -v tests/
```

The test suite covers the database layer, importer and filter engine (63 tests total). New features should include tests where practical.

---

## Questions?

Open an issue or start a discussion on GitHub. Contributions of any size are welcome — from fixing a typo to adding a whole new feature.
