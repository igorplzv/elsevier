#!/usr/bin/env python3
"""
ScienceDirect Article Search Tool
Uses the Elsevier ScienceDirect Search API to find and display articles.
"""

import requests
import json
from typing import Optional, Dict, List
from dataclasses import dataclass
import sys


@dataclass
class Article:
    """Represents a ScienceDirect article."""
    title: str
    authors: List[str]
    publication_name: str
    doi: str
    pii: str
    cover_date: str
    url: str
    abstract: Optional[str] = None

    def __str__(self) -> str:
        """Format article for display."""
        authors_str = ", ".join(self.authors) if self.authors else "Unknown"
        lines = [
            f"\n{'=' * 80}",
            f"Title: {self.title}",
            f"Authors: {authors_str}",
            f"Publication: {self.publication_name}",
            f"Date: {self.cover_date}",
            f"DOI: {self.doi}",
            f"URL: {self.url}",
        ]
        if self.abstract:
            lines.append(f"Abstract: {self.abstract[:300]}...")
        lines.append('=' * 80)
        return '\n'.join(lines)


class ScienceDirectSearcher:
    """Client for searching ScienceDirect articles via Elsevier API."""

    BASE_URL = "https://api.elsevier.com/content/search/scidir"

    def __init__(self, api_key: str, inst_token: Optional[str] = None):
        """
        Initialize the ScienceDirect searcher.

        Args:
            api_key: Your Elsevier API key
            inst_token: Optional institutional token for access to subscribed content
        """
        self.api_key = api_key
        self.inst_token = inst_token
        self.headers = {
            'X-ELS-APIKey': api_key,
            'Accept': 'application/json'
        }
        if inst_token:
            self.headers['X-ELS-Insttoken'] = inst_token

    def search(
        self,
        query: str,
        count: int = 25,
        start: int = 0,
        subscribed_only: bool = False,
        date_range: Optional[tuple] = None
    ) -> Dict:
        """
        Search for articles on ScienceDirect.

        Args:
            query: Search query (supports Boolean operators: AND, OR, NOT)
            count: Number of results to return (max 200)
            start: Starting index for pagination
            subscribed_only: Limit results to subscribed content only
            date_range: Optional tuple of (start_year, end_year) for date filtering

        Returns:
            Dictionary containing search results and metadata
        """
        # Build query string
        search_query = query
        if date_range:
            start_year, end_year = date_range
            if start_year == end_year:
                search_query += f" AND PUBYEAR({start_year})"
            else:
                search_query += f" AND PUBYEAR > {start_year-1} AND PUBYEAR < {end_year+1}"

        # Build parameters
        params = {
            'query': search_query,
            'count': min(count, 200),  # API max is 200
            'start': start
        }

        if subscribed_only:
            params['subscribed'] = 'true'

        try:
            response = requests.get(
                self.BASE_URL,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            status_code = None

            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code

                # Provide helpful error messages
                if status_code == 401:
                    error_msg = "Authentication failed. Please check your API key."
                elif status_code == 403:
                    error_msg = ("Access forbidden. This could mean:\n"
                                "  1. Your API key is invalid or expired\n"
                                "  2. You don't have access to the requested content\n"
                                "  3. An institutional token may be required\n"
                                "  4. Rate limits may have been exceeded\n"
                                f"Original error: {str(e)}")
                elif status_code == 429:
                    error_msg = "Rate limit exceeded. Please wait before making more requests."

            return {
                'error': error_msg,
                'status_code': status_code
            }

    def parse_results(self, response: Dict) -> List[Article]:
        """
        Parse API response into Article objects.

        Args:
            response: JSON response from the API

        Returns:
            List of Article objects
        """
        articles = []

        if 'error' in response:
            print(f"Error: {response['error']}")
            if response.get('status_code'):
                print(f"Status Code: {response['status_code']}")
            return articles

        # Navigate the response structure
        search_results = response.get('search-results', {})
        entries = search_results.get('entry', [])

        for entry in entries:
            # Skip error entries
            if entry.get('error'):
                continue

            # Extract authors
            authors = []
            if 'authors' in entry and entry['authors']:
                author_list = entry['authors'].get('author', [])
                authors = [a.get('given-name', '') + ' ' + a.get('surname', '')
                          for a in author_list if isinstance(a, dict)]

            # Extract article data
            article = Article(
                title=entry.get('dc:title', 'No title available'),
                authors=authors,
                publication_name=entry.get('prism:publicationName', 'Unknown'),
                doi=entry.get('prism:doi', ''),
                pii=entry.get('pii', ''),
                cover_date=entry.get('prism:coverDate', ''),
                url=entry.get('link', [{}])[0].get('@href', ''),
                abstract=entry.get('dc:description', None)
            )
            articles.append(article)

        return articles

    def search_and_display(
        self,
        query: str,
        count: int = 25,
        **kwargs
    ) -> None:
        """
        Search for articles and display results.

        Args:
            query: Search query
            count: Number of results
            **kwargs: Additional search parameters
        """
        print(f"\nSearching ScienceDirect for: '{query}'")
        print(f"Retrieving up to {count} results...\n")

        response = self.search(query, count, **kwargs)
        articles = self.parse_results(response)

        if not articles:
            print("No articles found or an error occurred.")
            return

        # Display metadata
        search_results = response.get('search-results', {})
        total_results = search_results.get('opensearch:totalResults', 'Unknown')
        print(f"Total results found: {total_results}")
        print(f"Displaying: {len(articles)} articles\n")

        # Display articles
        for i, article in enumerate(articles, 1):
            print(f"\n[{i}] {article}")

        # Save to JSON file
        output_file = 'search_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(response, f, indent=2, ensure_ascii=False)
        print(f"\n\nFull results saved to: {output_file}")


def main():
    """Main function to run the search tool."""
    # Try to import config, fall back to default if not available
    try:
        from config import API_KEY, INST_TOKEN
    except ImportError:
        API_KEY = "61c260a6a468a1bfbaa1a2c004f1282"
        INST_TOKEN = None

    # Initialize searcher
    searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)

    # Example searches
    if len(sys.argv) > 1:
        # Use command-line argument as query
        query = ' '.join(sys.argv[1:])
        searcher.search_and_display(query, count=10)
    else:
        # Interactive mode
        print("=" * 80)
        print("ScienceDirect Article Search Tool")
        print("=" * 80)
        print("\nSupported query operators:")
        print("  - AND, OR, NOT for Boolean searches")
        print("  - DOI(\"10.xxxx/xxxxx\") for DOI search")
        print("  - PUBYEAR(2024) for year filtering")
        print("\nExamples:")
        print("  - machine learning AND healthcare")
        print("  - climate change OR global warming")
        print("  - artificial intelligence NOT robotics")
        print("=" * 80)

        while True:
            try:
                query = input("\nEnter search query (or 'quit' to exit): ").strip()

                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break

                if not query:
                    print("Please enter a search query.")
                    continue

                # Ask for number of results
                count_input = input("Number of results (default 10, max 200): ").strip()
                count = int(count_input) if count_input.isdigit() else 10

                # Perform search
                searcher.search_and_display(query, count=count)

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue


if __name__ == "__main__":
    main()
