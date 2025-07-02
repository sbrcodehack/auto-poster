#!/bin/bash

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers in user directory (non-root)
PLAYWRIGHT_BROWSERS_PATH=0 python -m playwright install chromium
