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

# ===== 2. СИСТЕМА ЯЗЫКОВ =====
lang_dict = {
    "Русский": {
        "menu": ["Главная", "Генератор", "Отзывы", "Авторы"],
        "main_title": "EasyDoc AI",
        "main_sub": "Ваш надежный ИИ-помощник для малого бизнеса.",
        "btn_start": "ЗАПУСТИТЬ ГЕНЕРАТОР",
        "gen_header": "Настройка шаблона",
        "doc_type": "Выберите тип документа:",
        "parties": "Информация о сторонах",
        "side1_lab": "Сторона 1 (Организация/БИН)",
        "side2_lab": "Сторона 2 (ФИО/ИИН)",
        "details": "Детали сделки",
        "addr_lab": "Юридические адреса и реквизиты",
        "btn_gen": "СОЗДАТЬ ДОКУМЕНТ",
        "ai_title": "🤖 EasyDoc AI Helper",
        "ai_status": "Документ успешно сформирован."
    },
    "English": {
        "menu": ["Home", "Generator", "Feedback", "Authors"],
        "main_title": "EasyDoc AI",
        "main_sub": "Your reliable AI assistant for small business.",
        "btn_start": "START GENERATOR",
        "gen_header": "Template Configuration",
        "doc_type": "Select document type:",
        "parties": "Parties Information",
        "side1_lab": "Side 1 (Organization/BIN)",
        "side2_lab": "Side 2 (Full Name/IIN)",
        "details": "Deal Details",
        "addr_lab": "Legal Addresses & Requisites",
        "btn_gen": "GENERATE DOCUMENT",
        "ai_title": "🤖 EasyDoc AI Helper",
        "ai_status": "Document generated successfully."
    },
    "Қазақша": {
        "menu": ["Басты бет", "Генератор", "Пікірлер", "Авторлар"],
        "main_title": "EasyDoc AI",
        "main_sub": "Шағын бизнеске арналған сенімді ИИ-көмекшіңіз.",
        "btn_start": "ГЕНЕРАТОРДЫ ҚОСУ",
        "gen_header": "Үлгіні баптау",
        "doc_type": "Құжат түрін таңдаңыз:",
        "parties": "Тараптар ақпараты",
        "side1_lab": "1-тарап (Ұйым/БСН)",
        "side2_lab": "2-тарап (Аты-жөні/ЖСН)",
        "details": "Мәміле мәліметтері",
        "addr_lab": "Заңды мекенжайлар мен деректемелер",
        "btn_gen": "ҚҰЖАТТЫ ЖАСАУ",
        "ai_title": "🤖 EasyDoc AI Helper",
        "ai_status": "Құжат сәтті жасалды."
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
        box-shadow: 0 15px 35px rgba(0,0,0,0.5); line-height: 1.4;
    }
    .doc-preview p, .doc-preview div, .doc-preview b, .doc-preview h3, .doc-preview h4 { color: black !important; }
    .ai-sidebar { background: rgba(99, 102, 241, 0.1); border: 1px solid #6366f1; padding: 20px; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# ===== 4. ГЕНЕРАЦИЯ WORD =====
def create_docx(doc_type, data):
    doc = Document()
    heading = doc.add_heading(doc_type.upper(), 1)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_p = doc.add_paragraph()
    date_p.add_run(f"г. Астана / Astana q.\t\t\t\t\t{datetime.now().strftime('%d.%m.%Y')}")
    
    p = doc.add_paragraph()
    p.add_run(f"\n{data.get('Сторона 1', '__________')} & {data.get('Сторона 2', '__________')}\n")
    
    doc.add_heading('1. ПРЕДМЕТ / МӘНІ', level=2)
    doc.add_paragraph(str(data.get('Детали', '')))
    
    doc.add_heading('2. РЕКВИЗИТЫ / ДЕРЕКТЕМЕЛЕР', level=2)
    doc.add_paragraph(str(data.get('Реквизиты', '')))
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ===== 5. SIDEBAR С ЧАСАМИ =====
tz = pytz.timezone('Asia/Almaty')
now = datetime.now(tz)

with st.sidebar:
    st.title("EasyDoc AI")
    # Живые часы
    st.markdown(f"### 🕒 {now.strftime('%H:%M:%S')}")
    sel_lang = st.selectbox("🌐 Язык / Language", ["Русский", "English", "Қазақша"])
    L = lang_dict[sel_lang]
    
    st.divider()
    st.write(f"📅 **{now.strftime('%d.%m.%Y')}**")
    
    # Синхронизация навигации с выбранным языком
    st.session_state.page = st.radio("Навигация", L["menu"])

# ===== 6. КОНТЕНТ =====

if st.session_state.page in ["Главная", "Home", "Басты бет"]:
    st.markdown(f"<div class='main-title'>{L['main_title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='main-sub'>{L['main_sub']}</div>", unsafe_allow_html=True)
    if os.path.exists("logo.png"): 
        st.image("logo.png", use_container_width=True)
    st.divider()
    _, col_m, _ = st.columns([1,2,1])
    if col_m.button(L["btn_start"], use_container_width=True): 
        st.session_state.page = L["menu"][1] # Переход на генератор
        st.rerun()

elif st.session_state.page in ["Генератор", "Generator"]:
    # Логотип по центру
    if os.path.exists("logo_pen.png"):
        c_l, c_m, c_r = st.columns([1, 1.5, 1])
        c_m.image("logo_pen.png", use_container_width=True)
    
    st.header(L["gen_header"])
    doc_choice = st.selectbox(L["doc_type"], [
        "Трудовой договор (Двуязычный Каз/Рус)",
        "Договор купли-продажи имущества",
        "Договор аренды помещения",
        "Договор об оказании услуг",
        "Договор купли-продажи ТС (Авто)"
    ])

    with st.form("main_form"):
        st.subheader(L["parties"])
        c1, c2 = st.columns(2)
        org_name = c1.text_input(L["side1_lab"])
        client_name = c2.text_input(L["side2_lab"])
        
        st.subheader(L["details"])
        col3, col4 = st.columns(2)
        if "Трудовой" in doc_choice:
            d1 = col3.text_input("Должность / Лауазымы")
            d2 = col4.text_input("Оклад / Жалақы")
            d3 = st.text_input("Срок / Мерзімі")
        else:
            d1 = col3.text_input("Предмет / Заты")
            d2 = col4.text_input("Сумма / Сомасы")
            d3 = st.text_input("Сроки / Мерзімдері")

        address = st.text_area(L["addr_lab"])
        submitted = st.form_submit_button(L["btn_gen"])

    if submitted:
        if org_name and client_name:
            res_col, ai_col = st.columns([2, 1])
            with res_col:
                st.markdown("<div class='doc-preview'>", unsafe_allow_html=True)
                if "Трудовой" in doc_choice:
                    st.markdown("<h3 style='text-align:center;'>№ __ ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР</h3>", unsafe_allow_html=True)
                    st.write(f"Астана қ. / г. Астана — {now.strftime('%d.%m.%Y')}")
                    k1, k2 = st.columns(2)
                    k1.markdown(f"**Жұмыс беруші:** {org_name}\n\n**Жұмыскер:** {client_name}\n\n**Лауазымы:** {d1}")
                    k2.markdown(f"**Работодатель:** {org_name}\n\n**Работник:** {client_name}\n\n**Должность:** {d1}")
                    st.write(f"**Жалақы / Оклад:** {d2} KZT")
                else:
                    st.markdown(f"<h3 style='text-align:center;'>{doc_choice.upper()}</h3>", unsafe_allow_html=True)
                    st.write(f"г. Астана, Дата: {now.strftime('%d.%m.%Y')}")
                    st.write(f"**Стороны / Тараптар:** {org_name} & {client_name}")
                    st.write(f"**Детали:** {d1} | **Условия:** {d2}")
                
                st.write(f"**Реквизиты:** {address}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Кнопка скачивания
                doc_data = {"Сторона 1": org_name, "Сторона 2": client_name, "Детали": d1, "Реквизиты": address}
                word_buf = create_docx(doc_choice, doc_data)
                st.download_button("📥 WORD (.DOCX)", word_buf, f"{client_name}.docx")

            with ai_col:
                st.markdown(f"""
                <div class='ai-sidebar'>
                    <h3 style='color:#6366f1;'>{L['ai_title']}</h3>
                    <p><b>Статус:</b> {L['ai_status']}</p>
                    <p>✅ Формат РК соблюден.</p>
                </div>
                """, unsafe_allow_html=True)

elif st.session_state.page in ["Авторы", "Authors", "Авторлар"]:
    st.header(L["menu"][3])
    col_img, col_txt = st.columns([1, 2])
    
    if os.path.exists("authors.jpg"):
        col_img.image("authors.jpg", width=300)
    
    with col_txt:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; border-left: 5px solid #6366f1;'>
            <h2 style='margin-top:0;'>Yeraly & Ramazan</h2>
            <p style='font-size: 1.2rem; color: #94a3b8;'>8 класс | НИШ ib Астана</p>
            <p>Разработчики интеллектуальной системы автоматизации документов EasyDoc AI.</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page in ["Отзывы", "Feedback", "Пікірлер"]:
    st.header(L["menu"][2])
    with st.form("feed"):
        st.text_input("Name / Аты")
        st.text_area("Message / Хабарлама")
        st.form_submit_button("Send / Жіберу")

st.markdown(f"<div style='text-align:center; opacity:0.3; padding:20px;'>EasyDoc AI ©️ {now.year} | Astana</div>", unsafe_allow_html=True)