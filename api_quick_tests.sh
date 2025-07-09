#!/bin/bash

# Quick API Tests for Book Translation Service
# Individual curl commands for quick testing

API_BASE_URL="http://localhost:8000"

echo "Book Translation Service - Quick API Tests"
echo "========================================="
echo "API Base URL: $API_BASE_URL"
echo ""

# Test 1: Service Information
echo "1. Get Service Information:"
echo "curl $API_BASE_URL/"
curl -s "$API_BASE_URL/" | jq '.' 2>/dev/null || curl -s "$API_BASE_URL/"
echo ""

# Test 2: Get Models
echo "2. Get Supported Models:"
echo "curl $API_BASE_URL/models"
curl -s "$API_BASE_URL/models" | jq '.' 2>/dev/null || curl -s "$API_BASE_URL/models"
echo ""

# Test 3: Authentication Status
echo "3. Check Authentication Status:"
echo "curl $API_BASE_URL/auth/status"
curl -s "$API_BASE_URL/auth/status" | jq '.' 2>/dev/null || curl -s "$API_BASE_URL/auth/status"
echo ""

# Test 4: Get User Info (Mock Mode)
echo "4. Get User Info (Mock Mode):"
echo "curl $API_BASE_URL/auth/user-info"
curl -s "$API_BASE_URL/auth/user-info" | jq '.' 2>/dev/null || curl -s "$API_BASE_URL/auth/user-info"
echo ""

# Test 5: Validate Translation Parameters
echo "5. Validate Translation Parameters:"
echo "curl '$API_BASE_URL/translate/validate?model=openai&language=zh-hans'"
curl -s "$API_BASE_URL/translate/validate?model=openai&language=zh-hans" | jq '.' 2>/dev/null || curl -s "$API_BASE_URL/translate/validate?model=openai&language=zh-hans"
echo ""

# Test 6: Start Translation Job
echo "6. Start Translation Job:"
echo "curl -X POST $API_BASE_URL/translate/start -H 'Content-Type: application/json' -d '{...}'"
curl -s -X POST "$API_BASE_URL/translate/start" \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "/workspace/books/test_book.epub",
    "model": "openai",
    "language": "zh-hans",
    "test_mode": true,
    "test_num": 3
  }' | jq '.' 2>/dev/null || curl -s -X POST "$API_BASE_URL/translate/start" \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "/workspace/books/test_book.epub",
    "model": "openai",
    "language": "zh-hans",
    "test_mode": true,
    "test_num": 3
  }'
echo ""

# Test 7: Get All Jobs
echo "7. Get All Translation Jobs:"
echo "curl $API_BASE_URL/translate/jobs"
curl -s "$API_BASE_URL/translate/jobs" | jq '.' 2>/dev/null || curl -s "$API_BASE_URL/translate/jobs"
echo ""

echo "========================================="
echo "Individual Test Commands:"
echo ""
echo "# Service Info"
echo "curl $API_BASE_URL/"
echo ""
echo "# Models"
echo "curl $API_BASE_URL/models"
echo ""
echo "# Auth Status"
echo "curl $API_BASE_URL/auth/status"
echo ""
echo "# User Info"
echo "curl $API_BASE_URL/auth/user-info"
echo ""
echo "# Validate Parameters"
echo "curl '$API_BASE_URL/translate/validate?model=openai&language=zh-hans'"
echo ""
echo "# Start Translation"
echo "curl -X POST $API_BASE_URL/translate/start \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"book_path\": \"/path/to/book.epub\", \"model\": \"openai\", \"language\": \"zh-hans\", \"test_mode\": true}'"
echo ""
echo "# Get All Jobs"
echo "curl $API_BASE_URL/translate/jobs"
echo ""
echo "# Get Specific Job (replace JOB_ID)"
echo "curl $API_BASE_URL/translate/jobs/JOB_ID"
echo ""
echo "# With Authentication Token"
echo "curl -H 'Authorization: Bearer YOUR_TOKEN' $API_BASE_URL/auth/user-info"
echo ""
echo "# Interactive Documentation"
echo "Open $API_BASE_URL/docs in your browser"
echo ""
echo "# Alternative Documentation"
echo "Open $API_BASE_URL/redoc in your browser"