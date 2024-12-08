# Using OpenAI GPT-3.5 for natural language meal recommendation:
# https://platform.openai.com/docs/models

# AI nutrition recommendation using a deep generative model and ChatGPT
# https://www.nature.com/articles/s41598-024-65438-x

import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
# https://platform.openai.com/docs/quickstart
os.environ["OPENAI_API_KEY"] = "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"

# Create the OpenAI client
# https://platform.openai.com/docs/quickstart
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

user_profiles = {}

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for collecting user preferences
@app.route('/collect_preferences', methods=['POST'])
def collect_preferences():
    user_id = request.json.get('user_id')
    preferences = request.json.get('preferences')
    allergies = request.json.get('allergies')
    dietary_restrictions = request.json.get('dietary_restrictions')
    dislikes = request.json.get('dislikes')

    # Save user profile
    # (not needed just thought I would add incase I wanted to take this project further with a database)
    user_profiles[user_id] = {
        "preferences": preferences,
        "allergies": allergies,
        "dietary_restrictions": dietary_restrictions,
        "dislikes": dislikes,
    }
    return jsonify({'success': True, 'message': 'Preferences collected successfully!'})

# Route to handle food recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = request.json.get('user_id')
    user_input = request.json.get('input')

    # Retrieve user profile
    # (not needed just thought I would add incase I wanted to take this project further with a database)
    user_profile = user_profiles.get(user_id, {})
    preferences = user_profile.get('preferences', "No preferences")
    allergies = user_profile.get('allergies', "No allergies")
    dietary_restrictions = user_profile.get('dietary_restrictions', "No restrictions")
    dislikes = user_profile.get('dislikes', "No dislikes")

    try:
        # Generate food recommendations
        # This provides all the requirements my project stated
        # https://platform.openai.com/docs/quickstart
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a helpful AI food assistant. Based on the user's preferences ({preferences}), "
                        f"allergies ({allergies}), dietary restrictions ({dietary_restrictions}), and dislikes ({dislikes}), "
                        f"generate multiple meal suggestions with detailed recipes and shopping lists. Ensure compliance with "
                        f"the user's dietary restrictions and allergies. Do not suggest anything harmful to the user."
                    )
                },
                {
                    "role": "user",
                    "content": f"{user_input}. Provide at least three meal suggestions with detailed recipes and shopping lists."
                }
            ],
            max_tokens=1000  # Token limit increased since were doing multiple meals
        )
        result = chat_completion.choices[0].message.content.strip()
        return jsonify({'success': True, 'response': result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Route for collecting feedback 
@app.route('/feedback', methods=['POST'])
def feedback():
    user_id = request.json.get('user_id')
    feedback = request.json.get('feedback')

    print(f"Feedback from user {user_id}: {feedback}")
    return jsonify({'success': True, 'message': 'Thank you for your feedback!'})

# Run app
if __name__ == '__main__':
    app.run(debug=True)
