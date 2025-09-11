import os
from typing import Optional, List, Dict, Any, Tuple
import requests

class PlacesError(RuntimeError):
    pass

# Timeouts configurables via .env
def _timeout_tuple() -> Tuple[float, float]:
    # connect, read
    conn = float(os.getenv("PLACES_CONNECT_TIMEOUT_S", "5"))
    read = float(os.getenv("PLACES_READ_TIMEOUT_S", "15"))
    return (conn, read)

_ENV_KEYS = ("GOOGLE_PLACES_API_KEY", "PLACES_API_KEY")

def _get_api_key() -> str:
    for k in _ENV_KEYS:
        v = os.getenv(k)
        if v:
            return v
    raise PlacesError(
        "Clé Google Places absente. Définis GOOGLE_PLACES_API_KEY (ou PLACES_API_KEY) dans l'environnement ou dans .env."
    )

class PlacesClient:
    BASE = "https://maps.googleapis.com/maps/api/place"

    def __init__(self, api_key: Optional[str] = None, language: str = "fr"):
        self.api_key = api_key or _get_api_key()
        self.language = language
        self._session = requests.Session()
        self._timeout = _timeout_tuple()

    def _get(self, path: str, **params) -> Dict[str, Any]:
        params.setdefault("key", self.api_key)
        params.setdefault("language", self.language)
        url = f"{self.BASE}/{path}"
        try:
            r = self._session.get(url, params=params, timeout=self._timeout)
            r.raise_for_status()
            data = r.json()
        except requests.Timeout as e:
            raise PlacesError("Délai d'attente dépassé pour l'API Google Places.") from e
        except requests.RequestException as e:
            raise PlacesError(f"Erreur réseau Google Places: {e}") from e
        except ValueError as e:
            raise PlacesError("Réponse Google Places invalide (JSON).") from e

        status = data.get("status")
        if status != "OK":
            msg = data.get("error_message") or status or "Erreur inconnue"
            raise PlacesError(f"Google Places renvoie une erreur: {msg}")
        return data

    def find_place(self, text_query: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        fields = fields or ["place_id", "name", "formatted_address", "photos"]
        return self._get(
            "findplacefromtext/json",
            input=text_query,
            inputtype="textquery",
            fields=",".join(fields),
        )

    def details(self, place_id: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        fields = fields or ["place_id", "name", "formatted_address", "photos", "geometry"]
        return self._get("details/json", place_id=place_id, fields=",".join(fields))

    def photo_url(self, photo_reference: Optional[str], maxwidth: int = 800) -> Optional[str]:
        if not photo_reference:
            return None
        return f"{self.BASE}/photo?maxwidth={int(maxwidth)}&photo_reference={photo_reference}&key={self.api_key}"

    def get_photo_urls(
        self, photos: Optional[List[Dict[str, Any]]], maxwidth: int = 800, limit: int = 4
    ) -> List[str]:
        urls: List[str] = []
        for p in (photos or []):
            # sécurise l'accès à photo_reference
            ref = p.get("photo_reference") if isinstance(p, dict) else None
            if ref:
                u = self.photo_url(ref, maxwidth=maxwidth)
                if u:
                    urls.append(u)
            if len(urls) >= limit:
                break
        return urls
