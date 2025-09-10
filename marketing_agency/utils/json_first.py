from typing import Optional

def extract_first_json(text: str) -> Optional[str]:
    """Retourne la première chaîne JSON (objets {...}) trouvée en tête de réponse."""
    if not text:
        return None
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return None
