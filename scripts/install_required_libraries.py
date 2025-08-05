import subprocess
import sys

required_libraries = [
    "pandas",
    "sqlalchemy",
    "psycopg2-binary",
    "python-dotenv"
]

def install(package):
    try:
        __import__(package.split("-")[0])
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print(f" {package} is already installed.")

if __name__ == "__main__":
    for lib in required_libraries:
        install(lib)
