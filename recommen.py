import numpy as np
from supabase import create_client, Client

# Initialize Supabase client
SUPABASE_URL = 'your_supabase_url'
SUPABASE_KEY = 'your_supabase_key'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch student and alumni profiles
def fetch_profiles():
    # Fetch student profile
    student_profile = supabase.from('students').select('*').single()
    
    # Fetch all alumni profiles
    alumni_profiles = supabase.from('alumni_profiles').select('*')
    
    return student_profile['data'], alumni_profiles['data']

# Match students with alumni based on shared attributes
def recommend_alumni(student_profile, alumni_profiles):
    recommendations = []

    for alumni in alumni_profiles:
        # Calculate similarity based on skills
        common_skills = set(student_profile['skills']).intersection(alumni['skills'])
        
        # Match based on industry and specialization
        if student_profile['industry'] == alumni['industry'] or \
           student_profile['specialization'] == alumni['specialization'] or \
           common_skills:
            recommendations.append(alumni)
    
    return recommendations

# Main function
def main():
    # Fetch profiles
    student_profile, alumni_profiles = fetch_profiles()
    
    # Recommend alumni
    recommended_alumni = recommend_alumni(student_profile, alumni_profiles)
    
    if recommended_alumni:
        print("Recommended Alumni Profiles:")
        for alumni in recommended_alumni:
            print(f"Name: {alumni['name']}, Industry: {alumni['industry']}, Skills: {', '.join(alumni['skills'])}")
    else:
        print("No relevant alumni found based on the current profile.")

if __name__ == '__main__':
    main()
