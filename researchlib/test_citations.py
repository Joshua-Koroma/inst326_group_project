import unittest
from researchlib_classes import (
    APACitationGenerator
)
from core_functions import (
    normalize_author_name,
    validate_isbn,
    sanitize_input,
    generate_citation
)

from typing import Dict, Any, List

class TestCoreFunctions(unittest.TestCase):

    def test_normalize_author_name(self):
        self.assertEqual(
            normalize_author_name("jane doe"),
            "Doe, Jane"
        )

        self.assertEqual(
            normalize_author_name("John Ronald Reuel Tolkien"),
            "Tolkien, John Ronald Reuel"
        )

    def test_validate_isbn_valid(self):
        self.assertTrue(validate_isbn("9780306406157"))
        self.assertTrue(validate_isbn("0306406152"))

    def test_validate_isbn_invalid(self):
        self.assertFalse(validate_isbn("abc123"))
        self.assertFalse(validate_isbn("123"))

    def test_sanitize_input(self):
        raw = 'Hello<script>alert("x")</script>'
        cleaned = sanitize_input(raw)
        self.assertNotIn("<", cleaned)
        self.assertNotIn(">", cleaned)


class TestGenerateCitationFunction(unittest.TestCase):

    def test_generate_apa_citation(self):
        metadata = {
            "author": "Doe, Jane",
            "title": "Test Title",
            "year": "2023"
        }

        citation = generate_citation(metadata, style="APA")
        self.assertEqual(
            citation,
            "Doe, Jane (2023). Test Title."
        )

    def test_generate_mla_citation(self):
        metadata = {
            "author": "Doe, Jane",
            "title": "Test Title",
            "year": "2023"
        }

        citation = generate_citation(metadata, style="MLA")
        self.assertEqual(
            citation,
            'Doe, Jane. "Test Title." 2023.'
        )

    def test_generate_invalid_style(self):
        metadata = {"author": "Doe", "title": "X", "year": "2020"}
        with self.assertRaises(ValueError):
            generate_citation(metadata, style="CHICAGO")


class TestAPACitationGenerator(unittest.TestCase):

    def setUp(self):
        self.valid_metadata = {
            "authors": ["Jane Doe", "John Smith"],
            "year": 2021,
            "title": "understanding widgets",
            "publisher": "Widget Press",
            "doi": "https://doi.org/10.1234/widget.2021"
        }

    def test_generator_output_structure(self):
        gen = APACitationGenerator(self.valid_metadata)
        result = gen.generate()

        self.assertIn("style", result)
        self.assertIn("citation", result)
        self.assertEqual(result["style"], "APA")

    def test_generator_citation_format(self):
        gen = APACitationGenerator(self.valid_metadata)
        citation = gen.generate()["citation"]

        self.assertTrue(citation.startswith("Doe, J., & Smith, J."))
        self.assertIn("(2021).", citation)
        self.assertIn("Understanding widgets.", citation)
        self.assertIn("Widget Press.", citation)
        self.assertIn("https://doi.org/10.1234/widget.2021", citation)

    def test_generator_no_authors(self):
        metadata = {
            "title": "Orphaned Work",
            "year": 1999
        }

        gen = APACitationGenerator(metadata)
        citation = gen.generate()["citation"]

        self.assertTrue(citation.startswith("Unknown Author"))

    def test_generator_invalid_metadata_type(self):
        with self.assertRaises(TypeError):
            APACitationGenerator("not a dict")

if __name__ == "__main__":
    unittest.main()