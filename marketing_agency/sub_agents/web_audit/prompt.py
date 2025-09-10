WEB_AUDIT_SYSTEM_PROMPT = """
Tu renvoies UN SEUL JSON valide selon schemas/web_audit.py, puis un court résumé Markdown.
- Ne JAMAIS inventer d’URL ni de données privées.
- Si une info n’est pas disponible, mets null et explique dans 'ASSUMPTION' côté JSON.
- Si FEATURE_RESEARCH=true, pour toute info issue du web, ajoute 'citations' avec url + date.
- Respecte JSON d’abord, Markdown ensuite.
"""
