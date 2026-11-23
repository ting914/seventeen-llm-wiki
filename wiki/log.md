# Log

## [2026-11-23 17:20] setup | 建立 schema 與資料夾骨架
- 建立 AGENTS.md、wiki/index.md、wiki/log.md、wiki/overview.md、wiki/open-questions.md
- 範圍：韓文迷你＋正規專輯；改版併入原專輯頁
- 重點：概念與故事線、成績與里程碑；簡報以時間軸為主線

## [2026-11-23 18:40] ingest | 01 Wikipedia — Seventeen discography
- 動到的頁面：albums/ 20 頁（新建）、milestones/ 3 頁（新建）、sources/wikipedia-discography.md、overview.md、index.md、open-questions.md
- 使用者審核：來源 ✅（另外加入 2 篇備選）／重點 ✅（Semicolon、Director's Cut 認定為特別專輯；17 Is Right Here 納入範圍）
- 檢查：第 1 輪 23 個問題（全是檢查程式誤報），修正後第 2 輪 0 個問題；用故意放錯的方式驗證過數字核對（詳見 checks/2026-11-23_1830_ingest_wikipedia-discography.md）

## [2026-11-23 19:00] ingest | 02 Wikipedia — Seventeen (South Korean band)
- 動到的頁面：新建 eras/ 5 頁、concepts/power-of-love.md、people/woozi.md、milestones/first-music-show-win.md、sources/wikipedia-seventeen-band.md；更新 albums/ 20 頁、milestones/ 3 頁、overview.md、index.md、open-questions.md
- 使用者審核：重點 ✅（確認 5 個時期；Director's Cut 經 Weverse Shop 查證是特別專輯；新增第 8 篇官方專輯全名）
- 檢查：擷取時發現 EP 序數矛盾（不採用）；第 1 輪 1 個問題（超前連結），修正後第 2 輪 0 個問題（詳見 checks/2026-11-23_1900_ingest_wikipedia-seventeen-band.md）

## [2026-11-23 19:30] ingest | 03 Soompi、08 官方專輯全名、09 Wikipedia〈Don't Wanna Cry〉
- 動到的頁面：新建 sources/ 3 頁、milestones/dont-wanna-cry-breakthrough.md、concepts/2017-seventeen-project.md、people/bumzu.md；更新 albums/（al1、5 張有官方序數的迷你專輯、17-is-right-here、所有序數行）、eras/era-2、people/woozi、overview、index、open-questions
- 使用者審核：來源 ✅（新增第 9 篇）／重點 ✅（「成績突破」；版權署名不寫）
- 檢查：新增「內文數字對照 raw」檢查。第 1 版程式失效，修正後抓到 3 個真的問題，包括第 1 篇就留下的序數錯標來源；修正後 0 個問題（詳見 checks/2026-11-23_1930_ingest_soompi-officialtitles-dwc.md）

## [2026-11-23 19:20] ingest | 04–07 批次：Weverse Face the Sun、Weverse HAPPY BURSTDAY、ABS-CBN、Substack
- 動到的頁面：新建 sources/ 4 頁、concepts/self-reference.md、concepts/carat-in-the-story.md；更新 albums/（face-the-sun、happy-burstday、17-is-right-here、teen-age、an-ode、al1、spill-the-feels）、eras/（1、3、4、5）、milestones/（global-recognition、dont-wanna-cry-breakthrough）、index、open-questions
- 使用者審核：來源 ✅（第 5 篇改用 Weverse 評論）／重點 ✅（新建 2 個概念頁）
- 檢查：第 1 輪 10 個問題（1 個誤報、序號誤報，以及概念頁的年份混用來源），修正後 0 個問題（詳見 checks/2026-11-23_2000_ingest_batch-04-07.md）

## [2026-11-23 20:10] slides | 教學 HTML 簡報「SEVENTEEN 十年特刊」
- 產出：slides/index.html（15 張）、slides/mapping.md（122 列）、slides/img/（16 張）、tools/check_slides.py
- 使用者審核：大綱 ✅；照片由使用者提供
- 寫對應表時回頭補 wiki：overview（主打歌、CARAT）、people/woozi（WONWOO 的說法）、sources/wikipedia-seventeen-band
- 檢查：check_slides 第 1 輪 7 個問題（反向檢查抓到 5 處沒寫進對應表）→ 0 個問題；故意放錯驗證通過；截圖修正 4 個版面問題（詳見 checks/2026-11-23_2100_slides.md）
- 網頁：https://claude.ai/artifact/62AmY2HPvLLSdaefXvkfyi

## [2026-11-23 20:20] slides | 依使用者回饋修正：照片不裁切、英文字體改 Times New Roman
- 檢查：check_slides 0 個問題；截圖確認 9 張含照片的投影片都沒有裁切（詳見 checks/2026-11-23_2100_slides.md 第 2 輪）
