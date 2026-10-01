"""Gemini AI Client Service with Multimodal Support, JSON Parsing, and Fallback Resilience.
"""

import json
import re
import logging
from typing import Optional, Union
from PIL import Image

from config import Config
from services import mock_catalog

logger = logging.getLogger(__name__)

# Initialize client placeholder
_client = None

def get_gemini_client():
    """Retrieve or initialize the Gemini client."""
    global _client
    if _client is not None:
        return _client
    
    api_key = Config.GEMINI_API_KEY
    if not api_key or api_key == "your_gemini_api_key_here":
        return None
        
    try:
        from google import genai
        _client = genai.Client(api_key=api_key)
        return _client
    except Exception as e:
        logger.error(f"Failed to initialize google.genai Client: {e}")
        return None


def clean_and_parse_json(text: str) -> Optional[dict]:
    """Extract and parse clean JSON from model output, handling markdown fences or leading whitespace."""
    if not text:
        return None
        
    # Remove markdown code block fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip(), flags=re.MULTILINE)
    
    # Locate first { and last }
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end+1]
        
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as err:
        logger.warning(f"Direct JSON parse failed: {err}. Attempting aggressive cleanup.")
        # Replace trailing commas
        cleaned_lenient = re.sub(r",\s*([\]}])", r"\1", cleaned)
        try:
            return json.loads(cleaned_lenient)
        except Exception:
            return None


def enforce_budget_limit(plan_data: dict, budget_limit: float) -> dict:
    """Ensure that the total estimated cost does not exceed the user's budget limit."""
    if not plan_data or "recommendations" not in plan_data:
        return plan_data
        
    items = plan_data.get("recommendations", [])
    total_cost = sum(float(item.get("price", 0.0)) for item in items)
    
    if total_cost > budget_limit and total_cost > 0:
        ratio = (budget_limit * 0.95) / total_cost
        for item in items:
            item["price"] = round(float(item.get("price", 0.0)) * ratio, 2)
        total_cost = sum(float(item.get("price", 0.0)) for item in items)
        
    plan_data["total_estimated_cost"] = round(total_cost, 2)
    plan_data["budget_limit"] = budget_limit
    return plan_data


class GeminiPlannerService:
    """Service wrapping Gemini multimodal interactions for the planners."""

    @classmethod
    def generate_home_plan(cls, room_type: str, style: str, budget: float, dimensions: str = "", extra_notes: str = "") -> dict:
        """Generate Home Interior Plan using Gemini 1.5 or fallback."""
        from services.prompt_templates import HOME_PLANNER_SYSTEM_PROMPT, build_home_planner_prompt
        
        client = get_gemini_client()
        user_prompt = build_home_planner_prompt(room_type, style, budget, dimensions, extra_notes)
        
        if client:
            try:
                from google.genai import types
                response = client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=HOME_PLANNER_SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.7
                    )
                )
                parsed = clean_and_parse_json(response.text)
                if parsed:
                    parsed["is_fallback"] = False
                    return enforce_budget_limit(parsed, budget)
            except Exception as e:
                logger.error(f"Gemini API call failed for Home Planner: {e}")
                if not Config.MOCK_FALLBACK_ON_ERROR:
                    raise
                    
        # Graceful fallback
        return mock_catalog.get_fallback_home_plan(room_type, style, budget, dimensions)

    @classmethod
    def generate_party_plan(cls, event_type: str, guest_count: int, budget: float, theme: str = "", dietary_notes: str = "") -> dict:
        """Generate Party Plan using Gemini 1.5 or fallback."""
        from services.prompt_templates import PARTY_PLANNER_SYSTEM_PROMPT, build_party_planner_prompt
        
        client = get_gemini_client()
        user_prompt = build_party_planner_prompt(event_type, guest_count, budget, theme, dietary_notes)
        
        if client:
            try:
                from google.genai import types
                response = client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=PARTY_PLANNER_SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.7
                    )
                )
                parsed = clean_and_parse_json(response.text)
                if parsed:
                    parsed["is_fallback"] = False
                    return enforce_budget_limit(parsed, budget)
            except Exception as e:
                logger.error(f"Gemini API call failed for Party Planner: {e}")
                if not Config.MOCK_FALLBACK_ON_ERROR:
                    raise

        # Graceful fallback
        return mock_catalog.get_fallback_party_plan(event_type, guest_count, budget, theme)

    @classmethod
    def generate_jewelry_plan(cls, occasion: str, budget: float, metal_preference: str = "Gold", 
                               outfit_description: str = "", outfit_image: Optional[Image.Image] = None) -> dict:
        """Generate Jewelry Plan with optional multimodal outfit image using Gemini 1.5 or fallback."""
        from services.prompt_templates import JEWELRY_PLANNER_SYSTEM_PROMPT, build_jewelry_planner_prompt
        
        client = get_gemini_client()
        has_image = outfit_image is not None
        user_prompt = build_jewelry_planner_prompt(occasion, budget, metal_preference, outfit_description, has_image)
        
        if client:
            try:
                from google.genai import types
                contents = [outfit_image, user_prompt] if has_image else [user_prompt]
                
                response = client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=JEWELRY_PLANNER_SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        temperature=0.7
                    )
                )
                parsed = clean_and_parse_json(response.text)
                if parsed:
                    parsed["is_fallback"] = False
                    return enforce_budget_limit(parsed, budget)
            except Exception as e:
                logger.error(f"Gemini API call failed for Jewelry Planner: {e}")
                if not Config.MOCK_FALLBACK_ON_ERROR:
                    raise

        # Graceful fallback
        return mock_catalog.get_fallback_jewelry_plan(occasion, budget, metal_preference, outfit_description)
