#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright dependencies and browsers
playwright install --with-deps
