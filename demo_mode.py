#!/usr/bin/env python3
"""
Demo mode for ScienceDirect Search Tool
Shows how the tool works with sample data
"""

from sciencedirect_search import Article, ScienceDirectSearcher
from typing import List, Dict
import json

# Sample realistic response data
SAMPLE_RESPONSE = {
    "search-results": {
        "opensearch:totalResults": "145623",
        "opensearch:startIndex": "0",
        "opensearch:itemsPerPage": "5",
        "entry": [
            {
                "dc:title": "Artificial intelligence in healthcare: past, present and future",
                "dc:creator": "Jiang, F.",
                "authors": {
                    "author": [
                        {"given-name": "Fei", "surname": "Jiang"},
                        {"given-name": "Yong", "surname": "Jiang"},
                        {"given-name": "Hui", "surname": "Zhi"}
                    ]
                },
                "prism:publicationName": "Stroke and Vascular Neurology",
                "prism:coverDate": "2024-06-01",
                "prism:doi": "10.1136/svn-2022-001853",
                "pii": "S0123456789012345",
                "link": [{"@href": "https://api.elsevier.com/content/article/pii/S0123456789012345"}],
                "dc:description": "Artificial intelligence (AI) aims to mimic human cognitive functions. It is bringing a paradigm shift to healthcare, powered by increasing availability of healthcare data and rapid progress of analytics techniques."
            },
            {
                "dc:title": "Machine learning applications in cancer research: A systematic review",
                "dc:creator": "Smith, J.",
                "authors": {
                    "author": [
                        {"given-name": "John", "surname": "Smith"},
                        {"given-name": "Mary", "surname": "Johnson"}
                    ]
                },
                "prism:publicationName": "Journal of Biomedical Informatics",
                "prism:coverDate": "2024-03-15",
                "prism:doi": "10.1016/j.jbi.2024.104321",
                "pii": "S1532046424001029",
                "link": [{"@href": "https://api.elsevier.com/content/article/pii/S1532046424001029"}],
                "dc:description": "Machine learning techniques have shown tremendous potential in cancer research, from early detection to treatment optimization. This systematic review examines recent applications and their clinical impact."
            },
            {
                "dc:title": "Deep learning for medical image analysis: A comprehensive survey",
                "dc:creator": "Zhang, L.",
                "authors": {
                    "author": [
                        {"given-name": "Li", "surname": "Zhang"},
                        {"given-name": "Wei", "surname": "Chen"},
                        {"given-name": "Ming", "surname": "Liu"}
                    ]
                },
                "prism:publicationName": "Medical Image Analysis",
                "prism:coverDate": "2024-01-20",
                "prism:doi": "10.1016/j.media.2024.102890",
                "pii": "S1361841524000129",
                "link": [{"@href": "https://api.elsevier.com/content/article/pii/S1361841524000129"}],
                "dc:description": "Deep learning has revolutionized medical image analysis. This survey provides a comprehensive overview of recent advances in convolutional neural networks, transformers, and other architectures for medical imaging tasks."
            },
            {
                "dc:title": "Natural language processing in clinical decision support systems",
                "dc:creator": "Brown, A.",
                "authors": {
                    "author": [
                        {"given-name": "Amanda", "surname": "Brown"},
                        {"given-name": "David", "surname": "Wilson"}
                    ]
                },
                "prism:publicationName": "Artificial Intelligence in Medicine",
                "prism:coverDate": "2023-12-10",
                "prism:doi": "10.1016/j.artmed.2023.102567",
                "pii": "S0933365723002345",
                "link": [{"@href": "https://api.elsevier.com/content/article/pii/S0933365723002345"}],
                "dc:description": "Natural language processing (NLP) enables computers to understand and generate human language. In clinical settings, NLP-powered decision support systems are transforming how physicians access and utilize medical knowledge."
            },
            {
                "dc:title": "Predictive analytics for patient outcomes using electronic health records",
                "dc:creator": "Garcia, M.",
                "authors": {
                    "author": [
                        {"given-name": "Maria", "surname": "Garcia"},
                        {"given-name": "Carlos", "surname": "Rodriguez"},
                        {"given-name": "Ana", "surname": "Martinez"}
                    ]
                },
                "prism:publicationName": "Journal of the American Medical Informatics Association",
                "prism:coverDate": "2023-11-05",
                "prism:doi": "10.1093/jamia/ocad234",
                "pii": "S1067502723001234",
                "link": [{"@href": "https://api.elsevier.com/content/article/pii/S1067502723001234"}],
                "dc:description": "Electronic health records contain vast amounts of patient data. This study demonstrates how predictive analytics can leverage this data to forecast patient outcomes and enable proactive interventions."
            }
        ]
    }
}


