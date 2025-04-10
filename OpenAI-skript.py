import openai
import json
import time

client = openai.OpenAI(
    api_key="..."
)

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
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06", # o1-2024-12-17
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1.0
    )

    answer = response.choices[0].message.content.strip()

    print(f"[{q['id']}] Odpoveď získaná.")
    results.append({
        "id": q['id'],
        "prompt": prompt,
        "model_answer": answer
    })

    time.sleep(1) # Pauza kvôli rate limitu

# Uloženie výsledkov
with open("vysledky-gpt-4o-2024-08-06.json", "w", encoding="utf-8") as f: # vysledky-o1-2024-12-17.json
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Hotovo! Výsledky ({len(results)} záznamov) máš v 'vysledky-gpt-4o-2024-08-06.json'") # vysledky-o1-2024-12-17.json