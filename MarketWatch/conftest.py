import sys
import os

# Add this file's directory (the project root) to Python's import path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)