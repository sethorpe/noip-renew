from models import LoginPage
from playwright.sync_api import (
    sync_playwright,
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
)
import sys
import traceback
from browser_config import (
    get_browser_config,
    get_context_config,
    BROWSER_TYPE,
    print_browser_config,
)
from logger import get_logger

log = get_logger("main")


def main():
    from config import print_config_summary

    log.info("=" * 60)
    log.info("No-IP Hostname Renewal Script Started")
    log.info("=" * 60)

    print_config_summary()
    print()
    print_browser_config()
    print()

    browser = None
    try:
        with sync_playwright() as p:
            log.info("Launching browser...")

            # Get the browser based on config
            browser_launcher = getattr(p, BROWSER_TYPE)
            browser = browser_launcher.launch(**get_browser_config())
            log.debug(f"Browser launched: {BROWSER_TYPE}")

            # Create a context with configuration
            context = browser.new_context(**get_context_config())
            page = context.new_page()
            log.debug("Browser context and page created")

            log.info("Logging into No-IP...")
            records_page = (
                LoginPage(page).navigate().login().enter_auth_code().open_dns_record()
            )

            log.info("Successfully navigated to DNS records page")
            log.info("Renewing hostname...")
            screenshot_path = records_page.renew_hostname()

            log.info("Hostname renewal completed successfully")
            log.info(f"Screenshot saved to: {screenshot_path}")

            browser.close()
            log.info("Browser closed")
            log.info("=" * 60)
            log.info("Script completed successfully")
            log.info("=" * 60)
            return 0

    except PlaywrightTimeoutError as e:
        log.error("Timeout Error: An element took too long to load")
        log.error(f"Details: {e}")
        log.warning("This might indicate a network issue or page structure change")
        return 1

    except PlaywrightError as e:
        log.error(f"Playwright Error: {e}")
        log.warning("This might indicate an issue with browser automation")
        return 1

    except Exception as e:
        log.error(f"Unexpected Error: {type(e).__name__}")
        log.error(f"Message: {e}")
        log.debug("Full traceback:", exc_info=True)
        return 1

    finally:
        if browser:
            try:
                browser.close()
                log.debug("Browser cleanup completed")
            except Exception as e:
                log.warning(f"Error during browser cleanup: {e}")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
