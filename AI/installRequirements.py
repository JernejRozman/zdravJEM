import subprocess
import sys

packages = [
    "torch",
    "pillow",
    "transformers",
    "scikit-learn",
    "pandas",
    "tqdm",
    "flask"
]

for package in packages:
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("\n✅ All packages installed successfully!")
