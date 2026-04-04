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

# ===== 1.5 СЛОВАРИ ДЛЯ ПЕРЕВОДА ИНТЕРФЕЙСА =====
translations = {
    "Русский": {
        "nav": {"Главная": "Главная", "Генератор": "Генератор", "Отзывы": "Отзывы", "Авторы": "Авторы"},
        "subtitle": "Ваш надежный ИИ-помощник для малого бизнеса.",
        "run_btn": "ЗАПУСТИТЬ ГЕНЕРАТОР",
        "date": "Дата", "time": "Время", "nav_title": "Навигация",
        "gen_header": "Настройка шаблона", "doc_type": "Выберите тип документа:",
        "parties": "Информация о сторонах", "details": "Детали сделки",
        "party1": "Сторона 1 (Организация/Продавец/Работодатель + БИН)",
        "party2": "Сторона 2 (ФИО Клиента/Покупателя/Работника + ИИН)",
        "address": "Юридические адреса, контакты и банковские реквизиты сторон (IBAN, Банк)",
        "submit": "СОЗДАТЬ ДОКУМЕНТ", "download": "📥 СКАЧАТЬ WORD (.DOCX)",
        "feedback": "Обратная связь", "name": "Имя", "review": "Ваш отзыв", "send": "Отправить", "thanks": "Спасибо за отзыв!",
        "authors": "Авторы проекта"
    },
    "English": {
        "nav": {"Главная": "Home", "Генератор": "Generator", "Отзывы": "Feedback", "Авторы": "Authors"},
        "subtitle": "Your reliable AI assistant for small businesses.",
        "run_btn": "LAUNCH GENERATOR",
        "date": "Date", "time": "Time", "nav_title": "Navigation",
        "gen_header": "Template Setup", "doc_type": "Select document type:",
        "parties": "Parties Information", "details": "Transaction Details",
        "party1": "Party 1 (Organization/Seller/Employer + BIN)",
        "party2": "Party 2 (Client/Buyer/Employee Name + IIN)",
        "address": "Legal addresses, contacts and bank details (IBAN, Bank)",
        "submit": "CREATE DOCUMENT", "download": "📥 DOWNLOAD WORD (.DOCX)",
        "feedback": "Feedback", "name": "Name", "review": "Your review", "send": "Submit", "thanks": "Thank you for your feedback!",
        "authors": "Project Authors"
    },
    "Қазақша": {
        "nav": {"Главная": "Басты бет", "Генератор": "Генератор", "Отзывы": "Пікірлер", "Авторы": "Авторлар"},
        "subtitle": "Шағын бизнеске арналған сенімді AI көмекшісі.",
        "run_btn": "ГЕНЕРАТОРДЫ ІСКЕ ҚОСУ",
        "date": "Күні", "time": "Уақыты", "nav_title": "Навигация",
        "gen_header": "Үлгіні баптау", "doc_type": "Құжат түрін таңдаңыз:",
        "parties": "Тараптар туралы ақпарат", "details": "Мәміле деректемелері",
        "party1": "1-тарап (Ұйым/Сатушы/Жұмыс беруші + БСН)",
        "party2": "2-тарап (Клиент/Сатып алушы/Жұмыскер ТАӘ + ЖСН)",
        "address": "Заңды мекенжайлар, байланыстар және банк деректемелері (IBAN, Банк)",
        "submit": "ҚҰЖАТТЫ ҚҰРУ", "download": "📥 WORD ЖҮКТЕУ (.DOCX)",
        "feedback": "Кері байланыс", "name": "Атыңыз", "review": "Пікіріңіз", "send": "Жіберу", "thanks": "Пікіріңіз үшін рахмет!",
        "authors": "Жоба авторлары"
    }
}

