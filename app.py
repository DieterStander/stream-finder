from flask import Flask, render_template, request
import google.generativeai as genai
import json

app = Flask(__name__)

# Your OpenAI API key here
genai.configure(api_key="AIzaSyBOcB46n0xeq27752rpFgBZhLptyaLSJuI")
model = genai.GenerativeModel(model_name="gemini-1.0-pro")

def query_chatgpt(sport):
    prompt = f'Which public broadcasters stream the {sport} for free to citizens in specific regions? Give five possibilities and prioritize English broadcasts. Try to exclude broadcasts where a paid subscription is required. Output the information in JSON format with the following structure: [{{"Country":"example_country", "Broadcaster":"example_broadcaster", "Website":"example_url", "Description":"example description"}}, {{"Country":"example_country", "Broadcaster":"example_broadcaster", "Website":"example_url", "Description":"example description"}}]'

    try:
        response = model.generate_content([prompt])
        # Extract JSON from the response
        json_text = response.candidates[0].content.parts[0].text
        json_text = json_text.strip("```json\n").strip("```")  # Remove leading and trailing "```"
        result = json.loads(json_text)  # Parse the JSON string into a Python object
        print(result)
        return result
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sport = request.form.get('sport')
        result = query_chatgpt(sport)
        return render_template('index.html', result=result, sport=sport)
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(port=5001)