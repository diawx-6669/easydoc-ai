import streamlit as st
import time
from datetime import date, datetime
import os
import pytz

# ===== 1. CORE CONFIG =====
st.set_page_config(page_title="EasyDoc AI | Enterprise", page_icon="📝", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = "Home"

def nav_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== 2. PREMIUM B2B DESIGN (CSS) =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp { background-color: #0b0f19; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    
    /* Центральный блок */
    .block-container { background: transparent; padding: 4rem 1rem; }

    /* Сайдбар и Меню */
    section[data-testid="stSidebar"] { background-color: #070a13 !important; border-right: 1px solid #1e293b; }
    .stRadio>div { display: flex; flex-direction: column; align-items: center; width: 100%; gap: 5px; }
    .stRadio>div>label {
        width: 100% !important;
        padding: 14px 20px !important;
        border-left: 3px solid transparent;
        transition: 0.2s;
        color: #94a3b8 !important;
        text-align: left;
        cursor: pointer;
    }
    .stRadio>div>label[data-testid="stWidgetActive"] {
        border-left: 3px solid #6366f1 !important;
        background: rgba(99, 102, 241, 0.08) !important;
        color: white !important;
    }

    /* Заголовки */
    .hero-title {
        font-size: 3.5rem; font-weight: 700; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(255,255,255,0.1));
    }
    
    /* Кнопки */
    .stButton>button {
        background: #6366f1 !important; color: white !important;
        border-radius: 6px !important; font-weight: 600 !important;
        border: none !important; height: 50px !important; width: 100% !important;
        text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px;
    }
    
    /* Документ Превью (A4 Style) */
    .doc-preview {
        background: white; color: #1a1a1a; padding: 60px;
        border-radius: 4px; box-shadow: 0 30px 60px rgba(0,0,0,0.6);
        font-family: 'Times New Roman', serif; line-height: 1.6;
        max-width: 650px; margin: 40px auto; position: relative;
        text-align: justify;
    }
    .doc-header { text-align: center; font-weight: bold; text-transform: uppercase; margin-bottom: 30px; font-size: 1.2rem; }
    .doc-stamp { 
        position: absolute; bottom: 50px; right: 50px; 
        width: 120px; border: 3px double #1e3a8a; 
        color: #1e3a8a; padding: 8px; text-align: center; 
        font-size: 0.7rem; transform: rotate(-12deg); font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ===== 3. ТЕКСТЫ ДОКУМЕНТОВ (БАЗА ДАННЫХ) =====
DOC_TEMPLATES = {
    "English": {
        "Employment": "This agreement is made between {pA} (Employer) and {pB} (Employee). The Employee is hired for the position mentioned in the records for a compensation of {sum} KZT per month.",
        "NDA": "The Disclosing Party {pA} and Receiving Party {pB} agree to keep all technical and business information strictly confidential. Penalty for breach: {sum} KZT.",
        "Service": "The Contractor {pB} agrees to provide services to {pA} as specified in the project scope. Total project value is set at {sum} KZT.",
        "Lease": "The Landlord {pA} grants the Tenant {pB} the right to occupy the premises. Monthly rent is {sum} KZT, payable on the 1st of each month."
    },
    "Русский": {
        "Трудовой договор": "Работодатель {pA} и Работник {pB} заключили настоящий договор. Работник принимается на работу с должностным окладом {sum} тенге в месяц.",
        "NDA (Конфиденциальность)": "Стороны {pA} и {pB} обязуются не разглашать коммерческую тайну. В случае нарушения, виновная сторона выплачивает штраф в размере {sum} тенге.",
        "Договор услуг": "Исполнитель {pB} обязуется оказать услуги Заказчику {pA}. Стоимость оказанных услуг согласно Акту составляет {sum} тенге.",
        "Договор аренды": "Арендодатель {pA} передает Арендатору {pB} во временное владение помещение. Арендная плата составляет {sum} тенге в месяц."
    },
    "Қазақша": {
        "Еңбек шарты": "Жұмыс беруші {pA} және Жұмысшы {pB} осы шартты жасасты. Жұмысшының айлық жалақысы {sum} теңге көлемінде белгіленді.",
        "NDA келісімі": "{pA} және {pB} тараптары коммерциялық құпияны сақтауға міндеттенеді. Ережені бұзған жағдайда айыппұл: {sum} теңге.",
        "Қызмет көрсету": "Орындаушы {pB} Тапсырыс берушіге {pA} қызмет көрсетуге міндеттенеді. Жұмыс құны: {sum} теңге.",
        "Жалдау шарты": "Жалға беруші {pA} Жалға алушыға {pB} нысанды пайдалануға береді. Ай сайынғы төлем: {sum} теңге."
    }
}

DICT = {
    "English": {"h_title": "EasyDoc AI", "btn_start": "Enter System", "btn_gen": "Generate", "f_pA": "Company", "f_pB": "Full Name", "f_sum": "Amount", "stamp": "VERIFIED BY AI"},
    "Русский": {"h_title": "EasyDoc AI", "btn_start": "Войти в систему", "btn_gen": "Сформировать", "f_pA": "Компания", "f_pB": "ФИО", "f_sum": "Сумма", "stamp": "ПОДТВЕРЖДЕНО AI"},
    "Қазақша": {"h_title": "EasyDoc AI", "btn_start": "Жүйеге кіру", "btn_gen": "Дайындау", "f_pA": "Мекеме", "f_pB": "Аты-жөні", "f_sum": "Құны", "stamp": "AI МАҚҰЛДАҒАН"}
}

# ===== 4. SIDEBAR =====
with st.sidebar:
    st.markdown("<h3 style='text-align:center;'>EasyDoc</h3>", unsafe_allow_html=True)
    lang = st.selectbox("Language", ("English", "Русский", "Қазақша"), index=1, label_visibility="collapsed")
    S = DICT[lang]
    
    st.divider()
    astana = datetime.now(pytz.timezone('Asia/Almaty'))
    st.markdown(f"<div style='text-align:center; font-size:0.8rem;'>{astana.strftime('%d.%m.%Y')} | <b>{astana.strftime('%H:%M')}</b></div>", unsafe_allow_html=True)
    
    st.divider()
    nav_list = ["Home", "Generator", "Feedback", "Authors"] if lang == "English" else ["Главная", "Генератор", "Отзывы", "Авторы"] if lang == "Русский" else ["Басты бет", "Генератор", "Кері байланыс", "Авторлар"]
    choice = st.radio("Menu", nav_list, label_visibility="collapsed")
    st.session_state.page = choice

# ===== 5. PAGES =====

# --- HOME ---
if st.session_state.page == nav_list[0]:
    st.markdown(f"<div class='hero-title'>{S['h_title']}</div>", unsafe_allow_html=True)
    
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1,2,1])
        c2.image("logo.png", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    if c2.button(S["btn_start"]): nav_to(nav_list[1])

# --- GENERATOR ---
elif st.session_state.page == nav_list[1]:
    c1, c2, c3 = st.columns([1,1,1])
    if os.path.exists("logo_pen.png"): c2.image("logo_pen.png", width=160)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ВЫБОР ТИПА ДОКУМЕНТА
    doc_type = st.selectbox("Type", list(DOC_TEMPLATES[lang].keys()))
    
    with st.form("gen_form"):
        pA = st.text_input(S["f_pA"])
        pB = st.text_input(S["f_pB"])
        summ = st.text_input(S["f_sum"])
        submitted = st.form_submit_button(S["btn_gen"])

    if submitted:
        if pA and pB:
            # ТЕКСТ ШАБЛОНА
            raw_text = DOC_TEMPLATES[lang][doc_type]
            final_text = raw_text.format(pA=pA, pB=pB, sum=summ)
            
            # ПРЕДПРОСМОТР (A4)
            st.markdown(f"""
            <div class="doc-preview">
                <div class="doc-header">{doc_type} №{int(time.time()) % 1000}</div>
                <p>г. Астана &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {astana.strftime('%d.%m.%Y')}</p>
                <p>{final_text}</p>
                <p>Настоящий документ составлен в двух экземплярах, имеющих равную юридическую силу. Стороны подтверждают достоверность данных.</p>
                <br><br>
                <p><b>ПОДПИСИ СТОРОН:</b></p>
                <p>________________ / {pA} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ________________ / {pB}</p>
                <div class="doc-stamp">{S['stamp']}<br>ID: {int(time.time()) % 10000}</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button("Скачать документ", final_text, f"{doc_type}.txt")
        else:
            st.error("Fill fields!")

# --- OTHERS ---
else:
    st.markdown(f"<h2 style='text-align:center;'>{st.session_state.page}</h2>", unsafe_allow_html=True)
    if os.path.exists("authors.jpg") and "Автор" in st.session_state.page:
        st.image("authors.jpg", use_container_width=True)
    st.write("<div style='text-align:center;'>Team: Yeraly & Ramazan</div>", unsafe_allow_html=True)