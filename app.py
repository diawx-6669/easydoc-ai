import streamlit as st
import time
from datetime import datetime
import os
import pytz
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import streamlit.components.v1 as components

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
    .feedback-card { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #6366f1; }
</style>
""", unsafe_allow_html=True)

# ===== 3. ГЕНЕРАЦИЯ WORD (ДИНАМИЧЕСКИЕ ШАБЛОНЫ) =====
def create_docx(doc_type, data):
    doc = Document()
    
    heading = doc.add_heading(doc_type.upper(), 1)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    date_p = doc.add_paragraph()
    date_p.add_run(f"г. Астана\t\t\t\t\t\t\t\t{datetime.now().strftime('%d.%m.%Y')} г.")
    
    p = doc.add_paragraph()
    
    # ---------------- ЛОГИКА ДЛЯ РАЗНЫХ ШАБЛОНОВ ----------------
    if "Трудовой" in doc_type:
        p.add_run(f"\n{data.get('Сторона 1')} (далее - Работодатель), с одной стороны, и {data.get('Сторона 2')} (далее - Работник), с другой стороны, совместно именуемые «Стороны», заключили настоящий Трудовой договор о нижеследующем:\n")
        
        doc.add_heading('1. ПРЕДМЕТ ДОГОВОРА', level=2)
        doc.add_paragraph(f"1.1. Работодатель принимает Работника на работу, а Работник обязуется выполнять работу (трудовую функцию) в должности: {data.get('Детали')}.")
        
        doc.add_heading('2. УСЛОВИЯ ОПЛАТЫ И СРОКИ', level=2)
        doc.add_paragraph(f"2.1. Работнику устанавливается оклад в размере: {data.get('Условия')}.")
        doc.add_paragraph(f"2.2. Срок действия договора: {data.get('Сроки')}.")
        role_1, role_2 = "Работодатель", "Работник"

    elif "имущества" in doc_type:
        p.add_run(f"\n{data.get('Сторона 1')} (далее - Продавец), с одной стороны, и {data.get('Сторона 2')} (далее - Покупатель), с другой стороны, заключили настоящий Договор о нижеследующем:\n")
        
        doc.add_heading('1. ПРЕДМЕТ ДОГОВОРА', level=2)
        doc.add_paragraph(f"1.1. Продавец обязуется передать в собственность Покупателя движимое имущество, а именно: {data.get('Детали')}, а Покупатель обязуется принять имущество и уплатить за него цену.")
        
        doc.add_heading('2. ЦЕНА ДОГОВОРА И ПОРЯДОК РАСЧЕТОВ', level=2)
        doc.add_paragraph(f"2.1. Общая стоимость имущества составляет: {data.get('Условия')}.")
        doc.add_paragraph(f"2.2. Сроки передачи имущества и оплаты: {data.get('Сроки')}.")
        role_1, role_2 = "Продавец", "Покупатель"

    elif "аренды" in doc_type:
        p.add_run(f"\n{data.get('Сторона 1')} (далее - Арендодатель), с одной стороны, и {data.get('Сторона 2')} (далее - Арендатор), с другой стороны, заключили настоящий Договор аренды о нижеследующем:\n")
        
        doc.add_heading('1. ПРЕДМЕТ ДОГОВОРА', level=2)
        doc.add_paragraph(f"1.1. Арендодатель передает, а Арендатор принимает во временное владение и пользование помещение, расположенное по адресу: {data.get('Детали')}.")
        
        doc.add_heading('2. АРЕНДНАЯ ПЛАТА И СРОК', level=2)
        doc.add_paragraph(f"2.1. Размер арендной платы составляет: {data.get('Условия')} в месяц.")
        doc.add_paragraph(f"2.2. Срок аренды: {data.get('Сроки')}.")
        role_1, role_2 = "Арендодатель", "Арендатор"

    elif "услуг" in doc_type:
        p.add_run(f"\n{data.get('Сторона 1')} (далее - Заказчик), с одной стороны, и {data.get('Сторона 2')} (далее - Исполнитель), с другой стороны, заключили настоящий Договор об оказании услуг о нижеследующем:\n")
        
        doc.add_heading('1. ПРЕДМЕТ ДОГОВОРА', level=2)
        doc.add_paragraph(f"1.1. Заказчик поручает, а Исполнитель принимает на себя обязательство оказать следующие услуги: {data.get('Детали')}.")
        
        doc.add_heading('2. СТОИМОСТЬ УСЛУГ И СРОКИ ИСПОЛНЕНИЯ', level=2)
        doc.add_paragraph(f"2.1. Стоимость оказываемых услуг составляет: {data.get('Условия')}.")
        doc.add_paragraph(f"2.2. Сроки выполнения услуг: {data.get('Сроки')}.")
        role_1, role_2 = "Заказчик", "Исполнитель"

    elif "Авто" in doc_type:
        p.add_run(f"\n{data.get('Сторона 1')} (далее - Продавец), с одной стороны, и {data.get('Сторона 2')} (далее - Покупатель), с другой стороны, заключили настоящий Договор купли-продажи транспортного средства:\n")
        
        doc.add_heading('1. ПРЕДМЕТ ДОГОВОРА', level=2)
        doc.add_paragraph(f"1.1. Продавец обязуется передать в собственность Покупателя Транспортное Средство: {data.get('Детали')}.")
        doc.add_paragraph(f"1.2. Идентификационные данные ТС (Гос. номер и VIN): {data.get('Сроки')}.")
        
        doc.add_heading('2. ЦЕНА ДОГОВОРА', level=2)
        doc.add_paragraph(f"2.1. Стоимость Транспортного Средства составляет: {data.get('Условия')}.")
        role_1, role_2 = "Продавец", "Покупатель"

    # ---------------- ОБЩИЕ ПУНКТЫ ----------------
    doc.add_heading('3. ОТВЕТСТВЕННОСТЬ СТОРОН', level=2)
    doc.add_paragraph("3.1. За неисполнение или ненадлежащее исполнение обязательств по настоящему Договору Стороны несут ответственность в соответствии с действующим законодательством Республики Казахстан.")
    
    doc.add_heading('4. АДРЕСА И РЕКВИЗИТЫ СТОРОН', level=2)
    doc.add_paragraph(f"{data.get('Реквизиты')}\n")
    
    sign_p = doc.add_paragraph()
    sign_p.add_run("\nПОДПИСИ СТОРОН:\n").bold = True
    sign_p.add_run(f"От лица ({role_1}): ___________________        От лица ({role_2}): ___________________")
    
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
    t = translations[selected_lang]
    
    st.divider()
    st.write(f"📅 **{t['date']}:** {now.strftime('%d.%m.%Y')}")
    
    # LIVE CLOCK ПОМОЩЬЮ HTML/JS КОМПОНЕНТА
    clock_html = f"""
    <div style="font-family: 'Inter', sans-serif; color: #f1f5f9; font-size: 1rem; margin-bottom: 1rem;">
        🕒 <b>{t['time']}:</b> <span id="live-clock"></span>
    </div>
    <script>
        function updateClock() {{
            const date = new Date();
            const timeString = date.toLocaleTimeString('ru-RU', {{timeZone: 'Asia/Almaty'}});
            document.getElementById('live-clock').innerText = timeString;
        }}
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """
    components.html(clock_html, height=30)
    
    # Навигация с переводом
    menu_keys = ["Главная", "Генератор", "Отзывы", "Авторы"]
    menu_labels = [t["nav"][k] for k in menu_keys]
    
    selected_label = st.radio(t["nav_title"], menu_labels, index=menu_keys.index(st.session_state.page))
    st.session_state.page = menu_keys[menu_labels.index(selected_label)]

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
        
        # Динамические плейсхолдеры в зависимости от типа документа
        if "Трудовой" in doc_choice:
            p1_label, p2_label = "Работодатель (Название + БИН)", "Работник (ФИО + ИИН)"
        elif "имущества" in doc_choice or "Авто" in doc_choice:
            p1_label, p2_label = "Продавец (ФИО/Организация + ИИН/БИН)", "Покупатель (ФИО/Организация + ИИН/БИН)"
        elif "аренды" in doc_choice:
            p1_label, p2_label = "Арендодатель (ФИО/Организация)", "Арендатор (ФИО/Организация)"
        else:
            p1_label, p2_label = "Заказчик (ФИО/Организация)", "Исполнитель (ФИО/Организация)"
            
        org_name = c1.text_input(p1_label)
        client_name = c2.text_input(p2_label)
        
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
                st.markdown("<div class='doc-preview'>", unsafe_allow_html=True)
                
                # ДИНАМИЧЕСКОЕ ПРЕВЬЮ
                if "Трудовой" in doc_choice:
                    st.markdown("<h3 style='text-align:center;'>№ __ ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='display:flex; justify-content:space-between;'><span>Астана қ. / г. Астана</span><span>{now.strftime('%d.%m.%Y')} ж/г.</span></p>", unsafe_allow_html=True)
                    k1, k2 = st.columns(2)
                    k1.write(f"**Жұмыс беруші:** {org_name}\n\n**Жұмыскер:** {client_name}\n\nЛауазымы: {d1}")
                    k2.write(f"**Работодатель:** {org_name}\n\n**Работник:** {client_name}\n\nДолжность: {d1}")
                    st.write(f"**Жалақы / Оклад:** {d2} KZT<br>**Сроки:** {d3}", unsafe_allow_html=True)
                    r1, r2 = "Работодатель", "Работник"
                else:
                    st.markdown(f"<h3 style='text-align:center;'>{doc_choice.upper()}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='display:flex; justify-content:space-between;'><span>г. Астана</span><span>{now.strftime('%d.%m.%Y')} г.</span></p>", unsafe_allow_html=True)
                    
                    if "имущества" in doc_choice or "Авто" in doc_choice:
                        r1, r2 = "Продавец", "Покупатель"
                    elif "аренды" in doc_choice:
                        r1, r2 = "Арендодатель", "Арендатор"
                    else:
                        r1, r2 = "Заказчик", "Исполнитель"
                        
                    st.markdown(f"<p><b>{org_name}</b> (далее - {r1}), с одной стороны, и <b>{client_name}</b> (далее - {r2}), с другой стороны, заключили настоящий договор о нижеследующем:</p>", unsafe_allow_html=True)
                    
                    st.markdown("<b>1. ПРЕДМЕТ ДОГОВОРА</b>", unsafe_allow_html=True)
                    st.write(f"1.1. Объектом договора является: {d1}.")
                    if "Авто" in doc_choice: st.write(f"1.2. Данные (VIN/Госномер): {d3}.")
                    
                    st.markdown("<b>2. ФИНАНСОВЫЕ УСЛОВИЯ И СРОКИ</b>", unsafe_allow_html=True)
                    st.write(f"2.1. Сумма/Оплата по договору: {d2}.")
                    if "Авто" not in doc_choice: st.write(f"2.2. Сроки и условия: {d3}.")
                    
                    st.markdown("<b>3. АДРЕСА И РЕКВИЗИТЫ СТОРОН</b>", unsafe_allow_html=True)
                    st.write(f"{address}")
                    
                st.write(f"<br><b>ПОДПИСИ СТОРОН:</b><br>От лица ({r1}): _______________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;От лица ({r2}): _______________", unsafe_allow_html=True)
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
                    <p><b>Анализ:</b> Применен шаблон <i>{doc_choice}</i>. Условия интегрированы.</p>
                    <hr>
                    <p style='font-size:0.8rem;'><i>Совет: Внимательно проверьте реквизиты и ИИН/БИН перед печатью и подписанием.</i></p>
                </div>
                """, unsafe_allow_html=True)

