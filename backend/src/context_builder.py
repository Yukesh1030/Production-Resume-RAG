import re


def detect_document_type(document: str) -> str:
    """
    Identify the general type of information contained
    in a retrieved resume chunk.
    """

    text = document.lower()

    if "real-time chat application" in text:
        return "PROJECT"

    if "ration shop management system" in text:
        return "PROJECT"

    if "software engineering projects" in text:
        return "PROJECT"

    if "internship" in text:
        return "EXPERIENCE"

    if "technical skills" in text:
        return "SKILLS"

    if "achievements" in text:
        return "ACHIEVEMENT"

    if "education" in text:
        return "EDUCATION"

    return "GENERAL"


def extract_project_names(document: str) -> list:
    """
    Extract explicitly mentioned project names from
    a retrieved document.
    """

    project_names = []

    patterns = [
        r"Real[-‐-‒–—―]Time Chat Application",
        r"Full[-‐-‒–—―]Stack Ration Shop Management System",
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            document,
            flags=re.IGNORECASE
        )

        for match in matches:

            normalized = re.sub(
                r"[-‐-‒–—―]",
                "-",
                match
            )

            if normalized not in project_names:
                project_names.append(normalized)

    return project_names


def build_context(results):
    """
    Build structured context for the LLM.

    Retrieved documents are grouped by information type.
    Project-related documents are explicitly identified so
    that list questions such as "What projects..." are less
    likely to omit a lower-ranked project.
    """

    context_parts = []

    project_documents = []
    other_documents = []

    for index, result in enumerate(results, start=1):

        document = result.get(
            "document",
            ""
        )

        document_type = detect_document_type(
            document
        )

        project_names = extract_project_names(
            document
        )

        structured_document = f"""
DOCUMENT {index}
----------------
TYPE: {document_type}
ID: {result.get("id", "unknown")}
RANK: {result.get("rank", index)}
SCORE: {result.get("score", "unknown")}

EXPLICIT PROJECTS IN THIS DOCUMENT:
{", ".join(project_names) if project_names else "None"}

CONTENT:
{document}
"""

        if document_type == "PROJECT" or project_names:
            project_documents.append(
                structured_document
            )
        else:
            other_documents.append(
                structured_document
            )

    # --------------------------------------------------------
    # Put project evidence first.
    # --------------------------------------------------------

    if project_documents:

        context_parts.append(
            """
IMPORTANT PROJECT EVIDENCE
==========================
The following retrieved documents contain explicitly
identified project information.

When the user asks about projects, inspect ALL of these
documents and include every distinct project explicitly
supported by the evidence.
"""
        )

        context_parts.extend(
            project_documents
        )

    # --------------------------------------------------------
    # Add remaining retrieved documents.
    # --------------------------------------------------------

    if other_documents:

        context_parts.append(
            """
OTHER RETRIEVED RESUME EVIDENCE
================================
"""
        )

        context_parts.extend(
            other_documents
        )

    return "\n".join(context_parts)