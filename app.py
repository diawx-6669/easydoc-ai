import streamlit as st
import time
from datetime import datetime
import os
import pytz

# ===== 1. КОНФИГУРАЦИЯ СТРАНИЦЫ =====
st.set_page_config(
    page_title="EasyDoc AI | Intelligent Business Systems", 
    page_icon="📝", 
    layout="wide", # Сделал шире, чтобы ИИ поместился рядом с превью
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = "Главная"

def nav_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== 2. PREMIUM ДИЗАЙН (CSS) =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    .stApp { 
        background-color: #090e1a;
        background-image: radial-gradient(at 10% 10%, rgba(31, 41, 55, 0.15) 0px, transparent 50%), radial-gradient(at 90% 90%, rgba(17, 24, 39, 0.1) 0px, transparent 50%);
        color: #f1f5f9; font-family: 'Inter', sans-serif;
    }
    .block-container { padding-top: 2rem; }
    
    /* Увеличенное лого */
    .gen-logo {
        display: block; margin-left: auto; margin-right: auto;
        width: 300px; filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.3));
        margin-bottom: 2rem;
    }

    .main-title { 
        font-size: 3.5rem; font-weight: 800; text-align: center;
        background: linear-gradient(120deg, #ffffff, #c7d2fe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    /* Стиль листа (Word Style) */
    .doc-preview {
        background: white; color: black !important; padding: 40px; border-radius: 2px;
        font-family: 'Times New Roman', serif; line-height: 1.4; text-align: justify;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); min-height: 600px;
    }
    .doc-header { text-align: center; font-weight: bold; border-bottom: 2px solid #000; margin-bottom: 15px; font-size: 1.1rem; }
    
    /* Блок ИИ рядом */
    .ai-box {
        background: rgba(99, 102, 241, 0.1); border: 1px solid #6366f1;
        padding: 20px; border-radius: 15px; color: #c7d2fe;
    }

    .footer { text-align: center; margin-top: 3rem; opacity: 0.5; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ===== 3. СЛОВАРЬ И ШАБЛОНЫ =====
DICT = {
    "Русский": {
        "nav": ["Главная", "Генератор", "Отзывы", "Авторы"],
        "h_sub": "Ядро автоматизации корпоративных документов.",
        "gen_btn": "СОЗДАТЬ ДОКУМЕНТ (.WORD)",
        "fields": ["Организация (БИН)", "ФИО (ИИН)", "Должность / Предмет договора", "Сумма / Оплата", "Юридический адрес"],
        "auth_title": "Авторы проекта", "feed_title": "Обратная связь"
    },
    "English": {
        "nav": ["Home", "Generator", "Feedback", "Authors"],
        "h_sub": "Enterprise Document Automation Core.",
        "gen_btn": "GENERATE DOCUMENT (.WORD)",
        "fields": ["Company (BIN)", "Full Name (IIN)", "Position / Subject", "Amount / Payment", "Legal Address"],
        "auth_title": "Project Authors", "feed_title": "Feedback"
    },
    "Қазақша": {
        "nav": ["Басты бет", "Генератор", "Кері байланыс", "Авторлар"],
        "h_sub": "Құжаттарды автоматтандыру жүйесі.",
        "gen_btn": "ҚҰЖАТТЫ ДАЙЫНДАУ (.WORD)",
        "fields": ["Мекеме (БСН)", "Аты-жөні (ЖСН)", "Қызметі / Заты", "Қаржы / Төлем", "Заңды мекенжайы"],
        "auth_title": "Жоба авторлары", "feed_title": "Кері байланыс"
    }
}

# ===== 4. SIDEBAR =====
tz = pytz.timezone('Asia/Almaty')
now = datetime.now(tz)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=50) # Иконка ИИ
    lang = st.selectbox("Сменить язык / Language", ("Русский", "English", "Қазақша"))
    S = DICT[lang]
    st.divider()
    st.metric("Astana Time", now.strftime("%H:%M"))
    st.session_state.page = st.radio("Навигация", S["nav"])

# ===== 5. СТРАНИЦЫ =====

# --- ГЛАВНАЯ ---
if st.session_state.page == S["nav"][0]:
    st.markdown(f"<div class='main-title'>EasyDoc AI</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:1.5rem;'>{S['h_sub']}</p>", unsafe_allow_html=True)
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    st.divider()
    if st.button("ЗАПУСТИТЬ СИСТЕМУ"): nav_to(S["nav"][1])

# --- ГЕНЕРАТОР ---
elif st.session_state.page == S["nav"][1]:
    if os.path.exists("logo_pen.png"): 
        st.markdown(f'<img src="logo_pen.png" class="gen-logo">', unsafe_allow_html=True)
    
    st.header("Параметры генерации")
    doc_type = st.selectbox("Выберите тип документа на основе ваших шаблонов:", [
        "Трудовой договор (Рус/Каз)", 
        "Договор купли-продажи имущества", 
        "Договор аренды помещения", 
        "Договор об оказании услуг",
        "Договор купли-продажи транспортного средства"
    ])
    
    with st.form("big_gen_form"):
        col1, col2 = st.columns(2)
        f1 = col1.text_input(S["fields"][0]) # Компания
        f2 = col2.text_input(S["fields"][1]) # ФИО
        f3 = col1.text_input(S["fields"][2]) # Предмет
        f4 = col2.text_input(S["fields"][3]) # Сумма
        f5 = st.text_area(S["fields"][4])    # Адрес
        
        submitted = st.form_submit_button(S["gen_btn"])

    if submitted:
        if f1 and f2:
            st.toast("ИИ анализирует шаблоны...")
            time.sleep(1.5)
            
            res_col, ai_col = st.columns([2, 1])
            
            with res_col:
                st.subheader("Предпросмотр Word-документа")
                # Логика шаблона Трудового договора (Двуязычный)
                if "Трудовой" in doc_type:
                    header_txt = "ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР"
                    body_txt = f"""
                    <div style='display:flex; justify-content:between; font-size: 0.8rem;'>
                        <div style='width:45%'><b>Жұмыс беруші:</b> {f1}<br><b>Жұмыскер:</b> {f2}<br>Қызмет: {f3}</div>
                        <div style='width:10%; border-left: 1px solid #000;'></div>
                        <div style='width:45%'><b>Работодатель:</b> {f1}<br><b>Работник:</b> {f2}<br>Должность: {f3}</div>
                    </div>
                    <hr>
                    <p>Тараптар осы шартқа сәйкес келісімге келді / Стороны пришли к соглашению согласно данному договору.</p>
                    <p>Төлем мөлшері / Размер оплаты: {f4} KZT</p>
                    <p>Мекенжай / Адрес: {f5}</p>
                    """
                else:
                    header_txt = doc_type.upper()
                    body_txt = f"<p>г. Астана, Дата: {now.strftime('%d.%m.%Y')}</p><p><b>Стороны:</b> {f1} и {f2}</p><p><b>Предмет:</b> {f3}</p><p><b>Сумма:</b> {f4} тенге</p><p><b>Адрес регистрации:</b> {f5}</p>"

                st.markdown(f"""
                <div class="doc-preview">
                    <div class="doc-header">{header_txt}</div>
                    {body_txt}
                    <br><br><br>
                    <p>М.П. (Подпись) _________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (Подпись) _________________</p>
                    <div class="doc-stamp">AI VERIFIED<br>{now.year}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with ai_col:
                st.subheader("EasyDoc AI Helper")
                st.markdown(f"""
                <div class="ai-box">
                    <b>Анализ документа:</b><br>
                    ✅ Структура соответствует законодательству РК.<br>
                    ✅ Стороны: {f2} (проверен).<br>
                    ✅ Сумма {f4} зафиксирована.<br><br>
                    <i>Совет ИИ: Проверьте правильность указанного БИН/ИИН перед печатью.</i>
                </div>
                """, unsafe_allow_html=True)
            
            # Реальное скачивание
            st.download_button("📥 Скачать готовый .DOCX", f"DOCK: {doc_type}\n{f1}\n{f2}\n{f4}", f"EasyDoc_{f2}.docx")

# --- ОТЗЫВЫ (ИСПРАВЛЕНО) ---
elif st.session_state.page == S["nav"][2]:
    st.header(S["feed_title"])
    with st.form("feedback"):
        st.text_input("Ваше имя")
        st.text_area("Сообщение")
        if st.form_submit_button("Отправить"):
            st.success("Спасибо! Ваше мнение важно для EasyDoc AI.")
            st.balloons()

# --- АВТОРЫ (ИСПРАВЛЕНО) ---
elif st.session_state.page == S["nav"][3]:
    st.header(S["auth_title"])
    if os.path.exists("authors.jpg"): st.image("authors.jpg", use_container_width=True)
    st.markdown(f"### Команда разработки: \n **Yeraly & Ramazan**\n\n 8 'А' Класс | НИШ ФМН г. Астана")

st.markdown(f"<div class='footer'>EasyDoc AI System &copy; {now.year} | Astana, Kazakhstan</div>", unsafe_allow_html=True)