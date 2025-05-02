
# 🏡 Smart PDF Property Parser – Backend

This is a FastAPI backend service for extracting structured real estate property data from PDF brochures using Google's Gemini API (Gemini 1.5 Pro).

It receives a PDF file, extracts text using PyMuPDF, and sends it to Gemini to return a clean JSON of fields like `price`, `location`, `bedrooms`, and more.

---

## 🚀 Features

- 📄 PDF parsing using PyMuPDF
- 🤖 AI-powered field extraction via Gemini API
- 📦 Clean JSON output with standardized property fields
- 🌐 CORS-enabled to connect with frontend (e.g., Vercel)
- 🧪 Error-handling and validation included

---

## 🛠️ Tech Stack

- **FastAPI** – Web framework  
- **Google Generative AI** – Gemini API for intelligent parsing  
- **PyMuPDF** – Lightweight PDF text extraction  
- **Uvicorn** – ASGI server  
- **Python-Dotenv** – Environment variable loading

---

## 📂 Folder Structure

```
backend/
│
├── main.py                   # FastAPI entry point
├── requirements.txt          # Dependency list
├── .env                      # API key config (not pushed to GitHub)
│
├── utils/
│   └── field_extractor.py    # Gemini JSON extractor
│
├── services/
    └── pdf_reader.py         # PDF text extraction logic
```

---

## 📦 Getting Started (Local)

```bash
# 1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Gemini API key
echo "GEMINI_API_KEY=sk-..." > .env

# 4. Run the server
uvicorn main:app --reload
```

---

## 📡 API Endpoint

### `POST /parse-pdf`

- **Request:** `multipart/form-data` with a `file` (PDF)
- **Response:** JSON object with extracted property fields

```bash
curl -X 'POST'   'http://127.0.0.1:8000/parse-pdf'   -F 'file=@sample.pdf'
```

---

## 🌐 Deployment Notes

- Hosted on [Render](https://render.com)
- Add `GEMINI_API_KEY` to the environment variables
- Start command: `uvicorn main:app --host=0.0.0.0 --port=10000`

