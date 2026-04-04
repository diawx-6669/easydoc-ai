import streamlit as st
import time
from datetime import datetime
import os
import pytz
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO

# ===== 1. НАСТРОЙКИ =====
st.set_page_config(page_title="EasyDoc AI", page_icon="📝", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = "Главная"

def nav_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== 🌐 ЛОКАЛИЗАЦИЯ =====
translations = {
    "Русский": {
        "main": "Главная",
        "generator": "Генератор",
        "reviews": "Отзывы",
        "authors": "Авторы",
        "start": "ЗАПУСТИТЬ ГЕНЕРАТОР",
        "settings": "Настройка шаблона",
        "create": "СОЗДАТЬ ДОКУМЕНТ",
        "download": "📥 СКАЧАТЬ WORD (.DOCX)",
        "date": "Дата",
        "time": "Время"
    },
    "English": {
        "main": "Home",
        "generator": "Generator",
        "reviews": "Reviews",
        "authors": "Authors",
        "start": "START GENERATOR",
        "settings": "Template Settings",
        "create": "CREATE DOCUMENT",
        "download": "📥 DOWNLOAD WORD (.DOCX)",
        "date": "Date",
        "time": "Time"
    },
    "Қазақша": {
        "main": "Басты бет",
        "generator": "Генератор",
        "reviews": "Пікірлер",
        "authors": "Авторлар",
        "start": "ГЕНЕРАТОРДЫ БАСТАУ",
        "settings": "Шаблонды баптау",
        "create": "ҚҰЖАТ ЖАСАУ",
        "download": "📥 WORD ЖҮКТЕУ (.DOCX)",
        "date": "Күні",
        "time": "Уақыты"
    }
}

# ===== CSS =====
st.markdown("""
<style>
.stApp { background-color: #090e1a; color: white; }
.main-title { font-size: 3rem; text-align:center; }
.main-sub { text-align:center; color:gray; }
.doc-preview {
    background:white; color:black; padding:40px;
    font-family:'Times New Roman';
}
</style>
""", unsafe_allow_html=True)

# ===== WORD =====
def create_docx(doc_type, data):
    doc = Document()
    heading = doc.add_heading(doc_type.upper(), 1)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(f"г. Астана    {datetime.now().strftime('%d.%m.%Y')}")

    doc.add_paragraph(f"{data['Сторона 1']} и {data['Сторона 2']} заключили договор")

    doc.add_heading('1. Предмет', 2)
    doc.add_paragraph(data['Детали'])

    doc.add_heading('2. Условия', 2)
    doc.add_paragraph(data['Условия'])

    doc.add_heading('3. Сроки', 2)
    doc.add_paragraph(data['Сроки'])

    doc.add_heading('4. Реквизиты', 2)
    doc.add_paragraph(data['Реквизиты'])

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ===== SIDEBAR =====
tz = pytz.timezone('Asia/Almaty')
now = datetime.now(tz)

with st.sidebar:
    st.title("EasyDoc AI")
    lang = st.selectbox("🌐 Language", ["Русский", "English", "Қазақша"])
    t = translations[lang]

    st.divider()
    st.write(f"📅 {t['date']}: {now.strftime('%d.%m.%Y')}")
    st.write(f"🕒 {t['time']}: {now.strftime('%H:%M:%S')}")

    menu = [t["main"], t["generator"], t["reviews"], t["authors"]]
    st.session_state.page = st.radio("Menu", menu)

# ===== ГЛАВНАЯ =====
if st.session_state.page == t["main"]:
    st.markdown("<div class='main-title'>EasyDoc AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-sub'>AI помощник для документов</div>", unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,2,1])
    if col2.button(t["start"], use_container_width=True):
        nav_to(t["generator"])

# ===== ГЕНЕРАТОР =====
elif st.session_state.page == t["generator"]:

    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        if os.path.exists("logo_pen.png"):
            st.image("logo_pen.png", use_container_width=True)

    st.header(t["settings"])

    doc_choice = st.selectbox("Тип документа", ["Договор услуг","Аренда","Купля-продажа"])

    with st.form("form"):
        col1,col2 = st.columns(2)
        org = col1.text_input("Сторона 1")
        client = col2.text_input("Сторона 2")

        d1 = st.text_input("Предмет")
        d2 = st.text_input("Условия")
        d3 = st.text_input("Сроки")
        address = st.text_area("Реквизиты")

        submitted = st.form_submit_button(t["create"])

    if submitted and org and client:

        colL,colR = st.columns([2,1])

        with colL:
            st.markdown("<div class='doc-preview'>", unsafe_allow_html=True)

            st.markdown(f"<h2 style='text-align:center'>{doc_choice}</h2>", unsafe_allow_html=True)
            st.write(f"г. Астана    {now.strftime('%d.%m.%Y')}")

            st.write(f"{org} и {client} заключили договор")

            st.markdown("### 1. Предмет")
            st.write(d1)

            st.markdown("### 2. Условия")
            st.write(d2)

            st.markdown("### 3. Сроки")
            st.write(d3)

            st.markdown("### 4. Реквизиты")
            st.write(address)

            st.write("\nПодписи:")
            st.write("___________     ___________")

            st.markdown("</div>", unsafe_allow_html=True)

            doc_data = {
                "Сторона 1": org,
                "Сторона 2": client,
                "Детали": d1,
                "Условия": d2,
                "Сроки": d3,
                "Реквизиты": address
            }

            file = create_docx(doc_choice, doc_data)

            st.download_button(t["download"], file, file_name="doc.docx")

        with colR:
            st.success("Документ готов")

# ===== ОТЗЫВЫ =====
elif st.session_state.page == t["reviews"]:
    st.text_input("Имя")
    st.text_area("Отзыв")
    if st.button("Отправить"):
        st.success("Спасибо!")

# ===== АВТОРЫ =====
elif st.session_state.page == t["authors"]:
    col1,col2 = st.columns([1,2])

    with col1:
        if os.path.exists("authors.jpg"):
            st.image("authors.jpg", width=200)

    with col2:
        st.markdown("### Yeraly & Ramazan")
        st.write("8 класс | Астана")
        st.write("Создатели EasyDoc AI")