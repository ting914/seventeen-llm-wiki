"""簡報檢查（AGENTS.md 6.4 第 4 步）。用法：python tools/check_slides.py [專案根目錄]
1. 對應表每一列的 wiki 頁面存在
2. 對應表「重點」裡的數字，要出現在它引用的 wiki 頁面裡（「推算」欄已說明的除外）
3. 對應表「重點」的文字，真的出現在那一張投影片上（對應表和投影片一致）
4. 反向：投影片上出現的每個數字，都要在該張投影片的對應表列裡找得到（抓「沒寫進對應表」的內容）
5. 長條圖程式裡的銷量，逐筆要在 wiki 裡找得到
6. 名詞先解釋：粉絲用語第一次出現不能早於名詞頁（第 3 張）
7. 每張投影片至少有一列對應；每張圖片檔都存在
"""
import os, re, sys, glob, html as H
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
issues = []
def add(item, where, desc): issues.append((item, where, desc))
NUM = r"\d[\d,.]*\d|\d"
def nums(s): return {x.replace(",", "").lstrip("0") or "0" for x in re.findall(NUM, s)}
def norm(s): return re.sub(r"\s+", "", H.unescape(s))

page = open(f"{ROOT}/slides/index.html", encoding="utf-8").read()
body = re.sub(r"<script.*?</script>", "", page, flags=re.S)
slides = {}
for sid, inner in re.findall(r'<section[^>]*id="s(\d+)"[^>]*>(.*?)</section>', body, flags=re.S):
    inner = re.sub(r'<div class="folio">.*?</div>', "", inner, flags=re.S)
    inner = re.sub(r'(alt|src|style)="[^"]*"', "", inner)
    slides[int(sid)] = H.unescape(re.sub(r"<[^>]+>", " ", inner))

rows = []
for line in open(f"{ROOT}/slides/mapping.md", encoding="utf-8"):
    m = re.match(r"^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \|$", line.strip())
    if m: rows.append((int(m.group(1)), m.group(2), m.group(3), m.group(4)))

for n, text, refs, derived in rows:
    where = f"第 {n} 張：{text[:24]}"
    if n not in slides: add("投影片存在", where, "沒有這張投影片"); continue
    if norm(text) not in norm(slides[n]): add("對應表和投影片一致", where, "投影片上找不到這段文字")
    paths = re.findall(r"\]\(\.\./wiki/([^)]+)\)", refs)
    pool = set()
    for p in paths:
        fp = f"{ROOT}/wiki/{p}"
        if not os.path.exists(fp): add("wiki 頁面存在", where, f"找不到 wiki/{p}"); continue
        pool |= nums(open(fp, encoding="utf-8").read())
    if paths:
        for x in nums(text) - pool - nums(derived):
            add("數字對照 wiki", where, f"數字 {x} 不在 {', '.join(paths)}")
    elif derived == "—":
        add("有 wiki 來源", where, "沒有 wiki 頁面，也沒有說明推算依據")

for n, txt in slides.items():
    mine = [r for r in rows if r[0] == n]
    if not mine: add("每張都有對應", f"第 {n} 張", "對應表裡沒有這張"); continue
    allowed = set().union(*(nums(r[1]) | nums(r[3]) for r in mine))
    flat = re.sub(r"\s+", " ", txt)
    for x in nums(txt) - allowed:
        ctx = re.search(r".{0,14}" + re.escape(x) + r".{0,14}", flat.replace(",", ""))
        add("反向：投影片數字都有對應", f"第 {n} 張", f"數字 {x} 沒寫進對應表：…{ctx.group(0) if ctx else ''}…")

wiki_all = "".join(open(p, encoding="utf-8").read() for p in glob.glob(f"{ROOT}/wiki/**/*.md", recursive=True))
m = re.search(r"const sales=(\[.*?\]);", page, flags=re.S)
if m:
    for name, yr, v in re.findall(r'\["(.+?)","(\d{4})",(\d+)\]', m.group(1)):
        if f"{int(v):,}" not in wiki_all: add("長條圖數字對照 wiki", name, f"{int(v):,} 不在 wiki 裡")
else: add("長條圖數字對照 wiki", "第 14 張", "找不到 sales 資料")

order = sorted(slides)
for term in ["音樂節目一位", "大賞", "預購", "改版專輯", "主打"]:
    first = next((n for n in order if term in slides[n]), None)
    if first is not None and first < 3: add("名詞先解釋", term, f"第 {first} 張就出現，早於名詞頁（第 3 張）")

for src in set(re.findall(r'src="([^"]+)"', page)):
    if not os.path.exists(f"{ROOT}/slides/{src}"): add("圖片存在", src, "找不到檔案")

print(f"核對 {len(slides)} 張投影片、{len(rows)} 列對應，發現 {len(issues)} 個問題")
for i in issues: print(" | ".join(i))
