import json
import os
import random
import streamlit as st

st.set_page_config(page_title="廢棄物題庫練習系統", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTION_BANK_PATH = os.path.join(BASE_DIR, "question_bank.json")


@st.cache_data
def load_question_bank():
    if not os.path.exists(QUESTION_BANK_PATH):
        raise FileNotFoundError(
            "找不到 question_bank.json，請確認它和 app.py 放在同一個資料夾。"
        )
    with open(QUESTION_BANK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def init_state():
    defaults = {
        "quiz_started": False,
        "questions": [],
        "current_index": 0,
        "score": 0,
        "submitted": False,
        "selected_choice": None,
        "show_result": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz():
    st.session_state.quiz_started = False
    st.session_state.questions = []
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.submitted = False
    st.session_state.selected_choice = None
    st.session_state.show_result = False


def start_quiz(question_bank, selected_volume, question_count):
    if selected_volume == "全部題庫":
        questions = list(question_bank)
    else:
        questions = [q for q in question_bank if q["volume"] == selected_volume]

    random.shuffle(questions)

    if question_count != "全部":
        questions = questions[: int(question_count)]

    st.session_state.questions = questions
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.submitted = False
    st.session_state.selected_choice = None
    st.session_state.show_result = False
    st.session_state.quiz_started = True


def go_next():
    st.session_state.current_index += 1
    st.session_state.submitted = False
    st.session_state.selected_choice = None
    st.session_state.show_result = False


init_state()

st.title("廢棄物題庫練習系統")
st.caption("可部署到 GitHub + Streamlit Community Cloud 的版本")

try:
    question_bank = load_question_bank()
except Exception as e:
    st.error(str(e))
    st.stop()

volumes = ["全部題庫"] + sorted({q["volume"] for q in question_bank})

with st.sidebar:
    st.header("測驗設定")
    selected_volume = st.selectbox("選擇冊數", volumes)
    question_count = st.selectbox("選擇題數", ["10", "20", "30", "50", "100", "全部"])
    st.write(f"目前題庫總題數：{len(question_bank)} 題")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("開始測驗", use_container_width=True):
            start_quiz(question_bank, selected_volume, question_count)
            st.rerun()
    with col_b:
        if st.button("重新開始", use_container_width=True):
            reset_quiz()
            st.rerun()

if not st.session_state.quiz_started:
    st.info("請從左側選擇冊數與題數，然後按「開始測驗」。")
    st.markdown(
        """
### 功能
- 單冊 / 全部題庫練習
- 隨機抽題
- 即時判斷對錯
- 顯示分數與正確率
- 可直接部署到 Streamlit Community Cloud
"""
    )
    st.stop()

questions = st.session_state.questions
idx = st.session_state.current_index
total = len(questions)

if idx >= total:
    accuracy = (st.session_state.score / total * 100) if total else 0
    st.success(
        f"測驗完成！答對 {st.session_state.score} / {total} 題，正確率 {accuracy:.1f}%"
    )
    if st.button("再做一次"):
        reset_quiz()
        st.rerun()
    st.stop()

q = questions[idx]

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"第 {idx + 1} / {total} 題")
    st.caption(q["volume"])
with col2:
    st.metric("目前分數", f"{st.session_state.score}")

st.markdown(f"### {q['question']}")

radio_key = f"radio_{idx}"
choice = st.radio(
    "請選擇答案",
    options=[0, 1, 2, 3],
    format_func=lambda i: f"{i + 1}. {q['options'][i]}",
    index=None,
    key=radio_key,
)

col_submit, col_next = st.columns(2)

with col_submit:
    if st.button("送出答案", disabled=st.session_state.submitted, use_container_width=True):
        if choice is None:
            st.warning("請先選擇一個答案。")
        else:
            st.session_state.submitted = True
            st.session_state.selected_choice = choice
            st.session_state.show_result = True
            if choice == q["answer_index"]:
                st.session_state.score += 1
            st.rerun()

with col_next:
    if st.button("下一題", disabled=not st.session_state.submitted, use_container_width=True):
        go_next()
        st.rerun()

if st.session_state.show_result:
    correct = q["answer_index"]
    correct_text = f"{correct + 1}. {q['options'][correct]}"
    if st.session_state.selected_choice == correct:
        st.success(f"答對了！正確答案：{correct_text}")
    else:
        st.error(f"答錯了！正確答案：{correct_text}")
