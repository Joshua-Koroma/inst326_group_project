# inst326_group_project
Your README must include: (DELETE WHEN DONE)

- Project title and description
- Team member names and roles
- Domain focus and problem statement
- Installation and setup instructions
- Usage examples for key functions
- Function library overview and organization
- Contribution guidelines for team members


# researchlib — Research Library Management Toolkit

`researchlib` is a lightweight Python package designed to support academic and digital library management tasks. It provides clean, well-structured utilities for validating research data, managing bibliographic metadata, generating unique record identifiers, and exporting or synchronizing datasets between systems.

This package is part of the **Function Library Project (INST326)**, focusing on encapsulation and data validation principles.


## Team Members & Roles

| Name | Role | Responsibilities |
|------|------|------------------|
| Steven Ulloa | Lead Developer | Core library structure, documentation, and examples |
| Joshua Koroma| Data Validation Specialist | Implementation of validation utilities |
| Ahmed | Quality Assurance | Testing, debugging, and code review |


## Domain Focus & Problem Statement

Modern library systems rely on consistent data structures for tracking publications, citations, and digital library content. However, such systems often lack a simple, modular backend that validates and manages core research data consistently.

**Problem:**  
Institutions need a lightweight, extensible toolkit to handle:
- ISBN and metadata validation  
- Research entry consistency  
- Keyword-based document indexing  
- JSON export and citation generation  

**Goal:**  
`researchlib` solves this by providing a Python module that cleanly separates logic into reusable components. This module is meant to serve as a very simple universal basis, one that allows existing library systems to adapt and adopt this module.

## ⚙️ Installation & Setup

### Option 1 — Local use

Clone or download the repository:

```bash
git clone https://github.com/yourusername/researchlib.git
cd researchlib
```

Make sure the structure looks like this:

```
Make sure the structure looks like this:

inst326_group_project/
│
├── researchlib/
│   ├── __init__.py
│   └── core_functions.py
│
├── examples/
|   └── demo_script.py
|
├──docs/
|  ├── README.md
|  ├── function_reference.md
|  └── usage_examples.md
```

You can run the demo directly:
```bash
python demo_script.py
```

### Option 2 — Editable install (recommended for development)

```bash
pip install -e .
```

Then you can use it anywhere:

```python
from researchlib import search_documents, generate_citation
```

---

## Usage Examples

Here are quick examples of how to use key functions.

```python
from researchlib import (
    validate_isbn,
    normalize_author_name,
    search_documents,
    generate_citation,
    export_to_json,
)

# Validate an ISBN
print(validate_isbn("978-3-16-148410-0"))  # True

# Normalize author name
print(normalize_author_name("DOE, JANE"))  # -> "Jane Doe"

# Search documents by keyword
results = search_documents("machine learning")
print(results)

# Generate formatted citation
citation = generate_citation("Jane Doe", "AI Research", "2025")
print(citation)

# Export research data
export_to_json(results, "output/research_data.json")
```

See [`usage_examples.md`](./usage_examples.md) for more in-depth examples.

---

---

## Library Structure

| Module | Description |
|---------|--------------|
| **`core_function.py`** | Implements main validation, search, and data processing functions |
| **`__init__.py`** | Exposes public API for top-level imports |
| **`demo_script.py`** | Sample runnable demonstration of all core functions |

Each module is self-contained and follows encapsulation principles with private attributes where appropriate.

---

---

## 🤝 Contribution Guidelines

Team members should follow these steps when contributing:

1. **Follow consistent naming conventions** for files and functions (snake_case).

2. **Document your code**:
   - Use docstrings for every function and class.
   - Update [`function_reference.md`](./function_reference.md) after adding or modifying functions.

3. **Test locally** before committing:
   ```bash
   python demo_script.py
   ```

4. **Submit a pull request (PR)** with a clear summary of changes.

---
