import os, requests, openai, json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

class ActionGetPhase(Action):
    def name(self): return "action_get_phase"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_id = tracker.sender_id
        chapter_id = tracker.get_slot("chapter_id")
        res = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/get_phase_content",
            headers={"apikey": SUPABASE_KEY,"Authorization": f"Bearer {SUPABASE_KEY}","Content-Type": "application/json"},
            json={"user_id": user_id,"chapter_id": chapter_id},
        )
        data = res.json()[0] if res.ok and res.json() else {}
        dispatcher.utter_message(json_message={
            "component": "ConceptPhase",
            "phase_json": data.get("phase_json", {}),
            "phase_id": data.get("phase_id"),
        })
        return []

class ActionAskDoubt(Action):
    def name(self): return "action_ask_doubt"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        question = tracker.latest_message.get("text")
        prompt = f"You are a NEET mentor. Explain clearly: {question}"
        reply = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user","content": prompt}]
        )
        answer = reply.choices[0].message.content.strip()
        dispatcher.utter_message(text=answer)
        return []
