"""researchlib_classes.py
Depends on the provided utility functions.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Optional


# ----- Functions assumed available in the namespace -----
# validate_isbn, normalize_author_name, generate_unique_id,
# sanitize_input, format_date, parse_metadata, search_documents,
# generate_citation, validate_research_entry, export_to_json,
# merge_databases, index_research_by_keyword, generate_universal_record

# -----------------------
# Domain classes
# -----------------------

class Author:
    """
    Representation of an author.

    Encapsulates author name normalization and lightweight metadata.

    Example:
        >>> a = Author("jane doe")
        >>> str(a)
        'Author: Doe, Jane'
        >>> a.to_dict()
        {'name': 'Doe, Jane', 'orcid': None}
    """
    def __init__(self, name: str, orcid: Optional[str] = None):
        if not name or not isinstance(name, str):
            raise ValueError("Author name must be a non-empty string.")
        self._name = normalize_author_name(name)
        self._orcid = sanitize_input(orcid) if orcid else None

    # properties
    @property
    def name(self) -> str:
        """Normalized name in 'Last, First' form."""
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Author name must be a non-empty string.")
        self._name = normalize_author_name(value)

    @property
    def orcid(self) -> Optional[str]:
        return self._orcid

    @orcid.setter
    def orcid(self, value: Optional[str]):
        self._orcid = sanitize_input(value) if value else None

    def to_dict(self) -> Dict[str, Optional[str]]:
        """Return a serializable representation."""
        return {"name": self._name, "orcid": self._orcid}

    def __str__(self) -> str:
        return f"Author: {self._name}"

    def __repr__(self) -> str:
        return f"Author(name={self._name!r}, orcid={self._orcid!r})"

class BaseAuthor(ABC):
    """Interface for all author-like objects in the library."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the normalized author name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def orcid(self) -> Optional[str]:
        """Return the ORCID identifier or None."""
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> Dict[str, Optional[str]]:
        """Return a JSON-serializable dictionary of this author."""
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """Return a readable representation."""
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Return representation (for debugging)."""
        raise NotImplementedError



class Document(BaseDocument):
    """
    Representation of a research document / archival item.

    - Encapsulates metadata and provides common behaviours:
      validation, citation generation, conversion to a universal record.

    Example:
        >>> doc = Document(title="On Widgets", author="Jane Doe", identifier="1234567890", year="2020")
        >>> doc.generate_citation()  # uses APA by default
        'Doe, Jane (2020). On Widgets.'
        >>> doc.to_universal_record()['author']
        'Doe, Jane'
    """
    def __init__(self,
                 title: str,
                 author: str,
                 identifier: Optional[str] = None,
                 year: Optional[str] = None,
                 abstract: Optional[str] = None,
                 keywords: Optional[List[str]] = None):
        # Basic validation & sanitization
        if not title or not isinstance(title, str):
            raise ValueError("title must be a non-empty string.")
        if not author or not isinstance(author, str):
            raise ValueError("author must be a non-empty string.")

        self._title = sanitize_input(title)
        self._author = normalize_author_name(author)
        # allow missing identifier -> generate one
        self._identifier = identifier if identifier else generate_unique_id(prefix="DOC")
        self._year = str(year) if year is not None else "n.d."
        self._abstract = sanitize_input(abstract) if abstract else ""
        self._keywords = keywords or []
        self._last_updated = datetime.now().strftime("%Y-%m-%d")

        # attempt to validate identifier if it looks like an ISBN
        # but do not force ISBN -- Validate_research_entry expects identifier in entry
        try:
            # call validate_isbn only if identifier looks numeric or contains hyphens
            if self._identifier and any(ch.isdigit() for ch in self._identifier):
                validate_isbn(self._identifier)
        except Exception:
            # don't raise here: not all identifiers are ISBNs; keep the identifier
            pass

    # properties + encapsulation
    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("title must be a non-empty string.")
        self._title = sanitize_input(value)
        self._touch()

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("author must be a non-empty string.")
        self._author = normalize_author_name(value)
        self._touch()

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("identifier must be a non-empty string.")
        self._identifier = sanitize_input(value)
        self._touch()

    @property
    def year(self) -> str:
        return self._year

    @year.setter
    def year(self, value: str):
        if value is None:
            self._year = "n.d."
        else:
            self._year = str(value)
        self._touch()

    @property
    def abstract(self) -> str:
        return self._abstract

    @abstract.setter
    def abstract(self, value: str):
        self._abstract = sanitize_input(value or "")
        self._touch()

    @property
    def keywords(self) -> List[str]:
        return list(self._keywords)

    def add_keyword(self, kw: str):
        if not kw or not isinstance(kw, str):
            raise ValueError("keyword must be a non-empty string.")
        k = sanitize_input(kw).lower()
        if k not in self._keywords:
            self._keywords.append(k)
            self._touch()

    def remove_keyword(self, kw: str):
        k = sanitize_input(kw).lower()
        if k in self._keywords:
            self._keywords.remove(k)
            self._touch()

    @property
    def last_updated(self) -> str:
        return self._last_updated

    # private helper
    def _touch(self):
        self._last_updated = datetime.now().strftime("%Y-%m-%d")

    # instance methods integrating functions
    def to_universal_record(self) -> Dict[str, Any]:
        """
        Convert the document into a universal record using generate_universal_record().
        Returns a dict that conforms to the universal record mapping.
        """
        record = {
            "title": self._title,
            "author": self._author,
            "year": self._year,
            "identifier": self._identifier,
            "keywords": self._keywords,
            "abstract": self._abstract,
            "last_updated": self._last_updated,
        }
        return generate_universal_record(record)

    def validate(self) -> bool:
        """
        Validate the document according to validate_research_entry().
        Raises ValueError if invalid; returns True if valid.
        """
        entry = {
            "title": self._title,
            "author": self._author,
            "year": self._year,
            "identifier": self._identifier,
        }
        return validate_research_entry(entry)

    def generate_citation(self, style: str = "APA") -> str:
        """
        Generate a citation string for the document using generate_citation().
        """
        metadata = {"author": self._author, "title": self._title, "year": self._year}
        return generate_citation(metadata, style=style)

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable dict representation of this Document."""
        return {
            "title": self._title,
            "author": self._author,
            "identifier": self._identifier,
            "year": self._year,
            "abstract": self._abstract,
            "keywords": self._keywords,
            "last_updated": self._last_updated,
        }

    def __str__(self) -> str:
        return f"{self._title} — {self._author} ({self._year})"

    def __repr__(self) -> str:
        return (f"Document(title={self._title!r}, author={self._author!r}, "
                f"identifier={self._identifier!r}, year={self._year!r})")


