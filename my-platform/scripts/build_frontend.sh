#!/bin/bash

# Frontend Build Script for PIM Platform
# This script builds the Next.js frontend and exports static files

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo -e "${GREEN}🚀 Building PIM Frontend...${NC}"

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ Frontend directory not found: $FRONTEND_DIR${NC}"
    exit 1
fi

cd "$FRONTEND_DIR"

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ package.json not found in frontend directory${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
npm ci --silent

echo -e "${YELLOW}🔍 Running type check...${NC}"
npm run type-check

echo -e "${YELLOW}🧹 Running linter...${NC}"
npm run lint

echo -e "${YELLOW}🏗️  Building Next.js application...${NC}"
npm run build

# Check if build was successful
if [ ! -d "out" ]; then
    echo -e "${RED}❌ Build failed - 'out' directory not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Frontend build completed successfully!${NC}"
echo -e "${GREEN}📁 Static files are ready in: $FRONTEND_DIR/out${NC}"

# Display build statistics
if [ -d "out" ]; then
    FILE_COUNT=$(find out -type f | wc -l)
    TOTAL_SIZE=$(du -sh out | cut -f1)
    echo -e "${GREEN}📊 Build stats: $FILE_COUNT files, $TOTAL_SIZE total${NC}"
fi

echo -e "${GREEN}🎉 Frontend build process completed!${NC}"

