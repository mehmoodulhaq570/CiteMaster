# CiteMaster ✨

**CiteMaster** is a smart Python package that helps you automatically generate formatted citations from research paper titles or files of titles. No more manual DOI searching or formatting—CiteMaster does it all for you!

---

## 🔥 Features

- 🔍 Extracts DOI from paper titles using the CrossRef API
- 🧠 Fetches corresponding BibTeX data
- 📝 Formats citations in **APA**, **MLA**, or **IEEE**
- 📂 Supports batch citation generation from `.txt` or `.csv` files

---

## 📦 Installation

Clone and install CiteMaster locally:

```bash
git clone https://github.com/yourusername/CiteMaster.git
cd CiteMaster
pip install requirements.txt
```

> **Note:** Make sure you’re using Python 3.7 or higher.

---

## 🚀 How to Use

CiteMaster provides an interactive interface.

### ▶️ Running the Program

```python
from auto_refgen import main

main()
```

You'll be prompted to input:

- A paper title or a file path (`.txt` or `.csv`)
- A citation format: `apa`, `mla`, or `ieee`

---

### 📌 Example 1: Single Paper Title

**Input:**

```
Enter a paper title or provide a file path (txt/csv): Deep Learning for Solar Energy Forecasting: A Review
Enter citation format (apa, mla, ieee): apa
```

**Output:**

```
DOI: 10.1016/j.rser.2020.109984

BibTeX:
@article{DeepLearning2020,
  title={Deep Learning for Solar Energy Forecasting: A Review},
  author={John Smith and Alice Johnson},
  journal={Renewable and Sustainable Energy Reviews},
  volume={132},
  pages={109984},
  year={2020},
  publisher={Elsevier}
}

Formatted Citation (APA):
Smith, J., & Johnson, A. (2020). Deep Learning for Solar Energy Forecasting: A Review. *Renewable and Sustainable Energy Reviews*, 132, 109984. https://doi.org/10.1016/j.rser.2020.109984
```

---

### 📄 Example 2: File of Titles

**Input:**

```
Enter a paper title or provide a file path (txt/csv): paper_titles.txt
Enter citation format (apa, mla, ieee): ieee
```

Each title will be processed and a formatted citation printed along with its BibTeX.

---

## 📁 Supported Input Formats

- **.txt file**: One paper title per line  
- **.csv file**: First column should contain the titles

**Example `paper_titles.txt`:**

```
Artificial Intelligence for Smart Grids
Machine Learning in Climate Forecasting
```

---

## ❌ Uninstalling

```bash
pip uninstall citemaster
```

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Feel free to open issues or submit pull requests. Suggestions and improvements are welcome!

---

## 📚 Acknowledgments

- [CrossRef API](https://www.crossref.org/)
- [BibTeX Format](https://www.bibtex.org/)
- Citation styles follow official formatting guidelines.

---

**Made ❤️ by [Mehmood Ul Haq]**
