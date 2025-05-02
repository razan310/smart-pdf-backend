import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))


from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.field_extractor import extract_fields_from_text
from services.pdf_reader import extract_text_from_pdf


app = FastAPI()


# Enable CORS for allowed frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://.*vercel\.app",
                   ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse-pdf")
async def parse_pdf(file: UploadFile = File(...)):
    temp_path = "temp.pdf"
    try:
        # Save uploaded PDF temporarily
        contents = await file.read()
        with open(temp_path, "wb") as f:
            f.write(contents)

        # Extract text from PDF
        raw_text = extract_text_from_pdf(temp_path)

        # Extract fields from brochure text
        fields = extract_fields_from_text(raw_text)

        # Handle extraction errors from Gemini
        if "error" in fields:
            raise HTTPException(status_code=422, detail=fields["error"])

        return {"data": fields}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)