import google.generativeai as genai
import json
import time


genai.configure(api_key="...")
model = genai.GenerativeModel("gemini-2.0-flash") # gemini-2.5-pro-exp-03-25

# Načítanie otázok
with open("dataset.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

results = []

print(f"Spúšťam testovanie {len(questions)} otázok...")

# Prechádzanie otázok
for q in questions:
    question_text = q['question_text']
    options_list = []
    for opt in q['options']:
        option_id = opt['id']
        option_text = opt['text']
        options_list.append(f"{option_id}) {option_text}")
    options_text = "\n".join(options_list)
    prompt = f"{question_text}\n\nMožnosti:\n{options_text}\n\nOdpoveď:"

    # Volanie API
    response = model.generate_content(prompt)
    answer = response.text.strip()

    print(f"[{q['id']}] Odpoveď získaná.")
    results.append({
        "id": q['id'],
        "prompt": prompt,
        "model_answer": answer
    })

    time.sleep(1) # Pauza kvôli rate limitu

# Uloženie výsledkov
with open("vysledky-gemini-2.0-flash.json", "w", encoding="utf-8") as f: # vysledky-gemini-2.5-pro-exp-03-25.json
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Hotovo! Výsledky ({len(results)} záznamov) máš v 'vysledky-gemini-2.0-flash.json'") # vysledky-gemini-2.5-pro-exp-03-25.json