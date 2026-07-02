import json
from pathlib import Path

path = Path("app/data/catalog.json")

text = path.read_text(encoding="utf-8")

# Remove illegal control characters except common whitespace
cleaned = "".join(
    ch for ch in text
    if ord(ch) >= 32 or ch in "\n\r\t"
)

data = json.loads(cleaned, strict=False)

path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("✅ Catalog cleaned successfully.")