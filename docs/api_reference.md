# API Reference

This API Reference lists all public classes and methods provided in the the researchlib classes module.

---

## `Author`

### Attributes
| Name | Type | Description |
|------|------|-------------|
| `name` | str | Full name of the author |
| `affiliation` | str | Organization or institution |
| `email` | str | Contact email address |

### Methods
| Name | Signature | Description |
|------|------------|-------------|
| `__init__(name, affiliation, email)` | Constructor |
| `to_dict()` | Converts author details to a dictionary |
| `__repr__()` | Returns formatted string representation |

---

## `Document`

### Attributes
| Name | Type | Description |
|------|------|-------------|
| `title` | str | Title of the document |
| `authors` | list[Author] | List of authors |
| `year` | int | Year of publication |
| `keywords` | list[str] | Tags or keywords |
| `content` | str | Full content or abstract |

### Methods
| Name | Signature | Description |
|------|------------|-------------|
| `__init__(title, authors, year, keywords, content)` | Constructor |
| `summary()` | Returns first few lines of text |
| `add_author(author)` | Adds an author to the list |
| `matches_keyword(keyword)` | Returns True if keyword is found |

---

## `Collection`

### Attributes
| Name | Type | Description |
|------|------|-------------|
| `name` | str | Name of the collection |
| `documents` | list[Document] | List of contained documents |

### Methods
| Name | Signature | Description |
|------|------------|-------------|
| `add_document(document)` | Adds a document |
| `remove_document(title)` | Removes a document by title |
| `search_by_keyword(keyword)` | Returns list of matching documents |
| `list_authors()` | Returns all unique authors |
| `export_to_json(filepath)` | Saves collection to JSON |

---

## `Indexer`

### Attributes
| Name | Type | Description |
|------|------|-------------|
| `index` | dict[str, list[Document]] | Keyword-based index |

### Methods
| Name | Signature | Description |
|------|------------|-------------|
| `build_index(collection)` | Builds index from given collection |
| `search(keyword)` | Retrieves matching documents |

---

## `ArchiveManager`

### Attributes
| Name | Type | Description |
|------|------|-------------|
| `collections` | dict[str, Collection] | Registered collections |

### Methods
| Name | Signature | Description |
|------|------------|-------------|
| `add_collection(collection)` | Adds a new collection |
| `get_collection(name)` | Retrieves collection by name |
| `merge_collections(name1, name2, merged_name)` | Combines two collections |
| `export_all(path)` | Exports all collections |
