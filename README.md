# BFHL FastAPI Service

A FastAPI backend that implements the `/bfhl` POST endpoint according to the project brief. This service processes arrays and returns categorized data including numbers, alphabets, special characters, and computed values.

## Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup and Installation

1. **Create and activate a virtual environment:**

   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate (Windows PowerShell)
   .venv\Scripts\Activate.ps1
   
   # Activate (Windows Command Prompt)
   .venv\Scripts\activate.bat
   
   # Activate (macOS/Linux)
   source .venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   # Production dependencies
   pip install -r requirements.txt
   
   # Or install development dependencies (includes testing tools)
   pip install -r requirements-dev.txt
   ```

3. **Configure user details (Optional):**

   Set environment variables to customize the API response:
   ```bash
   # Windows PowerShell
   $env:BFHL_FULL_NAME = "john_doe"
   $env:BFHL_DOB_DDMMYYYY = "17091999"
   $env:BFHL_EMAIL = "john@xyz.com"
   $env:BFHL_ROLL_NUMBER = "ABCD123"
   
   # macOS/Linux
   export BFHL_FULL_NAME="john_doe"
   export BFHL_DOB_DDMMYYYY="17091999"
   export BFHL_EMAIL="john@xyz.com"
   export BFHL_ROLL_NUMBER="ABCD123"
   ```

4. **Start the server:**

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API:**
   - API Base URL: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

### Test Suite Overview

The project includes comprehensive tests that validate the API against all requirements from the project brief. The test suite covers:

1. **Example A**: Basic mixed data processing (`["a", "1", "334", "4", "R", "$"]`)
2. **Example B**: Complex data with multiple types (`["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"]`)
3. **Example C**: Alphabet-only data (`["A", "ABcD", "DOE"]`)
4. **Edge Cases**: Empty data arrays and invalid request formats
5. **Error Handling**: Malformed requests and server error scenarios

### Running Tests

#### Prerequisites
```bash
# Install development dependencies (if not already done)
pip install -r requirements-dev.txt
```

#### Run All Tests
```bash
# Basic test run
pytest

# Verbose output with detailed results
pytest -v

# Run with coverage report
pytest --cov=app

# Run specific test file
pytest tests/test_bfhl.py

# Run specific test function
pytest tests/test_bfhl.py::test_example_a
```

#### Test Output Example
```
======================================== test session starts =========================================
platform win32 -- Python 3.12.7, pytest-8.4.1
rootdir: C:\Users\thkr\bfhl-api
configfile: pytest.ini
collected 5 items

tests/test_bfhl.py::test_example_a PASSED                                                       [ 20%]
tests/test_bfhl.py::test_example_b PASSED                                                       [ 40%]
tests/test_bfhl.py::test_example_c PASSED                                                       [ 60%]
tests/test_bfhl.py::test_empty_data PASSED                                                      [ 80%]
tests/test_bfhl.py::test_invalid_request_format PASSED                                          [100%]

========================================= 5 passed in 0.31s =========================================
```

### Test Cases Explained

#### test_example_a
**Input**: `["a", "1", "334", "4", "R", "$"]`

**Validates**:
- Odd numbers: `["1"]`
- Even numbers: `["334", "4"]`
- Alphabets: `["A", "R"]` (converted to uppercase)
- Special characters: `["$"]`
- Sum: `"339"` (1 + 334 + 4)
- Concatenation: `"Ra"` (R,a reversed → a,R → A,r alternating case)

#### test_example_b
**Input**: `["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"]`

**Validates**:
- Complex data processing with multiple categories
- Sum calculation: `"103"` (2 + 4 + 5 + 92)
- Concatenation: `"ByA"` (a,y,b → b,y,a → B,y,A alternating case)

#### test_example_c
**Input**: `["A", "ABcD", "DOE"]`

**Validates**:
- Alphabet-only processing
- Complex concatenation: `"EoDdCbAa"` (A,A,B,c,D,D,O,E → E,O,D,D,C,B,A,A → E,o,D,d,C,b,A,a)
- Empty arrays for numbers and special characters

#### test_empty_data
**Input**: `[]`

**Validates**:
- Handling of empty input arrays
- All response arrays are empty
- Sum is "0"
- concat_string is empty

#### test_invalid_request_format
**Input**: Invalid JSON structure

**Validates**:
- Error handling for malformed requests
- Proper HTTP 422 status code
- is_success: false in error responses

### Manual Testing Scenarios

After starting the server (`uvicorn app.main:app --reload`), you can test these scenarios:

1. **Valid Request** (should return 200):
   ```bash
   curl -X POST "http://localhost:8000/bfhl" \
        -H "Content-Type: application/json" \
        -d '{"data": ["test", "123", "@"]}'
   ```

2. **Invalid Request** (should return 422):
   ```bash
   curl -X POST "http://localhost:8000/bfhl" \
        -H "Content-Type: application/json" \
        -d '{"invalid": "data"}'
   ```

3. **Empty Data** (should return 200):
   ```bash
   curl -X POST "http://localhost:8000/bfhl" \
        -H "Content-Type: application/json" \
        -d '{"data": []}'
   ```

## Examples

### Example 1: Mixed Data Processing
```bash
# Request
curl -X POST "http://localhost:8000/bfhl" \
     -H "Content-Type: application/json" \
     -d '{"data": ["a", "1", "334", "4", "R", "$"]}'

