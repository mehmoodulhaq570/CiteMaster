# Configuration Guide for CiteMaster

CiteMaster supports configuration through a JSON file to customize various settings.

## Creating a Configuration File

Create a `config.json` file in your project root:

```bash
python -c "from cite_master.config import Config; Config.create_default_config_file()"
```

Or create it manually:

```json
{
  "output_dir": "outputs",
  "citations_filename": "citations_output.txt",
  "bibtex_filename": "bibtex_output.txt",
  "log_filename": "errors.log",
  "api_timeout": 30,
  "api_retry_attempts": 3,
  "api_retry_delay": 1,
  "api_rate_limit": 50,
  "batch_progress_threshold": 50,
  "max_workers": 5,
  "cache_enabled": true,
  "cache_expiry_days": 30,
  "crossref_base_url": "https://api.crossref.org/works",
  "crossref_mailto": "",
  "verbose": false,
  "quiet": false,
  "color_output": true
}
```

## Configuration Options

### Output Settings

- **output_dir** (string): Directory for output files. Default: `"outputs"`
- **citations_filename** (string): Name for citations output file. Default: `"citations_output.txt"`
- **bibtex_filename** (string): Name for BibTeX output file. Default: `"bibtex_output.txt"`
- **log_filename** (string): Name for log file. Default: `"errors.log"`

### API Settings

- **api_timeout** (integer): Request timeout in seconds. Default: `30`
- **api_retry_attempts** (integer): Number of retry attempts for failed API calls. Default: `3`
- **api_retry_delay** (float): Initial delay between retries in seconds. Default: `1.0`
- **api_rate_limit** (integer): Maximum requests per minute. Default: `50`

### Processing Settings

- **batch_progress_threshold** (integer): Show progress bar for files with more items than this. Default: `50`
- **max_workers** (integer): Number of parallel workers for batch processing. Default: `5`
- **cache_enabled** (boolean): Enable/disable caching of DOI lookups. Default: `true`
- **cache_expiry_days** (integer): Days before cached items expire. Default: `30`

### CrossRef API Settings

- **crossref_base_url** (string): Base URL for CrossRef API. Default: `"https://api.crossref.org/works"`
- **crossref_mailto** (string): Your email for better API rate limits (optional). Default: `""`

### Output Formatting

- **verbose** (boolean): Enable verbose logging. Default: `false`
- **quiet** (boolean): Suppress non-essential output. Default: `false`
- **color_output** (boolean): Enable colored terminal output. Default: `true`

## Using Configuration Programmatically

```python
from cite_master.config import Config, get_config, set_config

# Load custom configuration
config = Config("path/to/config.json")
set_config(config)

# Get configuration values
timeout = config.get("api_timeout")

# Update configuration
config.set("api_timeout", 60)

# Save configuration
config.save_to_file("path/to/config.json")

# Use global configuration
global_config = get_config()
output_dir = global_config.get("output_dir")
```

## Environment-Specific Configurations

You can maintain different configuration files for different environments:

```bash
# Development
config.dev.json

# Production
config.prod.json

# Testing
config.test.json
```

Then load the appropriate one:

```python
config = Config("config.prod.json")
```

## Best Practices

1. **Email for CrossRef**: Add your email to `crossref_mailto` for better API rate limits
2. **Timeout**: Increase `api_timeout` if you have slow network connection
3. **Retry Attempts**: Increase `api_retry_attempts` for unreliable networks
4. **Cache**: Enable `cache_enabled` to speed up repeated requests
5. **Verbose Mode**: Enable `verbose` for debugging issues

## Troubleshooting

### Configuration Not Loading

- Check that `config.json` exists in the correct location
- Verify JSON syntax is valid
- Check file permissions

### Settings Not Applied

- Ensure you're loading the config before using CiteMaster
- Check that the config file path is correct
- Restart the application after changing config

### API Rate Limits

If you hit rate limits:

1. Add your email to `crossref_mailto`
2. Reduce `api_rate_limit`
3. Increase `api_retry_delay`
