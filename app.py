from flask import Flask, request, render_template, redirect, flash
import requests
from transformers import pipeline
from waitress import serve
from deep_translator import GoogleTranslator


app = Flask(__name__)
app.secret_key = 'tajni_kljuc'

NARUTO_API_URL = "https://narutodb.xyz/api/character/1344"
BATMAN_API_URL = "https://narutodb.xyz/api/character/1344"
GANDALF_API_URL = "https://narutodb.xyz/api/character/1344"  

CURRENT_TOKEN = 50

chatbot = pipeline("text-generation", model="gpt2")  

conversation_historyN = []
conversation_historyB = []
conversation_historyG = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Naruto')
def naruto():
    return render_template('index.html', conversation_historyN=conversation_historyN)

@app.route('/Batman')
def batman():
    return render_template('batman.html', conversation_historyB=conversation_historyB)

@app.route('/Gandalf')
def gandalf():
    return render_template('gandalf.html', conversation_historyG=conversation_historyG)

#Funkcija za generisanje odgovora za lika
@app.route('/askNaruto', methods=['POST'])
def askNaruto():
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

    conversation_historyN.append(f"User: {user_input}")
    conversation_historyN.append(f"Naruto: {translated_response}")

    return render_template('index.html', user_input=user_input, naruto_response=naruto_response, conversation_historyN=conversation_historyN)

#Funkcija za postavljanje tokena
@app.route('/set_tokenNaruto', methods=['POST'])
def set_tokenNaruto():
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
    return redirect('/Naruto')

#Funkcija za brisanje razgovora
@app.route('/clear_chatNaruto', methods=['POST'])
def clear_chatNaruto():
    global conversation_historyN
    conversation_historyN = []
    flash("Razgovor je obrisan!", "info")
    return redirect('/Naruto')

#Funkcija za generisanje odgovora za lika
@app.route('/askBatman', methods=['POST'])
def askBatman():
    user_input = request.form['user_input']
    
# Prevod korisničkog unosa na engleski
    translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)


    headers = {'Authorization': f'Bearer {CURRENT_TOKEN}'}
    response = requests.get(BATMAN_API_URL)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'name' in data:
            batman_name = data['name']
            
            context = f"""Batman is a serious, analytical, and strategic character. He is focused on fighting crime and always thinks logically and methodically. Therefore, it's important to ask him specific questions and avoid vague or overly emotional statements. He values efficiency and clarity in communication. His dedication to Gotham City and its safety means his attention is often directed at real threats, so questions about his strategies, research, or the technology he uses could be a good way to prompt a response.
               User: {translated_input}  Batman:"""  
            batman_response = chatbot(
                context,
                max_new_tokens=int(CURRENT_TOKEN),
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                truncation=True,
                pad_token_id=50256
            )[0]['generated_text']
            
            batman_response = batman_response.replace("User:", "").strip()

            if "Batman:" in batman_response:
                batman_response = batman_response.split("Batman:")[1].strip()
            else:
                batman_response = "Betmen nije odgovorio na očekivani način."
        else:
            batman_response = "Došlo je do greške sa API-jem."
    else:
        batman_response = "Greška sa API-jem."
    
    # Prevod odgovora nazad na srpski
    translated_response = GoogleTranslator(source='en', target='sr').translate(batman_response)

    conversation_historyB.append(f"User: {user_input}")
    conversation_historyB.append(f"Betmen: {translated_response}")

    return render_template('batman.html', user_input=user_input, batman_response=batman_response, conversation_historyB=conversation_historyB)

#Funkcija za postavljanje tokena
@app.route('/set_tokenBatman', methods=['POST'])
def set_tokenBatman():
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
    return redirect('/Batman')

#Funkcija za brisanje razgovora
@app.route('/clear_chatBatman', methods=['POST'])
def clear_chatBatman():
    global conversation_historyB
    conversation_historyB = []
    flash("Razgovor je obrisan!", "info")
    return redirect('/Batman')

#Funkcija za generisanje odgovora za lika
@app.route('/askGandalf', methods=['POST'])
def askGandalf():
    user_input = request.form['user_input']
    
# Prevod korisničkog unosa na engleski
    translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)


    headers = {'Authorization': f'Bearer {CURRENT_TOKEN}'}
    response = requests.get(GANDALF_API_URL)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'name' in data:
            gandalf_name = data['name']
            
            context = f"""Gandalf is a wise and powerful wizard with a deep understanding of the world and its forces. He speaks with great wisdom, often offering guidance that requires contemplation and reflection. When conversing with Gandalf, it’s important to approach him with respect and patience, as he often speaks in a thoughtful and philosophical manner. He values deeper meanings and encourages others to think beyond immediate circumstances. Gandalf’s answers are often filled with metaphor and insight, as he seeks to guide others on their journeys, not just provide simple answers.
               User: {translated_input}  Gandalf:"""  
            gandalf_response = chatbot(
                context,
                max_new_tokens=int(CURRENT_TOKEN),
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                truncation=True,
                pad_token_id=50256
            )[0]['generated_text']
            
            gandalf_response = gandalf_response.replace("User:", "").strip()

            if "Gandalf:" in gandalf_response:
                gandalf_response = gandalf_response.split("Gandalf:")[1].strip()
            else:
                gandalf_response = "Gandalf nije odgovorio na očekivani način."
        else:
            gandalf_response = "Došlo je do greške sa API-jem."
    else:
        gandalf_response = "Greška sa API-jem."
    
    # Prevod odgovora nazad na srpski
    translated_response = GoogleTranslator(source='en', target='sr').translate(gandalf_response)

    conversation_historyG.append(f"User: {user_input}")
    conversation_historyG.append(f"Gandalf: {translated_response}")

    return render_template('gandalf.html', user_input=user_input, gandalf_response=gandalf_response, conversation_historyG=conversation_historyG)

#Funkcija za postavljanje tokena
@app.route('/set_tokenGandalf', methods=['POST'])
def set_tokenGandalf():
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
    return redirect('/Gandalf')

#Funkcija za brisanje razgovora
@app.route('/clear_chatGandalf', methods=['POST'])
def clear_chatGandalf():
    global conversation_historyG
    conversation_historyG = []
    flash("Razgovor je obrisan!", "info")
    return redirect('/Gandalf')

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)