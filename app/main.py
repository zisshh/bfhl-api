from typing import List
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field


class DataRequest(BaseModel):
    data: List[str] = Field(..., description="Array of strings to process")


class BFHLResponse(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str


APP_TITLE = "BFHL API"
APP_DESCRIPTION = (
    "REST API that processes an input array and returns categorized values, "
    "following the BFHL brief."
)

app = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION, version="0.1.0")


def _load_user_config() -> tuple[str, str, str]:
    full_name = os.getenv("BFHL_FULL_NAME", "john_doe").lower()
    dob_ddmmyyyy = os.getenv("BFHL_DOB_DDMMYYYY", "17091999")
    user_id = f"{full_name}_{dob_ddmmyyyy}"

    email = os.getenv("BFHL_EMAIL", "john@xyz.com")
    roll_number = os.getenv("BFHL_ROLL_NUMBER", "ABCD123")
    return user_id, email, roll_number


def _alternating_caps_from_reversed_letters(letters: List[str]) -> str:
    # Reverse the sequence of letters first
    rev = list(reversed(letters))
    # Apply alternating caps starting with uppercase
    out_chars: List[str] = []
    for idx, ch in enumerate(rev):
        out_chars.append(ch.upper() if idx % 2 == 0 else ch.lower())
    return "".join(out_chars)


@app.post("/bfhl", response_model=BFHLResponse, tags=["bfhl"])
def process_bfhl(request: DataRequest) -> BFHLResponse:
    try:
        user_id, email, roll_number = _load_user_config()

        odd_numbers: List[str] = []
        even_numbers: List[str] = []
        alphabets: List[str] = []
        special_characters: List[str] = []

        total_sum = 0
        alpha_letters: List[str] = []  # Collect alphabetical characters for concat logic

        for item in request.data:
            # Ensure item is a string
            if not isinstance(item, str):
                raise ValueError(f"All data items must be strings, got {type(item)}")
            
            # Classify each element
            if item.isdigit():
                # Numeric-only string
                try:
                    num_val = int(item)
                    total_sum += num_val
                    if num_val % 2 == 0:
                        even_numbers.append(item)
                    else:
                        odd_numbers.append(item)
                except ValueError:
                    # If conversion fails, treat as special character
                    special_characters.append(item)
            elif item.isalpha():
                # Alphabet-only string
                upper_item = item.upper()
                alphabets.append(upper_item)
                alpha_letters.extend(list(upper_item))
            else:
                # Anything else is considered special characters
                special_characters.append(item)

        concat_string = _alternating_caps_from_reversed_letters(alpha_letters)

        return BFHLResponse(
            is_success=True,
            user_id=user_id,
            email=email,
            roll_number=roll_number,
            odd_numbers=odd_numbers,
            even_numbers=even_numbers,
            alphabets=alphabets,
            special_characters=special_characters,
            sum=str(total_sum),
            concat_string=concat_string,
        )
    
    except Exception as e:
        # Return error response with is_success=False
        user_id, email, roll_number = _load_user_config()
        return BFHLResponse(
            is_success=False,
            user_id=user_id,
            email=email,
            roll_number=roll_number,
            odd_numbers=[],
            even_numbers=[],
            alphabets=[],
            special_characters=[],
            sum="0",
            concat_string="",
        )


# Optional local dev entry-point
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


# -------- Convenience endpoints (root + health) --------

@app.get("/", include_in_schema=False)
def root() -> HTMLResponse:
    html = (
        "<html><head><title>BFHL API</title></head><body>"
        "<h1>BFHL API</h1>"
        "<p>Welcome! This service exposes a single endpoint:</p>"
        "<ul><li><code>POST /bfhl</code> — process your input array</li></ul>"
        "<p>Interactive docs: <a href=\"/docs\">/docs</a></p>"
        "</body></html>"
    )
    return HTMLResponse(content=html)


@app.get("/healthz", include_in_schema=False)
def healthz() -> JSONResponse:
    return JSONResponse({"status": "ok"})
