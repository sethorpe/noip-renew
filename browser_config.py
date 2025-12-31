import os
from dotenv import load_dotenv

load_dotenv()


def _str_to_bool(value: str) -> bool:
    """Convert string to boolean"""
    return value.lower() in ("true", "1", "yes", "on")


HEADLESS: bool = _str_to_bool(os.getenv("HEADLESS", "true"))
BROWSER_TYPE: str = os.getenv("BROWSER_TYPE", "chromium")  # chromium, firefox, webkit
SLOW_MOTION: int = int(os.getenv("SLOW_MOTION", "0"))
SCREENSHOT_DIR: str = os.getenv("SCREENSHOT_DIR", ".")

BROWSER_ARGS: list[str] = [
    "--disable-blink-features=AutomationControlled",  # Makes detection harder
    "--start-maximized",  # Maximize window on launch (Chromium only)
]

VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1920"))
VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
NAVIGATION_TIMEOUT: int = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
ACTION_TIMEOUT: int = int(os.getenv("ACTION_TIMEOUT", "15000"))


def get_browser_config() -> dict:
    """Get browser launch configuration"""
    return {
        "headless": HEADLESS,
        "slow_mo": SLOW_MOTION,
        "args": BROWSER_ARGS,
    }


def get_context_config() -> dict:
    """Get browser context configuration"""
    config = {
        "user_agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    if HEADLESS:
        # In headless mode, use explicit viewport size
        config["viewport"] = {
            "width": VIEWPORT_WIDTH,
            "height": VIEWPORT_HEIGHT,
        }
    else:
        # In headed mode, use no_viewport to allow --start-maximized to work
        config["no_viewport"] = True

    return config


def print_browser_config():
    """Print browser config"""
    print("Browser Configuration:")
    print(f"    - Type: {BROWSER_TYPE}")
    print(f"    - Headless: {HEADLESS}")
    print(f"    - Slow Motion: {SLOW_MOTION}ms")
    print(f"    - Viewport: {VIEWPORT_WIDTH} x {VIEWPORT_HEIGHT}")
    print(f"    - Screenshot Directory: {SCREENSHOT_DIR}")
    print(f"    - Default Timeout: {DEFAULT_TIMEOUT}ms")
