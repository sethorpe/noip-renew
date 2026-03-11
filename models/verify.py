from playwright.sync_api import Page, expect, TimeoutError
from config import otp_secret
from .base import BasePage
from .dashboard import DashboardPage
import pyotp
from logger import get_logger

log = get_logger("verify")


class VerifyPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.two_factor_auth_dialog = page.locator("#sign-up-wrap")
        self.header = page.get_by_role("heading", name="Two-Factor Authentication")
        self.verify_button = page.get_by_role("button", name="Verify")
        self.otp_inputs = page.locator("#totp-input input")

        try:
            log.debug("Waiting for 2FA page to load...")
            expect(self.header).to_be_visible(timeout=10000)
            log.info("2FA page loaded successfully")
        except (AssertionError, TimeoutError):
            log.error("Failed to reach 2FA page - page not found")
            raise Exception(
                "Failed to reach 2FA page. "
                "This might indicate incorrect login credentials or page structure change."
            )

    def _generate_otp(self):
        """Generate OTP code with validation"""
        if not otp_secret:
            log.error("OTP_SECRET is not configured")
            raise ValueError("OTP_SECRET is not configured")

        try:
            log.debug("Generating OTP code...")
            totp = pyotp.TOTP(otp_secret)
            code = totp.now()

            if not code or len(code) != 6 or not code.isdigit():
                log.error(f"Generated invalid OTP code: {code}")
                raise ValueError(f"Generated invalid OTP code: {code}")

            log.debug(f"OTP code generated: {code[:2]}****")
            return code
        except Exception as e:
            log.error(f"OTP generation failed: {e}")
            raise Exception(f"Failed to generate OTP: {e}")

    def enter_auth_code(self):
        """Enter OTP code with validation"""
        otp = self._generate_otp()

        input_count = self.otp_inputs.count()
        log.debug(f"Found {input_count} OTP input fields")

        if input_count == 0:
            log.error("No OTP input fields found on page")
            raise Exception(
                "No OTP input fields found on page. Page structure may have changed."
            )

        if input_count != 6:
            log.error(f"Expected 6 OTP inputs, found {input_count}")
            raise Exception(
                f"Expected 6 OTP input fields, found {input_count}. "
                "Page structure may have changed."
            )

        try:
            log.debug("Filling OTP input fields...")
            for i in range(input_count):
                self.otp_inputs.nth(i).fill(otp[i])
            log.info("OTP entered successfully")
        except Exception as e:
            log.error(f"Failed to fill OTP field {i+1}: {e}")
            raise Exception(f"Failed to fill OTP input field {i+1}: {e}")

        try:
            log.debug("Clicking verify button...")
            self.verify_button.click()
            self.page.wait_for_load_state("networkidle", timeout=15000)
            log.info("2FA verification successful, redirected to dashboard")
        except (AssertionError, TimeoutError):
            self.capture_screenshot(prefix="error_2fa_timeout")
            log.error("Verify button timeout - OTP may be incorrect or expired")
            raise Exception(
                "Verify button click failed or page took too long to load. "
                "OTP may be incorrect or expired."
            )

        return DashboardPage(self.page)