class BaseDocument(ABC):
    """
    Abstract interface for all document-like objects in the library.
    Ensures consistent metadata behavior and interoperability.
    """

    # ----- Required metadata properties -----

    @property
    @abstractmethod
    def title(self) -> str:
        """Return the normalized title."""
        raise NotImplementedError

    @property
    @abstractmethod
    def author(self) -> str:
        """Return the normalized author name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def identifier(self) -> str:
        """Return the unique identifier."""
        raise NotImplementedError

    @property
    @abstractmethod
    def year(self) -> str:
        """Return the publication year (or 'n.d.')."""
        raise NotImplementedError

    @property
    @abstractmethod
    def keywords(self) -> List[str]:
        """Return list of keywords."""
        raise NotImplementedError

    # ----- Required core behaviors -----

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation."""
        raise NotImplementedError

    @abstractmethod
    def generate_citation(self, style: str = "APA") -> str:
        """Generate a citation string."""
        raise NotImplementedError

    @abstractmethod
    def to_universal_record(self) -> Dict[str, Any]:
        """Return a universal record mapping."""
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> bool:
        """Validate the document and return True if valid."""
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """readable representation."""
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Debug representation."""
        raise NotImplementedError


class Collection(BaseCollection):
    """
    A named collection of Documents.

    Responsibilities:
    - Hold documents
    - Search within collection
    - Export collection metadata

    Example:
        >>> c = Collection("Medieval Manuscripts")
        >>> d = Document("Treatise", "John Smith", identifier="9780306406157", year="2001")
        >>> c.add_document(d)
        >>> c.find_by_identifier("9780306406157") is d
        True
    """
    def __init__(self, name: str, description: Optional[str] = None):
        if not name or not isinstance(name, str):
            raise ValueError("Collection name must be a non-empty string.")
        self._name = sanitize_input(name)
        self._description = sanitize_input(description) if description else ""
        self._documents: Dict[str, Document] = {}  # keyed by identifier
        self._created = datetime.now().strftime("%Y-%m-%d")

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def size(self) -> int:
        return len(self._documents)

    def add_document(self, doc: Document):
        """Add a Document to the collection. Overwrites if identifier exists."""
        if not isinstance(doc, Document):
            raise TypeError("add_document expects a Document instance.")
        self._documents[doc.identifier] = doc

    def remove_document(self, identifier: str) -> Optional[Document]:
        """Remove and return a document by identifier, or None if missing."""
        return self._documents.pop(identifier, None)

    def list_documents(self) -> List[Document]:
        return list(self._documents.values())

    def find_by_identifier(self, identifier: str) -> Optional[Document]:
        return self._documents.get(identifier)

    def search(self, query: str, fields: Optional[List[str]] = None) -> List[Document]:
        """
        Search documents within this collection using the search_documents function.
        Returns Document instances that match.
        """
        # convert documents to dicts for the search function
        docs_as_dicts = [d.to_dict() for d in self._documents.values()]
        matches = search_documents(query, docs_as_dicts, fields=fields)
        found_ids = {m["identifier"] for m in matches}
        return [self._documents[i] for i in found_ids if i in self._documents]

    def export(self, filepath: str):
        """Export the collection as a JSON array of document dicts using export_to_json()."""
        data = {
            "collection": self._name,
            "description": self._description,
            "created": self._created,
            "documents": [d.to_dict() for d in self._documents.values()]
        }
        export_to_json(data, filepath)

    def merge_with(self, other: "Collection"):
        """
        Merge another Collection into this one, preferring documents with the latest last_updated.
        Uses merge_databases on dict representations.
        """
        if not isinstance(other, Collection):
            raise TypeError("merge_with expects another Collection.")
        local_db = [d.to_dict() for d in self._documents.values()]
        remote_db = [d.to_dict() for d in other._documents.values()]
        merged = merge_databases(local_db, remote_db)
        # rebuild _documents from merged list
        self._documents = {item["identifier"]: Document(
            title=item["title"],
            author=item["author"],
            identifier=item["identifier"],
            year=item.get("year", "n.d."),
            abstract=item.get("abstract", ""),
            keywords=item.get("keywords", [])
        ) for item in merged}

    def __str__(self) -> str:
        return f"Collection: {self._name} ({self.size} documents)"

    def __repr__(self) -> str:
        return f"Collection(name={self._name!r}, size={self.size})"

class BaseCollection(ABC):
    """
    Abstract interface for document collections.
    Ensures consistent behavior and interoperability across collection types.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the collection name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """Return the collection description."""
        raise NotImplementedError

    @property
    @abstractmethod
    def size(self) -> int:
        """Return the number of documents in the collection."""
        raise NotImplementedError

    @abstractmethod
    def add_document(self, doc) -> None:
        """Add a document to the collection."""
        raise NotImplementedError

    @abstractmethod
    def remove_document(self, identifier: str):
        """Remove and return a document by identifier."""
        raise NotImplementedError

    @abstractmethod
    def list_documents(self) -> List:
        """Return all documents in the collection."""
        raise NotImplementedError

    @abstractmethod
    def find_by_identifier(self, identifier: str):
        """Find a document by its identifier."""
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str, fields: Optional[List[str]] = None) -> List:
        """Search within the collection."""
        raise NotImplementedError

    @abstractmethod
    def export(self, filepath: str) -> None:
        """Export the collection to a JSON file."""
        raise NotImplementedError

    @abstractmethod
    def merge_with(self, other: "BaseCollection") -> None:
        """Merge another collection into this one."""
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """Human-readable representation."""
        raise NotImplementedError

