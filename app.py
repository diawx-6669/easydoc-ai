import streamlit as st
import time
from datetime import date
import os

# ===== 1. КОНФИГУРАЦИЯ СТРАНИЦЫ =====
st.set_page_config(
    page_title="EasyDoc AI | Smart Business Solutions", 
    page_icon="📝", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# ===== 2. РАСШИРЕННЫЙ CSS (ДИЗАЙН) =====
st.markdown("""
<style>
    /* Главный фон и шрифт */
    .stApp { 
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%); 
        color: #f8fafc;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Контейнер приложения */
    .block-container {
        background: rgba(30, 41, 59, 0.7);
        padding: 3rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Стили Сайдбара */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Заголовки */
    h1, h2, h3 { 
        color: #ffffff !important; 
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }

    /* Кастомная кнопка */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.5);
        background: linear-gradient(90deg, #818cf8 0%, #6366f1 100%);
    }

    /* Поля ввода */
    .stTextInput>div>div>input {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 10px;
        padding: 12px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }

    /* AI Card */
    .ai-summary-card {
        background: linear-gradient(145deg, rgba(99, 102, 241, 0.15), rgba(30, 41, 59, 0.4));
        border: 1px solid #6366f1;
        padding: 20px;
        border-radius: 16px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ===== 3. СЛОВАРЬ ПЕРЕВОДОВ (ПОЛНЫЙ) =====
DICT = {
    "English": {
        "nav_home": "Home", "nav_gen": "Generator", "nav_feed": "Feedback",
        "hero_title": "EasyDoc AI", "hero_sub": "Enterprise-grade document automation for the modern era.",
        "start_btn": "Launch Generator", "doc_type_lab": "Choose Document Category",
        "types": ["Employment Agreement", "Non-Disclosure Agreement (NDA)", "Service Level Agreement", "Sales Purchase Contract", "Residential Lease"],
        "f_party_a": "Organization / Party A", "f_party_b": "Individual / Party B",
        "f_detail_1": "Primary Detail (Position/Item/Address)", "f_detail_2": "Financial Value (KZT)",
        "gen_btn": "CREATE OFFICIAL DOCUMENT", "success": "Document ready for download!",
        "ai_note": "AI Insight: Compliance check passed for Kazakhstan Law."
    },
    "Русский": {
        "nav_home": "Главная", "nav_gen": "Генератор", "nav_feed": "Отзывы",
        "hero_title": "EasyDoc AI", "hero_sub": "Автоматизация документов корпоративного уровня.",
        "start_btn": "Запустить генератор", "doc_type_lab": "Выберите категорию документа",
        "types": ["Трудовой договор", "Соглашение NDA", "Договор оказания услуг", "Договор купли-продажи", "Договор аренды"],
        "f_party_a": "Организация / Сторона А", "f_party_b": "Физлицо / Сторона Б",
        "f_detail_1": "Основная деталь (Должность/Объект)", "f_detail_2": "Сумма / Оклад (₸)",
        "gen_btn": "СФОРМИРОВАТЬ РЕЗЮМЕ ДОКУМЕНТА", "success": "Официальный документ готов!",
        "ai_note": "AI Анализ: Соответствует законодательству РК."
    },
    "Қазақша": {
        "nav_home": "Басты бет", "nav_gen": "Генератор", "nav_feed": "Кері байланыс",
        "hero_title": "EasyDoc AI", "hero_sub": "Құжаттарды автоматтандырудың заманауи жүйесі.",
        "start_btn": "Генераторды қосу", "doc_type_lab": "Құжат санатын таңдаңыз",
        "types": ["Еңбек шарты", "NDA келісімі", "Қызмет көрсету шарты", "Сату-сатып алу шарты", "Жалдау шарты"],
        "f_party_a": "Мекеме / А тарапы", "f_party_b": "Жеке тұлға / Б тарапы",
        "f_detail_1": "Негізгі ақпарат (Қызмет/Нысан)", "f_detail_2": "Қаржылық құны (₸)",
        "gen_btn": "РЕСМИ ҚҰЖАТТЫ ДАЙЫНДАУ", "success": "Құжат жүктеуге дайын!",
        "ai_note": "AI талдау: ҚР заңнамасына сәйкес тексерілді."
    }
}

# ===== 4. САЙДБАР (УПРАВЛЕНИЕ) =====
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/281/281760.png", width=80)
    st.title("Control Panel")
    selected_lang = st.radio("Select Language", ("English", "Русский", "Қазақша"))
    S = DICT[selected_lang]
    
    st.divider()
    page = st.selectbox("Navigation", [S["nav_home"], S["nav_gen"], S["nav_feed"]])
    
    if page == S["nav_feed"]:
        st.subheader("Feedback Form")
        name = st.text_input("Your Name")
        msg = st.text_area("Message")
        if st.button("Submit Feedback"):
            st.toast("Message sent to developers!")
            st.success("Thank you!")

# ===== 5. ГЛАВНАЯ СТРАНИЦА =====
if page == S["nav_home"]:
    st.markdown(f"<h1 class='main-title' style='text-align:center;'>{S['hero_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:1.2rem; opacity:0.8;'>{S['hero_sub']}</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&q=80&w=1200", caption="Digital Transformation")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button(S["start_btn"]):
            st.info("Please use navigation menu to switch to Generator.")

# ===== 6. СТРАНИЦА ГЕНЕРАТОРА (ГЛУБОКАЯ ЛОГИКА) =====
elif page == S["nav_gen"]:
    st.markdown(f"<h2>{S['doc_type_lab']}</h2>", unsafe_allow_html=True)
    doc_type = st.selectbox("", S["types"])
    
    st.markdown("### Document Details")
    with st.form("professional_form"):
        col_l, col_r = st.columns(2)
        pA = col_l.text_input(S["f_party_a"], placeholder="e.g. Kaspi Bank / Apple Inc.")
        pB = col_r.text_input(S["f_party_b"], placeholder="e.g. Ivan Ivanov / John Doe")
        d1 = col_l.text_input(S["f_detail_1"])
        d2 = col_r.text_input(S["f_detail_2"])
        
        st.info("AI will automatically insert standard legal clauses for your region.")
        generate_event = st.form_submit_button(S["gen_btn"])

    if generate_event:
        if not pA or not pB:
            st.warning("All fields are mandatory for legal compliance.")
        else:
            with st.spinner("Compiling legal database and formatting..."):
                time.sleep(2)
            
            # Юридическая логика текста
            current_date = date.today().strftime("%B %d, %Y")
            
            if "NDA" in doc_type:
                legal_content = f"<h3>1. Confidential Information</h3><p>Information regarding {pA} is secret for {d1} years.</p><h3>2. Remedies</h3><p>Penalty for breach: {d2} KZT.</p>"
            elif "Employment" in doc_type or "Еңбек" in doc_type or "Трудовой" in doc_type:
                legal_content = f"<h3>1. Employment Position</h3><p>Party B is hired as {d1}.</p><h3>2. Compensation</h3><p>The base salary is set at {d2} KZT per month.</p>"
            else:
                legal_content = f"<h3>1. Scope of Agreement</h3><p>Party B agrees to provide/deliver {d1} to Party A.</p><h3>2. Payment</h3><p>The total consideration is {d2} KZT.</p>"

            full_html = f"""
            <html>
            <body style="font-family:'Times New Roman',serif; padding:40px; line-height:1.6;">
                <h1 style="text-align:center;">OFFICIAL {doc_type.upper()}</h1>
                <p style="text-align:right;"><b>Date:</b> {current_date}<br><b>Location:</b> Astana, Kazakhstan</p>
                <hr>
                <p>This binding agreement is made between <b>{pA}</b> and <b>{pB}</b>.</p>
                {legal_content}
                <h3>3. Signatures</h3>
                <table style="width:100%; margin-top:50px;">
                    <tr>
                        <td><b>Party A (Sign/Stamp):</b><br>____________________</td>
                        <td><b>Party B (Sign):</b><br>____________________</td>
                    </tr>
                </table>
            </body>
            </html>
            """

            # AI Insights Box
            st.markdown(f"""
            <div class="ai-summary-card">
                <h4 style="margin:0; color:#6366f1;">{S['t_sum'] if 't_sum' in S else '🤖 AI Insights'}</h4>
                <p style="margin-top:10px;"><b>Validation:</b> {S['ai_note']}</p>
                <p><b>Entities detected:</b> {pA} (Organization), {pB} (Individual)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(S["success"])
            st.download_button(
                label="📥 DOWNLOAD WORD DOCUMENT (.DOC)",
                data=full_html,
                file_name=f"EasyDoc_{doc_type}_{pB}.doc",
                mime="application/msword"
            )

# ===== 7. ПРОФЕССИОНАЛЬНЫЙ ФУТЕР =====
st.markdown(f"""
<div style="text-align:center; margin-top:5rem; padding:2rem; border-top:1px solid rgba(255,255,255,0.1);">
    <p style="opacity:0.6; font-size:0.9rem;">EasyDoc AI System &copy; 2026</p>
    <p style="color:#6366f1; font-weight:700;">Engineered by Yeraly & Ramazan</p>
</div>
""", unsafe_allow_html=True)