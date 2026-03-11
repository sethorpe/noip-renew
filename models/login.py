from playwright.sync_api import Page, TimeoutError
from .base import BasePage
from .verify import VerifyPage
from config import noip_password, noip_username
from logger import get_logger

log = get_logger("login")


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_field = page.locator("#username")
        self.password_field = page.locator("#password")
        self.login_button = page.get_by_role("button", name="Log In")

    def navigate(self):
        """Navigate to login page"""
        try:
            log.debug("Navigating to No-IP login page...")
            self.page.goto("https://www.noip.com/login", timeout=30000)
            self.page.wait_for_load_state("networkidle", timeout=30000)
            log.info("Successfully loaded login page")
        except TimeoutError:
            log.error("Failed to load No-IP login page - timeout")
            raise Exception(
                "Failed to load No-IP login page. "
                "Please check your internet connection."
            )
        except Exception as e:
            log.error(f"Navigation failed: {e}")
            raise Exception(f"Navigation to login page failed: {e}")

        return self

    def login(self):
        """Login with credentials"""
        if not noip_username or not noip_password:
            log.error("Username or password not configured")
            raise ValueError("Username or password not configured")

        try:
            log.debug(f"Filling credentials for user: {noip_username}")
            self.username_field.fill(noip_username)
            self.password_field.fill(noip_password)
            self.login_button.click()
            log.debug("Login form submitted, waiting for page load...")
            self.page.wait_for_load_state("networkidle", timeout=15000)
            log.info("Login successful, redirected to 2FA page")
        except TimeoutError:
            self.capture_screenshot(prefix="error_login_timeout")
            log.error("Login timeout - credentials may be incorrect")
            raise Exception(
                "Login failed or took too long. "
                "Please verify credentials are correct."
            )
        except Exception as e:
            self.capture_screenshot(prefix="error_login")
            log.error(f"Login submission failed: {e}")
            raise Exception(f"Failed to submit login form: {e}")

        return VerifyPage(self.page)