class BaseIndexer(ABC):
    """
    Abstract interface for indexers used to map keywords to document identifiers.
    Ensures consistent search behavior and interoperability.
    """

    @property
    @abstractmethod
    def index(self) -> Dict[str, List[str]]:
        """Return the keyword → identifiers mapping."""
        raise NotImplementedError

    @abstractmethod
    def search_keyword(self, keyword: str) -> List[str]:
        """Return a list of identifiers matching the given keyword."""
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable representation."""
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Return a debugging representation."""
        raise NotImplementedError


class Indexer(BaseIndexer):
    """
    Build and query a simple inverted index of Documents.

    - Uses index_research_by_keyword() internally.
    - Provides keyword -> identifiers mapping and a convenience search method.

    Example:
        >>> c = Collection("Test")
        >>> d1 = Document("The Blue Book", "Alice A", identifier="ID-1", abstract="blue book about art")
        >>> d2 = Document("Red Guide", "Bob B", identifier="ID-2", abstract="red guide to cooking")
        >>> c.add_document(d1); c.add_document(d2)
        >>> idx = Indexer.from_collection(c)
        >>> 'blue' in idx.index
        True
        >>> idx.search_keyword('blue')
        ['ID-1']
    """
   def __init__(self, index: Optional[Dict[str, List[str]]] = None):
        self._index = index or {}

    @property
    def index(self) -> Dict[str, List[str]]:
        # return a shallow copy for safety
        return dict(self._index)

    @classmethod
    def from_documents(cls, documents: List[Document]) -> "Indexer":
        docs = [d.to_dict() for d in documents]
        idx = index_research_by_keyword(docs)
        return cls(index=idx)

    @classmethod
    def from_collection(cls, collection: Collection) -> "Indexer":
        return cls.from_documents(collection.list_documents())

    def search_keyword(self, keyword: str) -> List[str]:
        if not keyword or not isinstance(keyword, str):
            raise ValueError("keyword must be a non-empty string.")
        return self._index.get(keyword.lower(), [])

    def add_document(self, doc: Document):
        # tokenize doc and update index (simple approach: rebuild entry tokens)
        # For simplicity and correctness, rebuild index for affected words
        docs = []
        # collect all documents by identifiers
        identifiers = set()
        for kw, ids in self._index.items():
            identifiers.update(ids)
        # add current doc to a fake documents list and rebuild full index
        # Real systems would incrementally update; here we rebuild externally
        # Note: callers usually call from_collection/from_documents after major changes
        raise NotImplementedError("Incremental add not implemented; rebuild index via from_collection/from_documents.")

    def __str__(self) -> str:
        return f"Indexer({len(self._index)} terms)"

    def __repr__(self) -> str:
        return f"Indexer(index_terms={len(self._index)})"

