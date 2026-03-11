from playwright.sync_api import Page, expect, TimeoutError
from .base import BasePage
from .records import RecordsPage
from config import dns_hostname
from logger import get_logger

log = get_logger("dashboard")


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dns_hostname_link = page.get_by_text(dns_hostname)
        log.debug(f"Dashboard page initialized for hostname: {dns_hostname}")

    def open_dns_record(self):
        """Open DNS record with validation"""
        try:
            log.debug(f"Looking for hostname link: {dns_hostname}")
            expect(self.dns_hostname_link).to_be_visible(timeout=10000)
            log.info(f"Hostname '{dns_hostname}' found on dashboard")
        except (AssertionError, TimeoutError):
            self.capture_screenshot(prefix="error_dashboard_hostname_not_found")
            log.error(f"Hostname '{dns_hostname}' not found on dashboard")
            raise Exception(
                f"DNS hostname '{dns_hostname}' not found on dashboard. "
                "Please verify the hostname exists in your No-IP account."
            )

        try:
            log.debug("Clicking on hostname link...")
            self.dns_hostname_link.click()
            self.page.wait_for_load_state("networkidle", timeout=15000)
            log.info("Successfully navigated to DNS records page")
        except Exception as e:
            self.capture_screenshot(prefix="error_dns_navigation")
            log.error(f"Failed to open DNS record: {e}")
            raise Exception(f"Failed to open DNS record: {e}")

        return RecordsPage(self.page)
