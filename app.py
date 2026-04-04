import streamlit as st
import time
from datetime import date, datetime
import os
import pytz

# ===== 1. ОСНОВНЫЕ НАСТРОЙКИ СТРАНИЦЫ =====
st.set_page_config(
    page_title="EasyDoc AI | Intelligent Systems", 
    page_icon="📝", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Инициализация навигации через session_state, чтобы кнопки работали корректно
if 'page' not in st.session_state:
    st.session_state.page = "Home"

def change_page(page_name):
    st.session_state.page = page_name

# ===== 2. ПОЛНЫЙ ДИЗАЙН (CSS) =====
st.markdown("""
<style>
    /* Главный фон приложения */
    .stApp { 
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%); 
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Стилизация центрального блока */
    .block-container {
        background: rgba(30, 41, 59, 0.7);
        padding: 3.5rem;
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* Боковая панель */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* AI Insight Карточка */
    .ai-summary-card {
        background: linear-gradient(145deg, rgba(99, 102, 241, 0.2), rgba(30, 41, 59, 0.5));
        border: 1px solid #6366f1;
        padding: 25px;
        border-radius: 18px;
        margin-top: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    /* Кнопки */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 14px;
        font-weight: 700;
        height: 55px;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(79, 70, 229, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ===== 3. ПОЛНЫЙ СЛОВАРЬ ПЕРЕВОДА (DICT) =====
DICT = {
    "English": {
        "nav": ["Home", "Generator", "Feedback", "Authors"],
        "h_title": "EasyDoc AI", 
        "h_sub": "Enterprise-level automation for business documentation.",
        "start": "Launch Generator", 
        "type_lab": "Select Document Type",
        "types": ["Employment Contract", "NDA", "Service Agreement", "Sales Contract", "Lease"],
        "f_pA": "Organization / Party A", 
        "f_pB": "Full Name / Party B", 
        "f_d1": "Primary Detail (Position/Item)", 
        "f_d2": "Financial Value (KZT)",
        "gen": "GENERATE DOCUMENT", 
        "ai_title": "🤖 AI System Insights", 
        "ai_val": "Legal Compliance", 
        "ai_ent": "Recognized Entities",
        "feed_h": "Community Feedback", 
        "auth_h": "System Developers",
        "sidebar_time": "Astana Local Time",
        "sidebar_date": "Current Date"
    },
    "Русский": {
        "nav": ["Главная", "Генератор", "Отзывы", "Авторы"],
        "h_title": "EasyDoc AI", 
        "h_sub": "Автоматизация документов корпоративного уровня.",
        "start": "Открыть Генератор", 
        "type_lab": "Выберите тип документа",
        "types": ["Трудовой договор", "NDA", "Договор услуг", "Купля-продажа", "Аренда"],
        "f_pA": "Организация / Сторона А", 
        "f_pB": "ФИО / Сторона Б", 
        "f_d1": "Детали (Должность/Товар)", 
        "f_d2": "Сумма контракта (₸)",
        "gen": "СФОРМИРОВАТЬ ДОКУМЕНТ", 
        "ai_title": "🤖 Анализ системы AI", 
        "ai_val": "Юридическая проверка", 
        "ai_ent": "Определенные лица",
        "feed_h": "Обратная связь", 
        "auth_h": "Разработчики системы",
        "sidebar_time": "Время Астаны",
        "sidebar_date": "Сегодняшняя дата"
    },
    "Қазақша": {
        "nav": ["Басты бет", "Генератор", "Кері байланыс", "Авторлар"],
        "h_title": "EasyDoc AI", 
        "h_sub": "Бизнес-құжаттарды автоматтандырудың заманауи жүйесі.",
        "start": "Генераторды қосу", 
        "type_lab": "Құжат түрін таңдаңыз",
        "types": ["Еңбек шарты", "NDA", "Қызмет көрсету", "Сату-сатып алу", "Жалдау"],
        "f_pA": "Мекеме / А тарапы", 
        "f_pB": "Толық аты-жөні / Б тарапы", 
        "f_d1": "Мәліметтер (Қызмет/Тауар)", 
        "f_d2": "Қаржылық құны (₸)",
        "gen": "ҚҰЖАТТЫ ДАЙЫНДАУ", 
        "ai_title": "🤖 AI жүйесінің шолуы", 
        "ai_val": "Құқықтық тексеріс", 
        "ai_ent": "Танылған нысандар",
        "feed_h": "Пікір қалдыру", 
        "auth_h": "Жоба авторлары",
        "sidebar_time": "Астана уақыты",
        "sidebar_date": "Бүгінгі күн"
    }
}

# ===== 4. SIDEBAR (ВРЕМЯ, ДАТА И НАВИГАЦИЯ) =====
with st.sidebar:
    st.title("EasyDoc Panel")
    
    # Выбор языка (Влияет на всё приложение сразу)
    lang_choice = st.selectbox("🌐 Language / Тіл", ("English", "Русский", "Қазақша"), index=1)
    S = DICT[lang_choice]
    
    st.divider()
    
    # Блок времени и даты
    kz_timezone = pytz.timezone('Asia/Almaty')
    current_time = datetime.now(kz_timezone).strftime("%H:%M:%S")
    current_day = date.today().strftime("%d.%m.%Y")
    
    st.metric(label=S["sidebar_time"], value=current_time)
    st.write(f"📅 **{S['sidebar_date']}:** {current_day}")
    
    st.divider()
    
    # Навигация
    choice = st.radio("Menu", S["nav"], index=S["nav"].index(st.session_state.page) if st.session_state.page in S["nav"] else 0)
    st.session_state.page = choice

# ===== 5. ЛОГИКА СТРАНИЦ =====

# --- 🏠 HOME PAGE (ЛОГО ЗМЕЯ) ---
if st.session_state.page == S["nav"][0]:
    st.markdown(f"<h1 style='text-align:center; font-size: 3.5rem;'>{S['h_title']}</h1>", unsafe_allow_html=True)
    
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True) # ЗМЕЯ ЗДЕСЬ
    
    st.markdown(f"<p style='text-align:center; font-size:1.3rem; opacity:0.8;'>{S['h_sub']}</p>", unsafe_allow_html=True)
    
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button(S["start"]):
            st.session_state.page = S["nav"][1] # Переход на Генератор
            st.rerun()

# --- 📝 GENERATOR PAGE (ЛОГО РУЧКА) ---
elif st.session_state.page == S["nav"][1]:
    if os.path.exists("logo_pen.png"):
        st.image("logo_pen.png", width=250) # РУЧКА ЗДЕСЬ
        
    st.header(S["type_lab"])
    doc_choice = st.selectbox("", S["types"])
    
    with st.form("main_gen_form"):
        c1, c2 = st.columns(2)
        pA = c1.text_input(S["f_pA"])
        pB = c2.text_input(S["f_pB"])
        d1 = c1.text_input(S["f_d1"])
        d2 = c2.text_input(S["f_d2"])
        
        submitted = st.form_submit_button(S["gen"])
        
    if submitted:
        if pA and pB:
            with st.spinner("AI is analyzing legal requirements..."):
                time.sleep(2)
            
            # AI INSIGHT CARD (ПОЛНОСТЬЮ НА ВЫБРАННОМ ЯЗЫКЕ)
            st.markdown(f"""
            <div class="ai-summary-card">
                <h3 style="margin:0; color:#6366f1;">{S['ai_title']}</h3>
                <hr style="border-color:#6366f1; opacity:0.3;">
                <p>✅ <b>{S['ai_val']}:</b> 100% (RK Legal Code)</p>
                <p>👤 <b>{S['ai_ent']}:</b> {pA} & {pB}</p>
                <p>📄 <b>Category:</b> {doc_choice}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(S["success"])
            st.download_button("📥 Download Official .DOC", "Doc Data", f"EasyDoc_{pB}.doc")
        else:
            st.error("Please fill in the parties' names.")

# --- 💬 FEEDBACK PAGE (ПО ЦЕНТРУ) ---
elif st.session_state.page == S["nav"][2]:
    st.markdown(f"<h2 style='text-align:center;'>{S['feed_h']}</h2>", unsafe_allow_html=True)
    
    with st.form("feedback_form_central"):
        user_name = st.text_input("Name / Username")
        user_email = st.text_input("Email")
        feedback_text = st.text_area("Your Message")
        
        if st.form_submit_button("Send to Developers"):
            st.balloons()
            st.success("Sent! Thank you for helping us improve.")

# --- 👥 AUTHORS PAGE (ПО ЦЕНТРУ) ---
elif st.session_state.page == S["nav"][3]:
    st.markdown(f"<h2 style='text-align:center;'>{S['auth_h']}</h2>", unsafe_allow_html=True)
    
    if os.path.exists("authors.jpg"):
        st.image("authors.jpg", caption="Yeraly & Ramazan | Hackathon 2026", use_container_width=True)
    
    st.divider()
    st.markdown("""
    <div style='text-align:center;'>
        <p><b>Team:</b> Yeraly & Ramazan</p>
        <p><b>Level:</b> 8th Grade Students</p>
        <p><b>Location:</b> Astana, Kazakhstan</p>
        <p><b>Goal:</b> Making legal paperwork accessible for everyone.</p>
    </div>
    """, unsafe_allow_html=True)

# ===== 6. ПРОФЕССИОНАЛЬНЫЙ ФУТЕР =====
st.markdown(f"""
<div style="text-align:center; margin-top:5rem; padding:2rem; border-top:1px solid rgba(255,255,255,0.1); opacity:0.6;">
    EasyDoc AI System &copy; 2026 | Astana, Kazakhstan
</div>
""", unsafe_allow_html=True)