from google.genai import Client
import os

proj = os.getenv("GCP_PROJECT_ID","marketing-digital-vegetal")
loc  = os.getenv("GCP_LOCATION","europe-west1")  # aligne avec .env

# Si tu veux forcer ici :
# proj, loc = "marketing-digital-vegetal", "europe-west1"

c = Client(vertexai=True, project=proj, location=loc)
print("OK models list, count:", len(list(c.models.list())))
r = c.models.generate_content(model="gemini-2.5-pro", contents="ping")
print("Prediction OK:", r.candidates[0].content.parts[0].text[:40])
