from playwright.sync_api import Page, expect, TimeoutError
from config import dns_hostname
from .base import BasePage
from logger import get_logger

log = get_logger("records")


class RecordsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.expiration_banner = page.locator(
            f'[id="expiration-banner-hostname-{dns_hostname}"]'
        )
        self.confirm_button = page.get_by_role("button", name="Confirm")

        try:
            log.debug(f"Checking for expiration banner for '{dns_hostname}'...")
            expect(self.expiration_banner).to_be_visible(timeout=10000)
            log.info(f"Expiration banner found for hostname '{dns_hostname}'")
        except (AssertionError, TimeoutError):
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

        except (AssertionError, TimeoutError) as e:
            self.capture_screenshot(prefix="error_renewal_timeout")
            log.error("Timeout waiting for renewal confirmation")
            log.warning("The expiration banner did not disappear after clicking confirm")
            raise Exception("Failed to confirm hostname renewal - banner still visible")
        except Exception as e:
            self.capture_screenshot(prefix="error_renewal")
            log.error(f"Renewal process failed: {e}")
            raise Exception(f"Failed to renew hostname: {e}")

        try:
            screenshot_path = self.capture_screenshot(prefix="dns_renewal")
            return screenshot_path
        except Exception as e:
            log.error(f"Screenshot capture failed: {e}")
            raise Exception(f"Renewal succeeded but screenshot failed: {e}")
