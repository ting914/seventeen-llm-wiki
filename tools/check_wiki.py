"""LLM Wiki 自動檢查（AGENTS.md 第 7 節）。用法：python tools/check_wiki.py [專案根目錄]"""
import os, re, sys, glob
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
W = os.path.join(ROOT, "wiki")
issues = []
def add(item, page, desc): issues.append((item, os.path.relpath(page, ROOT), desc))

pages = sorted(glob.glob(f"{W}/**/*.md", recursive=True))
link_re = re.compile(r"\]\(([^)#\s]+\.md)\)")
inbound = {os.path.normpath(p): 0 for p in pages}

for p in pages:
    txt = open(p, encoding="utf-8").read()
    # 1. 連結有效
    for l in link_re.findall(txt):
        if l.startswith("http"): continue
        tgt = os.path.normpath(os.path.join(os.path.dirname(p), l))
        if not os.path.exists(tgt): add("連結有效", p, f"斷掉的連結 {l}")
        elif tgt in inbound and tgt != os.path.normpath(p): inbound[tgt] += 1
    # 2. 內容頁要有「來源」一節，事實句要附來源
    if "/albums/" in p or "/milestones/" in p or "/eras/" in p or "/concepts/" in p:
        if "## 來源" not in txt: add("有來源一節", p, "缺少「## 來源」")
        body = re.sub(r"^---\n.*?\n---\n", "", txt, flags=re.S).split("## 來源")[0]  # 跳過 frontmatter（第 1 輪誤報修正）
        for line in body.splitlines():
            if re.search(r"\d{3},\d{3}|第 \d+ 名|\d{4}-\d{2}-\d{2}", line) and "來源" not in line \
               and not line.startswith(("|", "release_date", "order", "- 前一張", "- 下一張")):
                add("事實附來源", p, f"含數字但沒附來源：{line.strip()[:50]}")
    # 3. 直接引用不超過 15 字（中文以字計、英文以詞計）
    for q in re.findall(r"[「\"“]([^」\"”\n]{1,200})[」\"”]", re.sub(r"^---\n.*?\n---\n", "", txt, flags=re.S)):  # 跳過 frontmatter、不跨行（ingest 04-07 誤報修正）
        n = len(q.split()) if re.search(r"[A-Za-z]{3,}", q) else len(q)
        if n > 15 and "title" not in q: add("引用長度", p, f"引用可能過長：{q[:30]}…")

# 4. 孤兒頁（index / log / open-questions 除外）
for p, n in inbound.items():
    if os.path.basename(p) in ("index.md", "log.md", "open-questions.md"): continue
    if n == 0: add("非孤兒頁", p, "沒有任何頁面連到這裡")

# 5. index 是否列出所有頁面
idx = open(f"{W}/index.md", encoding="utf-8").read()
for p in pages:
    rel = os.path.relpath(p, W).replace(os.sep, "/")
    if rel in ("index.md", "log.md") : continue
    if f"({rel})" not in idx: add("index 已更新", p, "沒有列在 index.md")

# 6. 專輯數字和 raw 逐項核對
raw_rows = {}
for rf in glob.glob(f"{ROOT}/raw/*.md"):
    for line in open(rf, encoding="utf-8"):
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([\d,]+)\s*\|", line)
        if m:
            name = re.sub(r"（.*?）", "", m.group(1)).strip()
            raw_rows[name.lower()] = m.groups()[1:]
for p in glob.glob(f"{W}/albums/*.md"):
    txt = open(p, encoding="utf-8").read()
    t = re.search(r'title_en: "(.+?)"', txt).group(1).lower()
    if t not in raw_rows: add("數字對照 raw", p, "raw 裡找不到這張專輯"); continue
    date, circle, bb, sales = raw_rows[t]
    if f"release_date: {date}" not in txt: add("數字對照 raw", p, f"發行日和 raw（{date}）不一致")
    if f"最高第 {circle} 名" not in txt: add("數字對照 raw", p, f"Circle 名次和 raw（{circle}）不一致")
    if f"韓國銷量 {sales} 張" not in txt: add("數字對照 raw", p, f"銷量和 raw（{sales}）不一致")

# 7. 內文數字對照 raw：每一行引用了某個來源，這行裡的數字都要出現在那篇來源的 raw 裡（第 3 輪 ingest 新增）
src_raw = {}
for sp in glob.glob(f"{W}/sources/*.md"):
    m = re.search(r"^raw: (.+)$", open(sp, encoding="utf-8").read(), re.M)
    if m: src_raw[os.path.basename(sp)] = open(os.path.normpath(os.path.join(os.path.dirname(sp), m.group(1))), encoding="utf-8").read()
def norm(x): return x.replace(",", "")
for p in pages:
    if "/sources/" in p: continue
    body = re.sub(r"^---\n.*?\n---\n", "", open(p, encoding="utf-8").read(), flags=re.S)
    for line in body.splitlines():
        cited = re.findall(r"(?:詮釋型)?來源：\[[^\]]+\]\(\.\./sources/([^)]+\.md)\)", line)
        if len(cited) != 1 or cited[0] not in src_raw: continue
        text = re.sub(r"^\s*\d+\.\s", "", line)  # 去掉編號列表的序號
        text = re.sub(r"（(?:詮釋型)?來源：.*?）|\[[^\]]*\]\([^)]*\)|\d{4}–\d{4}", "", text)
        raw_nums = {norm(x) for x in re.findall(r"\d[\d,.]*\d|\d", src_raw[cited[0]])}  # 以完整數字比對（子字串比對會被 2017 裡的 7 騙過）
        for n in re.findall(r"\d[\d,.]*\d|\d", text):
            if norm(n) not in raw_nums: add("內文數字對照 raw", p, f"數字 {n} 不在 {cited[0]} 的 raw 裡：{line.strip()[:40]}")

print(f"檢查 {len(pages)} 頁，發現 {len(issues)} 個問題")
for i in issues: print(" | ".join(i))
