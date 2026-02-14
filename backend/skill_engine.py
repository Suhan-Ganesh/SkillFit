"""
Skill extraction and demand scoring engine.
No NLP libraries, no regex complexity.
"""

def extract_skills_from_text(text: str, skills: list) -> list:
    """
    Extracts skills from text using case-insensitive substring matching.
    
    Args:
        text: Job description text.
        skills: List of skill keywords to look for.
        
    Returns:
        List of unique matching skills found in the text.
    """
    if not text:
        return []
    
    # Normalize text to lowercase
    text_lower = text.lower()
    
    found_skills = []
    for skill in skills:
        # Simple substring match as per requirements
        if skill in text_lower:
            found_skills.append(skill)
            
    return found_skills

def compute_demand_scores(job_descriptions: list, skills: list) -> dict:
    """
    Computes demand scores for skills based on frequency across job descriptions.
    
    Args:
        job_descriptions: List of job description strings.
        skills: List of all possible skills.
        
    Returns:
        Dictionary mapping skill to demand score (0.0 to 1.0).
    """
    if not job_descriptions:
        return {}
        
    total_jobs = len(job_descriptions)
    skill_counts = {skill: 0 for skill in skills}
    
    for desc in job_descriptions:
        # Get unique skills per job description
        found = extract_skills_from_text(desc, skills)
        for skill in found:
            skill_counts[skill] += 1
            
    demand_scores = {}
    for skill, count in skill_counts.items():
        if count > 0:
            score = count / total_jobs
            demand_scores[skill] = round(score, 3)
            
    return demand_scores
