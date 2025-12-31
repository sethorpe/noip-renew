from playwright.sync_api import Page, expect, TimeoutError
from config import dns_hostname
from datetime import datetime
from pathlib import Path
from browser_config import SCREENSHOT_DIR
from logger import get_logger

log = get_logger("records")


class RecordsPage:
    def __init__(self, page: Page):
        self.page = page
        self.expiration_banner = page.locator(
            f'[id="expiration-banner-hostname-{dns_hostname}"]'
        )
        self.confirm_button = page.get_by_role("button", name="Confirm")

        try:
            log.debug(f"Checking for expiration banner for '{dns_hostname}'...")
            expect(self.expiration_banner).to_be_visible(timeout=10000)
            log.info(f"Expiration banner found for hostname '{dns_hostname}'")
        except TimeoutError:
            log.warning(f"Expiration banner not found for '{dns_hostname}'")
            raise Exception(
                f"Expiration banner not found for hostname '{dns_hostname}'. "
                "The hostname might already be renewed or not expiring within 7 days."
            )

    def renew_hostname(self) -> str:
        """Renew hostname with error handling

        Returns:
            str: Path to the screenshot file

        Raises:
            Exception: If renewal or screenshot capture fails
        """
        try:
            log.debug("Clicking confirm button to renew hostname...")
            self.confirm_button.click()

            # Wait for the page to respond to the click
            self.page.wait_for_load_state("networkidle", timeout=15000)

            # Wait for the expiration banner to disappear (proof that renewal succeeded)
            log.debug("Waiting for expiration banner to disappear...")
            expect(self.expiration_banner).to_be_hidden(timeout=10000)
            log.info("Expiration banner hidden - renewal successful")

        except TimeoutError as e:
            log.error("Timeout waiting for renewal confirmation")
            log.warning("The expiration banner did not disappear after clicking confirm")
            raise Exception("Failed to confirm hostname renewal - banner still visible")
        except Exception as e:
            log.error(f"Renewal process failed: {e}")
            raise Exception(f"Failed to renew hostname: {e}")

        try:
            screenshot_path = self._capture_screenshot()
            return screenshot_path
        except Exception as e:
            log.error(f"Screenshot capture failed: {e}")
            raise Exception(f"Renewal succeeded but screenshot failed: {e}")

    def _capture_screenshot(self) -> str:
        """Capture screenshot

        Returns:
            str: Absolute path to the screenshot file
        """
        try:
            screenshot_dir = Path(SCREENSHOT_DIR)
            if not screenshot_dir.is_absolute():
                screenshot_dir = Path(__file__).parent.parent / screenshot_dir

            timestamp: str = datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M")
            screenshot_path = screenshot_dir / f"dns_renewal_{timestamp}.png"

            screenshot_path.parent.mkdir(parents=True, exist_ok=True)

            log.debug(f"Saving screenshot to: {screenshot_path}")
            self.page.screenshot(path=str(screenshot_path))
            log.info(f"Screenshot saved: {screenshot_path.name}")

            return str(screenshot_path.absolute())

        except Exception as e:
            log.error(f"Screenshot save failed: {e}")
            raise Exception(f"Screenshot save failed: {e}")
