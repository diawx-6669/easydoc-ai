import streamlit as st
import time
from datetime import date
import os

# ===== НАСТРОЙКА СТРАНИЦЫ =====
st.set_page_config(page_title="EasyDoc AI", page_icon="📝", layout="centered")

# ===== СТИЛЬ (НОВЫЙ ДИЗАЙН) =====
st.markdown("""
<style>

/* ФОН */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}

/* КОНТЕЙНЕР */
.block-container {
    background: #1e293b;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}

/* ЗАГОЛОВКИ */
h1, h2 {
    text-align: center;
    color: white !important;
}

/* ТЕКСТ */
p, label {
    color: #cbd5e1 !important;
}

/* INPUT */
.stTextInput>div>div>input {
    background-color: #334155 !important;
    color: white !important;
    border-radius: 10px;
    border: 2px solid transparent;
    padding: 12px;
}

.stTextInput>div>div>input:focus {
    border: 2px solid #6366f1 !important;
}

/* SELECT */
.stSelectbox div[data-baseweb="select"] {
    background-color: #334155 !important;
    color: white !important;
    border-radius: 10px;
}

/* КНОПКА */
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 55px;
    width: 100%;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 25px rgba(99,102,241,0.5);
}

/* FOOTER */
.footer-text {
    text-align: center;
    color: #94a3b8;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# ===== ЛОГО =====
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h1>📝 EasyDoc AI</h1>", unsafe_allow_html=True)

# ===== ЯЗЫК =====
st.markdown("### 🌍 Выберите язык / Тілді таңдаңыз:")
lang = st.selectbox("", ("Русский", "Қазақша"))

st.divider()

# ===== РУССКИЙ =====
if lang == "Русский":
    st.markdown("<h2>📄 Создать договор</h2>", unsafe_allow_html=True)
    
    with st.form("form_ru"):
        c1, c2 = st.columns(2)
        with c1:
            emp = st.text_input("Организация")
            pos = st.text_input("Должность")
        with c2:
            work = st.text_input("ФИО Работника")
            sal = st.text_input("Оклад (₸)")
        
        submitted = st.form_submit_button(" СГЕНЕРИРОВАТЬ")

    if submitted:
        if emp and work:
            with st.spinner("Создание документа..."):
                time.sleep(1)

            html_doc = f"""
            <html>
            <body style="font-family: Arial;">
                <h1 style="text-align:center;">ТРУДОВОЙ ДОГОВОР</h1>
                <p><b>Дата:</b> {date.today()}</p>
                <p><b>Работодатель:</b> {emp}</p>
                <p><b>Работник:</b> {work}</p>
                <p><b>Должность:</b> {pos}</p>
                <p><b>Оклад:</b> {sal} тенге</p>
                <br><br>
                <p>Подпись: ________________</p>
            </body>
            </html>
            """

            st.success("✅ Документ готов!")
            st.download_button("📥 Скачать .DOC", html_doc, f"Dogovor_{work}.doc")

# ===== КАЗАХСКИЙ =====
else:
    st.markdown("<h2>📄 Шарт жасау</h2>", unsafe_allow_html=True)
    
    with st.form("form_kz"):
        c1, c2 = st.columns(2)
        with c1:
            emp = st.text_input("Жұмыс беруші")
            pos = st.text_input("Қызметі")
        with c2:
            work = st.text_input("Жұмыскер")
            sal = st.text_input("Жалақы (₸)")
        
        submitted = st.form_submit_button("ДАЙЫНДАУ")

    if submitted:
        if emp and work:
            with st.spinner("Дайындалуда..."):
                time.sleep(1)

            html_doc_kz = f"""
            <html>
            <body style="font-family: Arial;">
                <h1 style="text-align:center;">ЕҢБЕК ШАРТЫ</h1>
                <p><b>Күні:</b> {date.today()}</p>
                <p><b>Жұмыс беруші:</b> {emp}</p>
                <p><b>Жұмыскер:</b> {work}</p>
                <p><b>Қызметі:</b> {pos}</p>
                <p><b>Жалақы:</b> {sal} теңге</p>
            </body>
            </html>
            """

            st.success("✅ Дайын!")
            st.download_button("📥 Жүктеу .DOC", html_doc_kz, f"Shart_{work}.doc")

# ===== FOOTER =====
st.markdown('<div class="footer-text">Made by Yeraly and Ramazan </div>', unsafe_allow_html=True)