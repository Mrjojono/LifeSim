import os
import runpy


if __name__ == "__main__":
    runpy.run_path(os.path.join(os.path.dirname(__file__), "main.py"), run_name="__main__")
