"""
Configuration file for ScienceDirect Search Tool
"""

# Elsevier API Configuration
API_KEY = "861c260a6a468a1bfbaa1a2c004f1282"

# Optional: Institutional token (if you have one)
# INST_TOKEN = "your-institutional-token-here"
INST_TOKEN = None

# API Settings
API_BASE_URL = "https://api.elsevier.com/content/search/scidir"
DEFAULT_RESULTS_COUNT = 10
MAX_RESULTS_PER_REQUEST = 200

# Output Settings
SAVE_TO_JSON = True
JSON_OUTPUT_FILE = "search_results.json"
