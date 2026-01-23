import sys
import os

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.engine import Engine

if __name__ == "__main__":
    app = Engine()
    app.run()