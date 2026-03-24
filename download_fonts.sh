#!/bin/bash
# Download correct Google Fonts for MagicTales text overlays
# Run this script to replace corrupted font files

set -e

echo "Downloading Google Fonts for MagicTales..."
echo "================================================"

# Create fonts directory if it doesn't exist
mkdir -p fonts

# Dancing Script
echo "Downloading Dancing Script..."
curl -L "https://fonts.google.com/download?family=Dancing%20Script" -o fonts/DancingScript.zip
unzip -o fonts/DancingScript.zip "static/DancingScript-Regular.ttf" -d fonts/
mv fonts/static/DancingScript-Regular.ttf fonts/DancingScript-Regular.ttf
rm -rf fonts/static fonts/DancingScript.zip

# Playfair Display
echo "Downloading Playfair Display..."
curl -L "https://fonts.google.com/download?family=Playfair%20Display" -o fonts/PlayfairDisplay.zip
unzip -o fonts/PlayfairDisplay.zip "static/PlayfairDisplay-Regular.ttf" -d fonts/
mv fonts/static/PlayfairDisplay-Regular.ttf fonts/PlayfairDisplay-Regular.ttf
rm -rf fonts/static fonts/PlayfairDisplay.zip

# Cormorant Garamond Regular
echo "Downloading Cormorant Garamond Regular..."
curl -L "https://fonts.google.com/download?family=Cormorant%20Garamond" -o fonts/CormorantGaramond.zip
unzip -o fonts/CormorantGaramond.zip "CormorantGaramond-Regular.ttf" -d fonts/
rm -f fonts/CormorantGaramond.zip

# Cormorant Garamond Bold
echo "Extracting Cormorant Garamond Bold..."
curl -L "https://fonts.google.com/download?family=Cormorant%20Garamond" -o fonts/CormorantGaramond.zip
unzip -o fonts/CormorantGaramond.zip "CormorantGaramond-Bold.ttf" -d fonts/
rm -f fonts/CormorantGaramond.zip

echo ""
echo "================================================"
echo "✅ Font download complete!"
echo ""
echo "Verifying fonts..."
file fonts/*.ttf

echo ""
echo "Next steps:"
echo "1. Verify all fonts show 'TrueType Font' (not HTML)"
echo "2. git add fonts/"
echo "3. git commit -m 'Fix: Replace corrupted HTML files with actual font files'"
echo "4. git push"
echo "5. Redeploy to production"
