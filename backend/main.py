"""
FastAPI Entry Point for Market Alignment Engine.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
import json
from typing import List, Dict

# Import modules
import config
import data_loader
import skill_engine
import gap_engine
import planner

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("MarketEngine")

app = FastAPI(title="Market Alignment Engine")

class AnalyzeRequest(BaseModel):
    role_name: str
    resume_text: str

@app.post("/analyze")
def analyze_market_fit(request: AnalyzeRequest):
    role_name = request.role_name
    resume_text = request.resume_text
    
    logger.info(f"Starting analysis for role: {role_name}")
    
    # 1. Load Dataset & Filter
    logger.info("[INFO] Loading dataset...")
    try:
        job_descriptions = data_loader.load_and_filter_jobs(role_name, limit=500)
        logger.info(f"Loaded {len(job_descriptions)} job descriptions.")
    except Exception as e:
        logger.error(f"Data loading failed: {e}")
        # If dataset is missing, we can't do much.
        raise HTTPException(status_code=500, detail=f"Data loading failed: {e}")
        
    if not job_descriptions:
        raise HTTPException(status_code=404, detail=f"No job postings found for role: {role_name}")

    # 2. Demand Scores (Compute or Load)
    clean_role_name = "".join(c for c in role_name if c.isalnum() or c in (' ', '_')).replace(' ', '_').lower()
    score_file = f"demand_scores_{clean_role_name}.json"
    
    demand_scores = {}
    
    if os.path.exists(score_file):
        logger.info(f"[INFO] Loading cached demand scores from {score_file}...")
        try:
            with open(score_file, 'r') as f:
                demand_scores = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load cache, recomputing. Error: {e}")
            
    if not demand_scores:
        logger.info("[INFO] Computing demand scores...")
        demand_scores = skill_engine.compute_demand_scores(job_descriptions, config.SKILLS)
        # Save cache
        try:
            with open(score_file, 'w') as f:
                json.dump(demand_scores, f)
            logger.info(f"Saved demand scores to {score_file}")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    # 3. Extract Candidate Skills
    logger.info("Extracting candidate skills...")
    candidate_skills = skill_engine.extract_skills_from_text(resume_text, config.SKILLS)
    logger.info(f"Found {len(candidate_skills)} candidate skills.")

    # 4. Rank Missing Skills
    logger.info("Ranking skill gaps...")
    # missing_skills_list is list of (skill, score)
    missing_skills_list = gap_engine.rank_skill_gaps(candidate_skills, demand_scores)
    
    # Format output
    # Top 10 demanded (general context)
    sorted_demand = sorted(demand_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    top_demanded_fmt = [{"skill": k, "score": v} for k, v in sorted_demand]
    
    missing_skills_fmt = [{"skill": k, "score": v} for k, v in missing_skills_list]

    # 5. Generate Roadmap
    logger.info("[INFO] Calling Llama planner...")
    roadmap = planner.generate_roadmap(missing_skills_list, role_name)

    return {
        "top_demanded_skills": top_demanded_fmt,
        "candidate_skills": candidate_skills,
        "missing_skills": missing_skills_fmt,
        "roadmap": roadmap
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
