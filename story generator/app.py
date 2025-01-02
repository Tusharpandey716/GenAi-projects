from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load GPT-2 model for text generation
story_generator = pipeline("text-generation", model="gpt2", framework="pt")

@app.route('/')
def home():
    return "Welcome to the GPT-2 Story Generator API. Use the `/generate` endpoint with a POST request."

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/generate', methods=['POST'])
def generate_story():
    try:
        # Parse JSON data from the POST request
        data = request.json
        genre = data.get("genre", "fantasy")
        prompt = data.get("prompt", "Once upon a time")
        
        # Append genre to the prompt for context
        full_prompt = f"{genre} story: {prompt}"
        
        # Generate a story using GPT-2
        output = story_generator(full_prompt, max_length=150, num_return_sequences=1)
        story = output[0]['generated_text']
        
        # Return the generated story as a JSON response
        return jsonify({"story": story})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
