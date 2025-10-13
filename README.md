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

## Installation & Setup

### Option 1 — Local use

Clone or download the repository:

```bash
git clone https://github.com/yourusername/researchlib.git
cd researchlib

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

You can run the demo directly:

python demo_script.py

Option 2 — Editable install (recommended for development)

pip install -e .

Then you can use it anywhere:

from researchlib import search_documents, generate_citation


