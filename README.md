# ScienceDirect Article Search Tool

A Python tool for searching and displaying articles published on ScienceDirect using the Elsevier API.

## Features

- Search ScienceDirect articles using Boolean queries
- Support for advanced search operators (AND, OR, NOT)
- Date range filtering by publication year
- DOI-based searches
- Pagination support for large result sets
- Results saved to JSON for further processing
- Both command-line and interactive modes

## Prerequisites

- Python 3.7 or higher
- Elsevier API key (get one from [dev.elsevier.com](https://dev.elsevier.com))
- (Optional) Institutional token for access to subscribed content

## Important Note About API Keys

The API key included in this repository is provided as an example. If you encounter 403 Forbidden errors:

1. **Register for your own API key** at [dev.elsevier.com](https://dev.elsevier.com)
2. **Update the API key** in `config.py`:
   ```python
   API_KEY = "your-new-api-key-here"
   ```
3. If you're from an institution with an Elsevier subscription, you may also need an **institutional token**:
   ```python
   INST_TOKEN = "your-institutional-token-here"
   ```

To get an API key:
- Visit https://dev.elsevier.com
- Click "I want an API key"
- Fill out the registration form
- Agree to the terms and conditions
- You'll receive your API key via email

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd elsevier
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Demo Mode (No API Key Required)

See how the tool works with sample data:
```bash
pip install -r requirements.txt
python demo_mode.py
```

### Option 2: Live API Mode (Requires Activated API Key)

1. **Get an API key** from https://dev.elsevier.com (see [API_KEY_SETUP.md](API_KEY_SETUP.md))

2. **Wait for activation email** (24-48 hours after registration)

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Update your API key** in `config.py`:
   ```python
   API_KEY = "your-activated-api-key-here"
   ```

5. **Test your setup:**
   ```bash
   python test_setup.py
   ```

6. **Start searching:**
   ```bash
   python sciencedirect_search.py "your search query"
   ```

## Usage

### Command-Line Mode

Search directly from the command line:

```bash
# Basic search
python sciencedirect_search.py machine learning

# Multi-word query
python sciencedirect_search.py "artificial intelligence AND healthcare"

# Boolean search
python sciencedirect_search.py "climate change" OR "global warming"
```

### Interactive Mode

Run without arguments for interactive mode:

```bash
python sciencedirect_search.py
```

Then enter your search queries when prompted.

### As a Python Module

Import and use in your own scripts:

```python
from sciencedirect_search import ScienceDirectSearcher

# Initialize with your API key
searcher = ScienceDirectSearcher("your-api-key-here")

# Basic search
response = searcher.search("machine learning", count=10)
articles = searcher.parse_results(response)

# Advanced search with date range
response = searcher.search(
    query="artificial intelligence",
    count=50,
    date_range=(2020, 2024),
    subscribed_only=True
)

# Display results
searcher.search_and_display("neural networks", count=15)
```

## Search Query Syntax

### Boolean Operators

- `AND` - Both terms must appear
  ```
  machine learning AND healthcare
  ```

- `OR` - Either term can appear
  ```
  climate change OR global warming
  ```

- `NOT` - Exclude results with this term
  ```
  artificial intelligence NOT robotics
  ```

### Special Searches

- **DOI Search**: Find a specific article by DOI
  ```
  DOI("10.1016/j.example.2024.01.001")
  ```

- **Year Filter**: Limit to specific publication year
  ```
  neural networks AND PUBYEAR(2024)
  ```

- **Year Range**: Use the API's date_range parameter
  ```python
  searcher.search("quantum computing", date_range=(2020, 2024))
  ```

## API Parameters

The `search()` method accepts the following parameters:

- `query` (str): Search query string
- `count` (int): Number of results to return (default: 25, max: 200)
- `start` (int): Starting index for pagination (default: 0)
- `subscribed_only` (bool): Limit to subscribed content (default: False)
- `date_range` (tuple): Optional (start_year, end_year) for filtering

## Output

### Console Output

Results are displayed in the console with:
- Article title
- Authors
- Publication name
- Publication date
- DOI
- URL to full article
- Abstract preview (first 300 characters)

### JSON Output

Full search results are automatically saved to `search_results.json` for further processing.

## Examples

### Example 1: Basic Research Topic

```bash
python sciencedirect_search.py machine learning AND medical diagnosis
```

### Example 2: Recent Papers on a Topic

```python
from sciencedirect_search import ScienceDirectSearcher

searcher = ScienceDirectSearcher("your-api-key")
searcher.search_and_display(
    "CRISPR gene editing",
    count=20,
    date_range=(2023, 2024)
)
```

### Example 3: Pagination for Large Result Sets

```python
# Get first 200 results
response1 = searcher.search("climate change", count=200, start=0)

# Get next 200 results
response2 = searcher.search("climate change", count=200, start=200)
```

## API Response Structure

The tool parses the following fields from the API response:

```json
{
  "search-results": {
    "opensearch:totalResults": "1234",
    "entry": [
      {
        "dc:title": "Article Title",
        "dc:creator": "Author Name",
        "prism:publicationName": "Journal Name",
        "prism:coverDate": "2024-01-15",
        "prism:doi": "10.1016/...",
        "pii": "S0123456789",
        "dc:description": "Abstract text...",
        "link": [{"@href": "https://..."}]
      }
    ]
  }
}
```

## Troubleshooting

### Authentication Errors

If you receive authentication errors:
1. Verify your API key is correct
2. Check that your API key is active at [dev.elsevier.com](https://dev.elsevier.com)
3. Ensure you're not exceeding rate limits

### No Results Found

- Try broader search terms
- Remove date restrictions
- Check query syntax (Boolean operators must be uppercase)

### Rate Limiting

The Elsevier API has rate limits. If you're making many requests:
- Add delays between requests
- Consider requesting more results per query (up to 200)
- Use pagination efficiently

## API Documentation

For more information about the Elsevier ScienceDirect API:
- Developer Portal: https://dev.elsevier.com
- API Documentation: https://dev.elsevier.com/api_docs.html
- GitHub Examples: https://github.com/ElsevierDev

## License

This tool is provided as-is for educational and research purposes.

## Support

For API-related issues, contact Elsevier support at integrationsupport@elsevier.com
