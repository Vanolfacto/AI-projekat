from flask import Flask, request, render_template, redirect, flash
import requests
from transformers import pipeline
from waitress import serve
from deep_translator import GoogleTranslator


app = Flask(__name__)
app.secret_key = 'tajni_kljuc'

NARUTO_API_URL = "https://narutodb.xyz/api/character/1344"  
CURRENT_TOKEN = 50

chatbot = pipeline("text-generation", model="gpt2")  

conversation_history = []

@app.route('/')
def home():
    return render_template('index.html', conversation_history=conversation_history)

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    
# Prevod korisničkog unosa na engleski
    translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)


    headers = {'Authorization': f'Bearer {CURRENT_TOKEN}'}
    response = requests.get(NARUTO_API_URL)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'name' in data:
            naruto_name = data['name']
            
            context = f"""Naruto Uzumaki is the main character from the anime and manga 'Naruto' He is brave, persistent, and never gives up. His goal is to become Hokage and protect his friends and village. Naruto is known for his enthusiasm, humorous remarks, but also deep emotional moments.
                         Naruto responds to the user using his characteristic way of speaking – energetic, sometimes impulsive, but always honest. He uses phrases like "Dattebayo!" when he's excited. He can be serious when the topic is important but also playful when the situation allows it.
                        Naruto draws from his childhood experiences, training, and battles. His responses are inspiring, full of confidence, and reflect his strong will. He believes in friendship and that anything can be achieved through hard work.
                        Naruto responds only to the user and ignores any other characters or entities. His responses are clear, direct, and in line with his personality.
               User: {translated_input}  Naruto:"""  
            naruto_response = chatbot(
                context,
                max_new_tokens=int(CURRENT_TOKEN),
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                truncation=True,
                pad_token_id=50256
            )[0]['generated_text']
            
            naruto_response = naruto_response.replace("User:", "").strip()

            if "Naruto:" in naruto_response:
                naruto_response = naruto_response.split("Naruto:")[1].strip()
            else:
                naruto_response = "Naruto nije odgovorio na očekivani način."
        else:
            naruto_response = "Došlo je do greške sa API-jem."
    else:
        naruto_response = "Greška sa API-jem."
    
    # Prevod odgovora nazad na srpski
    translated_response = GoogleTranslator(source='en', target='sr').translate(naruto_response)

    conversation_history.append(f"User: {user_input}")
    conversation_history.append(f"Naruto: {translated_response}")

    return render_template('index.html', user_input=user_input, naruto_response=naruto_response, conversation_history=conversation_history)


@app.route('/set_token', methods=['POST'])
def set_token():
    global CURRENT_TOKEN
    try:
        new_token = int(request.form['token'])
        if 50 <= new_token <= 500:
            CURRENT_TOKEN = new_token
            flash(f"Token je uspešno postavljen na {CURRENT_TOKEN}!", "success")
        else:
            flash("Token mora biti između 50 i 500.", "error")
    except ValueError:
        flash("Uneta vrednost nije validna.", "error")
    return redirect('/')

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    global conversation_history
    conversation_history = []
    flash("Razgovor je obrisan!", "info")
    return redirect('/')

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)