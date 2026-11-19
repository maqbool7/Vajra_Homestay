import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)
client = genai.Client()

HOTEL_CONTEXT = """
You are the helpful virtual assistant for 'Vajara Homestay' located in Coastal Hills, California.
- Check-in: 3:00 PM | Check-out: 11:00 AM
- Rooms: Deluxe Double ($59/night), Deluxe Single ($59/night), Superior Room ($59/night).
- Amenities: Outdoor swimming pool, Spa & Wellness Center, 24/7 Room Service, Free Parking, Pet Friendly, Free High Speed Wifi, Dynamic Breakfast.
- Contact: phone (+1-800-555-0199), email (info@vjarahomestay.com).
Please keep answers friendly, concise, and accurate to these details.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/amenities')
def amenities():
    return render_template('amenities.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'Please enter a question.'})

    try:
        prompt = f"{HOTEL_CONTEXT}\nGuest Question: {user_message}\nAnswer:"
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"Sorry, I had trouble processing that request. ({str(e)})"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)