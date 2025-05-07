import pandas as pd
import os
from datetime import datetime

DATA_FILE = 'mouse_clicks_log.csv'
REPORT_FILE = 'mouse_clicks_report.xlsx'

if not os.path.exists(DATA_FILE):
    print(f'找不到 {DATA_FILE}，請先執行監控腳本產生資料！')
    exit(1)

# 讀取資料
try:
    df = pd.read_csv(DATA_FILE)
except Exception as e:
    print(f'讀取資料失敗: {e}')
    exit(1)

# 處理時間欄位
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
else:
    print('缺少 timestamp 欄位，無法進行時段分析')
    exit(1)

# 檢查是否有 app 欄位
if 'app' not in df.columns:
    print("mouse_clicks_log.csv 缺少 'app' 欄位，請先用新版監控腳本產生有 app 欄位的資料！\n目前無法進行分軟體、分時段、分專案分析。\n建議：刪除舊資料或僅保留新版資料，再重新執行分析。")
    exit(1)

# 分時段分析（每小時）
df['hour'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:00')
hourly = df.groupby(['app', 'hour']).agg({'left':'max', 'right':'max', 'middle':'max'}).reset_index()
# 計算每小時的增量（每小時最後一筆減前一小時最後一筆）
def calc_hourly_delta(df, key):
    df = df.sort_values('hour')
    df[key+'_delta'] = df[key].diff().fillna(df[key])
    return df
hourly = hourly.groupby('app').apply(lambda g: calc_hourly_delta(g, 'left')).reset_index(drop=True)
hourly = hourly.groupby('app').apply(lambda g: calc_hourly_delta(g, 'right')).reset_index(drop=True)
hourly = hourly.groupby('app').apply(lambda g: calc_hourly_delta(g, 'middle')).reset_index(drop=True)

# 分專案（以 window 為專案名）
project = df.groupby(['app', 'window']).agg({'left':'max', 'right':'max', 'middle':'max'}).reset_index()

# 總表
summary = df.groupby('app').agg({'left':'max', 'right':'max', 'middle':'max'}).reset_index()

# 模板格式 summary
summary_fmt = pd.DataFrame()
for app in ['AutoCAD', 'Revit']:
    row = summary[summary['app'] == app]
    if not row.empty:
        l = int(row['left'].values[0])
        r = int(row['right'].values[0])
        m = int(row['middle'].values[0])
        s = l + r + m
        summary_fmt = pd.concat([
            summary_fmt,
            pd.DataFrame({
                'App': [f'{app} Total Clicks'],
                'RIGHT': [r],
                'MIDDLE': [m],
                'LEFT': [l],
                'SUM': [s]
            })
        ], ignore_index=True)
    else:
        summary_fmt = pd.concat([
            summary_fmt,
            pd.DataFrame({
                'App': [f'{app} Total Clicks'],
                'RIGHT': [0],
                'MIDDLE': [0],
                'LEFT': [0],
                'SUM': [0]
            })
        ], ignore_index=True)

# 匯出 Excel
with pd.ExcelWriter(REPORT_FILE) as writer:
    hourly.to_excel(writer, sheet_name='分時段', index=False)
    project.to_excel(writer, sheet_name='分專案', index=False)
    summary.to_excel(writer, sheet_name='總表', index=False)
    summary_fmt.to_excel(writer, sheet_name='模板格式', index=False)

print(f'分析報表已匯出：{REPORT_FILE}')
print('工作表包含：分時段、分專案、總表、模板格式')
