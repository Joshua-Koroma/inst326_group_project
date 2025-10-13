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

def sanitize_input(data: str) -> str:
    """
    Remove potentially unsafe characters from user-provided strings.

    Args:
        data (str): Input string.

    Returns:
        str: Sanitized string.
    """

    if not isinstance(data, str):
        raise TypeError("Expected a string for input data.")
    
    blacklist = '<>"\'%;()&+'
    return ''.join(c for c in data if c not in blacklist).strip()

def format_date(date_str: str) -> str:
    date_str = "2025-10-12"

    dt = datetime.striptime(date_str, "%Y-%m-%d")

    iso_date = dt.date().isoformat()

    return iso_date

    """
    Args:
        date_str (str): Date string in various common formats.

    Returns:
        str: Date in ISO format (YYYY-MM-DD).
    """
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Date format not recognized. Use MM/DD/YYYY or YYYY-MM-DD.")

# -=-=-=-=-=-=-=-=-=-=-=-
# MEDIUM UTILITY FUNCTIONS
# =-=-=-=-=-=-=-=-=-=-=-=

def parse_metadata(record: str) -> Dict[str, Any]: 

    if not record:
        raise ValueError("Metadata record cannot be empty.")
    try:
      return json.loads(record)
    except json.JSONDecodeError:
      metadata = {}

      lines = record.strip().splitlines()

      for line in lines:
        if not line.strip():
          continue
        parts = line.split(":", 1)
        if len(parts) == 2:
          key, value = parts
          metadata[key.strip()] = value.strip()
    return metadata

    """
    Parse metadata from a JSON or key-value formatted string.

    Args:
        record (str): Metadata string, JSON or "key: value" pairs.

    Returns:
        dict: Parsed metadata dictionary.
    """


def search_documents(query: str, documents: List[Dict[str, Any]], fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Search documents for a query string across specified fields.

    Args:
        query (str): Search query.
        documents (list): List of document dictionaries.
        fields (list, optional): Specific fields to search in.

    Returns:
        list: Filtered list of matching documents.
    """
    query = query.lower().strip()
    if not query:
        raise ValueError("Search query cannot be empty.")

    results = []
    for doc in documents:
        search_fields = fields or doc.keys()
        for f in search_fields:
            val = str(doc.get(f, "")).lower()
            if query in val:
                results.append(doc)
                break
    return results


def generate_citation(metadata: Dict[str, Any], style: str = "APA") -> str:
    """
    Generate a formatted citation string based on metadata.

    Args:
        metadata (dict): Document metadata (author, title, year, etc.).
        style (str): Citation style ('APA', 'MLA', etc.).

    Returns:
        str: Formatted citation string.
    """
    author = metadata.get("author") or "Unknown Author"
    title = metadata.get("title") or "Untitled"
    year = metadata.get("year") or "n.d."

    style = style.upper()

    if style == "APA":
        return f"{author} ({year}). {title}."
    elif style == "MLA":
        return f'{author}. "{title}." {year}.'
    else:
        raise ValueError(f"Unsupported citation style: {style}")



def validate_research_entry(entry: Dict[str, Any]) -> bool:
    """
    Validate a research entry to ensure required fields exist and have the correct formats.

    Args:
        entry (dict): Research entry metadata.

    Returns:
        bool: True if entry is valid, raises ValueError otherwise.
    """
    required_fields = ["title", "author", "year", "identifier"]
    for field in required_fields:
        if field not in entry or not entry[field]:
            raise ValueError(f"Missing or empty required field: {field}")
    if not validate_isbn(entry.get("identifier", "")):
        raise ValueError("Invalid ISBN/Identifier format.")
    return True


def export_to_json(data: Any, filepath: str) -> None:
    """
    Export data to a JSON file.

    Args:
        data (Any): Data to export.
        filepath (str): File path to save JSON.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise IOError(f"Failed to export data to {filepath}: {e}")


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