# Response
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["1"],
  "even_numbers": ["334", "4"],
  "alphabets": ["A", "R"],
  "special_characters": ["$"],
  "sum": "339",
  "concat_string": "Ra"
}
```

### Example 2: Complex Data with Multiple Categories
```bash
# Request
curl -X POST "http://localhost:8000/bfhl" \
     -H "Content-Type: application/json" \
     -d '{"data": ["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"]}'

# Response
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["5"],
  "even_numbers": ["2", "4", "92"],
  "alphabets": ["A", "Y", "B"],
  "special_characters": ["&", "-", "*"],
  "sum": "103",
  "concat_string": "ByA"
}
```

### Example 3: Alphabet-Only Data
```bash
# Request
curl -X POST "http://localhost:8000/bfhl" \
     -H "Content-Type: application/json" \
     -d '{"data": ["A", "ABcD", "DOE"]}'

# Response
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": [],
  "even_numbers": [],
  "alphabets": ["A", "ABCD", "DOE"],
  "special_characters": [],
  "sum": "0",
  "concat_string": "EoDdCbAa"
}
```

## Project Structure

```
thkr/
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI application and endpoints
├── tests/
│   ├── __init__.py
│   └── test_bfhl.py         # Test suite for the API
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies (includes testing)
├── pytest.ini             # Pytest configuration
├── README.md               # This file
└── PROJECT_BRIEF.md        # Original project requirements
```

## Dependencies

### Production Dependencies
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and settings management

### Development Dependencies
- **pytest**: Testing framework
- **httpx**: HTTP client for testing FastAPI applications

## Error Handling

The API includes comprehensive error handling:

- **422 Unprocessable Entity**: Invalid request format or missing required fields
- **500 Internal Server Error**: Server-side processing errors
- **is_success field**: Indicates operation status in all responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite to ensure all tests pass
6. Submit a pull request

## License

This project is created for educational purposes as part of a coding assignment.

### Endpoint Details

**POST** `/bfhl`

Processes an array of mixed data and returns categorized results.

#### Request Format
```json
{
  "data": ["a", "1", "334", "4", "R", "$"]
}
```

#### Response Format
```json
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["1"],
  "even_numbers": ["334", "4"],
  "alphabets": ["A", "R"],
  "special_characters": ["$"],
  "sum": "339",
  "concat_string": "Ra"
}
```

### How to Send Requests

#### 1. Using Swagger UI (Recommended for Testing)

1. Start the server (see Quick Start above)
2. Open http://localhost:8000/docs in your browser
3. Click on the `/bfhl` POST endpoint
4. Click "Try it out"
5. Replace the example request body with your data:
   ```json
   {
     "data": ["your", "data", "here", "1", "2", "$"]
   }
   ```
6. Click "Execute"
7. View the response below

#### 2. Using curl (Command Line)

```bash
# Example request
curl -X POST "http://localhost:8000/bfhl" \
     -H "Content-Type: application/json" \
     -d '{"data": ["a", "1", "334", "4", "R", "$"]}'

# Expected response
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["1"],
  "even_numbers": ["334", "4"],
  "alphabets": ["A", "R"],
  "special_characters": ["$"],
  "sum": "339",
  "concat_string": "Ra"
}
```

#### 3. Using PowerShell (Windows)

```powershell
# Example request
$body = @{
    data = @("a", "1", "334", "4", "R", "$")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/bfhl" `
                  -Method Post `
                  -Body $body `
                  -ContentType "application/json"
```

#### 4. Using Python requests

```python
import requests

# Example request
response = requests.post(
    "http://localhost:8000/bfhl",
    json={"data": ["a", "1", "334", "4", "R", "$"]}
)

print("Status Code:", response.status_code)
print("Response:", response.json())
```

### Response Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `is_success` | boolean | Indicates if the operation was successful |
| `user_id` | string | User identifier in format `{full_name_ddmmyyyy}` |
| `email` | string | User's email address |
| `roll_number` | string | User's roll number |
| `odd_numbers` | array | All odd numbers from input (as strings) |
| `even_numbers` | array | All even numbers from input (as strings) |
| `alphabets` | array | All alphabetic strings converted to uppercase |
| `special_characters` | array | All non-alphanumeric characters |
| `sum` | string | Sum of all numeric values (returned as string) |
| `concat_string` | string | Alphabetic characters reversed with alternating case |

### Data Processing Logic

1. **Numbers**: Classified as odd or even, included in sum calculation
2. **Alphabets**: Converted to uppercase, individual characters used for concatenation
3. **Special Characters**: Any non-alphanumeric characters
4. **Concatenation**: Alphabetic characters are reversed and formatted with alternating case (starting uppercase)

