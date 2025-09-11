import os, sys, glob
from datetime import timedelta
from google.cloud import storage

CRED_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
BUCKET_NAME = "agent-market-digit"

# prendre le dernier PDF dans exports/
pdfs = sorted(glob.glob(os.path.join("exports","*.pdf")), key=os.path.getmtime, reverse=True)
if not pdfs:
    print("Aucun PDF trouvé dans exports/. Générez-en un avec generate_audit_pdf.py")
    sys.exit(1)

LOCAL_FILE = pdfs[0]
BLOB_NAME = os.path.basename(LOCAL_FILE)

print("Using creds:", CRED_PATH)
print("Local file:", LOCAL_FILE)

client = storage.Client()

# ⚠️ n'appelle PAS l’API (évite 'storage.buckets.get')
bucket = client.bucket(BUCKET_NAME)

blob = bucket.blob(BLOB_NAME)
blob.upload_from_filename(LOCAL_FILE)
print("Upload OK -> gs://{}/{}".format(BUCKET_NAME, BLOB_NAME))

# Génère une URL signée 7 jours (bucket reste privé)
url = blob.generate_signed_url(
    version="v4",
    expiration=timedelta(days=7),
    method="GET",
)
print("Signed URL (7d):", url)
