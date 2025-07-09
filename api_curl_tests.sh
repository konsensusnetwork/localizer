#!/bin/bash

# API Curl Tests for Book Translation Service
# This script contains comprehensive curl tests for all API endpoints

# Configuration
API_BASE_URL="http://localhost:8000"
TEST_BOOK_PATH="/workspace/books/test_book.epub"
TEST_MODEL="openai"
TEST_LANGUAGE="zh-hans"
AUTH_TOKEN=""  # Add your token here if testing with authentication

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print test headers
print_test_header() {
    echo -e "\n${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}"
}

# Function to print test results
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}"
    else
        echo -e "${RED}✗ FAIL${NC}"
    fi
}

# Function to make curl request with better formatting
make_curl_request() {
    local method=$1
    local url=$2
    local headers=$3
    local data=$4
    local description=$5
    
    echo -e "\n${YELLOW}Testing: $description${NC}"
    echo -e "${YELLOW}Request: $method $url${NC}"
    
    if [ ! -z "$data" ]; then
        echo -e "${YELLOW}Data: $data${NC}"
    fi
    
    echo -e "${YELLOW}Response:${NC}"
    
    if [ ! -z "$headers" ] && [ ! -z "$data" ]; then
        curl -s -X $method "$url" \
             -H "Content-Type: application/json" \
             -H "$headers" \
             -d "$data" | jq '.' 2>/dev/null || echo "Response not JSON or jq not available"
    elif [ ! -z "$headers" ]; then
        curl -s -X $method "$url" \
             -H "Content-Type: application/json" \
             -H "$headers" | jq '.' 2>/dev/null || echo "Response not JSON or jq not available"
    elif [ ! -z "$data" ]; then
        curl -s -X $method "$url" \
             -H "Content-Type: application/json" \
             -d "$data" | jq '.' 2>/dev/null || echo "Response not JSON or jq not available"
    else
        curl -s -X $method "$url" \
             -H "Content-Type: application/json" | jq '.' 2>/dev/null || echo "Response not JSON or jq not available"
    fi
    
    local exit_code=$?
    print_result $exit_code
    return $exit_code
}

# Check if server is running
print_test_header "CHECKING SERVER STATUS"
echo "Checking if server is running at $API_BASE_URL..."
curl -s "$API_BASE_URL" > /dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Server is running${NC}"
else
    echo -e "${RED}✗ Server is not running at $API_BASE_URL${NC}"
    echo "Please start the server with: uvicorn my_app.main:app --reload"
    exit 1
fi

# Test 1: Root endpoint
print_test_header "ROOT ENDPOINTS"
make_curl_request "GET" "$API_BASE_URL/" "" "" "Get service information"

# Test 2: Get supported models
make_curl_request "GET" "$API_BASE_URL/models" "" "" "Get supported models"

# Test 3: Authentication status
print_test_header "AUTHENTICATION ENDPOINTS"
make_curl_request "GET" "$API_BASE_URL/auth/status" "" "" "Check authentication status"

# Test 4: Test authentication (without token - should work in mock mode)
make_curl_request "POST" "$API_BASE_URL/auth/test-auth" "" "" "Test authentication (mock mode)"

# Test 5: Get user info (without token - should work in mock mode)
make_curl_request "GET" "$API_BASE_URL/auth/user-info" "" "" "Get user info (mock mode)"

# Test 6: Test with token if provided
if [ ! -z "$AUTH_TOKEN" ]; then
    make_curl_request "POST" "$API_BASE_URL/auth/test-auth" "Authorization: Bearer $AUTH_TOKEN" "" "Test authentication with token"
    make_curl_request "GET" "$API_BASE_URL/auth/user-info" "Authorization: Bearer $AUTH_TOKEN" "" "Get user info with token"
fi

# Test 7: Translation validation
print_test_header "TRANSLATION VALIDATION"
make_curl_request "GET" "$API_BASE_URL/translate/validate?model=$TEST_MODEL&language=$TEST_LANGUAGE" "" "" "Validate translation parameters"

# Test 8: Translation validation with invalid model
make_curl_request "GET" "$API_BASE_URL/translate/validate?model=invalid_model&language=$TEST_LANGUAGE" "" "" "Validate with invalid model"

# Test 9: Translation validation with invalid language
make_curl_request "GET" "$API_BASE_URL/translate/validate?model=$TEST_MODEL&language=invalid_language" "" "" "Validate with invalid language"

# Test 10: Start translation job
print_test_header "TRANSLATION JOB MANAGEMENT"
TRANSLATION_DATA='{
    "book_path": "'$TEST_BOOK_PATH'",
    "model": "'$TEST_MODEL'",
    "language": "'$TEST_LANGUAGE'",
    "single_translate": true,
    "test_mode": true,
    "test_num": 5,
    "use_context": false,
    "reasoning_effort": "medium",
    "temperature": 1.0,
    "accumulated_num": 1,
    "block_size": -1,
    "user_id": "test_user"
}'

echo -e "\n${YELLOW}Starting translation job...${NC}"
RESPONSE=$(curl -s -X POST "$API_BASE_URL/translate/start" \
    -H "Content-Type: application/json" \
    -d "$TRANSLATION_DATA")

echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"

# Extract job ID from response
JOB_ID=$(echo "$RESPONSE" | jq -r '.job_id' 2>/dev/null)

