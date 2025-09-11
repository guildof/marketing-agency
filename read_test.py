import os, sys
p = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
print("PY: GOOGLE_APPLICATION_CREDENTIALS =", p)
print("PY: exists:", os.path.exists(p))
print("PY: size:", os.stat(p).st_size, "bytes")
with open(p, "r", encoding="utf-8") as f:
    s = f.read(120)
print("PY: open OK — preview safe:", s[:120].replace("\n","\\n"))
print("PY: OK")
