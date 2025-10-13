## Utility Functions

### `validate_isbn(isbn: str) -> bool`
Validates ISBN-10 or ISBN-13 format.

**Args:**
- `isbn`: ISBN string to validate.

**Returns:** `bool` — `True` if valid, otherwise `False`.

**Raises:** `ValueError` if input is empty.

**Example:**
```python
validate_isbn("978-0135166307")  # True
```
---

### `normalize_author_name(name: str) -> str`
Converts author names into standardized “Last, First” format.

**Example:**
```python
normalize_author_name("john doe")  # "Doe, John"
```
---

### `generate_unique_id(prefix: str = "DOC") -> str`
Generates a unique 10-character identifier.

**Example:**
```python
generate_unique_id("BOOK")  # "BOOK-A12B3C4D5E"
```
---

### `sanitize_input(data: str) -> str`
Removes unsafe characters from user input.

**Example:**
```python
sanitize_input("<script>alert('XSS')</script>")
# "scriptalertXSSscript"
```
---

### `format_date(date_str: str) -> str`
Formats a date string into ISO format (`YYYY-MM-DD`).

**Example:**
```python
format_date("03/15/2021")  # "2021-03-15"
```
---

## Metadata and Search Functions

### `parse_metadata(record: str) -> Dict[str, Any]`
Parses JSON or “key: value” formatted strings into a dictionary.

**Example:**
```python
parse_metadata('{"title": "AI Research", "year": 2024}')
```
---

### `search_documents(query, documents, fields=None)`
Searches documents for a keyword across given fields.

**Example:**
```python
search_documents("quantum", docs, ["title", "abstract"])
```
---

### `generate_citation(metadata, style="APA")`
Generates a formatted citation in APA or MLA style.

**Example:**
```python
generate_citation({"author": "Doe, J.", "title": "AI Ethics", "year": "2023"}, "MLA")
```
---

### `validate_research_entry(entry)`
Validates that a research entry includes all required fields and a valid ISBN.

**Example:**
```python
validate_research_entry({
    "title": "AI Research", "author": "John Doe",
    "year": "2023", "identifier": "9780135166307"
})
```
---

### `export_to_json(data, filepath)`
Exports Python data as JSON to a specified file path.

**Example:**
```python
export_to_json(library_data, "output.json")
```
---

## Advanced Functions

### `merge_databases(local_db, remote_db)`
Merges local and remote databases with conflict resolution by latest update.

**Example:**
```python
merged = merge_databases(local_data, remote_data)
```
---

### `index_research_by_keyword(documents)`
Creates a keyword-to-document index for fast lookups.

**Example:**
```python
index = index_research_by_keyword(documents)
index["quantum"]
```
---

### `generate_universal_record(record)`
Converts arbitrary metadata into a standard library-compatible format.

**Example:**
```python
record = generate_universal_record({"name": "AI in 2025", "author": "Jane Smith"})
```
