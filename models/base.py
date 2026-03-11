from playwright.sync_api import Page
from datetime import datetime
from pathlib import Path
from browser_config import SCREENSHOT_DIR
from logger import get_logger

log = get_logger("base")


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def capture_screenshot(self, prefix: str = "screenshot") -> str:
        """Capture a screenshot of the current page.

        Args:
            prefix: Filename prefix for the screenshot (default: 'screenshot')

        Returns:
            str: Absolute path to the screenshot file
        """
        try:
            screenshot_dir = Path(SCREENSHOT_DIR)
            if not screenshot_dir.is_absolute():
                screenshot_dir = Path(__file__).parent.parent / screenshot_dir

            timestamp: str = datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M")
            screenshot_path = screenshot_dir / f"{prefix}_{timestamp}.png"

            screenshot_path.parent.mkdir(parents=True, exist_ok=True)

            log.debug(f"Saving screenshot to: {screenshot_path}")
            self.page.screenshot(path=str(screenshot_path))
            log.info(f"Screenshot saved: {screenshot_path.name}")

            return str(screenshot_path.absolute())

        except Exception as e:
            log.error(f"Screenshot save failed: {e}")
            raise Exception(f"Screenshot save failed: {e}")
