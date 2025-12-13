"""
Demo Script for ResearchLib
---------------------------
Demonstrates key functionalities of the researchlib package,
including data validation, search, citation generation,
database synchronization, and JSON export.
"""
import sys
import os
sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from researchlib.core_functions import (
    validate_isbn,
    normalize_author_name,
    generate_unique_id,
    sanitize_input,
    format_date,
    parse_metadata,
    search_documents,
    generate_citation,
    validate_research_entry,
    export_to_json,
    merge_databases,
    index_research_by_keyword,
    generate_universal_record,
    retrieve_citations
)

# ----------------------------
# STEP 1: Basic utility demos
# ----------------------------

print("=== Utility Function Demos ===")

isbn = "978-0135166307"
print(f"Validating ISBN {isbn}: {validate_isbn(isbn)}")

author_name = "john doe"
print(f"Normalized author name: {normalize_author_name(author_name)}")

unique_id = generate_unique_id("BOOK")
print(f"Generated unique ID: {unique_id}")

unsafe_input = "<script>alert('XSS');</script>"
print(f"Sanitized input: {sanitize_input(unsafe_input)}")

formatted_date = format_date("03/15/2025")
print(f"Formatted date: {formatted_date}")

print("\n")

# ----------------------------
# STEP 2: Metadata and validation
# ----------------------------

print("=== Metadata and Validation Demos ===")

raw_metadata = """
title: AI Research
author: Alice Brown
year: 2024
identifier: 9780135166307
"""

metadata = parse_metadata(raw_metadata)
print("Parsed metadata:", metadata)

# Validate the metadata as a research entry
validate_research_entry(metadata)
print("Research entry is valid.")

# ----------------------------
# STEP 3: Citation generation
# ----------------------------

print("\n=== Citation Generation ===")

apa_citation = generate_citation(metadata, "APA")
mla_citation = generate_citation(metadata, "MLA")

print("APA:", apa_citation)
print("MLA:", mla_citation)

print("\n=== Retrieve Citations from our savefile. ===")
retrieve_citations()

# ----------------------------
# STEP 4: Search documents
# ----------------------------

print("\n=== Search Documents ===")

documents = [
    {"title": "AI Research", "abstract": "Study on neural architectures", "identifier": "9780135166307"},
    {"title": "Quantum Computing", "abstract": "Qubit theory basics", "identifier": "9780321765615"},
    {"title": "Ethics in AI", "abstract": "Social implications of ML", "identifier": "9780201616224"}
]

results = search_documents("ai", documents)
print(f"Search results for 'ai': {[doc['title'] for doc in results]}")

# ----------------------------
# STEP 5: Synchronize databases
# ----------------------------

print("\n=== Database Synchronization ===")

local_db = [
    {"identifier": "9780135166307", "last_updated": "2025-01-01", "title": "AI Research"},
    {"identifier": "9780321765615", "last_updated": "2025-02-01", "title": "Quantum Computing"}
]

remote_db = [
    {"identifier": "9780135166307", "last_updated": "2025-03-15", "title": "AI Research - Revised"},
    {"identifier": "9780201616224", "last_updated": "2025-02-10", "title": "Ethics in AI"}
]

merged = merge_databases(local_db, remote_db)
print("Merged database:")
for entry in merged:
    print(f"- {entry['identifier']}: {entry['title']} (Updated {entry.get('last_updated')})")

# ----------------------------
# STEP 6: Keyword indexing
# ----------------------------

print("\n=== Keyword Index ===")
index = index_research_by_keyword(documents)
print(f"Keywords indexed: {len(index)} total")
print(f"Documents for keyword 'quantum': {index.get('quantum', [])}")

# ----------------------------
# STEP 7: Generate a universal record
# ----------------------------

print("\n=== Universal Record ===")

raw_record = {
    "name": "AI in 2025",
    "author": "jane smith",
    "publication_date": "2025",
    "abstract": "Trends in AI research and applications"
}

universal = generate_universal_record(raw_record)
print("Universal record:")
for key, val in universal.items():
    print(f"  {key}: {val}")

# ----------------------------
# STEP 8: Export results to JSON
# ----------------------------

print("\n=== Export to JSON ===")
export_to_json(merged, "merged_research.json")
print("Exported merged database to 'merged_research.json' successfully!")

print("\nDemo completed successfully.")
