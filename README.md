# Rasa Server for Adaptive Learning (Render Deploy)

## Steps
1. Commit this asa-server folder to GitHub.
2. On Render.com → New Web Service → Connect repo → root: asa-server.
3. Add environment variables:
   - SUPABASE_URL
   - SUPABASE_KEY
   - OPENAI_API_KEY
4. Render auto-builds and runs:
   rasa run --enable-api --cors "*" --port 10000 --actions actions
5. Your endpoint:
   https://rasa-hummingbird.onrender.com/webhooks/rest/webhook
