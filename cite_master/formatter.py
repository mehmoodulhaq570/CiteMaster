import bibtexparser
from .exceptions import CitationFormatError, setup_logging

logger = setup_logging()

def format_citation(bibtex, style="apa"):
    """Formats a BibTeX citation into APA, MLA, or IEEE style."""
    bib_database = bibtexparser.loads(bibtex)
    entry = bib_database.entries[0]

    authors = entry.get("author", "Unknown Author").replace(" and ", " & ") if style.lower() == "apa" else entry.get("author", "Unknown Author").replace(" and ", ", ")
    title = entry.get("title", "Unknown Title")
    journal = entry.get("journal", "Unknown Journal")
    year = entry.get("year", "Unknown Year")
    volume = entry.get("volume", "")
    issue = entry.get("number", "")
    pages = entry.get("pages", "")
    doi = entry.get("doi", "")

    if style.lower() == "apa":
        return f"{authors} ({year}). {title}. *{journal}*, *{volume}*({issue}), {pages}. https://doi.org/{doi}"

    elif style.lower() == "mla":
        return f"{authors}. \"{title}.\" *{journal}*, vol. {volume}, no. {issue}, {year}, pp. {pages}. https://doi.org/{doi}."

    elif style.lower() == "ieee":
        author_list = authors.split(", ")
        formatted_authors = []
        
        # Format authors correctly with initials before last names
        for author in author_list:
            name_parts = author.split()
            if len(name_parts) >= 2:
                initials = " ".join([name[0] + "." for name in name_parts[:-1]])
                formatted_authors.append(f"{initials} {name_parts[-1]}")
            else:
                formatted_authors.append(author)

        # Handle "and" before the last author
        if len(formatted_authors) > 1:
            formatted_authors_str = ', '.join(formatted_authors[:-1]) + ", and " + formatted_authors[-1]
        else:
            formatted_authors_str = formatted_authors[0]

        # Page formatting for IEEE
        page_prefix = "p." if "-" not in pages else "pp."
        doi_text = f", doi: {doi}" if doi else ""

        return f"{formatted_authors_str}, \"{title},\" *{journal}*, vol. {volume}, no. {issue}, {page_prefix} {pages}, {year}{doi_text}."

    logger.error(f"Invalid citation style requested: {style}")
    raise CitationFormatError(style)


# Example Usage
# sample_bibtex = """
# @article{Smith2023,
#   author = {Smith, J. and Doe, A.},
#   title = {AI in Climate Change Research},
#   journal = {Nature},
#   volume = {32},
#   number = {4},
#   pages = {123-130},
#   year = {2023},
#   doi = {10.1111/1758-5899.70003}
# }
# """

# print("\nAPA Citation:")
# print(format_citation(sample_bibtex, "apa"))

# print("\nMLA Citation:")
# print(format_citation(sample_bibtex, "mla"))

# print("\nIEEE Citation:")
# print(format_citation(sample_bibtex, "ieee"))
