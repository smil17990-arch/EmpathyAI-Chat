
import os
import streamlit as st
from google import generativeai
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# ----------------------------------------
# 1. クライアントの初期化（エラー処理を含む）
# ----------------------------------------
try:
    # tryブロックは、必ず字下げ（スペース4つ）する
    client = generativeai.GenerativeModel(
        # ★ カンマを追加！
        model_name='gemini-2.5-flash',
        
        # ★ 長い文字列は括弧 () で囲み、最後にカンマを打つ！
        system_instruction=(
            'あなたは、優しく、批判せずに話を聞き、共感と感情の受け止めに特化した傾聴AIコンシェルジュです。'
            'アドバイスや解決策の提案はせず、ユーザーの言葉をオウム返しするのではなく、深く共感し、発言を促してください。'
        ) # ← 括弧で閉じているので、ここにはカンマは不要
    )
    
except Exception as e:
    # exceptブロックはtryと必ず同じ深さにする
    st.error("Geminiクライアントの初期化に失敗しました。")
    st.warning("APIキーがターミナルに正しく設定されているか確認してください。")
    st.stop()

# ----------------------------------------
# 2. アプリのUIとセッションステートの設定
# ----------------------------------------
# --- st.title("傾聴AIコンシェルジュ") の直前に貼り付ける ---


# ----------------------------------------
# 2. アプリのUIとセッションステートの設定
# ----------------------------------------


st.title("傾聴AIコンシェルジュ")
st.markdown("悩みや出来事を話してください。私が受け止めます。")

# Streamlitのセッションステートに履歴を初期化する
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- 3. 履歴の表示とユーザー入力の処理 ---
# 履歴の表示
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
            # Geminiにリクエスト送信
            response = client.generate_content(prompt)
            
            # 結果を表示
            st.markdown(response.text)
            
            # AIの応答を履歴に追加
            st.session_state.messages.append({"role": "assistant", "content": response.text})

