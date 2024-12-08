import os
from openai import OpenAI


# Original Code

os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_food_details(user_preferences):
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI food assistant."},
            {"role": "user", "content": f"Provide a detailed meal suggestion, including a recipe, and shopping list based on the following preferences: {user_preferences}"}
        ],
        max_tokens=500  #response length
    )
    
    return chat_completion.choices[0].message.content.strip()

#user preferences
preferences = "I am halal, I like spicy food, perfer my food to be seasoned well, i am vegan"

food_details = get_food_details(preferences)
print(food_details)
