
---

## Class References for ResearchLib

Explain the purpose and relationship of each class:

```markdown
# Class Design Document

## Overview

The Digital Archives system models the research library domain using object-oriented principles.
Each class encapsulates related data and behavior, supporting scalability and reuse.

---

### 1. Author
- **Responsibility**: Represents a single author entity.
- **Attributes**: `_name`, `_orcid`
- **Key Methods**:
  - `to_dict()`
  - name normalization via `normalize_author_name()`

---

### 2. Document
- **Responsibility**: Core metadata unit.
- **Integrates**: `validate_isbn()`, `generate_citation()`, `generate_universal_record()`, etc.
- **Key Methods**:
  - `validate()`
  - `generate_citation(style="APA")`
  - `to_universal_record()`
  - `add_keyword()`

---

### 3. Collection
- **Responsibility**: Container of Documents.
- **Integrates**: `search_documents()`, `merge_databases()`, `export_to_json()`
- **Relationships**:
  - Contains multiple `Document` instances.
- **Key Methods**:
  - `add_document()`
  - `search()`
  - `merge_with()`

---

### 4. Indexer
- **Responsibility**: Build and query inverted keyword indexes.
- **Integrates**: `index_research_by_keyword()`
- **Key Methods**:
  - `from_collection()`
  - `search_keyword()`

---

### 5. ArchiveManager
- **Responsibility**: High-level, manage collections and coordinate indexing.
- **Integrates**: `merge_databases()`, `generate_universal_record()`
- **Key Methods**:
  - `build_global_index()`
  - `merge_collections()`
  - `export_archive()`

---