class BaseArchiveManager(ABC):
    """Abstract interface for archive manager components."""

    @abstractmethod
    def add_collection(self, collection: Collection):
        raise NotImplementedError

    @abstractmethod
    def remove_collection(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def list_collections(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def build_global_index(self) -> BaseIndexer:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError


class ArchiveManager(BaseArchiveManager):
    """
    Manager / façade for collections and documents. Coordinates:
      - Collections
      - Indexer creation
      - Bulk import / export
      - Merge operations

    Example:
        >>> am = ArchiveManager()
        >>> col = Collection("Main")
        >>> am.add_collection(col)
        >>> am.list_collections()
        ['Main']
    """
     def __init__(self):
        self._collections: Dict[str, Collection] = {}
        self._global_index: Optional[Indexer] = None

    def add_collection(self, collection: Collection):
        if not isinstance(collection, Collection):
            raise TypeError("add_collection expects a Collection instance.")
        if collection.name in self._collections:
            raise ValueError(f"A collection named {collection.name!r} already exists.")
        self._collections[collection.name] = collection
        self._global_index = None  # mark index stale

    def remove_collection(self, name: str) -> Optional[Collection]:
        col = self._collections.pop(name, None)
        if col:
            self._global_index = None
        return col

    def list_collections(self) -> List[str]:
        return list(self._collections.keys())

    def get_collection(self, name: str) -> Optional[Collection]:
        return self._collections.get(name)

    def build_global_index(self) -> Indexer:
        # build an index across all documents in all collections
        all_docs = []
        for col in self._collections.values():
            all_docs.extend(col.list_documents())
        self._global_index = Indexer.from_documents(all_docs)
        return self._global_index

    def find_document(self, identifier: str) -> Optional[Document]:
        for col in self._collections.values():
            doc = col.find_by_identifier(identifier)
            if doc:
                return doc
        return None

    def import_records(self, records: List[Dict[str, Any]], collection_name: str):
        """
        Import a list of raw records (dicts) into a named collection.
        Each record is converted to a Document via generate_universal_record mapping.
        """
        if collection_name not in self._collections:
            self._collections[collection_name] = Collection(collection_name)
        col = self._collections[collection_name]
        for rec in records:
            uni = generate_universal_record(rec)
            doc = Document(
                title=uni["title"],
                author=uni["author"],
                identifier=uni["identifier"],
                year=uni.get("year", "n.d."),
                abstract=uni.get("abstract", ""),
                keywords=uni.get("keywords", [])
            )
            col.add_document(doc)
        self._global_index = None

    def export_archive(self, filepath: str):
        """
        Export the entire archive as JSON with collections and documents.
        """
        data = {
            "exported_at": datetime.now().strftime("%Y-%m-%d"),
            "collections": {
                name: {
                    "description": col.description,
                    "created": getattr(col, "_created", ""),
                    "documents": [d.to_dict() for d in col.list_documents()]
                }
                for name, col in self._collections.items()
            }
        }
        export_to_json(data, filepath)

    def merge_collections(self, target: str, source: str):
        """
        Merge source collection into target collection using Collection.merge_with.
        """
        if target not in self._collections or source not in self._collections:
            raise ValueError("Both target and source collections must exist.")
        self._collections[target].merge_with(self._collections[source])
        self._global_index = None

    def __str__(self) -> str:
        return f"ArchiveManager({len(self._collections)} collections)"

    def __repr__(self) -> str:
        return f"ArchiveManager(collections={list(self._collections.keys())!r})"

class BaseMember(ABC):
    """Abstract interface for all library members."""

    @property
    @abstractmethod
    def card_id(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def block(self):
        """Block the member."""
        raise NotImplementedError

    @abstractmethod
    def unblock(self):
        """Unblock the member."""
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Return serializable representation."""
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

class Member(BaseMember):
    """
    Library member profile. Minimal PII
    """
    VALID_TYPES = {"student", "faculty", "staff", "guest"}
    VALID_STATUS = {"active", "blocked", "expired"}

    def __init__(self, name: str, email: str, member_type: str = "student",
                 card_id: Optional[str] = None, status: str = "active"):
        if not name or not isinstance(name, str):
            raise ValueError("Member name must be a non-empty string.")
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string.")

        self._name = sanitize_input(name)
        self._email = sanitize_input(email)
        self._type = member_type if member_type in self.VALID_TYPES else "student"
        self._status = status if status in self.VALID_STATUS else "active"
        self._card_id = card_id if card_id else generate_unique_id(prefix="CARD")
        self._registered = datetime.now().strftime("%Y-%m-%d")
        self._stats = {"checkouts": 0, "overdues": 0, "fines_outstanding": 0.0}

    @property
    def card_id(self) -> str:
        return self._card_id

    @property
    def status(self) -> str:
        return self._status

    @property
    def member_type(self) -> str:
        return self._type

    def block(self):
        """temporarily disable member’s privs."""
        self._status = "blocked"

    def unblock(self):
        """reinstate member’s privs."""
        self._status = "active"

    def to_dict(self) -> Dict[str, Any]:
        """return a JSON ready representation of this member."""
        return {
            "name": self._name,
            "email": self._email,
            "type": self._type,
            "status": self._status,
            "card_id": self._card_id,
            "registered": self._registered,
            "stats": self._stats,
        }

    def __str__(self):
        return f"Member: {self._name} ({self._type}) – {self._status}"

    def __repr__(self):
        return (f"Member(name={self._name!r}, email={self._email!r}, "
                f"type={self._type!r}, status={self._status!r})")
