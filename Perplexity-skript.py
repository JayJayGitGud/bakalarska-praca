import openai
import json
import time

client = openai.OpenAI(
    api_key="...",
    base_url="https://api.perplexity.ai"
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
        model="sonar-pro", # sonar-reasoning-pro
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
with open("vysledky-perplexity-sonar-pro.json", "w", encoding="utf-8") as f: # vysledky-perplexity-sonar-reasoning-pro.json
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Hotovo! Výsledky ({len(results)} záznamov) máš v 'vysledky-perplexity-sonar-pro.json'") # vysledky-perplexity-sonar-reasoning-pro.json