from pathlib import Path
import sys

# Add src to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))