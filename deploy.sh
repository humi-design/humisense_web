#!/bin/bash
# HUMISENSE Deployment Script for cPanel
# Run this script to set up and deploy the application

set -e

echo "=========================================="
echo "HUMISENSE Deployment Script"
echo "=========================================="

# Get the directory where the script is located
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

echo "Working directory: $APP_DIR"

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
else
    echo "Virtual environment already exists."
fi

# Step 2: Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Step 4: Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Step 5: Install MySQL client libraries
echo "Installing MySQL client libraries..."
pip install mysqlclient pymysql cryptography || pip install pymysql cryptography

# Step 6: Create logs directory
echo "Creating logs directory..."
mkdir -p logs
chmod 755 logs

# Step 7: Set permissions
echo "Setting permissions..."
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
chmod 755 passenger_wsgi.py
chmod 755 deploy.sh

# Step 8: Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure your settings."
fi

echo "=========================================="
echo "Deployment setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Make sure your .env file is configured"
echo "2. Restart the Python app in cPanel Setup Python App"
echo "3. Check logs/error.log for any errors"
echo ""
