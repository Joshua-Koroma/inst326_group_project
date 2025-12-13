import json
import sys
import os
sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from researchlib.researchlib_classes import Author, Document, Collection, ArchiveManager, APACitationGenerator
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
# Simple presentation of possible function using the researchlib python package
user_collection = Collection("Personal Collection")
while (True):
    print("Enter your command here (Type 'help' for a list of commands!)")
    user_input = input()
    if user_input == "help":
        print("citations: views your saved citations \ndocuments: adds a document to your current collection \ncollection: views your current collection \nquit: quit's the program.")
    elif user_input == "citations":
        retrieve_citations()
    elif user_input == "documents":
        print("Enter the Author's name: ")
        author_name = input()
        author = Author(author_name)
        print("Enter the document's title: ")
        doc_name = input()
        print("Enter the year the document was published: ")
        input_year = input()
        print("Generating Document...")
        doc = Document(doc_name, author.name, year=input_year)
        doc.generate_citation()
        user_collection.add_document(doc)
        print("Document succesfully added to your Personal Collection. (Hint, Check your updated list of citations!)")
    elif user_input == "collection":
        print(user_collection.list_documents())
    elif user_input == "quit":
        break
    else:
        print("Invalid command!")