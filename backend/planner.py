"""
Planner module for generating learning roadmaps using Ollama.
"""

import requests
import json
import logging

# Configure logger
logger = logging.getLogger(__name__)

def generate_roadmap(missing_skills: list, role_name: str) -> str:
    """
    Generates a 30-day learning roadmap using local Llama 3 via Ollama.
    
    Args:
        missing_skills: List of tuples (skill, score) - top missing skills.
        role_name: Target job role.
        
    Returns:
        String containing the roadmap or error message.
    """
    # Only take top 5 missing skills
    top_missing = [skill for skill, score in missing_skills[:5]]
    
    if not top_missing:
        return "No missing skills identified. You are well-aligned!"

    prompt = (
        f"Act as a career coach. Create a 30-day learning roadmap for a '{role_name}' role. "
        f"Focus specifically on learning these skills: {', '.join(top_missing)}. "
        "Provide a week-by-week plan. Be concise and actionable."
    )

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "temperature": 0.3,
        "stream": False
    }

    try:
        logger.info(f"Calling Ollama for {role_name} roadmap...")
        response = requests.post(url, json=payload, timeout=60) # 60s timeout
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "No response content from model.")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama request failed: {e}")
        return f"Planner unavailable: Could not connect to Ollama. {e}"
    except Exception as e:
        logger.error(f"An error occurred during roadmap generation: {e}")
        return f"Planner unavailable: {e}"