elif st.session_state.page == "Отзывы":
    st.header(t["feedback"])
    
    # ФЕЙКОВЫЕ ОТЗЫВЫ И ПОЖЕЛАНИЯ
    st.subheader("Последние отзывы пользователей")
    st.markdown("""
    <div class='feedback-card'>
        <b>👤 Айдос, ИП "AlmatyTech"</b> ⭐⭐⭐⭐⭐<br>
        <i>Отличный генератор! Сэкономил кучу времени на договорах аренды. <br>
        <span style='color: #fbbf24;'>💡 Пожелание:</span> Добавьте возможность загружать свои собственные шаблоны.</i>
    </div>
    <div class='feedback-card'>
        <b>👤 Елена, HR-менеджер</b> ⭐⭐⭐⭐⭐<br>
        <i>Трудовые договоры на двух языках (Каз/Рус) — это просто спасение! <br>
        <span style='color: #fbbf24;'>💡 Пожелание:</span> Было бы здорово, если бы можно было сохранять базу сотрудников, чтобы не вводить ИИН каждый раз.</i>
    </div>
    <div class='feedback-card'>
        <b>👤 Марат, Автосалон</b> ⭐⭐⭐⭐<br>
        <i>Всё супер, договоры купли-продажи авто составляются за секунду. <br>
        <span style='color: #fbbf24;'>💡 Пожелание:</span> Хотелось бы интеграцию с Egov для автозаполнения данных по ИИН/БИН.</i>
    </div>
    <hr>
    """, unsafe_allow_html=True)
    
    with st.form("feed"):
        st.write("**Оставить свой отзыв:**")
        st.text_input(t["name"])
        st.text_area(t["review"])
        if st.form_submit_button(t["send"]): 
            st.success(t["thanks"])

elif st.session_state.page == "Авторы":
    st.header(t["authors"])
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if os.path.exists("authors.jpg"): 
            st.image("authors.jpg", use_container_width=True) 
            
    with col2:
        st.markdown("### Yeraly & Ramazan")
        st.markdown("**8 класс | Астана**")
        st.write("Разработчики проекта EasyDoc AI. Мы создали этот инструмент, чтобы автоматизировать рутину малого бизнеса и сделать работу с документами проще и быстрее.")

st.markdown(f"<div style='text-align:center; opacity:0.3; padding:20px; '>EasyDoc AI ©️ {now.year} | Astana</div>", unsafe_allow_html=True)