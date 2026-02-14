"""
Gap engine for ranking missing skills.
"""

def rank_skill_gaps(candidate_skills: list, demand_scores: dict) -> list:
    """
    Identifies and ranks missing skills based on market demand.
    
    Args:
        candidate_skills: List of skills the candidate possesses.
        demand_scores: Dictionary of {skill: score} from the market.
        
    Returns:
        List of tuples (skill, score) for missing skills, sorted by score descending.
    """
    # Normalize candidate skills to lowercase for comparison
    candidate_set = set(s.lower() for s in candidate_skills)
    
    missing_skills = []
    
    for skill, score in demand_scores.items():
        if skill not in candidate_set:
            missing_skills.append((skill, score))
            
    # Sort by score descending
    missing_skills.sort(key=lambda x: x[1], reverse=True)
    
    return missing_skills
