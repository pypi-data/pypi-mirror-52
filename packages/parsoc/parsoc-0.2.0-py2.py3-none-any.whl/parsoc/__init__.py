"""Core module of the project."""

from datetime import datetime

from docx import Document  # type: ignore


def _listmap(func, coll):
    """Map item in coll with func."""
    return list(map(func, coll))


def _timestamp_or_none(time):
    """Return a timestamp or None."""
    if time:
        return datetime.timestamp(time)

    return None


def parse_properties(properties):
    """Parse the core properties of a document."""
    return {
        "author": properties.author,
        "category": properties.category,
        "comments": properties.comments,
        "content_status": properties.content_status,
        "created": _timestamp_or_none(properties.created),
        "identifier": properties.identifier,
        "keywords": properties.keywords,
        "language": properties.language,
        "last_modified_by": properties.last_modified_by,
        "last_printed": _timestamp_or_none(properties.last_printed),
        "modified": _timestamp_or_none(properties.modified),
        "revision": properties.revision,
        "subject": properties.subject,
        "title": properties.title,
        "version": properties.version,
    }


def parse_paragraph(paragraph):
    """Parse a paragraph of a document."""
    return paragraph.text


def parse_table(table):
    """Parse a table of a document."""
    lines = []

    for row in table.rows:
        line = []

        for cell in row.cells:
            line.append(cell.text)

        lines.append(line)

    return lines


def parse_document(document) -> dict:
    """Parse the content of a document."""
    return {
        "tables": _listmap(parse_table, document.tables),
        "properties": parse_properties(document.core_properties),
        "paragraphs": _listmap(parse_paragraph, document.paragraphs),
    }
