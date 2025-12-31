import subprocess
import sys
from browser_config import BROWSER_TYPE


def main():
    """Install the Playwright browser specified in .env configuration"""
    print("=" * 60)
    print("No-IP Automation - Browser Setup")
    print("=" * 60)
    print(f"\nInstalling Playwright browser: {BROWSER_TYPE}")
    print("This may take a few minutes...\n")

    try:
        result = subprocess.run(
            ["playwright", "install", BROWSER_TYPE],
            check=True,
            capture_output=True,
            text=True,
        )

        if result.stdout:
            print(result.stdout)

        print(f"\nBrowser installation complete!")
        print(f"You can now run: poetry run python -m main")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"\nBrowser installation failed!")
        print(f"Error: {e}")
        if e.stderr:
            print(f"Details: {e.stderr}")
        print(f"\nYou can manually install the browser with:")
        print(f"  playwright install {BROWSER_TYPE}")
        return 1
    except FileNotFoundError:
        print("\nPlaywright CLI not found!")
        print("Make sure you've installed dependencies with: poetry install")
        return 1


if __name__ == "__main__":
    sys.exit(main())