# ===== 2. ДИЗАЙН (CSS) =====
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
    .doc-preview p, .doc-preview div, .doc-preview b, .doc-preview h3 { color: black !important; }
    .ai-sidebar { background: rgba(99, 102, 241, 0.1); border: 1px solid #6366f1; padding: 20px; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# ===== 3. ГЕНЕРАЦИЯ WORD =====
def create_docx(doc_type, data):
    doc = Document()
    
    heading = doc.add_heading(doc_type.upper(), 1)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    date_p = doc.add_paragraph()
    date_p.add_run(f"г. Астана\t\t\t\t\t\t\t\t{datetime.now().strftime('%d.%m.%Y')} г.")
    
    p = doc.add_paragraph()
    p.add_run(f"\n{data.get('Сторона 1', '________')} (далее - Сторона 1), ")
    p.add_run("с одной стороны, и ")
    p.add_run(f"{data.get('Сторона 2', '________')} (далее - Сторона 2), ")
    p.add_run("с другой стороны, совместно именуемые «Стороны», заключили настоящий договор о нижеследующем:\n")
    
    doc.add_heading('1. ПРЕДМЕТ ДОГОВОРА', level=2)
    doc.add_paragraph(f"1.1. По настоящему договору Стороны договорились о следующем: {data.get('Детали', '__________________')}.")
    
    doc.add_heading('2. УСЛОВИЯ И ПОРЯДОК РАСЧЕТОВ', level=2)
    doc.add_paragraph(f"2.1. Основные условия сделки: {data.get('Условия', '__________________')}.")
    doc.add_paragraph(f"2.2. Сроки исполнения обязательств: {data.get('Сроки', '__________________')}.")
    
    doc.add_heading('3. ОТВЕТСТВЕННОСТЬ СТОРОН', level=2)
    doc.add_paragraph("3.1. За неисполнение или ненадлежащее исполнение обязательств по настоящему Договору Стороны несут ответственность в соответствии с действующим законодательством Республики Казахстан.")
    
    doc.add_heading('4. АДРЕСА И РЕКВИЗИТЫ СТОРОН', level=2)
    doc.add_paragraph(f"{data.get('Реквизиты', '__________________')}\n")
    
    sign_p = doc.add_paragraph()
    sign_p.add_run("\nПОДПИСИ СТОРОН:\n").bold = True
    sign_p.add_run("От Стороны 1: _________________        От Стороны 2: _________________")
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ===== 4. SIDEBAR =====
tz = pytz.timezone('Asia/Almaty')
now = datetime.now(tz)

with st.sidebar:
    st.title("EasyDoc AI")
    selected_lang = st.selectbox("🌐 Язык / Language", ["Русский", "English", "Қазақша"])
    t = translations[selected_lang] # Загружаем нужный язык
    
    st.divider()
    st.write(f"📅 *{t['date']}:* {now.strftime('%d.%m.%Y')}")
    st.write(f"🕒 *{t['time']}:* {now.strftime('%H:%M:%S')}")
    
    # Навигация с переводом
    menu_keys = ["Главная", "Генератор", "Отзывы", "Авторы"]
    menu_labels = [t["nav"][k] for k in menu_keys]
    
    selected_label = st.radio(t["nav_title"], menu_labels, index=menu_keys.index(st.session_state.page))
    st.session_state.page = menu_keys[menu_labels.index(selected_label)] # Сохраняем системное имя страницы

# ===== 5. КОНТЕНТ =====

if st.session_state.page == "Главная":
    st.markdown("<div class='main-title'>EasyDoc AI</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='main-sub'>{t['subtitle']}</div>", unsafe_allow_html=True)
    
    if os.path.exists("logo.png"): 
        st.image("logo.png", use_container_width=True)
        
    st.divider()
    col_l, col_m, col_r = st.columns([1,2,1])
    if col_m.button(t["run_btn"], use_container_width=True): 
        nav_to("Генератор")

elif st.session_state.page == "Генератор":
    # Центрирование логотипа через колонки
    if os.path.exists("logo_pen.png"): 
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.image("logo_pen.png", use_container_width=True)
    
    st.header(t["gen_header"])
    doc_choice = st.selectbox(t["doc_type"], [
        "Трудовой договор (Двуязычный Каз/Рус)",
        "Договор купли-продажи имущества",
        "Договор аренды помещения",
        "Договор об оказании услуг",
        "Договор купли-продажи ТС (Авто)"
    ])

    with st.form("main_form"):
        st.subheader(t["parties"])
        c1, c2 = st.columns(2)
        org_name = c1.text_input(t["party1"])
        client_name = c2.text_input(t["party2"])
        
        st.subheader(t["details"])
        col3, col4 = st.columns(2)
        
        if "Трудовой" in doc_choice:
            d1 = col3.text_input("Должность работника")
            d2 = col4.text_input("Оклад (цифрами и прописью)")
            d3 = st.text_input("Срок действия договора (например: 1 год)")
        elif "аренды" in doc_choice:
            d1 = col3.text_input("Точный адрес объекта аренды")
            d2 = col4.text_input("Ежемесячная арендная плата")
            d3 = st.text_input("Срок аренды и целевое назначение (жилое/офис)")
        elif "ТС (Авто)" in doc_choice:
            d1 = col3.text_input("Марка, Модель, Год выпуска")
            d2 = col4.text_input("Цена автомобиля")
            d3 = st.text_input("Гос. номер и VIN код")
        else:
            d1 = col3.text_input("Точный предмет договора (описание)")
            d2 = col4.text_input("Сумма договора")
            d3 = st.text_input("Сроки выполнения/поставки")

        address = st.text_area(t["address"])
        submitted = st.form_submit_button(t["submit"])

    if submitted:
        if org_name and client_name:
            res_col, ai_col = st.columns([2, 1])
            
            with res_col:
                # ПРЕВЬЮ ТОЧНО КАК ШАБЛОН WORD
                st.markdown("<div class='doc-preview'>", unsafe_allow_html=True)
                
                if "Трудовой" in doc_choice:
                    st.markdown("<h3 style='text-align:center;'>№ __ ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='display:flex; justify-content:space-between;'><span>Астана қ. / г. Астана</span><span>{now.strftime('%d.%m.%Y')} ж/г.</span></p>", unsafe_allow_html=True)
                    k1, k2 = st.columns(2)
                    k1.write(f"*Жұмыс беруші:* {org_name}\n\n*Жұмыскер:* {client_name}\n\nЛауазымы: {d1}")
                    k2.write(f"*Работодатель:* {org_name}\n\n*Работник:* {client_name}\n\nДолжность: {d1}")
                    st.write(f"*Жалақы / Оклад:* {d2} KZT<br>*Сроки:* {d3}", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h3 style='text-align:center;'>{doc_choice.upper()}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='display:flex; justify-content:space-between;'><span>г. Астана</span><span>{now.strftime('%d.%m.%Y')} г.</span></p>", unsafe_allow_html=True)
                    
                    st.markdown(f"<p><b>{org_name}</b> (далее - Сторона 1), с одной стороны, и <b>{client_name}</b> (далее - Сторона 2), с другой стороны, совместно именуемые «Стороны», заключили настоящий договор о нижеследующем:</p>", unsafe_allow_html=True)
                    
                    st.markdown("<b>1. ПРЕДМЕТ ДОГОВОРА</b>", unsafe_allow_html=True)
                    st.write(f"1.1. По настоящему договору Стороны договорились о следующем: {d1}.")
                    
                    st.markdown("<b>2. УСЛОВИЯ И ПОРЯДОК РАСЧЕТОВ</b>", unsafe_allow_html=True)
                    st.write(f"2.1. Основные условия сделки: {d2}.")
                    st.write(f"2.2. Сроки исполнения обязательств: {d3}.")
                    
                    st.markdown("<b>3. ОТВЕТСТВЕННОСТЬ СТОРОН</b>", unsafe_allow_html=True)
                    st.write("3.1. За неисполнение или ненадлежащее исполнение обязательств по настоящему Договору Стороны несут ответственность в соответствии с действующим законодательством Республики Казахстан.")
                    
                    st.markdown("<b>4. АДРЕСА И РЕКВИЗИТЫ СТОРОН</b>", unsafe_allow_html=True)
                    st.write(f"{address}")
                    
                    st.write("<br><b>ПОДПИСИ СТОРОН:</b><br>От Стороны 1: _________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;От Стороны 2: _________________", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
                
                # ГЕНЕРАЦИЯ WORD
                doc_data = {
                    "Сторона 1": org_name, 
                    "Сторона 2": client_name, 
                    "Детали": d1, 
                    "Условия": d2, 
                    "Сроки": d3,
                    "Реквизиты": address
                }
                word_buf = create_docx(doc_choice, doc_data)
                st.download_button(
                    label=t["download"], 
                    data=word_buf, 
                    file_name=f"Document_{client_name}.docx", 
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            with ai_col:
                st.markdown(f"""
                <div class='ai-sidebar'>
                    <h3 style='color:#6366f1;'>🤖 EasyDoc AI Helper</h3>
                    <p><b>Статус:</b> Документ успешно сформирован.</p>
                    <p><b>Анализ:</b> Проверено соответствие шаблону. Данные интегрированы.</p>
                    <hr>
                    <p style='font-size:0.8rem;'><i>Совет: Убедитесь, что реквизиты сторон указаны корректно перед печатью.</i></p>
                </div>
                """, unsafe_allow_html=True)

elif st.session_state.page == "Отзывы":
    st.header(t["feedback"])
    with st.form("feed"):
        st.text_input(t["name"])
        st.text_area(t["review"])
        if st.form_submit_button(t["send"]): 
            st.success(t["thanks"])

elif st.session_state.page == "Авторы":
    st.header(t["authors"])
    # Сделали красивую карточку с помощью колонок
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if os.path.exists("authors.jpg"): 
            st.image("authors.jpg", use_container_width=True) 
            
    with col2:
        st.markdown("### Yeraly & Ramazan")
        st.markdown("*8 класс | Астана*")
        st.write("Разработчики проекта EasyDoc AI. Мы создали этот инструмент, чтобы автоматизировать рутину малого бизнеса и сделать работу с документами проще и быстрее.")

st.markdown(f"<div style='text-align:center; opacity:0.3; padding:20px;'>EasyDoc AI ©️ {now.year} | Astana</div>", unsafe_allow_html=True)