import os
import logging
from tqdm import tqdm
from .extract_doi import get_doi_from_title, process_file
from .fetch_bibtex import fetch_bibtex_from_doi
from .formatter import format_citation

# Setup logging
logging.basicConfig(filename="errors.log", level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Output directory
os.makedirs("outputs", exist_ok=True)

def main():
    print("📚 Welcome to CiteMaster: Paper Citation Formatter!\n")
    user_input = input("Enter a paper title or provide a file path (txt/csv): ").strip()

    citation_format = input("Enter citation format (apa, mla, ieee): ").strip().lower()
    while citation_format not in ["apa", "mla", "ieee"]:
        citation_format = input("Invalid format. Please enter 'apa', 'mla', or 'ieee': ").strip().lower()

    include_bibtex = input("Do you want the BibTeX citation as well? (yes/no): ").strip().lower()

    if user_input.endswith(".txt") or user_input.endswith(".csv"):
        save_citations_to_file = input("Do you want to save formatted citations to outputs/citations_output.txt? (yes/no): ").strip().lower()
        save_bibtex_to_file = "no"
        if include_bibtex == "yes":
            save_bibtex_to_file = input("Do you want to save BibTeX entries to outputs/bibtex_output.txt? (yes/no): ").strip().lower()

        results = process_multiple_titles(user_input, citation_format, include_bibtex)

        all_bibtex_entries = []
        all_formatted_citations = []
        seen_titles = set()
        use_progress = len(results) > 50
        iterator = tqdm(results.items(), desc="Processing", unit="paper") if use_progress else results.items()

        for title, data in iterator:
            if title in seen_titles:
                continue
            seen_titles.add(title)

            print(f"\nTitle: {title}\nFormatted Citation ({citation_format.upper()}):\n{data['citation']}\n")
            all_formatted_citations.append(f"{title}\n{data['citation']}\n")

            if include_bibtex == "yes" and data['bibtex']:
                print(f"BibTeX:\n{data['bibtex']}\n")
                all_bibtex_entries.append(data['bibtex'])

        # Handle file name conflicts for citations
        citations_filename = "outputs/citations_output.txt"
        if os.path.exists(citations_filename):
            base, ext = os.path.splitext(citations_filename)
            counter = 2
            while os.path.exists(f"{base}_{counter}{ext}"):
                counter += 1
            citations_filename = f"{base}_{counter}{ext}"

        if save_citations_to_file == "yes":
            with open(citations_filename, "w", encoding="utf-8") as f:
                f.write("\n\n".join(all_formatted_citations))
            print(f"✅ Formatted citations saved to {citations_filename}")

        # Handle file name conflicts for BibTeX
        if include_bibtex == "yes" and save_bibtex_to_file == "yes":
            bibtex_filename = "outputs/bibtex_output.txt"
            if os.path.exists(bibtex_filename):
                base, ext = os.path.splitext(bibtex_filename)
                counter = 2
                while os.path.exists(f"{base}_{counter}{ext}"):
                    counter += 1
                bibtex_filename = f"{base}_{counter}{ext}"

            with open(bibtex_filename, "w", encoding="utf-8") as f:
                f.write("\n\n".join(all_bibtex_entries))
            print(f"✅ BibTeX entries saved to {bibtex_filename}")

    else:
        formatted_citation, bibtex = process_single_title(user_input, citation_format, include_bibtex)
        print(f"\nFormatted Citation ({citation_format.upper()}):\n{formatted_citation}\n")
        if include_bibtex == "yes" and bibtex:
            print(f"BibTeX:\n{bibtex}\n")
            if input("Do you want to save this BibTeX to outputs/bibtex_output.txt? (yes/no): ").strip().lower() == "yes":
                with open("outputs/bibtex_output.txt", "w", encoding="utf-8") as f:
                    f.write(bibtex)
                print("✅ BibTeX saved to outputs/bibtex_output.txt")


def process_single_title(title, citation_format="apa", include_bibtex="no"):
    """Processes a single paper title, fetches DOI, BibTeX, and formats the citation."""
    try:
        doi = get_doi_from_title(title)
        if doi:
            bibtex = fetch_bibtex_from_doi(doi)
            formatted_citation = format_citation(bibtex, citation_format)
            return formatted_citation, bibtex if include_bibtex == "yes" else ""
        return "DOI not found.", ""
    except Exception as e:
        logging.error(f"Error processing title: {title} — {e}")
        return "❌ Error occurred while processing title.", ""


def process_multiple_titles(file_path, citation_format="apa", include_bibtex="no"):
    """Processes a file containing multiple paper titles."""
    try:
        dois = process_file(file_path)
        results = {}
        for title, doi in dois.items():
            try:
                if title in results:
                    continue  # Skip already processed titles

                if doi:
                    bibtex = fetch_bibtex_from_doi(doi)
                    formatted_citation = format_citation(bibtex, citation_format)
                    results[title] = {
                        "citation": formatted_citation,
                        "bibtex": bibtex if include_bibtex == "yes" else ""
                    }
                else:
                    results[title] = {"citation": "DOI not found.", "bibtex": ""}
            except Exception as e:
                logging.error(f"Error processing title: {title} — {e}")
                results[title] = {"citation": "❌ Error occurred", "bibtex": ""}
        return results
    except Exception as e:
        logging.error(f"Error reading file: {file_path} — {e}")
        return {}

if __name__ == "__main__":
    main()
