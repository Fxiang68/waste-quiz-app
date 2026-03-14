# 廢棄物題庫練習系統（Streamlit 版）

這是可部署到 **GitHub + Streamlit Community Cloud** 的題庫練習 App。

## 專案結構

```bash
streamlit_quiz_app/
├─ app.py
├─ question_bank.json
├─ requirements.txt
└─ README.md
```

## 本機執行

先安裝套件：

```bash
pip install -r requirements.txt
```

啟動 App：

```bash
streamlit run app.py
```

## 部署到 GitHub + Streamlit

1. 建立 GitHub repository
2. 上傳 `app.py`、`question_bank.json`、`requirements.txt`
3. 前往 Streamlit Community Cloud
4. 連接 GitHub repo
5. Main file path 選 `app.py`
6. 按 Deploy

## 注意
- `question_bank.json` 必須和 `app.py` 放在同一層
- 若題庫很大，第一次載入會稍慢，之後會快很多
