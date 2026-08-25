import os

from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field

SUPPORTED_EXTENSIONS = {"pdf", "docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    path: str = Field(
        description="Absolute or relative path to a PDF or DOCX file on disk to convert to markdown."
    ),
) -> str:
    """Reads a PDF or DOCX file from disk and converts its contents to markdown-formatted text.

    Use this tool when you have a filesystem path to a document (rather than
    already-loaded binary data) and want its contents as markdown. The file
    extension determines how the file is parsed, so it must end in '.pdf' or
    '.docx'.

    Raises:
        FileNotFoundError: if no file exists at the given path.
        ValueError: if the file's extension is not '.pdf' or '.docx'.

    Example:
        >>> document_path_to_markdown("/tmp/report.docx")
        '# Report\\n\\nThis is the report body...'
    """
    extension = os.path.splitext(path)[1].lstrip(".").lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '.{extension}' for '{path}'. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}."
        )

    with open(path, "rb") as f:
        binary_data = f.read()

    return binary_document_to_markdown(binary_data, extension)
