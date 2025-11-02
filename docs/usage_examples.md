## Add and Validate Research Entries
```python
from researchlib import validate_research_entry, generate_unique_id

entry = {
    "title": "Neural Network Advances",
    "author": "Alice Brown",
    "year": "2024",
    "identifier": "9780135166307"
}

validate_research_entry(entry)
dataset_id = generate_unique_id("DATA")
print(dataset_id)
```

## Search Documents
```python
from researchlib import search_documents

docs = [
    {"title": "AI Ethics", "abstract": "Explores fairness in ML systems", "identifier": "9780135166307"},
    {"title": "Quantum Computing 101", "abstract": "An introduction to qubits", "identifier": "9780321765615"}
]

results = search_documents("quantum", docs)
for r in results:
    print(r["title"])
```

## Generate and Export Citations
```python
from researchlib import generate_citation, export_to_json

metadata = {"author": "Brown, Alice", "title": "AI Research Ethics", "year": "2025"}
citation = generate_citation(metadata, "APA")

print(citation)
export_to_json({"citation": citation}, "citation_output.json")
```

## Merge Two Databases
```python
from researchlib import merge_databases

local = [{"identifier": "9780135166307", "last_updated": "2025-01-01"}]
remote = [{"identifier": "9780135166307", "last_updated": "2025-04-01"}]

merged_db = merge_databases(local, remote)
print(merged_db)
```

## Create a Keyword Index
```python
from researchlib import index_research_by_keyword

docs = [
    {"title": "Quantum Systems", "abstract": "Quantum computing applications", "identifier": "DOC-001"},
    {"title": "Machine Learning", "abstract": "AI and data science", "identifier": "DOC-002"},
]

index = index_research_by_keyword(docs)
print(index["quantum"])  # ['DOC-001']
```

## Normalize and Generate Universal Records
```python
from researchlib import generate_universal_record

record = {
    "name": "AI Foundations",
    "author": "john doe",
    "publication_date": "2023",
    "abstract": "Foundational AI theories"
}

standard = generate_universal_record(record)
print(standard)
```

---

## Class Examples


```python
"""
Demonstration of core classes.
Run with: python examples/demo_script.py
"""

from researchlib.digital_archives import Author, Document, Collection, ArchiveManager

def main():
    # Create an author and document
    author = Author("Jane Doe", orcid="0000-0002-1234-5678")
    doc = Document(
        title="Librarianship in the Digital Age",
        author=author.name,
        identifier="9780306406157",
        year="2021",
        abstract="A discussion of digital transformation in archives."
    )
    doc.add_keyword("digital")
    doc.add_keyword("archives")

    # Create a collection and add the document
    collection = Collection("Modern Library Science", "Research papers on digital archiving.")
    collection.add_document(doc)

    # Export collection
    collection.export("examples/modern_library.json")

    # Use ArchiveManager
    manager = ArchiveManager()
    manager.add_collection(collection)
    manager.build_global_index()

    print("Collections:", manager.list_collections())
    print("Citation:", doc.generate_citation())
    print("Universal Record:", doc.to_universal_record())

if __name__ == "__main__":
    main()