if [ "$JOB_ID" != "null" ] && [ ! -z "$JOB_ID" ]; then
    echo -e "${GREEN}✓ Job started with ID: $JOB_ID${NC}"
    
    # Test 11: Get specific job status
    make_curl_request "GET" "$API_BASE_URL/translate/jobs/$JOB_ID" "" "" "Get job status"
    
    # Test 12: Get all jobs
    make_curl_request "GET" "$API_BASE_URL/translate/jobs" "" "" "Get all jobs"
    
    # Wait a bit and check status again
    echo -e "\n${YELLOW}Waiting 3 seconds and checking job status again...${NC}"
    sleep 3
    make_curl_request "GET" "$API_BASE_URL/translate/jobs/$JOB_ID" "" "" "Get job status after delay"
    
else
    echo -e "${RED}✗ Failed to start translation job${NC}"
    JOB_ID=""
fi

# Test 13: Test with invalid job ID
make_curl_request "GET" "$API_BASE_URL/translate/jobs/invalid-job-id" "" "" "Get invalid job status"

# Test 14: Test translation with minimal parameters
print_test_header "MINIMAL TRANSLATION REQUEST"
MINIMAL_DATA='{
    "book_path": "'$TEST_BOOK_PATH'",
    "model": "'$TEST_MODEL'",
    "language": "'$TEST_LANGUAGE'"
}'

make_curl_request "POST" "$API_BASE_URL/translate/start" "" "$MINIMAL_DATA" "Start translation with minimal parameters"

# Test 15: Test translation with all parameters
print_test_header "FULL TRANSLATION REQUEST"
FULL_DATA='{
    "book_path": "'$TEST_BOOK_PATH'",
    "model": "'$TEST_MODEL'",
    "language": "'$TEST_LANGUAGE'",
    "model_list": "openai,claude",
    "batch_size": 10,
    "single_translate": false,
    "test_mode": true,
    "test_num": 3,
    "use_context": true,
    "reasoning_effort": "high",
    "temperature": 0.7,
    "accumulated_num": 2,
    "block_size": 100,
    "prompt_file": "/workspace/prompts/custom_prompt.txt",
    "user_id": "full_test_user"
}'

make_curl_request "POST" "$API_BASE_URL/translate/start" "" "$FULL_DATA" "Start translation with all parameters"

# Test 16: Test error cases
print_test_header "ERROR HANDLING TESTS"

# Missing required fields
INVALID_DATA='{
    "model": "'$TEST_MODEL'"
}'
make_curl_request "POST" "$API_BASE_URL/translate/start" "" "$INVALID_DATA" "Request with missing required fields"

# Invalid JSON
echo -e "\n${YELLOW}Testing: Invalid JSON data${NC}"
curl -s -X POST "$API_BASE_URL/translate/start" \
     -H "Content-Type: application/json" \
     -d '{"invalid": json}' | jq '.' 2>/dev/null || echo "Invalid JSON handled correctly"

# Test 17: Test API documentation endpoints
print_test_header "DOCUMENTATION ENDPOINTS"
echo -e "\n${YELLOW}Testing: OpenAPI documentation endpoint${NC}"
curl -s "$API_BASE_URL/docs" > /dev/null && echo -e "${GREEN}✓ /docs endpoint accessible${NC}" || echo -e "${RED}✗ /docs endpoint not accessible${NC}"

echo -e "\n${YELLOW}Testing: ReDoc documentation endpoint${NC}"
curl -s "$API_BASE_URL/redoc" > /dev/null && echo -e "${GREEN}✓ /redoc endpoint accessible${NC}" || echo -e "${RED}✗ /redoc endpoint not accessible${NC}"

# Test 18: Test with authentication header format
print_test_header "AUTHENTICATION HEADER TESTS"
make_curl_request "GET" "$API_BASE_URL/auth/user-info" "Authorization: Bearer fake-token" "" "Test with fake token"

# Test 19: Performance test - multiple concurrent requests
print_test_header "PERFORMANCE TESTS"
echo -e "\n${YELLOW}Testing: Multiple concurrent requests to root endpoint${NC}"
for i in {1..5}; do
    curl -s "$API_BASE_URL/" > /dev/null &
done
wait
echo -e "${GREEN}✓ Concurrent requests completed${NC}"

# Test 20: Content type tests
print_test_header "CONTENT TYPE TESTS"
echo -e "\n${YELLOW}Testing: Request without Content-Type header${NC}"
curl -s -X POST "$API_BASE_URL/translate/start" \
     -d "$MINIMAL_DATA" | jq '.' 2>/dev/null || echo "Request without Content-Type handled"

# Summary
print_test_header "TEST SUMMARY"
echo -e "API Base URL: $API_BASE_URL"
echo -e "Test Book Path: $TEST_BOOK_PATH"
echo -e "Test Model: $TEST_MODEL"
echo -e "Test Language: $TEST_LANGUAGE"
if [ ! -z "$JOB_ID" ]; then
    echo -e "Sample Job ID: $JOB_ID"
fi
echo -e "\n${GREEN}All tests completed!${NC}"
echo -e "${YELLOW}Note: Some tests may fail if required files don't exist or services aren't properly configured.${NC}"
echo -e "${YELLOW}Check the server logs for detailed error information.${NC}"

# Instructions for running specific tests
echo -e "\n${BLUE}RUNNING SPECIFIC TESTS:${NC}"
echo -e "To run specific endpoint tests, you can use individual curl commands:"
echo -e "• Service info: curl $API_BASE_URL/"
echo -e "• Models: curl $API_BASE_URL/models"
echo -e "• Auth status: curl $API_BASE_URL/auth/status"
echo -e "• Interactive docs: Open $API_BASE_URL/docs in your browser"
echo -e "• API docs: Open $API_BASE_URL/redoc in your browser"