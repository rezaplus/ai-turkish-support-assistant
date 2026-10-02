from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class ParsedSection:
    title: str
    content: str


@dataclass
class ParsedDocument:
    filename: str
    title: str
    version: int
    status: str
    effective_date: date
    sections: list[ParsedSection]


def parse_markdown_document(file_path: Path) -> ParsedDocument:
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = ""
    version = 1
    status = "active"
    effective_date = None

    sections: list[ParsedSection] = []
    current_section = None
    current_content: list[str] = []

    for line in lines:
        line = line.strip()

        if line.startswith("# "):
            title = line[2:].strip()

        elif line.startswith("Version:"):
            version = int(line.split(":", 1)[1].strip())

        elif line.startswith("Status:"):
            status = line.split(":", 1)[1].strip()

        elif line.startswith("Effective-Date:"):
            value = line.split(":", 1)[1].strip()
            effective_date = date.fromisoformat(value)

        elif line.startswith("## "):
            if current_section:
                sections.append(
                    ParsedSection(
                        title=current_section,
                        content="\n".join(current_content).strip(),
                    )
                )

            current_section = line[3:].strip()
            current_content = []

        elif current_section and line:
            current_content.append(line)

    if current_section:
        sections.append(
            ParsedSection(
                title=current_section,
                content="\n".join(current_content).strip(),
            )
        )

    if not title:
        raise ValueError(f"Missing title: {file_path}")

    if effective_date is None:
        raise ValueError(f"Missing Effective-Date: {file_path}")

    return ParsedDocument(
        filename=file_path.name,
        title=title,
        version=version,
        status=status,
        effective_date=effective_date,
        sections=sections,
    )