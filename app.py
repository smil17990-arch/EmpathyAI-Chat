
import streamlit as st
import requests
import json

# ★★★ 認証情報をコードに直接記述 (インストール不要) ★★★
PROJECT_ID = "digital-vim-471122-t5"
API_KEY = "AIzaSyCsdzek88GdM7heHAJ2t_Ol4cESlBFzFDQ"
ENDPOINT_URL = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/gemini-2.5-flash:generateContent"

# --- 1. アプリケーション設定 ---
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.title("傾聴AIコンシェルジュ (公開最終版)")
st.warning("注: このアプリは、互換性のためWeb APIを直接使用しています。")

# --- 2. 履歴の初期化 ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'history' not in st.session_state:
    st.session_state.history = [] # 会話履歴を保持するリスト

# --- 3. Geminiにリクエストを送信する関数 ---
def generate_response_via_api(prompt, history):
    # システムプロンプトを含む、完全な会話履歴を作成
    contents = [{
        "role": "user", 
        "parts": [{"text": "あなたは優しく、批判せず話を聞くコンシェルジュです。" + prompt}]
    }]
    # 以前の会話をcontentsに追加するロジック（簡略化）

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "contents": contents,
        "config": {
            "systemInstruction": "あなたは、優しく、批判せずに話を聞き、共感と感情の受け止めに特化した傾聴AIコンシェルジュです。",
            "temperature": 0.8
        }
    }

    try:
        response = requests.post(ENDPOINT_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status() # HTTPエラーがあれば例外を発生させる
        
        # 応答を解析
        response_json = response.json()
        return response_json['candidates'][0]['content']['parts'][0]['text']
    
    except Exception as e:
        return f"エラーが発生しました: {e}"

# --- 4. UIと処理 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("話しかけてください"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AIがあなたの言葉を受け止めています..."):
            # APIを直接叩いて応答を取得
            ai_response_text = generate_response_via_api(prompt, st.session_state.history)
            
            st.markdown(ai_response_text)
            
            # 履歴とメッセージを更新
            st.session_state.messages.append({"role": "assistant", "content": ai_response_text})




