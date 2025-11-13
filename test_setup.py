#!/usr/bin/env python3
"""
Test script to verify ScienceDirect Search Tool configuration
"""

from sciencedirect_search import ScienceDirectSearcher

def test_configuration():
    """Test if the API configuration is working."""
    print("=" * 80)
    print("ScienceDirect Search Tool - Configuration Test")
    print("=" * 80)
    print()

    # Try to import configuration
    try:
        from config import API_KEY, INST_TOKEN
        print("✓ Configuration file loaded successfully")
        print(f"  API Key: {API_KEY[:8]}..." if len(API_KEY) > 8 else f"  API Key: {API_KEY}")
        print(f"  Institutional Token: {'Set' if INST_TOKEN else 'Not set'}")
    except ImportError:
        print("⚠ Config file not found, using default API key")
        API_KEY = "61c260a6a468a1bfbaa1a2c004f1282"
        INST_TOKEN = None
        print(f"  API Key: {API_KEY[:8]}...")
        print(f"  Institutional Token: Not set")

    print()
    print("-" * 80)
    print("Testing API connection...")
    print("-" * 80)
    print()

    # Initialize searcher
    try:
        searcher = ScienceDirectSearcher(API_KEY, INST_TOKEN)
        print("✓ Searcher initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize searcher: {e}")
        return False

    # Perform test search
    print("\nPerforming test search for 'science'...")
    try:
        response = searcher.search("science", count=1)

        if 'error' in response:
            print("\n✗ API request failed")
            print(f"   Error: {response['error']}")
            if response.get('status_code'):
                print(f"   Status Code: {response['status_code']}")
            print()
            print("Troubleshooting suggestions:")
            print("  1. Check if your API key is valid at https://dev.elsevier.com")
            print("  2. Register for a new API key if needed")
            print("  3. Update your API key in config.py")
            print("  4. Check TROUBLESHOOTING.md for more help")
            return False
        else:
            print("\n✓ API request successful!")

            # Parse results
            search_results = response.get('search-results', {})
            total_results = search_results.get('opensearch:totalResults', 0)
            entries = search_results.get('entry', [])

            print(f"   Total results available: {total_results}")
            print(f"   Results returned: {len(entries)}")

            if entries and len(entries) > 0:
                first_entry = entries[0]
                if not first_entry.get('error'):
                    print(f"   Sample title: {first_entry.get('dc:title', 'N/A')[:60]}...")

            print()
            print("=" * 80)
            print("✓ Setup is working correctly!")
            print("=" * 80)
            print()
            print("You can now use the search tool:")
            print("  python sciencedirect_search.py 'your search query'")
            print("  python examples.py")
            print()
            return True

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print()
        print("Please check:")
        print("  1. Your internet connection")
        print("  2. Python dependencies (pip install -r requirements.txt)")
        print("  3. TROUBLESHOOTING.md for more help")
        return False


if __name__ == "__main__":
    import sys

    success = test_configuration()
    sys.exit(0 if success else 1)
