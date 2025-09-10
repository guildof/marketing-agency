#!/usr/bin/env python
"""
postprocess_audit.py

Usage:
  # Générer PDF localement à partir d'un fichier contenant la réponse complète de l'agent (JSON + Markdown)
  python postprocess_audit.py --input path/to/agent_output.txt --client "Fleurs de Loire"

  # Générer et uploader sur GCS (nécessite GOOGLE_APPLICATION_CREDENTIALS et bucket)
  python postprocess_audit.py --input path/to/agent_output.txt --client "Fleurs de Loire" --upload-bucket my-bucket
"""
import argparse
import json
import os
from marketing_agency.utils.json_first import extract_first_json
from marketing_agency.schemas.audit import AuditOutput
from generate_audit_pdf import generate_pdf_from_audit

def upload_to_gcs(local_path: str, bucket_name: str) -> str:
    from google.cloud import storage
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob_name = os.path.basename(local_path)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)
    try:
        blob.make_public()
        return blob.public_url
    except Exception:
        # si pas possible, renvoyer un chemin interne
        return f"gs://{bucket_name}/{blob_name}"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Fichier contenant la réponse de l'agent (JSON + Markdown)")
    p.add_argument("--client", default="Client", help="Nom du client pour le PDF")
    p.add_argument("--upload-bucket", default=None, help="Si renseigné, upload le PDF sur ce bucket GCS")
    args = p.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"Fichier introuvable : {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        full = f.read()

    json_str = extract_first_json(full)
    if not json_str:
        raise SystemExit("Aucun JSON détecté en tête du fichier d'entrée.")

    # Validation stricte via Pydantic (lance une exception si invalide)
    data = json.loads(json_str)
    AuditOutput(**data)  # validation

    # Génération PDF
    pdf_path = generate_pdf_from_audit(data, client_name=args.client)
    print(f"PDF local : {pdf_path}")

    # Upload optionnel
    if args.upload_bucket:
        url = upload_to_gcs(pdf_path, args.upload_bucket)
        print(f"PDF uploadé : {url}")

if __name__ == "__main__":
    main()
