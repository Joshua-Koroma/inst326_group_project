# Class Design Document

## Overview
This document describes the object-oriented design for the **Archives Management System** implemented in the `researchlib` module.

The system models research documents, authors, and collections, and provides indexing and archival management through several cooperating classes.

---

## Class Diagram (Conceptual)

```
Author ──┐
         │
         ▼
Document ───► Collection ───► ArchiveManager
                    │
                    ▼
                 Indexer
```

---

## Class Descriptions

### `Author`
**Purpose:** Represents an author of one or more research documents.  
**Key Attributes:**
- `name` (str): Full name of the author.
- `affiliation` (str): Organization or institution.
- `email` (str): Contact information.
**Key Methods:**
- `__repr__()`: Returns a string representation.
- `to_dict()`: Converts to a dictionary for serialization.

---

### `Document`
**Purpose:** Represents a research paper, report, or article.  
**Key Attributes:**
- `title` (str)
- `authors` (list[Author])
- `year` (int)
- `keywords` (list[str])
- `content` (str)
**Key Methods:**
- `summary()`: Returns first few lines of content.
- `add_author(author)`: Adds an Author instance.
- `matches_keyword(keyword)`: Boolean check for keyword presence.

---

### `Collection`
**Purpose:** Organizes multiple `Document` objects.  
**Key Attributes:**
- `name` (str)
- `documents` (list[Document])
**Key Methods:**
- `add_document(document)`
- `remove_document(title)`
- `search_by_keyword(keyword)`
- `list_authors()`
- `export_to_json(filepath)`

---

### `Indexer`
**Purpose:** Builds a keyword-based index for fast lookup of documents.  
**Key Attributes:**
- `index` (dict[str, list[Document]]) – keyword → list of documents
**Key Methods:**
- `build_index(collection)`
- `search(keyword)`

---

### `ArchiveManager`
**Purpose:** High-level interface for managing multiple `Collection` instances.  
**Key Attributes:**
- `collections` (dict[str, Collection])
**Key Methods:**
- `add_collection(collection)`
- `get_collection(name)`
- `merge_collections(name1, name2, merged_name)`
- `export_all(path)`

---

## Design Rationale

- **Encapsulation:** Each class manages its own state.
- **Composition:** `Document` uses `Author`; `Collection` aggregates `Document`; `ArchiveManager` aggregates `Collection`.
- **Scalability:** New features like metadata search or database export can extend `ArchiveManager`.
- **Reusability:** Each component can be used standalone for testing or separate projects.

---

## Example Usage

```python
from researchlib.digital_archives import Author, Document, Collection, ArchiveManager

a1 = Author("Dr. Jane Doe", "Onett", "jane@example.com")
d1 = Document(ONETT", [a1], 2024, ["AI", "ML"], "This paper explores...")
collection = Collection("Research Papers")
collection.add_document(d1)

archive = ArchiveManager()
archive.add_collection(collection)
archive.export_all("output/")
```

---
