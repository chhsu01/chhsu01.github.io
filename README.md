# AutoCAD & Revit 滑鼠點擊統計工具

## 工具簡介
本工具可分別統計 AutoCAD 與 Revit 軟體下，滑鼠左鍵、右鍵、中鍵的點擊次數，適合用於工程效率分析、行為紀錄與工作優化。支援一鍵匯出 Excel 報表，方便後續統計與分享。

## 功能特色
- **即時統計**：分軟體記錄每種滑鼠鍵的點擊次數
- **F12 快捷查詢**：即時顯示目前累積點擊數（命令列）
- **資料自動儲存**：每 30 秒自動寫入 CSV，防止資料遺失
- **Excel 報表**：自動產生分時段、分專案、總表與簡潔模板格式
- **簡易網頁下載**：附現成下載頁面，可自訂 Google Ads 區塊

## 安裝步驟
1. 安裝 [Python 3.8 以上版本](https://www.python.org/downloads/)
2. **請先切換到本專案資料夾再執行下列指令**：
   ```powershell
   cd D:\CascadeProjects\mouse-clicks-tool
   pip install -r requirements.txt
   ```

## 使用說明
1. 執行滑鼠監控：
   ```bash
   python mouse_counter.py
   ```
   - 在 AutoCAD 或 Revit 前景視窗點擊滑鼠即可累積統計
   - 按 F12 可即時查詢目前統計結果
2. 匯出 Excel 報表：
   ```bash
   python mouse_clicks_report.py
   ```
   - 產生 `mouse_clicks_report.xlsx`，內含多種分析工作表

## 執行注意事項
> **請勿直接雙擊 .py 檔案！**

- 直接點擊 Python 檔案，視窗會一閃即逝，無法看到任何統計或錯誤訊息。
- 請務必使用「命令列」(PowerShell 或命令提示字元) 執行腳本，才能正常互動與查看輸出。

### 正確操作步驟
1. 進入 `mouse-clicks-tool` 資料夾，在空白處按住 Shift + 滑鼠右鍵，選「在此處開啟 PowerShell 視窗」或「命令提示字元」。
2. **務必先切換到專案資料夾**：
   ```powershell
   cd D:\CascadeProjects\mouse-clicks-tool
   ```
3. 安裝必要套件（只需一次）：
   ```powershell
   pip install -r requirements.txt
   ```
4. 執行監控腳本：
   ```powershell
   python mouse_counter.py
   ```
   - 在 AutoCAD/Revit 點擊滑鼠，按 F12 查詢統計。
5. 執行報表腳本：
   ```powershell
   python mouse_clicks_report.py
   ```
   - 產生 Excel 報表。

### 如果沒反應怎麼辦？
- 請確認已安裝 Python 3.8 以上版本，且已安裝所有必要套件。
- 請務必在命令列視窗下執行腳本。
- 若有錯誤訊息，請將命令列畫面截圖，方便排查。

## 檔案結構
- `mouse_counter.py`：主程式，負責即時監控與統計
- `mouse_clicks_report.py`：報表產生器，輸出 Excel
- `requirements.txt`：必要 Python 套件清單
- `README.md`：本說明文件
- `index.html`：下載網頁範本（含廣告區塊）

## 授權
本工具開放自由學習與個人用途，商業應用請聯絡作者。

## 延伸
- 可自行擴充公司資料，或串接後端 API 取得更多資訊。
- 可加入搜尋、分類、篩選等功能。
