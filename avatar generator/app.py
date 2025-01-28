from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = "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"

@app.route('/generate-avatar', methods=['POST'])
def generate_avatar():
    try:
        data = request.json
        description = data.get('description', 'a cartoon avatar with a friendly face')
        
        # Use OpenAI's new method to generate images
        response = openai.Image.create_edit(
            prompt=description,
            n=1,
            size="512x512"
        )
        avatar_url = response['data'][0]['url']
        
        return jsonify({"avatar_url": avatar_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)