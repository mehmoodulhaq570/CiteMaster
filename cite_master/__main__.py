from .extract_doi import get_doi_from_title, process_file
from .fetch_bibtex import fetch_bibtex_from_doi
from .formatter import format_citation

def main():
    user_input = input("Enter a paper title or provide a file path (txt/csv): ").strip()
    citation_format = input("Enter citation format (apa, mla, ieee): ").strip().lower()
    include_bibtex = input("Do you want the BibTeX citation as well? (yes/no): ").strip().lower()
    
    if user_input.endswith(".txt") or user_input.endswith(".csv"):
        results = process_multiple_titles(user_input, citation_format, include_bibtex)
        for title, data in results.items():
            print(f"\nTitle: {title}\nFormatted Citation ({citation_format.upper()}):\n{data['citation']}\n")
            if include_bibtex == "yes":
                print(f"BibTeX:\n{data['bibtex']}\n")
    else:
        formatted_citation, bibtex = process_single_title(user_input, citation_format, include_bibtex)
        print(f"\nFormatted Citation ({citation_format.upper()}):\n{formatted_citation}\n")
        if include_bibtex == "yes":
            print(f"BibTeX:\n{bibtex}\n")

def process_single_title(title, citation_format="apa", include_bibtex="no"):
    """Processes a single paper title, fetches DOI, BibTeX, and formats the citation."""
    doi = get_doi_from_title(title)
    if doi:
        bibtex = fetch_bibtex_from_doi(doi)
        formatted_citation = format_citation(bibtex, citation_format)
        return formatted_citation, bibtex if include_bibtex == "yes" else ""
    return "DOI not found.", ""

def process_multiple_titles(file_path, citation_format="apa", include_bibtex="no"):
    """Processes a file containing multiple paper titles."""
    dois = process_file(file_path)
    results = {}
    for title, doi in dois.items():
        if doi:
            bibtex = fetch_bibtex_from_doi(doi)
            formatted_citation = format_citation(bibtex, citation_format)
            results[title] = {"citation": formatted_citation, "bibtex": bibtex if include_bibtex == "yes" else ""}
        else:
            results[title] = {"citation": "DOI not found.", "bibtex": ""}
    return results

if __name__ == "__main__":
    main()
