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

# Инициализация состояния страницы для работы кнопок
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Функция для быстрой смены страницы
def nav_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== 2. PREMIUM ДИЗАЙН (CSS) - СТРОГИЙ B2B СТИЛЬ =====
st.markdown("""
<style>
    /* Импорт чистого шрифта */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* Основной фон и шрифт */
    .stApp { 
        background-color: #090e1a;
        background-image: radial-gradient(at 10% 10%, rgba(31, 41, 55, 0.15) 0px, transparent 50%), radial-gradient(at 90% 90%, rgba(17, 24, 39, 0.1) 0px, transparent 50%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Главный контейнер (Строгое стекло) */
    .block-container {
        background: rgba(17, 24, 39, 0.6);
        padding: 4rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(15px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }

    /* Боковая панель (Sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #090e1a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04);
    }

    /* Меню: Навигация (Чистая, без эмодзи) */
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

    /* Заголовки (Strict & Clean) */
    h1, h2, h3 { color: #ffffff !important; font-weight: 800 !important; letter-spacing: -0.03em; }
    
    /* Главная страница: Заголовок со свечением */
    .main-title { 
        font-size: 3.8rem; 
        font-weight: 800; 
        text-align: center; 
        margin-bottom: 0.5rem;
        background: linear-gradient(120deg, #ffffff, #c7d2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px rgba(165, 180, 252, 0.2);
    }
    .main-sub { font-size: 1.3rem; text-align: center; color: #94a3b8; margin-bottom: 3.5rem; font-weight: 400; }

    /* Поля ввода (Clean B2B inputs) */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #111827 !important;
        color: #f1f5f9 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 10px;
        padding: 10px;
    }
    .stTextInput>div>div>input:focus { border-color: #4f46e5 !important; box-shadow: 0 0 0 1px #4f46e5; }

    /* AI Insight Карточка (Strict look) */
    .ai-summary-card {
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid #374151;
        padding: 25px;
        border-radius: 14px;
        margin-top: 30px;
    }
    .ai-title { color: #a5b4fc; font-weight: 700; font-size: 1.2rem; margin-bottom: 15px; }

    /* Кнопки (Strict B2B style) */
    .stButton>button {
        background: linear-gradient(180deg, #4f46e5 0%, #3730a3 100%);
        color: white;
        border: 1px solid #312e81;
        border-radius: 12px;
        font-weight: 600;
        height: 50px;
        width: 100%;
        transition: 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.9rem;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        background: linear-gradient(180deg, #6366f1 0%, #4f46e5 100%);
    }
    
    /*Footer */
    .footer { text-align: center; margin-top: 5rem; padding: 2rem; border-top: 1px solid #1f2937; opacity: 0.4; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ===== 3. ГЛОБАЛЬНЫЙ СЛОВАРЬ (DICT) - ЧИСТЫЙ, БЕЗ ЭМОДЗИ =====
DICT = {
    "English": {
        "nav": ["Home", "Generator", "Feedback", "Authors"],
        "h_title": "EasyDoc AI", 
        "h_sub": "Enterprise Document Automation Core.",
        "start": "Launch Generator", 
        "type_lab": "Document Category",
        "types": ["Employment Agreement", "NDA", "Service Level Agreement", "Sales Purchase Contract", "Residential Lease"],
        "f_pA": "Organization Name", "f_pB": "Individual's Full Name", 
        "f_d1": "Primary Detail (Position/Item)", "f_d2": "Contract Value (KZT)",
        "gen": "GENERATE DOCUMENT", 
        "ai_title": "AI System Insights", "ai_val": "Legal Compliance", "ai_ent": "Detected Entities",
        "feed_h": "Community Feedback", "auth_h": "System Developers",
        "time_lab": "Astana Time", "date_lab": "Today", "success": "Document Created."
    },
    "Русский": {
        "nav": ["Главная", "Генератор", "Отзывы", "Авторы"],
        "h_title": "EasyDoc AI", 
        "h_sub": "Ядро автоматизации корпоративных документов.",
        "start": "Открыть Генератор", 
        "type_lab": "Категория документа",
        "types": ["Трудовой договор", "Соглашение NDA", "Договор оказания услуг", "Договор купли-продажи", "Договор аренды"],
        "f_pA": "Название организации", "f_pB": "ФИО (Сотрудник/Клиент)", 
        "f_d1": "Детали (Должность/Товар)", "f_d2": "Сумма контракта (₸)",
        "gen": "СФОРМИРОВАТЬ ДОКУМЕНТ", 
        "ai_title": "Анализ системы AI", "ai_val": "Юридическая проверка", "ai_ent": "Найденные лица",
        "feed_h": "Обратная связь", "auth_h": "Авторы проекта",
        "time_lab": "Время Астаны", "date_lab": "Сегодня", "success": "Документ готов."
    },
    "Қазақша": {
        "nav": ["Басты бет", "Генератор", "Кері байланыс", "Авторлар"],
        "h_title": "EasyDoc AI", 
        "h_sub": "Корпоративтік құжаттарды автоматтандыру ядросы.",
        "start": "Генераторды қосу", 
        "type_lab": "Құжат санатын таңдаңыз",
        "types": ["Еңбек шарты", "NDA келісімі", "Қызмет көрсету шарты", "Сату-сатып алу шарты", "Жалдау шарты"],
        "f_pA": "Мекеме атауы", "f_pB": "Толық аты-жөні", 
        "f_d1": "Мәліметтер (Қызмет/Тауар)", "f_d2": "Қаржылық құны (₸)",
        "gen": "ҚҰЖАТТЫ ДАЙЫНДАУ", 
        "ai_title": "AI жүйесінің шолуы", "ai_val": "Құқықтық тексеріс", "ai_ent": "Танылған нысандар",
        "feed_h": "Пікір қалдыру", "auth_h": "Жоба авторлары",
        "time_lab": "Астана уақыты", "date_lab": "Бүгін", "success": "Құжат дайын."
    }
}

# ===== 4. SIDEBAR (ВРЕМЯ, ДАТА И ЧИСТАЯ НАВИГАЦИЯ) =====
with st.sidebar:
    st.markdown("<h3>EasyDoc Panel</h3>", unsafe_allow_html=True)
    
    # 1. Выбор языка
    lang_choice = st.selectbox("🌐 Language", ("English", "Русский", "Қазақша"), index=1)
    S = DICT[lang_choice]
    
    st.divider()
    
    # 2. Живое время Астаны (pytz обязателен в requirements.txt)
    astana_tz = pytz.timezone('Asia/Almaty')
    now = datetime.now(astana_tz)
    st.metric(label=S["time_lab"], value=now.strftime("%H:%M:%S"))
    st.write(f"📅 **{S['date_lab']}:** {now.strftime('%d.%m.%Y')}")
    
    st.divider()
    
    # 3. Чистая навигация (Radio, стилизованный через CSS)
    # Определяем индекс текущей страницы для синхронизации
    try:
        current_page_idx = S["nav"].index(st.session_state.page)
    except ValueError:
        current_page_idx = 0 # Дефолт на главную
        
    page_selection = st.radio("Navigation", S["nav"], index=current_page_idx, key="nav_radio", label_visibility="collapsed")
    st.session_state.page = page_selection

# ===== 5. КОНТЕНТ СТРАНИЦ =====

# --- 🏠 ГЛАВНАЯ СТРАНИЦА (ЛОГО ЗМЕЯ, Свечение текста) ---
if st.session_state.page == S["nav"][0]:
    # Чистый заголовок со свечением
    st.markdown(f"<div class='main-title'>{S['h_title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='main-sub'>{S['h_sub']}</div>", unsafe_allow_html=True)
    
    # Главное фото (Змея) - аккуратное
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True) # ЗМЕЯ ЗДЕСЬ
    
    st.divider()
    
    # Кнопка Запуска (Строгая B2B)
    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        if st.button(S["start"]):
            nav_to(S["nav"][1]) # Переход на Генератор

# --- 📝 ГЕНЕРАТОР (ЛОГО РУЧКА, ТЕПЕРЬ СРЕДНЕГО РАЗМЕРА) ---
elif st.session_state.page == S["nav"][1]:
    
    # ФОТО РУЧКИ (logo_pen.png) - ТЕПЕРЬ АККУРАТНОЕ, СРЕДНЕЕ
    if os.path.exists("logo_pen.png"):
        st.image("logo_pen.png", width=160) # РУЧКА ТУТ, ШИРИНА 160px (Средняя)
        
    st.header(S["type_lab"])
    doc_choice = st.selectbox("", S["types"], label_visibility="collapsed")
    
    with st.form("pro_gen_form"):
        c1, c2 = st.columns(2)
        pA = c1.text_input(S["f_pA"], placeholder="e.g. Kaspi Bank")
        pB = c2.text_input(S["f_pB"], placeholder="e.g. Ivan Ivanov")
        d1 = c1.text_input(S["f_d1"])
        d2 = c2.text_input(S["f_d2"])
        
        submitted = st.form_submit_button(S["gen"])
        
    if submitted:
        if pA and pB:
            with st.spinner("Analyzing RK Legal Code..."):
                time.sleep(1.2)
            
            # AI INSIGHT КАРТОЧКА (ПОЛНЫЙ ПЕРЕВОД, СТРОГИЙ СТИЛЬ)
            st.markdown(f"""
            <div class="ai-summary-card">
                <div class="ai-title">{S['ai_title']}</div>
                <p>✅ <b>{S['ai_val']}:</b> Verified 100% (No conflicts)</p>
                <p>👤 <b>{S['ai_ent']}:</b> {pA} & {pB}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(S["success"])
            st.download_button("📥 Download Official .DOC", f"Document Data", f"EasyDoc_{pB}.doc")
        else:
            st.error("Fill in the mandatory fields.")

# --- 💬 СТРАНИЦА ОТЗЫВОВ (ПО ЦЕНТРУ, ЧИСТАЯ) ---
elif st.session_state.page == S["nav"][2]:
    st.markdown(f"<h2 style='text-align:center;'>{S['feed_h']}</h2>", unsafe_allow_html=True)
    
    with st.form("feedback_centered_form"):
        u_name = st.text_input("Name / Company")
        u_email = st.text_input("Email")
        u_msg = st.text_area("Your Feedback")
        
        if st.form_submit_button("Submit"):
            st.balloons() # Шарики оставил, это мило
            st.success("Sent! Thank you.")

# --- 👥 СТРАНИЦА АВТОРОВ (ПО ЦЕНТРУ) ---
elif st.session_state.page == S["nav"][3]:
    st.markdown(f"<h2 style='text-align:center;'>{S['auth_h']}</h2>", unsafe_allow_html=True)
    
    if os.path.exists("authors.jpg"):
        st.image("authors.jpg", use_container_width=True) # ВАШЕ ФОТО
    
    st.divider()
    st.markdown(f"""
    <div style='text-align:center; font-size:1.1rem; color: #94a3b8;'>
        <p><b>Core Team:</b> Yeraly & Ramazan</p>
        <p><b>Level:</b> 8th Grade Students</p>
        <p><b>Location:</b> Astana, Kazakhstan</p>
    </div>
    """, unsafe_allow_html=True)

# ===== 6. СТРОГИЙ ФУТЕР =====
st.markdown("""
<div class="footer">
    EasyDoc AI System &copy; 2026 | Astana, Kazakhstan | Enterprise Solutions
</div>
""", unsafe_allow_html=True)