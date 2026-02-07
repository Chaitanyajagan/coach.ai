import sys
print(f"Python Executable: {sys.executable}")
print(f"Path: {sys.path}")
try:
    from dotenv import load_dotenv
    print("SUCCESS: dotenv imported")
except ImportError as e:
    print(f"ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")
