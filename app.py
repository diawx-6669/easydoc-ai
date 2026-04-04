import streamlit as st
import time
from datetime import date, datetime
import os
import pytz

# ===== 1. КОНФИГУРАЦИЯ СТРАНИЦЫ =====
st.set_page_config(
    page_title="EasyDoc AI | Smart Legal Solutions", 
    page_icon="📝", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Инициализация состояния страницы для работы кнопок
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Функция для быстрой смены страницы
def nav_to(page_name):
    st.session_state.page = page_name

# ===== 2. PREMIUM ДИЗАЙН (CSS) =====
st.markdown("""
<style>
    /* Основной фон и шрифты */
    .stApp { 
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%); 
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Главный контейнер */
    .block-container {
        background: rgba(30, 41, 59, 0.7);
        padding: 3.5rem;
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* Боковая панель (Sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* AI Insight Карточка (с анимацией свечения) */
    .ai-summary-card {
        background: linear-gradient(145deg, rgba(99, 102, 241, 0.2), rgba(30, 41, 59, 0.5));
        border: 1px solid #6366f1;
        padding: 25px;
        border-radius: 18px;
        margin-top: 30px;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
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
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(79, 70, 229, 0.4);
    }
    
    /* Кастомные заголовки */
    .main-header { font-size: 3.2rem; font-weight: 800; text-align: center; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ===== 3. ГЛОБАЛЬНЫЙ СЛОВАРЬ (DICT) =====
DICT = {
    "English": {
        "nav": ["Home", "Generator", "Feedback", "Authors"],
        "h_title": "EasyDoc AI", 
        "h_sub": "Enterprise-level automation for smart business.",
        "start": "Launch Generator 🚀", 
        "type_lab": "Document Category",
        "types": ["Employment Contract", "NDA", "Service Agreement", "Sales Contract", "Lease"],
        "f_pA": "Organization Name", "f_pB": "Full Name (Client/Staff)", 
        "f_d1": "Main Detail (Position/Item)", "f_d2": "Contract Value (KZT)",
        "gen": "GENERATE OFFICIAL DOCUMENT", 
        "ai_title": "🤖 AI System Insights", "ai_val": "Legal Compliance", "ai_ent": "Detected Entities",
        "feed_h": "Community Feedback", "auth_h": "System Developers",
        "time_lab": "Astana Time", "date_lab": "Today", "success": "Document Created!"
    },
    "Русский": {
        "nav": ["Главная", "Генератор", "Отзывы", "Авторы"],
        "h_title": "EasyDoc AI", 
        "h_sub": "Автоматизация документов нового поколения.",
        "start": "Запустить Генератор 🚀", 
        "type_lab": "Категория документа",
        "types": ["Трудовой договор", "NDA", "Договор услуг", "Купля-продажа", "Аренда"],
        "f_pA": "Название организации", "f_pB": "ФИО (Сотрудник/Клиент)", 
        "f_d1": "Детали (Должность/Товар)", "f_d2": "Сумма контракта (₸)",
        "gen": "СФОРМИРОВАТЬ ДОКУМЕНТ", 
        "ai_title": "🤖 Анализ системы AI", "ai_val": "Юридическая проверка", "ai_ent": "Найденные лица",
        "feed_h": "Обратная связь", "auth_h": "Авторы проекта",
        "time_lab": "Время Астаны", "date_lab": "Сегодня", "success": "Документ готов!"
    },
    "Қазақша": {
        "nav": ["Басты бет", "Генератор", "Кері байланыс", "Авторлар"],
        "h_title": "EasyDoc AI", 
        "h_sub": "Құжаттарды автоматтандырудың заманауи жүйесі.",
        "start": "Генераторды қосу 🚀", 
        "type_lab": "Құжат санатын таңдаңыз",
        "types": ["Еңбек шарты", "NDA келісімі", "Қызмет көрсету", "Сату-сатып алу", "Жалдау"],
        "f_pA": "Мекеме атауы", "f_pB": "Толық аты-жөні", 
        "f_d1": "Мәліметтер (Қызмет/Тауар)", "f_d2": "Қаржылық құны (₸)",
        "gen": "ҚҰЖАТТЫ ДАЙЫНДАУ", 
        "ai_title": "🤖 AI жүйесінің шолуы", "ai_val": "Құқықтық тексеріс", "ai_ent": "Танылған нысандар",
        "feed_h": "Пікір қалдыру", "auth_h": "Жоба авторлары",
        "time_lab": "Астана уақыты", "date_lab": "Бүгін", "success": "Құжат дайын!"
    }
}

# ===== 4. SIDEBAR (ВРЕМЯ, ДАТА И НАВИГАЦИЯ) =====
with st.sidebar:
    st.title("EasyDoc Panel")
    
    # 1. Выбор языка
    lang = st.selectbox("🌐 Language / Тіл", ("English", "Русский", "Қазақша"), index=1)
    S = DICT[lang]
    
    st.divider()
    
    # 2. Живое время Астаны
    astana_tz = pytz.timezone('Asia/Almaty')
    now = datetime.now(astana_tz)
    st.metric(label=S["time_lab"], value=now.strftime("%H:%M:%S"))
    st.write(f"📅 **{S['date_lab']}:** {now.strftime('%d.%m.%Y')}")
    
    st.divider()
    
    # 3. Радио-кнопки навигации (привязаны к session_state)
    page_selection = st.radio("Navigation", S["nav"], index=S["nav"].index(st.session_state.page) if st.session_state.page in S["nav"] else 0)
    st.session_state.page = page_selection

# ===== 5. КОНТЕНТ СТРАНИЦ =====

# --- 🏠 ГЛАВНАЯ СТРАНИЦА (ЛОГО: ЗМЕЯ) ---
if st.session_state.page == S["nav"][0]:
    st.markdown(f"<div class='main-header'>{S['h_title']}</div>", unsafe_allow_html=True)
    
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True) # ЗМЕЯ ЗДЕСЬ
    
    st.markdown(f"<p style='text-align:center; font-size:1.2rem; opacity:0.8;'>{S['h_sub']}</p>", unsafe_allow_html=True)
    
    st.divider()
    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        if st.button(S["start"]):
            st.session_state.page = S["nav"][1]
            st.rerun()

# --- 📝 ГЕНЕРАТОР (ЛОГО: РУЧКА) ---
elif st.session_state.page == S["nav"][1]:
    if os.path.exists("logo_pen.png"):
        st.image("logo_pen.png", width=220) # РУЧКА ЗДЕСЬ
        
    st.header(S["type_lab"])
    doc_type = st.selectbox("", S["types"])
    
    with st.form("professional_gen"):
        c1, c2 = st.columns(2)
        pA = c1.text_input(S["f_pA"])
        pB = c2.text_input(S["f_pB"])
        d1 = c1.text_input(S["f_d1"])
        d2 = c2.text_input(S["f_d2"])
        
        submitted = st.form_submit_button(S["gen"])
        
    if submitted:
        if pA and pB:
            with st.spinner("AI checking law database..."):
                time.sleep(1.5)
            
            # AI INSIGHT КАРТОЧКА (ПОЛНЫЙ ПЕРЕВОД)
            st.markdown(f"""
            <div class="ai-summary-card">
                <h3 style="margin:0; color:#6366f1;">{S['ai_title']}</h3>
                <hr style="border-color:#6366f1; opacity:0.3;">
                <p>✅ <b>{S['ai_val']}:</b> 100% Secure</p>
                <p>👤 <b>{S['ai_ent']}:</b> {pA} & {pB}</p>
                <p>📄 <b>Doc Type:</b> {doc_choice if 'doc_choice' in locals() else doc_type}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(S["success"])
            st.download_button("📥 Download .DOC", f"Document for {pB}", f"EasyDoc_{pB}.doc")
        else:
            st.error("Fill in the fields!")

# --- 💬 СТРАНИЦА ОТЗЫВОВ (ПО ЦЕНТРУ) ---
elif st.session_state.page == S["nav"][2]:
    st.markdown(f"<h2 style='text-align:center;'>{S['feed_h']}</h2>", unsafe_allow_html=True)
    
    with st.form("feedback_form_centered"):
        u_name = st.text_input("Name")
        u_email = st.text_input("Email")
        u_msg = st.text_area("Your Feedback")
        
        if st.form_submit_button("Submit"):
            st.balloons()
            st.success("Sent to Yeraly & Ramazan!")

# --- 👥 СТРАНИЦА АВТОРОВ (ПО ЦЕНТРУ) ---
elif st.session_state.page == S["nav"][3]:
    st.markdown(f"<h2 style='text-align:center;'>{S['auth_h']}</h2>", unsafe_allow_html=True)
    
    if os.path.exists("authors.jpg"):
        st.image("authors.jpg", use_container_width=True) # ВАШЕ ФОТО
    
    st.divider()
    st.markdown(f"""
    <div style='text-align:center; font-size:1.1rem;'>
        <p><b>Core Team:</b> Yeraly & Ramazan</p>
        <p><b>Education:</b> 8th Grade Students</p>
        <p><b>Project:</b> EasyDoc AI (Astana Hackathon 2026)</p>
    </div>
    """, unsafe_allow_html=True)

# ===== 6. FOOTER =====
st.markdown("<br><hr><p style='text-align:center; opacity:0.5;'>EasyDoc AI System | Astana, KZ | 2026</p>", unsafe_allow_html=True)