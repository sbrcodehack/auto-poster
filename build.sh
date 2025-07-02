#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers without sudo/root
python -m playwright install --with-deps
