import streamlit as st
import random


# =====================================
# ตั้งค่าหน้าเว็บ
# =====================================

st.set_page_config(
    page_title="เกมบวกเลข",
    page_icon="🧮",
    layout="centered"
)


# =====================================
# ตัวแปรเริ่มต้น
# =====================================

if "started" not in st.session_state:
    st.session_state.started = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "question_number" not in st.session_state:
    st.session_state.question_number = 0

if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "n1" not in st.session_state:
    st.session_state.n1 = 0

if "n2" not in st.session_state:
    st.session_state.n2 = 0

if "level" not in st.session_state:
    st.session_state.level = ""

if "result" not in st.session_state:
    st.session_state.result = ""


# =====================================
# สร้างโจทย์
# =====================================

def next_question():

    q = st.session_state.question_number + 1

    # -----------------------------
    # กำหนดระดับความยาก
    # -----------------------------

    if q <= 3:

        n1 = random.randint(1, 9)
        n2 = random.randint(1, 9)
        level = "ง่าย"

    elif q <= 6:

        n1 = random.randint(10, 99)
        n2 = random.randint(10, 99)
        level = "ปานกลาง"

    elif q <= 9:

        n1 = random.randint(100, 999)
        n2 = random.randint(100, 999)
        level = "ยาก"

    else:

        n1 = random.randint(1000, 9999)
        n2 = random.randint(1000, 9999)
        level = "ยากสุดๆ"

    correct = n1 + n2

    # -----------------------------
    # สร้างตัวเลือก
    # -----------------------------

    answers = [correct]

    while len(answers) < 4:

        number = random.randint(
            max(1, correct - 100),
            correct + 100
        )

        if number not in answers:
            answers.append(number)

    random.shuffle(answers)

    # -----------------------------
    # เก็บข้อมูล
    # -----------------------------

    st.session_state.question_number = q
    st.session_state.n1 = n1
    st.session_state.n2 = n2
    st.session_state.level = level
    st.session_state.correct_answer = correct
    st.session_state.answers = answers
    st.session_state.result = ""


# =====================================
# ตรวจคำตอบ
# =====================================

def check_answer(choice):

    answer = st.session_state.answers[choice]
    correct = st.session_state.correct_answer

    if answer == correct:

        st.session_state.score += 1

        st.session_state.result = (
            "correct",
            "✅ ถูกต้อง!"
        )

    else:

        st.session_state.result = (
            "wrong",
            f"❌ ผิด! เฉลยคือ {correct}"
        )


# =====================================
# เริ่มเกม
# =====================================

def start_game():

    name = st.session_state.player_name.strip()

    if name == "":
        st.warning("กรุณาใส่ชื่อผู้เล่น")
        return

    st.session_state.started = True
    st.session_state.score = 0
    st.session_state.question_number = 0

    next_question()


# =====================================
# จบเกม
# =====================================

def finish_game():

    name = st.session_state.player_name
    score = st.session_state.score

    # บันทึกคะแนน
    with open("scores.txt", "a", encoding="utf-8") as file:
        file.write(f"{name} : {score}/10\n")

    st.success(
        f"🎉 จบเกม!\n\n"
        f"ผู้เล่น: {name}\n\n"
        f"คะแนน: {score} / 10"
    )

    st.session_state.started = False

    st.session_state.player_name = ""

    st.session_state.score = 0
    st.session_state.question_number = 0
    st.session_state.answers = []
    st.session_state.result = ""


# =====================================
# หัวข้อ
# =====================================

st.title("🧮 เกมฝึกบวกเลข")


# =====================================
# หน้าเริ่มเกม
# =====================================

if "player_name" not in st.session_state:
    st.session_state.player_name = ""


if not st.session_state.started:

    st.subheader("ชื่อผู้เล่น")

    st.text_input(
        "กรอกชื่อ",
        key="player_name"
    )

    if st.button(
        "🎮 เริ่มเกม",
        use_container_width=True
    ):

        start_game()
        st.rerun()


# =====================================
# หน้าเกม
# =====================================

else:

    q = st.session_state.question_number

    st.write(
        f"### ข้อที่ {q} / 10"
    )

    st.write(
        f"**ระดับ: {st.session_state.level}**"
    )

    st.divider()

    st.markdown(
        f"# {st.session_state.n1} + "
        f"{st.session_state.n2} = ?"
    )

    st.write("")

    # -----------------------------
    # แสดงผลถูก/ผิด
    # -----------------------------

    if st.session_state.result:

        result_type, result_text = st.session_state.result

        if result_type == "correct":
            st.success(result_text)

        else:
            st.error(result_text)


    # -----------------------------
    # ถ้ายังไม่ได้ตอบ
    # -----------------------------

    if not st.session_state.result:

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                f"A. {st.session_state.answers[0]}",
                use_container_width=True
            ):

                check_answer(0)
                st.rerun()


            if st.button(
                f"C. {st.session_state.answers[2]}",
                use_container_width=True
            ):

                check_answer(2)
                st.rerun()


        with col2:

            if st.button(
                f"B. {st.session_state.answers[1]}",
                use_container_width=True
            ):

                check_answer(1)
                st.rerun()


            if st.button(
                f"D. {st.session_state.answers[3]}",
                use_container_width=True
            ):

                check_answer(3)
                st.rerun()


    # -----------------------------
    # หลังตอบแล้ว
    # -----------------------------

    else:

        st.write(
            f"คะแนนปัจจุบัน: "
            f"**{st.session_state.score} / {q}**"
        )

        if q < 10:

            if st.button(
                "➡️ ข้อต่อไป",
                use_container_width=True
            ):

                next_question()
                st.rerun()

        else:

            if st.button(
                "🏆 ดูผลคะแนน",
                use_container_width=True
            ):

                finish_game()
                st.rerun()