import streamlit as st
import time
from datetime import date, datetime
import os
import pytz

# ===== 1. CORE CONFIG =====
st.set_page_config(page_title="EasyDoc AI", page_icon="📝", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = "Home"

def nav_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== 2. ULTRA-CLEAN B2B DESIGN (CSS) =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp { background-color: #0b0f19; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    
    /* Центральный контейнер */
    .block-container {
        background: rgba(17, 24, 39, 0.4);
        padding: 4rem 2rem;
        border-radius: 0;
        border: none;
    }

    /* Сайдбар и индикатор активной страницы */
    section[data-testid="stSidebar"] { background-color: #070a13 !important; border-right: 1px solid #1e293b; }
    
    .stRadio>div { display: flex; flex-direction: column; align-items: center; width: 100%; }
    .stRadio>div>label {
        width: 100% !important;
        padding: 12px 20px !important;
        border-left: 3px solid transparent;
        transition: 0.2s;
        color: #94a3b8 !important;
        text-align: center;
    }
    /* Синяя полоска слева для активного пункта */
    .stRadio>div>label[data-testid="stWidgetActive"] {
        border-left: 3px solid #6366f1 !important;
        background: rgba(99, 102, 241, 0.05) !important;
        color: white !important;
    }

    /* Заголовки со свечением */
    .hero-title {
        font-size: 3.5rem; font-weight: 700; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem; filter: drop-shadow(0 0 15px rgba(255,255,255,0.1));
    }
    
    /* Кнопки: Строгий бизнес-стиль */
    .stButton>button {
        background: #6366f1 !important; color: white !important;
        border-radius: 4px !important; font-weight: 600 !important;
        border: none !important; height: 48px !important; width: 100% !important;
        letter-spacing: 0.5px; text-transform: uppercase; font-size: 0.85rem;
    }
    
    /* Поля ввода: Тонкие границы */
    input { border: 1px solid #1e293b !important; background: #0f172a !important; border-radius: 4px !important; }

    /* ПРЕДПРОСМОТР ДОКУМЕНТА (ЛИСТ А4) */
    .doc-preview {
        background: white; color: #1a1a1a; padding: 50px;
        border-radius: 2px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        font-family: 'Times New Roman', serif; line-height: 1.5;
        max-width: 600px; margin: 30px auto; position: relative;
    }
    .doc-header { text-align: center; font-weight: bold; text-transform: uppercase; margin-bottom: 40px; }
    .doc-stamp { 
        position: absolute; bottom: 60px; right: 60px; 
        width: 100px; opacity: 0.7; border: 3px double #1e3a8a; 
        color: #1e3a8a; padding: 5px; text-align: center; font-size: 0.6rem; transform: rotate(-15deg);
    }
</style>
""", unsafe_allow_html=True)

# ===== 3. DICTIONARY (STRICT) =====
DICT = {
    "English": {
        "nav": ["Home", "Generator", "Feedback", "Authors"],
        "h_title": "EasyDoc AI", "h_sub": "Standardized Automation Platform",
        "btn_start": "Enter System", "btn_gen": "Generate Document",
        "f_pA": "Party A (Company)", "f_pB": "Party B (Full Name)", "f_sum": "Amount (KZT)",
        "preview_h": "Document Live Preview", "stamp": "APPROVED BY AI"
    },
    "Русский": {
        "nav": ["Главная", "Генератор", "Отзывы", "Авторы"],
        "h_title": "EasyDoc AI", "h_sub": "Платформа стандартизации документов",
        "btn_start": "Войти в систему", "btn_gen": "Сформировать документ",
        "f_pA": "Сторона А (Компания)", "f_pB": "Сторона Б (ФИО)", "f_sum": "Сумма (₸)",
        "preview_h": "Предпросмотр документа", "stamp": "ПОДТВЕРЖДЕНО AI"
    },
    "Қазақша": {
        "nav": ["Басты бет", "Генератор", "Кері байланыс", "Авторлар"],
        "h_title": "EasyDoc AI", "h_sub": "Құжаттарды стандарттау платформасы",
        "btn_start": "Жүйеге кіру", "btn_gen": "Құжатты дайындау",
        "f_pA": "А Тарабы (Мекеме)", "f_pB": "Б Тарабы (Аты-жөні)", "f_sum": "Құны (₸)",
        "preview_h": "Құжатты алдын ала қарау", "stamp": "AI МАҚҰЛДАҒАН"
    }
}

# ===== 4. SIDEBAR =====
with st.sidebar:
    st.markdown("<h3 style='text-align:center;'>EasyDoc</h3>", unsafe_allow_html=True)
    lang = st.selectbox("Language", ("English", "Русский", "Қазақша"), label_visibility="collapsed")
    S = DICT[lang]
    
    st.divider()
    # Часы
    astana = datetime.now(pytz.timezone('Asia/Almaty'))
    st.markdown(f"<div style='text-align:center; font-size:0.8rem; color:#64748b;'>{astana.strftime('%d.%m.%Y')}<br><b>{astana.strftime('%H:%M:%S')}</b></div>", unsafe_allow_html=True)
    
    st.divider()
    # Навигация (Радио-кнопка по центру)
    choice = st.radio("Menu", S["nav"], label_visibility="collapsed")
    st.session_state.page = choice

# ===== 5. PAGES =====

# --- HOME ---
if st.session_state.page == S["nav"][0]:
    st.markdown(f"<div class='hero-title'>{S['h_title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#94a3b8; margin-bottom:40px;'>{S['h_sub']}</p>", unsafe_allow_html=True)
    
    if os.path.exists("logo.png"):
        # Змея строго по центру
        col1, col2, col3 = st.columns([1,3,1])
        col2.image("logo.png", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    if col2.button(S["btn_start"]):
        nav_to(S["nav"][1])

# --- GENERATOR ---
elif st.session_state.page == S["nav"][1]:
    # Ручка строго по центру, средний размер
    col1, col2, col3 = st.columns([1,1,1])
    if os.path.exists("logo_pen.png"):
        col2.image("logo_pen.png", width=180)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("gen_form"):
        pA = st.text_input(S["f_pA"], placeholder="e.g. Kaspi Tech")
        pB = st.text_input(S["f_pB"], placeholder="e.g. Ivan Ivanov")
        summ = st.text_input(S["f_sum"], placeholder="500 000")
        
        submitted = st.form_submit_button(S["btn_gen"])

    if submitted:
        if pA and pB:
            # СЕКЦИЯ ПРЕДПРОСМОТРА
            st.markdown(f"### {S['preview_h']}")
            st.markdown(f"""
            <div class="doc-preview">
                <div class="doc-header">Договор № {astana.strftime('%Y/%m')}</div>
                <p>г. Астана &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "{astana.strftime('%d.%m.%Y')}"</p>
                <p><b>{pA}</b>, именуемое в дальнейшем "Заказчик", с одной стороны, и <b>{pB}</b>, именуемый в дальнейшем "Исполнитель", заключили настоящий договор о нижеследующем:</p>
                <p>1. Исполнитель обязуется оказать услуги по автоматизации систем, а Заказчик обязуется принять и оплатить услуги в размере <b>{summ} тенге</b>.</p>
                <p>2. Услуги считаются оказанными после подписания Акта выполненных работ.</p>
                <p><br>Юридические адреса сторон:<br>Заказчик: ___________ &nbsp;&nbsp; Исполнитель: ___________</p>
                <div class="doc-stamp">{S['stamp']}<br>ID: {int(time.time())}</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button("Скачать PDF", "DOC DATA", "contract.pdf")
        else:
            st.error("Fill mandatory fields")

# --- FEEDBACK & AUTHORS (Центрировано) ---
else:
    st.markdown(f"<h2 style='text-align:center;'>{st.session_state.page}</h2>", unsafe_allow_html=True)
    if st.session_state.page == S["nav"][3] and os.path.exists("authors.jpg"):
        st.image("authors.jpg", use_container_width=True)
    st.write("<div style='text-align:center;'>Development Team: Yeraly & Ramazan</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top:100px; text-align:center; opacity:0.3; font-size:0.7rem;'>SYSTEM ID: 0x4450 | ASTANA 2026</div>", unsafe_allow_html=True)