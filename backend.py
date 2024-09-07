from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# Initialize Supabase client
SUPABASE_URL = 'your_supabase_url'
SUPABASE_KEY = 'your_supabase_key'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch profiles
def fetch_profiles(student_id):
    student_profile = supabase.from('students').select('*').eq('id', student_id).single()
    alumni_profiles = supabase.from('alumni_profiles').select('*')
    return student_profile['data'], alumni_profiles['data']

# Match students with alumni
def recommend_alumni(student_profile, alumni_profiles):
    recommendations = []
    for alumni in alumni_profiles:
        common_skills = set(student_profile['skills']).intersection(alumni['skills'])
        if student_profile['industry'] == alumni['industry'] or \
           student_profile['specialization'] == alumni['specialization'] or \
           common_skills:
            recommendations.append(alumni)
    return recommendations

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    student_id = data['student_id']
    
    # Fetch student and alumni profiles
    student_profile, alumni_profiles = fetch_profiles(student_id)
    
    # Get recommendations
    recommended_alumni = recommend_alumni(student_profile, alumni_profiles)
    
    if recommended_alumni:
        return jsonify({"recommended_alumni": recommended_alumni})
    else:
        return jsonify({"message": "No relevant alumni found"})

if __name__ == '__main__':
    app.run(debug=True)
