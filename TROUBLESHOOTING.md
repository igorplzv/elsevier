# Troubleshooting Guide

## Common Issues and Solutions

### 403 Forbidden Error

**Symptom:** Getting "403 Client Error: Forbidden" when making API requests.

**Possible Causes:**
1. Invalid or expired API key
2. API key doesn't have proper permissions
3. Institutional token required for the content you're trying to access
4. Rate limits exceeded

**Solutions:**

#### 1. Verify Your API Key
```bash
# Check if your API key is registered at dev.elsevier.com
# Your API key should look like: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
```

Visit [dev.elsevier.com](https://dev.elsevier.com) and check:
- Is your API key active?
- Has it been approved?
- Does it have the correct permissions?

#### 2. Get a New API Key

If your API key is not working:

1. Go to https://dev.elsevier.com
2. Click "I want an API key"
3. Fill out the registration form with:
   - Your name and email
   - Your institution (if applicable)
   - Intended use (research, education, etc.)
4. Agree to terms and conditions
5. Submit and wait for approval email
6. Update `config.py` with your new API key

#### 3. Add Institutional Token

If you're accessing content that requires institutional access:

```python
# In config.py
API_KEY = "your-api-key"
INST_TOKEN = "your-institutional-token"  # Get this from your institution
```

Contact your institution's library to get an institutional token.

#### 4. Check Rate Limits

The Elsevier API has rate limits. If you're making many requests:

- Add delays between requests:
  ```python
  import time
  for query in queries:
      searcher.search(query)
      time.sleep(1)  # Wait 1 second between requests
  ```

- Request more results per query (up to 200):
  ```python
  searcher.search(query, count=200)  # Instead of multiple requests
  ```

### 401 Unauthorized Error

**Symptom:** Getting "401 Unauthorized" error.

**Solution:** This means authentication failed. Check that:
1. Your API key is correctly entered in `config.py`
2. There are no extra spaces or characters in the API key
3. The API key is valid and active

### No Results Found

**Symptom:** Search returns 0 results.

**Solutions:**

1. **Broaden your search:**
   ```python
   # Instead of:
   "very specific term AND another specific term"

   # Try:
   "broader term OR related term"
   ```

2. **Remove date restrictions:**
   ```python
   # Instead of:
   searcher.search("query", date_range=(2024, 2024))

   # Try:
   searcher.search("query")  # Search all dates
   ```

3. **Check query syntax:**
   - Boolean operators must be UPPERCASE: `AND`, `OR`, `NOT`
   - Use quotes for exact phrases: `"machine learning"`
   - Check for typos in your search terms

### Connection Timeout

**Symptom:** Request times out after 30 seconds.

**Solutions:**

1. Check your internet connection
2. Try again later (API might be temporarily unavailable)
3. Increase timeout in the code:
   ```python
   # In sciencedirect_search.py, line ~111
   response = requests.get(
       self.BASE_URL,
       headers=self.headers,
       params=params,
       timeout=60  # Increase from 30 to 60 seconds
   )
   ```

### JSON Decode Error

**Symptom:** Error parsing JSON response.

**Possible Causes:**
- API returned an error page instead of JSON
- Network issue corrupted the response

**Solution:**
Check the raw response:
```python
response = requests.get(url, headers=headers, params=params)
print(response.text)  # See what the API actually returned
print(response.status_code)  # Check status code
```

### Module Not Found Error

**Symptom:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**
```bash
pip install requests
# Or install all dependencies:
pip install -r requirements.txt
```

### SSL Certificate Error

**Symptom:** SSL certificate verification failed.

**Solutions:**

1. **Update certificates:**
   ```bash
   pip install --upgrade certifi
   ```

2. **Check system time:** Ensure your system clock is correct

3. **Temporary workaround (not recommended for production):**
   ```python
   # Add verify=False to requests (only for testing!)
   response = requests.get(url, headers=headers, params=params, verify=False)
   ```

## Getting Help

If none of these solutions work:

1. **Check API Status:**
   - Visit [dev.elsevier.com](https://dev.elsevier.com) to see if there are any service announcements

2. **Contact Elsevier Support:**
   - Email: integrationsupport@elsevier.com
   - Include:
     - Your API key (first 8 characters only for security)
     - The exact error message
     - The query you were trying to run
     - Date and time of the error

3. **Check Documentation:**
   - API Docs: https://dev.elsevier.com/api_docs.html
   - Developer Portal: https://dev.elsevier.com

## Testing Your Setup

Run this test to verify your configuration:

```python
from sciencedirect_search import ScienceDirectSearcher
from config import API_KEY, INST_TOKEN

# Initialize
searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)

# Simple test search
response = searcher.search("test", count=1)

if 'error' in response:
    print(f"Error: {response['error']}")
    print(f"Status: {response.get('status_code', 'Unknown')}")
else:
    print("Success! Your setup is working.")
    search_results = response.get('search-results', {})
    total = search_results.get('opensearch:totalResults', 0)
    print(f"Found {total} total results for 'test' query")
```

Save this as `test_setup.py` and run it to verify everything works.
