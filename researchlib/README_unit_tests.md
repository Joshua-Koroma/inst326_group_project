# ResearchLib Unit Tests

This module contains unit tests for the core citation and validation utilities used in the **ResearchLib** project. The tests are written using Python’s built-in `unittest` framework and verify correct behavior for citation generation, input validation, and metadata handling.

---

## Tested Components

These tests cover functionality from the following modules:

### `core_functions`
- `normalize_author_name`
- `validate_isbn`
- `sanitize_input`
- `generate_citation`

### `researchlib_classes`
- `APACitationGenerator`

---

## Test Coverage Overview

### Core Function Tests (`TestCoreFunctions`)
- **Author name normalization**
  - Converts names into *Last, First* format
- **ISBN validation**
  - Accepts valid ISBN-10 and ISBN-13 formats
  - Rejects malformed or invalid ISBNs
- **Input sanitization**
  - Removes potentially unsafe characters (e.g., HTML tags)

### Citation Generation Tests (`TestGenerateCitationFunction`)
- **APA citation formatting**
- **MLA citation formatting**
- **Invalid citation style handling**
  - Ensures unsupported styles raise a `ValueError`

### APA Citation Generator Tests (`TestAPACitationGenerator`)
- **Output structure**
  - Confirms returned object contains `style` and `citation`
- **Citation formatting**
  - Verifies authors, year, title capitalization, publisher, and DOI
- **Missing author handling**
  - Defaults to `"Unknown Author"` when no authors are provided
- **Input validation**
  - Raises `TypeError` when metadata is not a dictionary

---

## Running the Tests

Make sure you are in the project root directory and that all required modules are importable.

### Run all tests:
```bash
python -m unittest test_filename.py
```

Or run directly:
```bash
python test_filename.py
```

Replace `test_filename.py` with the actual name of the test file.

---

## Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

---

## Notes

- These tests assume deterministic citation formatting.
- If citation styles or formatting rules change, expected values in the tests must be updated accordingly.
- The test file can be safely extended to include additional citation styles or validation logic.

---
