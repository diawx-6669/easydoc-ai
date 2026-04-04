import streamlit as st
import time
from datetime import date
import os

# ===== НАСТРОЙКА СТРАНИЦЫ =====
st.set_page_config(page_title="EasyDoc AI", page_icon="📝", layout="centered")

# ===== СТИЛЬ (ТВОЙ НОВЫЙ ДИЗАЙН) =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}
.block-container {
    background: #1e293b;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}
h1, h2, h3 {
    text-align: center;
    color: white !important;
}
p, label {
    color: #cbd5e1 !important;
}
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
.stSelectbox div[data-baseweb="select"] {
    background-color: #334155 !important;
    color: white !important;
    border-radius: 10px;
}
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

# ===== ВЫБОР ЯЗЫКА =====
st.markdown("### 🌍 Выберите язык / Тілді таңдаңыз:")
lang = st.selectbox("", ("Русский", "Қазақша"))
st.divider()

# ===== ЛОГИКА ДЛЯ РУССКОГО ЯЗЫКА =====
if lang == "Русский":
    st.markdown("### 📄 Выберите тип документа:")
    doc_type = st.selectbox("Тип документа", ("Трудовой договор", "NDA (Конфиденциальность)", "Договор оказания услуг"))

    with st.form("form_ru"):
        if doc_type == "Трудовой договор":
            c1, c2 = st.columns(2)
            comp = c1.text_input("Организация")
            pos = c1.text_input("Должность")
            work = c2.text_input("ФИО Работника")
            sal = c2.text_input("Оклад (₸)")
        elif doc_type == "NDA (Конфиденциальность)":
            c1, c2 = st.columns(2)
            comp = c1.text_input("Компания (Раскрывающая сторона)")
            work = c2.text_input("Получатель (ФИО)")
            fine = c1.text_input("Штраф за разглашение (₸)")
            term = c2.text_input("Срок действия (лет)")
        else:
            c1, c2 = st.columns(2)
            comp = c1.text_input("Заказчик")
            work = c2.text_input("Исполнитель")
            service = c1.text_input("Вид услуги")
            price = c2.text_input("Стоимость услуг (₸)")
        
        submitted = st.form_submit_button("СГЕНЕРИРОВАТЬ")

    if submitted:
        if comp and work:
            with st.spinner("Создание документа..."):
                time.sleep(1)
            
            # Наполнение документа в зависимости от типа
            if doc_type == "Трудовой договор":
                title, content = "ТРУДОВОЙ ДОГОВОР", f"<p>Работнику {work} в компании {comp} на позиции {pos} назначен оклад {sal} тенге.</p>"
            elif doc_type == "NDA (Конфиденциальность)":
                title, content = "СОГЛАШЕНИЕ О НЕРАЗГЛАШЕНИИ", f"<p>{work} обязуется хранить тайны {comp} в течение {term} лет. Штраф: {fine} тенге.</p>"
            else:
                title, content = "ДОГОВОР ОКАЗАНИЯ УСЛУГ", f"<p>Исполнитель {work} обязуется выполнить '{service}' для Заказчика {comp} за {price} тенге.</p>"

            html_doc = f"<html><body style='font-family:Arial;'><h1>{title}</h1><p>Дата: {date.today()}</p>{content}<br><p>Подпись: ________</p></body></html>"
            st.success("✅ Готово!")
            st.download_button("📥 Скачать .DOC", html_doc, f"{doc_type}_{work}.doc")

# ===== ЛОГИКА ДЛЯ КАЗАХСКОГО ЯЗЫКА =====
else:
    st.markdown("### 📄 Құжат түрін таңдаңыз:")
    doc_type = st.selectbox("Құжат түрі", ("Еңбек шарты", "NDA (Құпиялылық)", "Қызмет көрсету шарты"))

    with st.form("form_kz"):
        if doc_type == "Еңбек шарты":
            c1, c2 = st.columns(2)
            comp = c1.text_input("Жұмыс беруші")
            pos = c1.text_input("Қызметі")
            work = c2.text_input("Жұмыскер")
            sal = c2.text_input("Жалақы (₸)")
        elif doc_type == "NDA (Құпиялылық)":
            c1, c2 = st.columns(2)
            comp = c1.text_input("Мекеме (Ақпарат беруші)")
            work = c2.text_input("Алушы (Аты-жөні)")
            fine = c1.text_input("Айыппұл мөлшері (₸)")
            term = c2.text_input("Мерзімі (жыл)")
        else:
            c1, c2 = st.columns(2)
            comp = c1.text_input("Тапсырыс беруші")
            work = c2.text_input("Орындаушы")
            service = c1.text_input("Қызмет түрі")
            price = c2.text_input("Қызмет құны (₸)")

        submitted = st.form_submit_button("ДАЙЫНДАУ")

    if submitted:
        if comp and work:
            with st.spinner("Дайындалуда..."):
                time.sleep(1)
            
            if doc_type == "Еңбек шарты":
                title, content = "ЕҢБЕК ШАРТЫ", f"<p>{comp} мекемесі {work}-ны {pos} қызметіне {sal} теңге жалақымен қабылдайды.</p>"
            elif doc_type == "NDA (Құпиялылық)":
                title, content = "ҚҰПИЯЛЫЛЫҚ ТУРАЛЫ КЕЛІСІМ", f"<p>{work} {comp} мекемесінің құпияларын {term} жыл сақтауға міндетті. Айыппұл: {fine} теңге.</p>"
            else:
                title, content = "ҚЫЗМЕТ КӨРСЕТУ ШАРТЫ", f"<p>Орындаушы {work} Тапсырыс беруші {comp} үшін '{service}' жұмысын {price} теңгеге орындайды.</p>"

            html_doc_kz = f"<html><body style='font-family:Arial;'><h1>{title}</h1><p>Күні: {date.today()}</p>{content}<br><p>Қолы: ________</p></body></html>"
            st.success("✅ Дайын!")
            st.download_button("📥 Жүктеу .DOC", html_doc_kz, f"{doc_type}_{work}.doc")

# ===== FOOTER =====
st.markdown('<div class="footer-text">Made by Yeraly and Ramazan</div>', unsafe_allow_html=True)