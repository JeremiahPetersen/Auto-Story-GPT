from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os
import json
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Set OpenAI API key from environment variable
openai.api_key  = os.getenv('OPENAI_API_KEY')

# Create a Flask web server
app = Flask(__name__)
# Enable CORS for the Flask app
CORS(app)

# Dictionary to hold multiple conversations. Each conversation corresponds to a different bot.
conversations = {}

# Function to get the last 500 words from a conversation.
def get_last_500_words(conversation):
    all_words = " ".join([m["content"] for m in conversation])
    return " ".join(all_words.split()[-500:])

# Function to call OpenAI API for a conversation and return the model's response.
def get_completion(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.4,
    )
    return response.choices[0].message["content"]

# Route to get the personality prompt for a given bot
@app.route('/api/get_personal_prompt', methods=['GET'])
def get_personal_prompt():
    bot_id = request.args.get('bot_id')
    with open('static/personalities.json') as f:
        personalities = json.load(f)['Personalities']
    if bot_id not in personalities:
        return jsonify({"error": "Bot id not found"}), 404
    return jsonify({"prompt": personalities[bot_id]})

# Main landing page
@app.route('/')
def index():
    return render_template('main.html')

# Route to generate the AI's response given a story and story idea
@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        bot_id = data.get('bot_id')
        model = data.get('model', 'gpt-3.5-turbo')
        story = data.get('story')  # get the story from the request
        story_idea = data.get('story_idea')  # get the story idea from the request

        with open('static/personalities.json') as f:
            personalities = json.load(f)['Personalities']
        if bot_id not in personalities:
            return jsonify({"error": "Bot id not found"}), 404

        character_prompt = personalities[bot_id]

        if bot_id not in conversations:
            conversations[bot_id] = [{"role": "assistant", "content": character_prompt}]
        conversation = conversations[bot_id]

        # Combine the story idea with the story
        conversation.append({"role": "user", "content": story_idea + ' ' + story})  
        
        response = get_completion(conversation, model)
        conversation.append({"role": "assistant", "content": response})

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to reset the conversation for a given bot
@app.route('/api/reset', methods=['POST'])
def reset():
    data = request.get_json()
    bot_id = data.get('bot_id')
    if bot_id in conversations:
        conversations[bot_id] = []
    return jsonify({"status": "conversation reset"})

# Route to delete the last response of the bot
@app.route('/api/delete_last', methods=['POST'])
def delete_last():
    data = request.get_json()
    bot_id = data.get('bot_id')
    if bot_id in conversations and len(conversations[bot_id]) > 0:
        conversations[bot_id].pop()
    return jsonify({"status": "last response deleted"})

@app.route('/api/adjust_continuity', methods=['POST'])
def adjust_continuity():
    data = request.get_json()
    story = data.get('story')
    prompt = f'Your task is to do 2 things.  First, check this story for continuity or logic issues. The second thing is to adjust the story so it fixes any continuity or logic issues you found.  Retain as much of the original story as possible, but make the edits needed to fix continuity and logic issues.  Your output should only be the new adjusted story.\n\nStory:\n\n{story}'

    response = get_completion([{ "role": "system", "content": "You are a helpful assistant." }, { "role": "user", "content": prompt }])

    return jsonify({"response": response})

@app.route('/api/rewrite_story', methods=['POST'])
def rewrite_story():
    data = request.get_json()
    story = data.get('story')
    prompt = f'Your task is to rewrite this story and make it better.  Fix any errors, and rewrite the story in the style of professional and popular fiction novels.  Use appropriate structure, punctuation, and grammar, similar to what you would see in a New York Times bestseller novel.  The language should be intelligent, and easy to read.  The story should be captivating, and make sense.\n\nStory:\n\n{story}'

    response = get_completion([{ "role": "system", "content": "You are a helpful assistant." }, { "role": "user", "content": prompt }])

    return jsonify({"response": response})

# Run the Flask app on port 5005 with debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5000)
