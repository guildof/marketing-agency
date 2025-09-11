import os, os.path as p
from datetime import timedelta
from google.cloud import storage
from generate_audit_pdf import generate_pdf_from_audit

def _signed_url(blob, days=7) -> str:
    return blob.generate_signed_url(version="v4", expiration=timedelta(days=days), method="GET")

def upload_to_gcs(local_path: str, bucket_name: str) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)  # no get_bucket() to avoid buckets.get
    blob = bucket.blob(p.basename(local_path))
    blob.upload_from_filename(local_path)
    return _signed_url(blob, days=7)

def export_audit_to_pdf_and_upload(audit_data: dict, client_name: str):
    """
    Retourne (pdf_path_local, signed_url_ou_None).
    """
    pdf_path = generate_audit_pdf(audit_data, client_name)
    bucket = os.getenv("AGENT_PDF_BUCKET")
    if not bucket:
        return pdf_path, None
    url = upload_to_gcs(pdf_path, bucket)
    return pdf_path, url

def generate_audit_pdf(audit_data: dict, client_name: str) -> str:
    # wrapper séparé pour garder le nom attendu
    return generate_pdf_from_audit(audit_data, client_name=client_name)
