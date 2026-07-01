import sys
from pathlib import Path

# make skills/cf-click/ importable so `import cf_click` works in tests
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
