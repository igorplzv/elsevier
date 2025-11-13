#!/usr/bin/env python3
"""
Examples of using the ScienceDirect Search Tool
"""

from sciencedirect_search import ScienceDirectSearcher

# Import configuration
try:
    from config import API_KEY, INST_TOKEN
except ImportError:
    # Use default API key if config not available
    API_KEY = "61c260a6a468a1bfbaa1a2c004f1282"
    INST_TOKEN = None


def example_basic_search():
    """Example 1: Basic keyword search"""
    print("\n" + "="*80)
    print("Example 1: Basic Keyword Search")
    print("="*80)

    searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)
    searcher.search_and_display("machine learning", count=5)


def example_boolean_search():
    """Example 2: Boolean search with AND operator"""
    print("\n" + "="*80)
    print("Example 2: Boolean Search (AND)")
    print("="*80)

    searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)
    searcher.search_and_display("artificial intelligence AND healthcare", count=5)


def example_date_range_search():
    """Example 3: Search with date range filtering"""
    print("\n" + "="*80)
    print("Example 3: Search with Date Range (2023-2024)")
    print("="*80)

    searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)
    response = searcher.search(
        query="neural networks",
        count=5,
        date_range=(2023, 2024)
    )

    articles = searcher.parse_results(response)
    for i, article in enumerate(articles, 1):
        print(f"\n[{i}] {article}")


def example_doi_search():
    """Example 4: Search by DOI"""
    print("\n" + "="*80)
    print("Example 4: Search by DOI")
    print("="*80)

    searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)

    # Example DOI - replace with a valid DOI
    doi = "10.1016/j.artmed.2024.102789"
    searcher.search_and_display(f'DOI("{doi}")', count=1)


def example_programmatic_access():
    """Example 5: Programmatic access to results"""
    print("\n" + "="*80)
    print("Example 5: Programmatic Access to Results")
    print("="*80)

    searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)

    # Perform search
    response = searcher.search("quantum computing", count=5)

    # Check for errors
    if 'error' in response:
        print(f"Error occurred: {response['error']}")
        return

    # Parse results
    articles = searcher.parse_results(response)

    # Process articles programmatically
    print(f"\nFound {len(articles)} articles\n")

    for i, article in enumerate(articles, 1):
        print(f"{i}. {article.title}")
        print(f"   Authors: {', '.join(article.authors[:3])}")  # First 3 authors
        print(f"   DOI: {article.doi}")
        print(f"   Date: {article.cover_date}")
        print()


def example_pagination():
    """Example 6: Pagination for large result sets"""
    print("\n" + "="*80)
    print("Example 6: Pagination (Fetching Multiple Pages)")
    print("="*80)

    searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)

    # Fetch first page
    response1 = searcher.search("climate change", count=10, start=0)
    articles1 = searcher.parse_results(response1)

    # Fetch second page
    response2 = searcher.search("climate change", count=10, start=10)
    articles2 = searcher.parse_results(response2)

    print(f"First page: {len(articles1)} articles")
    print(f"Second page: {len(articles2)} articles")
    print(f"Total fetched: {len(articles1) + len(articles2)} articles")


def example_error_handling():
    """Example 7: Error handling"""
    print("\n" + "="*80)
    print("Example 7: Error Handling")
    print("="*80)

    searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)

    # Perform search
    response = searcher.search("example query", count=5)

    # Check for errors
    if 'error' in response:
        print("An error occurred:")
        print(f"  Error message: {response['error']}")
        if response.get('status_code'):
            print(f"  Status code: {response['status_code']}")
        print("\nTroubleshooting tips:")
        print("  1. Check your API key is valid at https://dev.elsevier.com")
        print("  2. Verify you have an active API key")
        print("  3. Consider adding an institutional token if available")
        print("  4. Check if you've exceeded rate limits")
    else:
        print("Search successful!")
        search_results = response.get('search-results', {})
        total_results = search_results.get('opensearch:totalResults', 0)
        print(f"Total results found: {total_results}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ScienceDirect Search Tool - Examples")
    print("="*80)
    print("\nThese examples demonstrate various features of the search tool.")
    print("Note: Some examples may fail if the API key is invalid or expired.")
    print("\nRunning examples...\n")

    # Run all examples
    examples = [
        example_basic_search,
        example_boolean_search,
        example_date_range_search,
        # example_doi_search,  # Uncomment to test DOI search
        example_programmatic_access,
        # example_pagination,  # Uncomment to test pagination
        example_error_handling,
    ]

    for example_func in examples:
        try:
            example_func()
            input("\nPress Enter to continue to next example...")
        except KeyboardInterrupt:
            print("\n\nExamples interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError running example: {e}")
            input("\nPress Enter to continue to next example...")

    print("\n" + "="*80)
    print("Examples completed!")
    print("="*80)
