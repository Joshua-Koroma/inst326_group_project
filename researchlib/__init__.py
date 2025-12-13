"""
Research Library Core Utilities
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

This package provides foundational tools for managing and merging research data
for libraries across institutions. It includes utilities for:

  - Metadata parsing and validation
  - Citation generation
  - Database merging/indexing
  - Record normalization
  
  These functions serve as the basic layer toward higher-level components and
  database integrations within a universal library system.

  Authors:  Joshua-Koroma, Steven Ulloa, Ahmed Baghdadi: UMD INST326
  Version: 1.0.0
  """

from .core_functions import(
    # --- Simple Utility Functions ---
    validate_isbn, normalize_author_name, generate_unique_i, sanitize_input, format_date,

    # --- Medium Complexity Functions ---
    parse_metadata, search_documents, generate_citation, validate_research_entry, export_to_json,

    # --- Complex Functions ---
    merge_databases, index_research_by_keyword, generate_universal_record

  )

_all_ = [
    # Simple
    "validate_isbn", "normalize_author_name", "generate_unique_id", "sanitize_input", "format_date",

    # Medium
    "parse_metadata", "search_documents", "generate_citation", "validate_research_entry", "export_to_json",

    # Complex
    "merge_databases", "index_research_by_keyword", "generate_universal_record"
]

# Package Metadata
__version__ = "1.0.5"
__authors__ = "Joshua Koroma, Ahmed Baghdadi, Steven Ulloa : UMD INST326"
__description__ = "A foundational function library for universal research and library data management."

