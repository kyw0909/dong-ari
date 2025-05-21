import requests
import firebase_admin
from firebase_admin import credentials, db
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import torch

# 🔐 네이버 뉴스 API 인증 정보
NAVER_CLIENT_ID = "VHgsF6Pba6O9sHo2aob6"
NAVER_CLIENT_SECRET = "HCUKdkCjqA"

# ✅ Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://clubproject-a2eed-default-rtdb.europe-west1.firebasedatabase.app/"
})

# ✨ KoBART 모델 및 토크나이저 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

def summarize_kobart(text):
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], max_length=100, min_length=20, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# 🔍 네이버 뉴스 가져오기
def fetch_news(query="인공지능", display=5):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": display,
        "sort": "date"
    }
    res = requests.get(url, headers=headers, params=params)
    return res.json().get("items", [])

# ☁️ Firebase에 저장
def save_to_firebase(title, content, summary):
    ref = db.reference("news")
    ref.push({
        "title": title,
        "content": content,
        "summary": summary
    })

# 🧠 전체 흐름
def main():
    articles = fetch_news()
    for article in articles:
        title = article.get("title")
        content = article.get("description")
        if content:
            summary = summarize_kobart(content)
            save_to_firebase(title, content, summary)
            print(f"✅ 저장 완료: {title}")

if __name__ == "__main__":
    main()
