import os
import pytest
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self) -> None:
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_document_path_to_markdown_with_docx(self) -> None:
        """Test converting a DOCX document to markdown given its path."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_document_path_to_markdown_with_pdf(self) -> None:
        """Test converting a PDF document to markdown given its path."""
        result = document_path_to_markdown(self.PDF_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_matches_binary_document_to_markdown(self) -> None:
        """Path-based conversion should match binary-based conversion for the same file."""
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        path_result = document_path_to_markdown(self.DOCX_FIXTURE)
        binary_result = binary_document_to_markdown(docx_data, "docx")

        assert path_result == binary_result

    def test_unsupported_extension_raises(self, tmp_path: "os.PathLike[str]") -> None:
        """An unsupported file extension should raise a clear error."""
        unsupported_file = os.path.join(tmp_path, "notes.txt")
        with open(unsupported_file, "w") as f:
            f.write("plain text, not a real document")

        with pytest.raises(Exception):
            document_path_to_markdown(unsupported_file)

    def test_nonexistent_path_raises_file_not_found(self) -> None:
        """A path that doesn't exist should raise FileNotFoundError."""
        missing_path = os.path.join(self.FIXTURES_DIR, "does_not_exist.pdf")

        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(missing_path)

    def test_return_type_is_str(self) -> None:
        """Result should always be a plain str, not e.g. bytes or a wrapper object."""
        result = document_path_to_markdown(self.PDF_FIXTURE)

        assert type(result) is str
