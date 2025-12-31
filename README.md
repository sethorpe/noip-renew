# No-IP Hostname Renewal Automation

Automated renewal of No-IP hostnames using Playwright and Python. This script logs into your No-IP account, handles 2FA authentication, and renews your hostname(s) to prevent expiration.

## Features

- Automated login with username/password
- Two-factor authentication (2FA) support using TOTP
- Configurable browser settings (headless, viewport, etc.)
- Comprehensive error handling and logging
- Screenshot capture after renewal
- GitHub Actions workflow for scheduled execution
- Environment-based configuration

## Requirements

- Python 3.13+
- Poetry (for dependency management)
- A No-IP account with TOTP 2FA enabled

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sethorpe/noip-automation.git
cd noip-automation
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

4. Configure your environment variables (see Configuration section below)

5. Install Playwright browser (installs the browser specified in your `.env` file):
```bash
poetry run python setup.py
```

## Configuration

Create a `.env` file with the following variables:

### Required Variables

```bash
# No-IP Credentials
DNS_HOSTNAME=your-hostname.ddns.net
NOIP_USERNAME=your-email@example.com
NOIP_PASSWORD=your-password
OTP_SECRET=YOUR_TOTP_SECRET_KEY
```

### Optional Browser Configuration

```bash
# Browser Settings (defaults shown)
HEADLESS=true
BROWSER_TYPE=chromium
SLOW_MOTION=0
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080
SCREENSHOT_DIR=.

# Timeouts (milliseconds)
DEFAULT_TIMEOUT=30000
NAVIGATION_TIMEOUT=30000
ACTION_TIMEOUT=15000

# Logging
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Usage

### Local Execution

Run the script locally:

```bash
poetry run python main.py
```

For debugging, set `HEADLESS=false` in your `.env` file to watch the browser automation.

### GitHub Actions (Scheduled)

The project includes a GitHub Actions workflow that runs automatically on the 1st of every month.

#### Setup GitHub Actions:

1. Push this repository to GitHub

2. Add the following secrets to your repository:
   - Go to: Settings → Secrets and variables → Actions
   - Add these repository secrets:
     - `DNS_HOSTNAME`
     - `NOIP_USERNAME`
     - `NOIP_PASSWORD`
     - `OTP_SECRET`

3. The workflow will run automatically on schedule, or you can trigger it manually:
   - Go to: Actions → No-IP Hostname Renewal → Run workflow

4. Screenshots from each run are saved as artifacts (90-day retention)

## How It Works

1. **Login**: Navigates to No-IP login page and submits credentials
2. **2FA**: Generates TOTP code and enters it in the verification form
3. **Navigate**: Finds your hostname on the dashboard
4. **Renew**: Clicks the renewal confirmation button
5. **Capture**: Takes a screenshot of the result
6. **Log**: All actions are logged for debugging

## Project Structure

```
noip-automation/
├── .github/
│   └── workflows/
│       └── noip-renewal.yml    # GitHub Actions workflow
├── models/                      # Page Object Model classes
│   ├── __init__.py
│   ├── login.py                # Login page
│   ├── verify.py               # 2FA verification page
│   ├── dashboard.py            # Dashboard page
│   └── records.py              # DNS records page
├── browser_config.py           # Browser configuration
├── config.py                   # Environment configuration
├── logger.py                   # Logging setup
├── main.py                     # Main entry point
├── .env.example                # Example environment file
├── .gitignore
├── pyproject.toml              # Poetry dependencies
└── README.md
```

## Logging

Logs are written to both console and file:
- **Console**: Simple, readable output
- **File**: Detailed logs in `logs/noip_automation_TIMESTAMP.log`

Set `LOG_LEVEL=DEBUG` for detailed debugging information.

## Troubleshooting

### Common Issues

**"Missing required environment variable"**
- Ensure all required variables are set in your `.env` file

**"Failed to reach 2FA page"**
- Verify your username and password are correct
- Check if No-IP has changed their login page structure

**"OTP may be incorrect or expired"**
- Verify your `OTP_SECRET` is correct
- Ensure your system time is synchronized

**"Expiration banner not found"**
- Your hostname might already be renewed
- Hostname might not be expiring within 7 days

### Debug Mode

Run with debug logging to see detailed information:

```bash
LOG_LEVEL=DEBUG poetry run python main.py
```

Watch the browser in action:

```bash
HEADLESS=false poetry run python main.py
```

## Security Considerations

- **Never commit your `.env` file** - It contains sensitive credentials
- **Use GitHub Secrets** for CI/CD - Never hardcode credentials
- **Rotate your OTP secret** if compromised
- **Review screenshots** before sharing - They may contain sensitive information

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is for personal use only. Use at your own risk. The authors are not responsible for any issues that may arise from using this automation tool.

## Acknowledgments

- Built with [Playwright](https://playwright.dev/)
- TOTP implementation using [PyOTP](https://github.com/pyauth/pyotp)
- Dependency management with [Poetry](https://python-poetry.org/)
