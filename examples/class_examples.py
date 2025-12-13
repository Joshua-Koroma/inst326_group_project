import json
import sys
import os
sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from researchlib.researchlib_classes import Author, Document, Collection, ArchiveManager, APACitationGenerator

# Create author and document
author = Author("Ada Lovelace")
doc = Document("Analytical Engine Notes", author.name, year="1843")

# Store in a collection
collection = Collection("Early Computing")
collection.add_document(doc)

# Build and export
collection.export("computing_collection.json")

# Manage via ArchiveManager
manager = ArchiveManager()
manager.add_collection(collection)
print(manager.list_collections())

# Import/Export Citations in APA Format
input_json = {
    "authors": ["Jane Doe", "John Smith"],
    "year": 2021,
    "title": "understanding widgets",
    "publisher": "Widget Press",
    "doi": "https://doi.org/10.1234/widget.2021"
}
generator = APACitationGenerator(input_json)
output_json = generator.generate()
print(json.dumps(output_json, indent=4))
