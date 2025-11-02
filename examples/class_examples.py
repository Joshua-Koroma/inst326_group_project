from researchlib.digital_archives import Author, Document, Collection, ArchiveManager

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
