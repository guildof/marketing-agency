import os
from marketing_agency.schemas.web_audit import Output, Audit, GBP, Instagram, Website

def run_web_audit(payload: dict) -> str:
    # 1) Entrée minimale
    brand = payload.get("brand")
    city = payload.get("city")
    urls = payload.get("urls", {}) or {}
    feature_research = os.getenv("FEATURE_RESEARCH", "false").lower() == "true"

    # 2) Découverte (v1 : on ne fait que normaliser ce qui est fourni)
    discover = {
        "urls": {
            "website": urls.get("website"),
            "gbp": urls.get("gbp"),
            "instagram": urls.get("instagram"),
        },
        "place_id": None,
        "confidence": 0.5 if any(urls.values()) else 0.0,
        "citations": []  # v1 sans recherche
    }

    # 3) Audit très simple (v1 : scores par présence)
    gbp_score = 60 if discover["urls"]["gbp"] else 0
    ig_score  = 40 if discover["urls"]["instagram"] else 0
    web_score = 50 if discover["urls"]["website"] else 0

    audit = Audit(
        gbp=GBP(rating=None, reviews=None, score=gbp_score),
        instagram=Instagram(followers=None, posts_30d=None, score=ig_score),
        website=Website(seo_onpage_score=0, cwv_mobile_score=None, score=web_score)
    )

    # 4) Scores globaux
    global_score = round((gbp_score + ig_score + web_score) / 3) if any([gbp_score, ig_score, web_score]) else 0
    scores = {"gbp": gbp_score, "instagram": ig_score, "website": web_score, "global": global_score}

    # 5) Actions 90j (simples & concrètes)
    actions = []
    if not discover["urls"]["gbp"]:
        actions.append({"title":"Créer/Revendiquer la fiche Google", "why":"Visibilité locale immédiate", "effort":"low", "impact":"high", "owner":"client"})
    if discover["urls"]["gbp"]:
        actions.append({"title":"Obtenir 10 avis clients avec photo", "why":"Améliore la preuve sociale sur Maps", "effort":"low", "impact":"high", "owner":"client"})
    if not discover["urls"]["website"]:
        actions.append({"title":"Créer une page contact simple (téléphone, horaires, adresse)", "why":"Contactabilité et SEO local de base", "effort":"med", "impact":"med", "owner":"agency"})
    if not discover["urls"]["instagram"]:
        actions.append({"title":"Calendrier Instagram 2 posts/sem.", "why":"Régularité et découverte locale", "effort":"low", "impact":"med", "owner":"agency"})

    output = Output(
        input={"brand": brand, "city": city, "urls": urls, "ASSUMPTION": "v1 sans recherche web"},
        discover=discover,
        audit=audit,
        scores=scores,
        actions_90j=actions
    )

    # 6) JSON d’abord, puis un bref Markdown
    json_block = output.model_dump_json(indent=2, ensure_ascii=False)
    md_block = f"\n\n# Synthèse\n- **Score global**: {global_score}\n- Priorités: " \
               f"{', '.join([a['title'] for a in actions[:3]]) if actions else 'ok'}\n"
    return json_block + md_block
