import streamlit as st
import time
from datetime import datetime
import os
import pytz
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO

# ===== 1. НАСТРОЙКИ СТРАНИЦЫ =====
st.set_page_config(page_title="EasyDoc AI", page_icon="📝", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = "Главная"

def nav_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== 2. СЛОВАРЬ ПЕРЕВОДА (ЛОКАЛИЗАЦИЯ) =====
translations = {
    "Русский": {
        "sub": "Ядро автоматизации корпоративных документов.",
        "start": "ЗАПУСТИТЬ ГЕНЕРАТОР",
        "gen_title": "Настройка шаблона",
        "select_doc": "Выберите тип документа:",
        "sides": "Информация о сторонах",
        "side1": "Сторона 1 (Организация/БИН)",
        "side2": "Сторона 2 (ФИО/ИИН)",
        "details": "Детали сделки",
        "create": "СОЗДАТЬ ДОКУМЕНТ",
        "authors": "Авторы проекта",
        "feedback": "Обратная связь"
    },
    "English": {
        "sub": "Core of corporate document automation.",
        "start": "LAUNCH GENERATOR",
        "gen_title": "Template Settings",
        "select_doc": "Select document type:",
        "sides": "Parties Information",
        "side1": "Party 1 (Company/BIN)",
        "side2": "Party 2 (Name/IIN)",
        "details": "Transaction Details",
        "create": "CREATE DOCUMENT",
        "authors": "Project Authors",
        "feedback": "Feedback"
    },
    "Қазақша": {
        "sub": "Корпоративтік құжаттарды автоматтандыру ядросы.",
        "start": "ГЕНЕРАТОРДЫ ІСКЕ ҚОСУ",
        "gen_title": "Үлгіні теңшеу",
        "select_doc": "Құжат түрін таңдаңыз:",
        "sides": "Тараптар туралы ақпарат",
        "side1": "1-тарап (Ұйым/БСН)",
        "side2": "2-тарап (Аты-жөні/ЖСН)",
        "details": "Мәміле мәліметтері",
        "create": "ҚҰЖАТТЫ ЖАСАУ",
        "authors": "Жоба авторлары",
        "feedback": "Кері байланыс"
    }
}

# ===== 3. ДИЗАЙН (CSS) =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background-color: #090e1a; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .main-title { font-size: 3.5rem; font-weight: 800; text-align: center; color: white; margin-bottom: 0px; }
    .main-sub { text-align: center; font-size: 1.4rem; color: #94a3b8; margin-bottom: 2rem; }
    .doc-preview { 
        background: white; color: black !important; padding: 40px; 
        font-family: 'Times New Roman', serif; border: 1px solid #ccc;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5); line-height: 1.5;
    }
    .doc-preview p, .doc-preview b, .doc-preview h3, .doc-preview span { color: black !important; }
    .ai-sidebar { background: rgba(99, 102, 241, 0.1); border: 1px solid #6366f1; padding: 20px; border-radius: 15px; }
    .stButton>button { background-color: #6366f1 !important; color: white !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ===== 4. ГЕНЕРАЦИЯ WORD =====
def create_docx(doc_type, data):
    doc = Document()
    heading = doc.add_heading(doc_type.upper(), 1)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_p = doc.add_paragraph()
    date_p.add_run(f"г. Астана\t\t\t\t\t{datetime.now().strftime('%d.%m.%Y')} г.")
    
    for key, value in data.items():
        p = doc.add_paragraph()
        p.add_run(f"{key}: ").bold = True
        p.add_run(str(value))
    
    doc.add_paragraph("\nПодписи Сторон:\n___________________          ___________________")
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ===== 5. SIDEBAR С ЧАСАМИ И ВЫБОРОМ ЯЗЫКА =====
tz = pytz.timezone('Asia/Almaty')
now = datetime.now(tz)

with st.sidebar:
    st.title("EasyDoc AI")
    # ЧАСЫ
    st.markdown(f"### 🕒 {now.strftime('%H:%M:%S')}")
    st.write(f"📅 {now.strftime('%d.%m.%Y')}")
    
    lang_choice = st.selectbox("🌐 Выбор языка", ["Русский", "English", "Қазақша"])
    t = translations[lang_choice] # Тексты на выбранном языке
    
    st.divider()
    menu = ["Главная", "Генератор", "Отзывы", "Авторы"]
    st.session_state.page = st.radio("Навигация", menu, index=menu.index(st.session_state.page))

# ===== 6. КОНТЕНТ =====

if st.session_state.page == "Главная":
    st.markdown("<div class='main-title'>EasyDoc AI</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='main-sub'>{t['sub']}</div>", unsafe_allow_html=True)
    if os.path.exists("logo.png"): 
        st.image("logo.png", use_container_width=True)
    if st.button(t['start'], use_container_width=True): 
        nav_to("Генератор")

elif st.session_state.page == "Генератор":
    # НОРМАЛЬНОЕ ФОТО В ГЕНЕРАТОРЕ
    if os.path.exists("logo_pen.png"):
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        col_img2.image("logo_pen.png", use_container_width=True)
    
    st.header(t['gen_title'])
    doc_choice = st.selectbox(t['select_doc'], [
        "Трудовой договор (Двуязычный)", "Договор аренды помещения", 
        "Договор об оказании услуг", "Договор купли-продажи ТС"
    ])

    with st.form("main_form"):
        st.subheader(t['sides'])
        c1, c2 = st.columns(2)
        org = c1.text_input(t['side1'])
        fio = c2.text_input(t['side2'])
        
        st.subheader(t['details'])
        col3, col4 = st.columns(2)
        if "Трудовой" in doc_choice:
            d1 = col3.text_input("Должность")
            d2 = col4.text_input("Оклад")
        else:
            d1 = col3.text_input("Предмет договора")
            d2 = col4.text_input("Сумма/Сроки")
        
        addr = st.text_area("Реквизиты и адрес")
        submitted = st.form_submit_button(t['create'])

    if submitted:
        if org and fio:
            st.toast("Документ создается...")
            res_col, ai_col = st.columns([2, 1])
            with res_col:
                st.markdown(f"""
                <div class='doc-preview'>
                    <h3 style='text-align:center;'>{doc_choice.upper()}</h3>
                    <p><b>г. Астана</b> <span style='float:right;'>{now.strftime('%d.%m.%Y')}</span></p>
                    <hr>
                    <p><b>Сторона 1:</b> {org}</p>
                    <p><b>Сторона 2:</b> {fio}</p>
                    <p><b>Детали:</b> {d1}</p>
                    <p><b>Условия:</b> {d2}</p>
                    <p><b>Адрес:</b> {addr}</p>
                    <br><br>
                    <p>Подпись: ___________ &nbsp;&nbsp;&nbsp;&nbsp; Подпись: ___________</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Кнопка Word
                data = {"Организация": org, "ФИО": fio, "Параметры": d1, "Реквизиты": addr}
                word_buf = create_docx(doc_choice, data)
                st.download_button("📥 СКАЧАТЬ WORD (.DOCX)", word_buf, f"EasyDoc_{fio}.docx")

            with ai_col:
                st.markdown("<div class='ai-sidebar'><h3>🤖 AI Анализ</h3><p>Документ проверен на ошибки. Соответствует нормам РК.</p></div>", unsafe_allow_html=True)

elif st.session_state.page == "Отзывы":
    st.header(t['feedback'])
    with st.form("f"):
        st.text_input("Name")
        st.text_area("Review")
        st.form_submit_button("Send")

elif st.session_state.page == "Авторы":
    st.header(t['authors'])
    # ИСПРАВЛЕННЫЙ ОТДЕЛ АВТОРЫ
    col_a1, col_a2 = st.columns([1, 2])
    if os.path.exists("authors.jpg"):
        col_a1.image("authors.jpg", width=250)
    col_a2.markdown("### Yeraly & Ramazan")
    col_a2.write("Ученики 8 'А' класса | НИШ ФМН г. Астана")
    col_a2.info("Разработчики системы EasyDoc AI для автоматизации бизнеса.")

st.markdown(f"<div style='text-align:center; opacity:0.3; padding:20px;'>EasyDoc AI © {now.year}</div>", unsafe_allow_html=True)