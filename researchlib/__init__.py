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

  Authors:  Joshua-Koroma, Steven Ulloa: UMD INST326
  Version: 1.0.0
  """

from .core_functions import(
    # --- Simple Utility Functions ---
    validate_isbn,
    #..., etc, etc,

    # --- Medium Complexity Functions ---

    # --- Complex Functions ---
    merge_databases

  )

_all_ = [
    # Simple
    "validate_isbn",
    #..., ..., ..., etc.

    # Medium

    # Complex
    "merge_databases" #,
]

# Package Metadata
__version__ = "1.0.0"
__authors__ = "..., ..., Steven Ulloa : UMD INST326"
__description__ = "A foundational function library for universal research and library data management."

