#!/bin/bash

# Google Workspace CLI Setup Script
# This script helps you authenticate with Google Workspace

set -e

echo "🌐 Google Workspace CLI Authentication"
echo "========================================"
echo ""

# Check if gws is installed
if ! command -v gws &> /dev/null; then
    echo "❌ Error: gws is not installed"
    echo "Run: npm install -g @googleworkspace/cli"
    exit 1
fi

echo "✅ gws CLI is installed ($(gws --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+'))"
echo ""

# Check if config directory exists
if [ ! -d "$HOME/.config/gws" ]; then
    echo "📁 Creating config directory..."
    mkdir -p "$HOME/.config/gws"
    echo "✅ Created $HOME/.config/gws"
    echo ""
fi

# Check if credentials exist
if [ ! -f "$HOME/.config/gws/client_secret.json" ]; then
    echo "⚠️  OAuth credentials not found!"
    echo ""
    echo "You need to set up OAuth credentials first:"
    echo ""
    echo "1. Go to: https://console.cloud.google.com/"
    echo "2. Create/select a project"
    echo "3. Enable APIs: Drive, Gmail, Calendar, Sheets, Docs"
    echo "4. Create OAuth consent screen (External, add yourself as test user)"
    echo "5. Create OAuth Client ID (Desktop app)"
    echo "6. Download the JSON file"
    echo ""
    echo "Then save it to:"
    echo "   $HOME/.config/gws/client_secret.json"
    echo ""
    read -p "Do you have the client_secret JSON file? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter the full path to your client_secret JSON file: " secret_path
        
        if [ -f "$secret_path" ]; then
            cp "$secret_path" "$HOME/.config/gws/client_secret.json"
            echo "✅ Credentials saved!"
            echo ""
        else
            echo "❌ File not found: $secret_path"
            exit 1
        fi
    else
        echo ""
        echo "Please complete the OAuth setup first, then run this script again."
        echo "See: /Users/mde/bug creation/GOOGLE_WORKSPACE_MCP_SETUP.md"
        exit 1
    fi
fi

echo "✅ OAuth credentials found"
echo ""

# Authenticate
echo "🔐 Starting authentication..."
echo ""
echo "This will open a browser window."
echo "If you see 'Google hasn't verified this app', click Advanced → Continue"
echo ""
read -p "Press Enter to continue..."

# Run authentication with specific services to avoid scope limits
gws auth login -s drive,gmail,calendar,sheets,docs

echo ""
echo "================================"
echo "✅ Authentication Complete!"
echo "================================"
echo ""
echo "Test your connection:"
echo "  gws drive files list --params '{\"pageSize\": 5}'"
echo ""
echo "Now you can use Google Workspace with AI in Cursor!"
