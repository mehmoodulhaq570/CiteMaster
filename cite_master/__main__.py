from .extract_doi import get_doi_from_title, process_file
from .fetch_bibtex import fetch_bibtex_from_doi
from .formatter import format_citation

def main():
    user_input = input("Enter a paper title or provide a file path (txt/csv): ").strip()
    if not user_input:
        print("\n⚠️ No input provided. Please enter a paper title or file path.")
        return

    citation_format = input("Enter citation format (apa, mla, ieee): ").strip().lower()
    if citation_format not in ["apa", "mla", "ieee"]:
        print("\n⚠️ Invalid citation format. Please choose from: apa, mla, ieee.")
        return

    include_bibtex = input("Do you want the BibTeX citation as well? (yes/no): ").strip().lower()
    if include_bibtex not in ["yes", "no"]:
        print("\n⚠️ Please enter 'yes' or 'no' for the BibTeX option.")
        return

    if user_input.endswith(".txt") or user_input.endswith(".csv"):
        save_bibtex_to_file = "no"
        if include_bibtex == "yes":
            save_bibtex_to_file = input("Do you want to save all BibTeX entries to a file (bibtex_output.txt)? (yes/no): ").strip().lower()
            if save_bibtex_to_file not in ["yes", "no"]:
                print("\n⚠️ Please enter 'yes' or 'no' to save BibTeX entries.")
                return

        results = process_multiple_titles(user_input, citation_format, include_bibtex)

        all_bibtex_entries = []
        for title, data in results.items():
            print(f"\nTitle: {title}\n📚 Citation ({citation_format.upper()}):\n{data['citation']}\n")
            if include_bibtex == "yes" and data['bibtex']:
                print(f"BibTeX:\n{data['bibtex']}\n")
                all_bibtex_entries.append(data['bibtex'])

        if include_bibtex == "yes" and save_bibtex_to_file == "yes" and all_bibtex_entries:
            with open("bibtex_output.txt", "w", encoding="utf-8") as f:
                f.write("\n\n".join(all_bibtex_entries))
            print("\n✅ BibTeX entries saved to bibtex_output.txt")

    else:
        formatted_citation, bibtex = process_single_title(user_input, citation_format, include_bibtex)
        print(f"\nCitation ({citation_format.upper()}):\n{formatted_citation}\n")
        if include_bibtex == "yes" and bibtex:
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
