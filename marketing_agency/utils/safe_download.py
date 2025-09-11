from pathlib import Path
from typing import Tuple
import requests

def download_pdf(url: str, dest_path: str, timeout: Tuple[float, float] = (5, 30), chunk: int = 8192) -> str:
    """
    Télécharge un PDF avec timeouts + gestion d'erreurs réseau + vérification content-type.
    Renvoie le chemin absolu du fichier téléchargé.
    """
    dest = Path(dest_path).expanduser().resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        with requests.get(url, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            ctype = (r.headers.get("Content-Type") or "").lower()
            if "pdf" not in ctype:
                # On autorise quand même certains serveurs qui ne posent pas le header,
                # mais s'il est présent et non-PDF, on bloque.
                if ctype:
                    raise ValueError(f"Le contenu n'est pas un PDF (Content-Type: {ctype}).")

            with open(dest, "wb") as f:
                for chunk_bytes in r.iter_content(chunk_size=chunk):
                    if chunk_bytes:
                        f.write(chunk_bytes)

    except requests.Timeout as e:
        raise TimeoutError("Timeout pendant le téléchargement du PDF.") from e
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur réseau pendant le téléchargement du PDF: {e}") from e

    return str(dest)
