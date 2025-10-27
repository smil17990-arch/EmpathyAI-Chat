
import os
import streamlit as st
from google.cloud import aiplatform # ← 代替SDKのインポート

# ページ設定 (最上部で実行)
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# --- 1. クライアントの初期化（エラー処理を含む） ---
try:
    # 認証情報を初期化し、プロジェクトIDを設定（ここでキー認証が行われる）
    # ★ プロジェクトIDを必ず置き換えること
    aiplatform.init(project='digital-vim-471122-t5
', location='us-central1') 
    
    # クライアント初期化（Vertex AI SDKを使用）
    client = aiplatform.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction='あなたは、優しく、批判せずに話を聞き、共感と感情の受け止めに特化した傾聴AIコンシェルジュです。'
    )
    
except Exception as e:
    st.error(f"Geminiクライアントの初期化に失敗しました。詳細: {e}")
    st.warning("プロジェクトIDが正しいか、またはAPIキーが有効か確認してください。")
    st.stop()
    
# --- 2. アプリのUIとセッションステートの設定 ---
st.title("傾聴AIコンシェルジュ")
st.markdown("悩みや出来事を話してください。私が受け止めます。")

# 会話履歴を保持するためのチャットセッションを開始
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = client.start_chat(history=[])

# Streamlitのセッションステートに履歴を初期化する
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- 3. 履歴の表示とユーザー入力の処理 ---
# 履歴の表示 (吹き出し形式で表示)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力を待つ
if prompt := st.chat_input("話しかけてください"):
    # ユーザー入力を履歴に追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIに応答してもらう
    with st.chat_message("assistant"):
        with st.spinner("AIがあなたの言葉を受け止めています..."):
            # セッションを使ってGeminiにリクエスト送信
            response = st.session_state.chat_session.send_message(prompt)
            
            # 結果を表示
            st.markdown(response.text)
            
            # AIの応答を履歴に追加
            st.session_state.messages.append({"role": "assistant", "content": response.text})