class DemoSearcher(ScienceDirectSearcher):
    """Demo version that uses sample data instead of API calls."""

    def __init__(self, api_key: str, inst_token=None):
        super().__init__(api_key, inst_token)
        self.demo_mode = True

    def search(self, query: str, count: int = 25, start: int = 0,
               subscribed_only: bool = False, date_range=None) -> Dict:
        """Return sample data instead of making API calls."""

        print(f"\n[DEMO MODE] Simulating search for: '{query}'")
        print(f"[DEMO MODE] In real mode, this would call the API with your credentials\n")

        # Modify sample response based on count
        response = SAMPLE_RESPONSE.copy()
        response["search-results"] = response["search-results"].copy()
        response["search-results"]["entry"] = response["search-results"]["entry"][:min(count, 5)]
        response["search-results"]["opensearch:itemsPerPage"] = str(min(count, 5))

        return response


def demo_basic_search():
    """Demo 1: Basic search"""
    print("="*80)
    print("DEMO 1: Basic Search")
    print("="*80)

    searcher = DemoSearcher("demo-api-key")
    searcher.search_and_display("artificial intelligence healthcare", count=3)


def demo_boolean_search():
    """Demo 2: Boolean search"""
    print("\n\n" + "="*80)
    print("DEMO 2: Boolean Search")
    print("="*80)

    searcher = DemoSearcher("demo-api-key")
    searcher.search_and_display("machine learning AND cancer", count=2)


def demo_programmatic():
    """Demo 3: Programmatic access"""
    print("\n\n" + "="*80)
    print("DEMO 3: Programmatic Access")
    print("="*80)

    searcher = DemoSearcher("demo-api-key")
    response = searcher.search("deep learning medical imaging", count=3)
    articles = searcher.parse_results(response)

    print(f"\nProcessing {len(articles)} articles programmatically:\n")

    for i, article in enumerate(articles, 1):
        print(f"{i}. {article.title}")
        print(f"   Journal: {article.publication_name}")
        print(f"   DOI: {article.doi}")
        print(f"   Authors: {', '.join(article.authors)}")
        print()


def demo_all():
    """Run all demos"""
    print("\n" + "="*80)
    print("ScienceDirect Search Tool - DEMO MODE")
    print("="*80)
    print("\nThis demo shows how the tool works with sample data.")
    print("With a valid, activated API key, it will fetch real articles from ScienceDirect.")
    print("\n" + "="*80 + "\n")

    demos = [
        demo_basic_search,
        demo_boolean_search,
        demo_programmatic,
    ]

    for demo in demos:
        demo()
        print("\n" + "-"*80)
        input("\nPress Enter to continue...")

    print("\n" + "="*80)
    print("Demo Complete!")
    print("="*80)
    print("\nTo use with real API:")
    print("1. Get a valid API key from https://dev.elsevier.com")
    print("2. Ensure the API key is activated (check your email)")
    print("3. Update config.py with your activated API key")
    print("4. Run: python sciencedirect_search.py")
    print()


if __name__ == "__main__":
    demo_all()
