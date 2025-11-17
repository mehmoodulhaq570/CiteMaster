# CiteMaster Quick Reference Guide

## 🚀 Quick Start

```bash
# Install
pip install cite-master

# Run
python -m cite_master
```

## 📋 What's New in v0.1.2

- ✅ **Fixed** version inconsistency across files
- ✅ **Added** comprehensive test suite (35+ tests)
- ✅ **Added** configuration management system
- ✅ **Enhanced** error handling with retry logic
- ✅ **Improved** UI with colors and statistics

## 🔧 Key Features

### 1. Configuration

```bash
# Create default config
python -c "from cite_master.config import Config; Config.create_default_config_file()"

# Edit config.json
{
    "api_timeout": 30,
    "api_retry_attempts": 3,
    "output_dir": "outputs",
    "verbose": false
}
```

### 2. Testing

```bash
# Install test deps
pip install -r tests/requirements-test.txt

# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=cite_master --cov-report=html
```

### 3. Error Handling

- Automatic retries on failures
- Clear error messages with suggestions
- Detailed logging in `errors.log`

### 4. UI Improvements

- ✅ Color-coded output
- 📊 Processing statistics
- ⏱️ Time estimates
- 📈 Success rates

## 📁 Project Structure

```
cite_master/
├── __init__.py          # Package exports
├── __main__.py          # Main application
├── config.py            # Configuration system
├── exceptions.py        # Custom exceptions & retry
├── ui_utils.py          # UI utilities
├── extract_doi.py       # DOI extraction
├── fetch_bibtex.py      # BibTeX fetching
└── formatter.py         # Citation formatting

tests/
├── conftest.py          # Test fixtures
├── test_extract_doi.py
├── test_fetch_bibtex.py
├── test_formatter.py
└── test_main.py
```

## 🎯 Next Recommended Features

### High Priority

1. **Caching System** - Reduce API calls
2. **Async Processing** - 5-10x faster
3. **Additional Formats** - Chicago, Vancouver, Harvard

### Medium Priority

4. **Export Options** - JSON, XML, Word, LaTeX
5. **PDF Support** - Extract DOIs from PDFs
6. **CLI Arguments** - Non-interactive mode

### Lower Priority

7. **Web Interface** - Flask/FastAPI
8. **Additional APIs** - PubMed, arXiv
9. **CI/CD Pipeline** - Automated testing

## 📖 Documentation

- `README.md` - General overview
- `CONFIGURATION.md` - Config guide
- `TESTING.md` - Testing guide
- `IMPROVEMENTS.md` - Detailed changes
- `CHANGELOG.md` - Version history

## 🔍 Troubleshooting

### Tests not running?

```bash
pip install pytest pytest-cov pytest-mock
```

### Import errors?

```bash
pip install -e .
```

### Config not loading?

Check `config.json` exists and has valid JSON syntax

### API rate limits?

Add email to config:

```json
{
  "crossref_mailto": "your.email@example.com"
}
```

## 💡 Tips

1. **Enable Verbose Mode** for debugging

   ```json
   { "verbose": true }
   ```

2. **Check Logs** for errors

   ```bash
   tail -f errors.log
   ```

3. **Run Tests** before deploying

   ```bash
   pytest tests/
   ```

4. **Use Color Output** for better readability (enabled by default)

5. **Configure Retries** for unreliable networks
   ```json
   {
     "api_retry_attempts": 5,
     "api_retry_delay": 2.0
   }
   ```

## 📈 Performance Tips

- Enable caching (when implemented)
- Increase `max_workers` for parallel processing
- Add your email to `crossref_mailto` for better rate limits
- Use batch processing for multiple papers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Run test suite
5. Submit pull request

## 📧 Support

- GitHub Issues: [Report bugs/features]
- Email: mehmooulhaq1040@gmail.com
- Check documentation files first

---

**Remember:** Always run tests before committing changes!

```bash
pytest tests/ -v
```
