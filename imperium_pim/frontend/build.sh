#!/bin/bash

# Build script for Next.js frontend integration with Frappe

echo "Building Next.js frontend for Frappe integration..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the Next.js app
echo "Building Next.js app..."
npm run build

# Create public directory structure for Frappe
echo "Setting up Frappe public directory structure..."
mkdir -p ../public

# Copy built assets to Frappe public directory
echo "Copying assets to Frappe public directory..."
if [ -d "build" ]; then
    # Copy the entire _next directory structure
    cp -r build/* ../public/
    echo "Assets copied successfully!"
    
    # List the copied files for verification
    echo "Copied files:"
    find ../public -type f -name "*.js" -o -name "*.css" | head -10
else
    echo "Build directory not found. Build may have failed."
    exit 1
fi

echo "Frontend build complete!"
echo "You can now access the PIM frontend at: /pim"
echo "Make sure to restart your Frappe server to pick up the new assets."
