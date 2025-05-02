
import json
import re
import os
import google.generativeai as genai

# Configure Gemini API using environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")


def extract_fields_from_text(text: str) -> dict:
    prompt = f"""
    You are a data extraction assistant. Your job is to extract the following real estate property fields in **valid JSON format only**. For fields with no available value, return "Not mentioned".

    Fields to extract:
    - property_name
    - property_type (e.g., villa, apartment, penthouse)
    - developer
    - country
    - city
    - location
    - price
    - description (one summary sentence)
    - bedrooms
    - bathroom
    - area (e.g., "1000 sqft" or "1200 - 1500 sqft")
    - payment_plan
    - handover (e.g., "Q1 2026")
    - down_payment (e.g., "20%")
    - average_price_per_sqft (can be "N/A")

    Boolean fields (return only "yes" or "no"):
    - has_maid_room
    - has_air_conditioning
    - has_balcony_terrace
    - has_bult_in_wadrobes
    - has_walk_in_closet
    - has_health_care_center
    - has_kids_play_area
    - has_laundry
    - has_sauna
    - has_spa
    - has_indoor_pool
    - has_lobby_reception
    - has_concierge
    - has_prayer_room
    - has_parking
    - has_garden
    - has_shared_pool
    - has_landmark_views
    - has_tennis_cout
    - has_running_track
    - has_outdoor_dining
    - has_outdoor_gymnasium
    - has_bbq_area
    - is_pet_friendly

    Only return a clean JSON response. No explanations. Here is the brochure text:
    ---
    {text}
    """

    try:
        # Generate response from Gemini
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Attempt to parse entire response as JSON
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass  

        # Fallback: extract first JSON block using regex
        json_text = re.search(r"\{.*?\}", raw, re.DOTALL)
        if json_text:
            return json.loads(json_text.group())

        # If no valid JSON found
        return {"error": "Could not extract valid JSON from Gemini output."}

    except Exception as e:
        return {"error": str(e)}
      