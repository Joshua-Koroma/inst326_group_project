import re
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

# -=-=-=-=-=-=-=-=-=-=-=-
# SIMPLE UTILITY FUNCTIONS
# =-=-=-=-=-=-=-=-=-=-=-=

def validate_isbn(isbn: str) -> bool:
    """
    Validate if the given string is a valid ISBN-10 or ISBN-13 format.

    Args:
        isbn (str): The ISBN string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not isbn:
        raise TypeError("ISBN cannot be empty and must be a string.")
    isbn_clean = isbn.replace("-", "").strip()
    if len(isbn_clean) == 10 and isbn_clean[:-1].isdigit():
        return True
    if len(isbn_clean) == 13 and isbn_clean.isdigit():
        return True
    return False
    
def normalize_author_name(name: str) -> str:
    """
    Standardize an author’s name into 'Last, First' format.

    Args:
        name (str): Author name, possibly in various formats.

    Returns:
        str: Standardized name in 'Last, First' format.
    """
    if not name:
        raise ValueError("Author name cannot be empty.")
    parts = name.strip().split()
    if len(parts) < 2:
        return name.title()
    return f"{parts[-1].title()}, {' '.join(p.title() for p in parts[:-1])}"

def generate_unique_id(prefix: str = "DOC") -> str:
    """
    Generate a unique identifier for a document or record.

    Args:
        prefix (str): Optional prefix for ID (default 'DOC').

    Returns:
        str: Unique ID string.
    """
    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"


# -=-=-=-=-=-=-=-=-=-=-=-
# MEDIUM UTILITY FUNCTIONS
# =-=-=-=-=-=-=-=-=-=-=-=

# -=-=-=-=-=-=-=-=-=-=-=-
# COMPLEX FUNCTIONS
# =-=-=-=-=-=-=-=-=-=-=-=

def merge_databases(local_db: List[Dict[str, Any]], remote_db: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    merge two research library databases by merging unique entries and resolving conflicts.

    Args:
        local_db (list): Local database entries.
        remote_db (list): Remote database entries.

    Returns:
        list: Merged and synchronized database.
    """
    merged = {item["identifier"]: item for item in local_db}
    for remote_item in remote_db:
        identifier = remote_item.get("identifier")
        if not identifier:
            continue
        if identifier not in merged:
            merged[identifier] = remote_item
        else:
            # Conflict resolution: prefer latest update
            local_time = merged[identifier].get("last_updated", "1970-01-01")
            remote_time = remote_item.get("last_updated", "1970-01-01")
            if remote_time > local_time:
                merged[identifier] = remote_item
    return list(merged.values())

def index_research_by_keyword(documents: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Create an inverted index of documents by keyword to optimize search.

    Args:
        documents (list): List of research documents.

    Returns:
        dict: Mapping of keywords to document identifiers.
    """
    index = {}
    for doc in documents:
        text_content = f"{doc.get('title', '')} {doc.get('abstract', '')}".lower()
        words = re.findall(r"\b[a-z]{3,}\b", text_content)
        for word in set(words):
            index.setdefault(word, []).append(doc.get("identifier"))
    return index

def generate_universal_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a standardized universal record compatible with other library systems.

    Args:
        record (dict): Original record with arbitrary metadata keys.

    Returns:
        dict: Normalized universal record structure.
    """
    mapping = {
        "title": record.get("title") or record.get("name"),
        "author": normalize_author_name(record.get("author", "Unknown")),
        "year": record.get("year") or record.get("publication_date", "n.d."),
        "identifier": record.get("identifier") or generate_unique_id(),
        "keywords": record.get("keywords", []),
        "abstract": record.get("abstract", ""),
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
    }
    if not mapping["title"] or not mapping["identifier"]:
        raise ValueError("Record must contain a valid title and identifier.")
    return mapping
