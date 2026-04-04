import streamlit as st
import time
from datetime import date, datetime
import os
import pytz

# ===== 1. КОНФИГУРАЦИЯ СТРАНИЦЫ (СТРОГАЯ) =====
st.set_page_config(
    page_title="EasyDoc AI | Intelligent Business Systems", 
    page_icon="📝", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Инициализация состояния страницы
if 'page' not in st.session_state:
    st.session_state.page = "Home"

def nav_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== 2. PREMIUM ДИЗАЙН (CSS) - ТВОЙ СТИЛЬ + ПРЕДПРОСМОТР =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    .stApp { 
        background-color: #090e1a;
        background-image: radial-gradient(at 10% 10%, rgba(31, 41, 55, 0.15) 0px, transparent 50%), radial-gradient(at 90% 90%, rgba(17, 24, 39, 0.1) 0px, transparent 50%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        background: rgba(17, 24, 39, 0.6);
        padding: 4rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(15px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }

    section[data-testid="stSidebar"] {
        background-color: #090e1a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04);
    }

    .stRadio>div { gap: 10px; }
    .stRadio>div>label {
        background-color: transparent !important;
        color: #94a3b8 !important;
        border-radius: 8px;
        padding: 10px 15px !important;
        border: 1px solid transparent;
        transition: 0.2s;
        font-weight: 500;
    }
    .stRadio>div>label:hover { background-color: rgba(255, 255, 255, 0.03) !important; color: white !important; }
    .stRadio>div>label[data-testid="stWidgetActive"] { 
        background-color: rgba(99, 102, 241, 0.05) !important;
        color: #a5b4fc !important;
        border: 1px solid rgba(99, 102, 241, 0.1) !important;
        border-left: 3px solid #6366f1 !important;
    }

    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; letter-spacing: -0.03em; }
    
    .main-title { 
        font-size: 3.8rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem;
        background: linear-gradient(120deg, #ffffff, #c7d2fe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px rgba(165, 180, 252, 0.2);
    }
    .main-sub { font-size: 1.3rem; text-align: center; color: #94a3b8; margin-bottom: 3.5rem; font-weight: 400; }

    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #111827 !important;
        color: #f1f5f9 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 10px;
        padding: 10px;
    }

    .stButton>button {
        background: linear-gradient(180deg, #4f46e5 0%, #3730a3 100%);
        color: white; border: 1px solid #312e81; border-radius: 12px;
        font-weight: 600; height: 50px; width: 100%; transition: 0.2s ease;
        text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.9rem;
    }

    /* СТИЛЬ ПРЕДПРОСМОТРА (БЕЛЫЙ ЛИСТ) */
    .doc-preview {
        background: white; color: #1a1a1a; padding: 50px;
        border-radius: 4px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        font-family: 'Times New Roman', serif; line-height: 1.5;
        max-width: 100%; margin: 30px auto; position: relative;
        text-align: justify;
    }
    .doc-header { text-align: center; font-weight: bold; text-transform: uppercase; margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
    .doc-stamp { 
        position: absolute; bottom: 40px; right: 40px; 
        width: 110px; border: 3px double #1e3a8a; 
        color: #1e3a8a; padding: 5px; text-align: center; 
        font-size: 0.7rem; transform: rotate(-15deg); font-weight: bold;
    }
    
    .footer { text-align: center; margin-top: 5rem; padding: 2rem; border-top: 1px solid #1f2937; opacity: 0.4; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ===== 3. ТЕКСТЫ И СЛОВАРЬ =====
DOC_TEXTS = {
    "English": {
        "Employment Agreement": "Company {pA} hires {pB} for the role of {d1}. Salary: {d2} KZT.",
        "NDA": "Parties {pA} and {pB} agree to keep {d1} secret. Penalty: {d2} KZT.",
        "Service Level Agreement": "Contractor {pB} provides {d1} to {pA} for {d2} KZT.",
        "Sales Purchase Contract": "Seller {pA} delivers {d1} to Buyer {pB} for {d2} KZT.",
        "Residential Lease": "Landlord {pA} leases property to {pB}. Monthly rent: {d2} KZT."
    },
    "Русский": {
        "Трудовой договор": "Мекеме {pA} жұмысқа {pB} азаматын {d1} лауазымына қабылдайды. Жалақысы: {d2} теңге.",
        "Соглашение NDA": "Стороны {pA} и {pB} обязуются хранить в тайне {d1}. Штраф: {d2} тенге.",
        "Договор оказания услуг": "Исполнитель {pB} оказывает услуги {d1} для {pA}. Стоимость: {d2} тенге.",
        "Договор купли-продажи": "Продавец {pA} передает товар {d1} Покупателю {pB}. Цена: {d2} тенге.",
        "Договор аренды": "Арендодатель {pA} сдает жилье {pB}. Плата: {d2} тенге."
    },
    "Қазақша": {
        "Еңбек шарты": "{pA} мекемесі {pB} азаматын {d1} қызметіне қабылдайды. Жалақы: {d2} теңге.",
        "NDA келісімі": "{pA} және {pB} тараптары {d1} құпия сақтауға келісті. Айыппұл: {d2} теңге.",
        "Қызмет көрсету шарты": "{pB} орындаушы {pA} үшін {d1} қызметін көрсетеді. Құны: {d2} теңге.",
        "Сату-сатып алу шарты": "{pA} сатушы {pB} сатып алушыға {d1} береді. Бағасы: {d2} теңге.",
        "Жалдау шарты": "{pA} жалға беруші {pB} жалға алушыға нысанды береді. Төлем: {d2} теңге."
    }
}

DICT = {
    "English": {
        "nav": ["Home", "Generator", "Feedback", "Authors"],
        "h_title": "EasyDoc AI", "h_sub": "Enterprise Document Automation Core.",
        "start": "Launch Generator", "type_lab": "Document Category",
        "f_pA": "Organization Name", "f_pB": "Full Name", 
        "f_d1": "Detail (Position/Item)", "f_d2": "Value (KZT)",
        "gen": "GENERATE DOCUMENT", "success": "Ready.", "stamp": "AI APPROVED"
    },
    "Русский": {
        "nav": ["Главная", "Генератор", "Отзывы", "Авторы"],
        "h_title": "EasyDoc AI", "h_sub": "Ядро автоматизации корпоративных документов.",
        "start": "Открыть Генератор", "type_lab": "Категория документа",
        "f_pA": "Организация", "f_pB": "ФИО", 
        "f_d1": "Детали (Должность/Товар)", "f_d2": "Сумма (₸)",
        "gen": "СФОРМИРОВАТЬ ПРЕВЬЮ", "success": "Готово.", "stamp": "ОДОБРЕНО AI"
    },
    "Қазақша": {
        "nav": ["Басты бет", "Генератор", "Кері байланыс", "Авторлар"],
        "h_title": "EasyDoc AI", "h_sub": "Құжаттарды автоматтандыру жүйесі.",
        "start": "Генераторды қосу", "type_lab": "Құжат түрі",
        "f_pA": "Мекеме атауы", "f_pB": "Толық аты-жөні", 
        "f_d1": "Мәліметтер", "f_d2": "Қаржы (₸)",
        "gen": "ҚҰЖАТТЫ ДАЙЫНДАУ", "success": "Дайын.", "stamp": "AI МАҚҰЛДАҒАН"
    }
}

# ===== 4. SIDEBAR =====
with st.sidebar:
    st.markdown("<h3 style='text-align:center;'>EasyDoc Panel</h3>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Language", ("English", "Русский", "Қазақша"), index=1)
    S = DICT[lang_choice]
    
    st.divider()
    astana_tz = pytz.timezone('Asia/Almaty')
    now = datetime.now(astana_tz)
    st.metric(label="Astana Time", value=now.strftime("%H:%M:%S"))
    
    st.divider()
    page_selection = st.radio("Navigation", S["nav"], label_visibility="collapsed")
    st.session_state.page = page_selection

# ===== 5. КОНТЕНТ =====

# --- ГЛАВНАЯ ---
if st.session_state.page == S["nav"][0]:
    st.markdown(f"<div class='main-title'>{S['h_title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='main-sub'>{S['h_sub']}</div>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.divider()
    col_l, col_m, col_r = st.columns([1,2,1])
    if col_m.button(S["start"]): nav_to(S["nav"][1])

# --- ГЕНЕРАТОР (ПРЕВЬЮ ТУТ) ---
elif st.session_state.page == S["nav"][1]:
    # Лого по центру (среднее)
    c1, c2, c3 = st.columns([1,1,1])
    if os.path.exists("logo_pen.png"): c2.image("logo_pen.png", width=180)
        
    st.header(S["type_lab"])
    # Список типов документов из словаря
    doc_types_list = list(DOC_TEXTS[lang_choice].keys())
    doc_choice = st.selectbox("", doc_types_list, label_visibility="collapsed")
    
    with st.form("pro_gen_form"):
        c1, c2 = st.columns(2)
        pA = c1.text_input(S["f_pA"])
        pB = c2.text_input(S["f_pB"])
        d1 = c1.text_input(S["f_d1"])
        d2 = c2.text_input(S["f_d2"])
        submitted = st.form_submit_button(S["gen"])
        
    if submitted:
        if pA and pB:
            with st.spinner("Processing..."): time.sleep(1)
            
            # ВЫВОД ПРЕВЬЮ (БЕЛЫЙ ЛИСТ)
            st.markdown(f"""
            <div class="doc-preview">
                <div class="doc-header">{doc_choice.upper()} №{int(time.time())%1000}</div>
                <p><b>City:</b> Astana &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> {now.strftime('%d.%m.%Y')}</p>
                <p>{DOC_TEXTS[lang_choice][doc_choice].format(pA=pA, pB=pB, d1=d1, d2=d2)}</p>
                <p>This document is electronically generated and holds legal power within the digital infrastructure of EasyDoc AI.</p>
                <br><br>
                <p>____________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ____________________</p>
                <p><i>Signature (Party A) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Signature (Party B)</i></p>
                <div class="doc-stamp">{S['stamp']}<br>VERIFIED</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(S["success"])
            st.download_button("📥 Download Official .DOC", f"DOC: {doc_choice}\nFrom: {pA}\nTo: {pB}", f"EasyDoc_{pB}.doc")
        else:
            st.error("Fill fields.")

# --- ОТЗЫВЫ ---
elif st.session_state.page == S["nav"][2]:
    st.markdown(f"<h2 style='text-align:center;'>{S['feed_h']}</h2>", unsafe_allow_html=True)
    with st.form("feedback_form"):
        st.text_input("Name")
        st.text_area("Message")
        if st.form_submit_button("Submit"):
            st.balloons()
            st.success("Sent!")

# --- АВТОРЫ ---
elif st.session_state.page == S["nav"][3]:
    st.markdown(f"<h2 style='text-align:center;'>{S['auth_h']}</h2>", unsafe_allow_html=True)
    if os.path.exists("authors.jpg"): st.image("authors.jpg", use_container_width=True)
    st.markdown("<div style='text-align:center; color:#94a3b8;'><p>Yeraly & Ramazan | 8th Grade | Astana</p></div>", unsafe_allow_html=True)

# ===== 6. ФУТЕР =====
st.markdown("<div class='footer'>EasyDoc AI System &copy; 2026 | Astana</div>", unsafe_allow_html=True)