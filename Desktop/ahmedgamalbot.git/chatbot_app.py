import streamlit as st
import requests
import json

api_key = "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"

st.set_page_config(page_title="AhmedGamalBot", page_icon="🤖", layout="centered")
st.title("💬 AhmedGamalBot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "أنت روبوت دردشة ذكي اسمه AhmedGamalBot، صُممت بواسطة أحمد البابكري. "
                "تتحدث العربية والإنجليزية بطلاقة، وتتصرف كأنك إنسان ودود ومهذب. "
                "إذا سألك أحد (من أنت؟، ما أنت؟، من صنعك؟، من أنشأك؟)، فأجب بوضوح بأنك صُممت وصُنعت بواسطة أحمد البابكري. "
                "لا تتحدث بأي طابع صيني، ولا تذكر الصين في أي جواب. "
                "كن مباشرًا في ردودك بدون شرح داخلي أو تفكير علني."
            )
        }
    ]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("اكتب رسالتك هنا...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("يفكر..."):
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://localhost",
                        "X-Title": "AhmedGamalBot"
                    },
                    data=json.dumps({
                        "model": "deepseek/deepseek-r1-0528:free",
                        "messages": st.session_state.messages
                    })
                )

                if response.status_code == 200:
                    result = response.json()
                    bot_reply = result["choices"][0]["message"]["content"]
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    st.error("❌ خطأ في الاتصال:")
                    st.text(response.text)

            except Exception as e:
                st.error("❌ فشل الاتصال بالسيرفر.")
                st.text(str(e))
