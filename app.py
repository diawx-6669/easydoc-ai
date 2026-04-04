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

# ===== 2. БОЛЬШОЙ СЛОВАРЬ ДЛЯ ПЕРЕВОДА ВСЕГО ИНТЕРФЕЙСА И ДОКУМЕНТОВ =====
translations = {
    "Русский": {
        "nav": {"Главная": "Главная", "Генератор": "Генератор", "Отзывы": "Отзывы", "Авторы": "Авторы"},
        "subtitle": "Ваш надежный ИИ-помощник для малого бизнеса.",
        "run_btn": "ЗАПУСТИТЬ ГЕНЕРАТОР",
        "date": "Дата", "time": "Время", "nav_title": "Навигация",
        "gen_header": "Настройка шаблона", "doc_type": "Выберите тип документа:",
        "submit": "СОЗДАТЬ ДОКУМЕНТ", "download": "📥 СКАЧАТЬ WORD (.DOCX)",
        "feedback": "Обратная связь", "name": "Имя", "review": "Ваш отзыв", "send": "Отправить", "thanks": "Спасибо за отзыв!",
        "authors": "Авторы проекта", "address_lbl": "Юридические адреса и реквизиты сторон",
        "city": "г. Астана",
        "docs": {
            "labor": "Трудовой договор (Двуязычный Каз/Рус)",
            "prop": "Договор купли-продажи движимого имущества",
            "rent": "Договор аренды помещения",
            "serv": "Договор об оказании услуг",
            "car": "Договор купли-продажи транспортного средства"
        },
        "fields": {
            "p1_labor": "Работодатель (Наименование компании и БИН)",
            "p2_labor": "Работник (ФИО, ИИН и номер удостоверения)",
            "p1_prop": "Продавец (ФИО/Компания, ИИН/БИН)",
            "p2_prop": "Покупатель (ФИО/Компания, ИИН/БИН)",
            "p1_rent": "Арендодатель (ФИО/Компания, ИИН/БИН)",
            "p2_rent": "Арендатор (ФИО/Компания, ИИН/БИН)",
            "p1_serv": "Заказчик (ФИО/Компания, ИИН/БИН)",
            "p2_serv": "Исполнитель (ФИО/Компания, ИИН/БИН)",
            "p1_car": "Продавец ТС (ФИО, ИИН, адрес)",
            "p2_car": "Покупатель ТС (ФИО, ИИН, адрес)",
            "labor_pos": "Должность работника", "labor_salary": "Размер оклада (в тенге)", "labor_term": "Срок договора (например, на 1 год)",
            "prop_name": "Наименование и описание имущества", "prop_price": "Стоимость имущества", "prop_term": "Срок передачи имущества",
            "rent_addr": "Точный адрес и площадь помещения", "rent_price": "Арендная плата в месяц", "rent_term": "Срок аренды",
            "serv_desc": "Описание оказываемых услуг", "serv_price": "Стоимость услуг", "serv_term": "Сроки оказания услуг",
            "car_desc": "Марка, модель и год выпуска авто", "car_price": "Стоимость автомобиля", "car_id": "Гос. номер и VIN код"
        }
    },
    "English": {
        "nav": {"Главная": "Home", "Генератор": "Generator", "Отзывы": "Feedback", "Авторы": "Authors"},
        "subtitle": "Your reliable AI assistant for small businesses.",
        "run_btn": "LAUNCH GENERATOR",
        "date": "Date", "time": "Time", "nav_title": "Navigation",
        "gen_header": "Template Setup", "doc_type": "Select document type:",
        "submit": "CREATE DOCUMENT", "download": "📥 DOWNLOAD WORD (.DOCX)",
        "feedback": "Feedback", "name": "Name", "review": "Your review", "send": "Submit", "thanks": "Thank you for your feedback!",
        "authors": "Project Authors", "address_lbl": "Legal addresses and bank details",
        "city": "Astana city",
        "docs": {
            "labor": "Labor Contract (Bilingual Kaz/Rus)",
            "prop": "Moveable Property Sale Agreement",
            "rent": "Lease Agreement",
            "serv": "Services Agreement",
            "car": "Vehicle Sale Agreement"
        },
        "fields": {
            "p1_labor": "Employer (Company Name & BIN)",
            "p2_labor": "Employee (Full Name, IIN & ID Number)",
            "p1_prop": "Seller (Full Name/Company, IIN/BIN)",
            "p2_prop": "Buyer (Full Name/Company, IIN/BIN)",
            "p1_rent": "Landlord (Full Name/Company, IIN/BIN)",
            "p2_rent": "Tenant (Full Name/Company, IIN/BIN)",
            "p1_serv": "Customer (Full Name/Company, IIN/BIN)",
            "p2_serv": "Contractor (Full Name/Company, IIN/BIN)",
            "p1_car": "Vehicle Seller (Name, IIN, Address)",
            "p2_car": "Vehicle Buyer (Name, IIN, Address)",
            "labor_pos": "Employee's Position", "labor_salary": "Salary amount (in KZT)", "labor_term": "Contract term (e.g., for 1 year)",
            "prop_name": "Name and description of the property", "prop_price": "Property cost", "prop_term": "Transfer deadline",
            "rent_addr": "Exact address and area of the premises", "rent_price": "Monthly rent payment", "rent_term": "Lease term",
            "serv_desc": "Description of services rendered", "serv_price": "Cost of services", "serv_term": "Deadlines for services",
            "car_desc": "Make, model and year of the car", "car_price": "Car cost", "car_id": "State number and VIN code"
        }
    },
    "Қазақша": {
        "nav": {"Главная": "Басты бет", "Генератор": "Генератор", "Отзывы": "Пікірлер", "Авторы": "Авторлар"},
        "subtitle": "Шағын бизнеске арналған сенімді AI көмекшісі.",
        "run_btn": "ГЕНЕРАТОРДЫ ІСКЕ ҚОСУ",
        "date": "Күні", "time": "Уақыты", "nav_title": "Навигация",
        "gen_header": "Үлгіні баптау", "doc_type": "Құжат түрін таңдаңыз:",
        "submit": "ҚҰЖАТТЫ ҚҰРУ", "download": "📥 WORD ЖҮКТЕУ (.DOCX)",
        "feedback": "Кері байланыс", "name": "Атыңыз", "review": "Пікіріңіз", "send": "Жіберу", "thanks": "Пікіріңіз үшін рахмет!",
        "authors": "Жоба авторлары", "address_lbl": "Тараптардың заңды мекенжайлары мен деректемелері",
        "city": "Астана қ.",
        "docs": {
            "labor": "Еңбек шарты (Екі тілде Қаз/Орыс)",
            "prop": "Жылжымалы мүлікті сатып алу-сату шарты",
            "rent": "Үй-жайды жалдау шарты",
            "serv": "Қызмет көрсету шарты",
            "car": "Көлік құралын сатып алу-сату шарты"
        },
        "fields": {
            "p1_labor": "Жұмыс беруші (Компания атауы және БСН)",
            "p2_labor": "Жұмыскер (ТАӘ, ЖСН және куәлік нөмірі)",
            "p1_prop": "Сатушы (ТАӘ/Компания, ЖСН/БСН)",
            "p2_prop": "Сатып алушы (ТАӘ/Компания, ЖСН/БСН)",
            "p1_rent": "Жалға беруші (ТАӘ/Компания, ЖСН/БСН)",
            "p2_rent": "Жалға алушы (ТАӘ/Компания, ЖСН/БСН)",
            "p1_serv": "Тапсырыс беруші (ТАӘ/Компания, ЖСН/БСН)",
            "p2_serv": "Орындаушы (ТАӘ/Компания, ЖСН/БСН)",
            "p1_car": "Көлік сатушысы (ТАӘ, ЖСН, мекенжайы)",
            "p2_car": "Көлік сатып алушысы (ТАӘ, ЖСН, мекенжайы)",
            "labor_pos": "Қызметкердің лауазымы", "labor_salary": "Жалақы мөлшері (теңгемен)", "labor_term": "Шарт мерзімі (мысалы, 1 жылға)",
            "prop_name": "Мүліктің атауы мен сипаттамасы", "prop_price": "Мүліктің құны", "prop_term": "Мүлікті тапсыру мерзімі",
            "rent_addr": "Үй-жайдың нақты мекенжайы мен ауданы", "rent_price": "Айлық жалдау ақысы", "rent_term": "Жалға алу мерзімі",
            "serv_desc": "Көрсетілетін қызметтердің сипаттамасы", "serv_price": "Қызметтердің құны", "serv_term": "Қызмет көрсету мерзімдері",
            "car_desc": "Автокөліктің маркасы, моделі және шыққан жылы", "car_price": "Автокөліктің құны", "car_id": "Мемлекеттік нөмірі және VIN коды"
        }
    }
}

# ===== 3. ДИЗАЙН (CSS) =====
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
    .doc-preview p, .doc-preview div, .doc-preview b, .doc-preview h3, .doc-preview span { color: black !important; }
    .ai-sidebar { background: rgba(99, 102, 241, 0.1); border: 1px solid #6366f1; padding: 20px; border-radius: 15px; }
    .feedback-card { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #6366f1; }
</style>
""", unsafe_allow_html=True)

# ===== 4. ГЕНЕРАЦИЯ WORD В ЗАВИСИМОСТИ ОТ ЯЗЫКА =====
def create_docx(doc_id, data, lang):
    doc = Document()
    date_str = datetime.now().strftime('%d.%m.%Y')
    
    # Задаем язык самого шаблона в зависимости от выбранного
    if doc_id == "labor":
        heading = doc.add_heading("ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР", 1)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        p = doc.add_paragraph()
        p.add_run(f"Астана қ. / г. Астана \t\t\t\t\t\t\t {date_str} ж/г.")
        
        p2 = doc.add_paragraph()
        p2.add_run(f"\nРаботодатель / Жұмыс беруші: {data.get('p1')}\nРаботник / Жұмыскер: {data.get('p2')}\n\n")
        p2.add_run("Стороны заключили настоящий договор / Тараптар осы шартты жасасты:\n").bold = True
        
        doc.add_heading('1. Предмет / Шарттың мәні', level=2)
        doc.add_paragraph(f"Принять на работу на должность / Жұмысқа қабылдау лауазымы: {data.get('d1')}")
        
        doc.add_heading('2. Оплата и Сроки / Төлем және Мерзімдері', level=2)
        doc.add_paragraph(f"Оклад составляет / Жалақы мөлшері: {data.get('d2')} KZT.")
        doc.add_paragraph(f"Срок действия / Қолданылу мерзімі: {data.get('d3')}.")

    else:
        # Для остальных документов переводим саму структуру на выбранный язык
        titles = {
            "Русский": {"prop": "ДОГОВОР КУПЛИ-ПРОДАЖИ", "rent": "ДОГОВОР АРЕНДЫ", "serv": "ДОГОВОР ОБ ОКАЗАНИИ УСЛУГ", "car": "ДОГОВОР КУПЛИ-ПРОДАЖИ ТС"},
            "English": {"prop": "SALE AND PURCHASE AGREEMENT", "rent": "LEASE AGREEMENT", "serv": "SERVICES AGREEMENT", "car": "VEHICLE SALE AGREEMENT"},
            "Қазақша": {"prop": "САТЫП АЛУ-САТУ ШАРТЫ", "rent": "ЖАЛДАУ ШАРТЫ", "serv": "ҚЫЗМЕТ КӨРСЕТУ ШАРТЫ", "car": "КӨЛІК ҚҰРАЛЫН САТЫП АЛУ-САТУ ШАРТЫ"}
        }
        
        doc_heading = titles[lang][doc_id]
        heading = doc.add_heading(doc_heading, 1)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        city = translations[lang]["city"]
        p = doc.add_paragraph()
        p.add_run(f"{city} \t\t\t\t\t\t\t {date_str}")
        
        # Названия ролей для преамбулы
        roles = {
            "Русский": {"prop": ("Продавец", "Покупатель"), "rent": ("Арендодатель", "Арендатор"), "serv": ("Заказчик", "Исполнитель"), "car": ("Продавец", "Покупатель")},
            "English": {"prop": ("Seller", "Buyer"), "rent": ("Landlord", "Tenant"), "serv": ("Customer", "Contractor"), "car": ("Seller", "Buyer")},
            "Қазақша": {"prop": ("Сатушы", "Сатып алушы"), "rent": ("Жалға беруші", "Жалға алушы"), "serv": ("Тапсырыс беруші", "Орындаушы"), "car": ("Сатушы", "Сатып алушы")}
        }
        r1, r2 = roles[lang][doc_id]
        
        # Преамбула на выбранном языке
        p2 = doc.add_paragraph()
        if lang == "Русский":
            p2.add_run(f"\n{data.get('p1')} (далее - {r1}), с одной стороны, и {data.get('p2')} (далее - {r2}), с другой стороны, заключили настоящий договор о нижеследующем:\n")
        elif lang == "English":
            p2.add_run(f"\n{data.get('p1')} (hereinafter - {r1}), on the one part, and {data.get('p2')} (hereinafter - {r2}), on the other part, have concluded this agreement as follows:\n")
        else:
            p2.add_run(f"\nБір тараптан {data.get('p1')} (бұдан әрі - {r1}), және екінші тараптан {data.get('p2')} (бұдан әрі - {r2}), төмендегілер туралы осы шартты жасасты:\n")

        # Разделы на выбранном языке
        secs = {
            "Русский": ["1. ПРЕДМЕТ ДОГОВОРА", "2. ФИНАНСОВЫЕ УСЛОВИЯ И СРОКИ", "3. АДРЕСА И РЕКВИЗИТЫ СТОРОН"],
            "English": ["1. SUBJECT OF THE AGREEMENT", "2. FINANCIAL CONDITIONS AND TERMS", "3. ADDRESSES AND DETAILS OF THE PARTIES"],
            "Қазақша": ["1. ШАРТТЫҢ МӘНІ", "2. ҚАРЖЫЛЫҚ ШАРТТАР МЕН МЕРЗІМДЕР", "3. ТАРАПТАРДЫҢ МЕКЕНЖАЙЛАРЫ МЕН ДЕРЕКТЕМЕЛЕРІ"]
        }
        
        doc.add_heading(secs[lang][0], level=2)
        doc.add_paragraph(f"{data.get('d1')}")
        
        doc.add_heading(secs[lang][1], level=2)
        doc.add_paragraph(f"{data.get('d2')}")
        doc.add_paragraph(f"{data.get('d3')}")
        
        doc.add_heading(secs[lang][2], level=2)
        doc.add_paragraph(f"{data.get('addr')}")
        
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ===== 5. SIDEBAR И ЧАСЫ =====
tz = pytz.timezone('Asia/Almaty')
now = datetime.now(tz)

with st.sidebar:
    st.title("EasyDoc AI")
    selected_lang = st.selectbox("🌐 Язык / Language", ["Русский", "English", "Қазақша"])
    t = translations[selected_lang]
    
    st.divider()
    st.write(f"📅 **{t['date']}:** {now.strftime('%d.%m.%Y')}")
    
    # LIVE CLOCK С ПОМОЩЬЮ HTML/JS КОМПОНЕНТА
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

# ===== 6. КОНТЕНТ ПО СТРАНИЦАМ =====

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
    st.header(t["gen_header"])
    
    # Динамический список документов на выбранном языке
    docs_mapping = {
        t["docs"]["labor"]: "labor",
        t["docs"]["prop"]: "prop",
        t["docs"]["rent"]: "rent",
        t["docs"]["serv"]: "serv",
        t["docs"]["car"]: "car"
    }
    
    doc_choice_ui = st.selectbox(t["doc_type"], list(docs_mapping.keys()))
    doc_id = docs_mapping[doc_choice_ui]

    # Специфические вопросы формы для каждого документа
    with st.form("main_form"):
        st.subheader("1. " + t["address_lbl"].split()[0])
        c1, c2 = st.columns(2)
        
        # Получаем ключи вопросов из словаря
        p1_q = t["fields"][f"p1_{doc_id}"]
        p2_q = t["fields"][f"p2_{doc_id}"]
        
        org_name = c1.text_input(p1_q)
        client_name = c2.text_input(p2_q)
        
        st.subheader("2. Детали")
        col3, col4 = st.columns(2)
        
        if doc_id == "labor":
            d1 = col3.text_input(t["fields"]["labor_pos"])
            d2 = col4.text_input(t["fields"]["labor_salary"])
            d3 = st.text_input(t["fields"]["labor_term"])
        elif doc_id == "rent":
            d1 = col3.text_input(t["fields"]["rent_addr"])
            d2 = col4.text_input(t["fields"]["rent_price"])
            d3 = st.text_input(t["fields"]["rent_term"])
        elif doc_id == "car":
            d1 = col3.text_input(t["fields"]["car_desc"])
            d2 = col4.text_input(t["fields"]["car_price"])
            d3 = st.text_input(t["fields"]["car_id"])
        elif doc_id == "serv":
            d1 = col3.text_input(t["fields"]["serv_desc"])
            d2 = col4.text_input(t["fields"]["serv_price"])
            d3 = st.text_input(t["fields"]["serv_term"])
        else: # prop
            d1 = col3.text_input(t["fields"]["prop_name"])
            d2 = col4.text_input(t["fields"]["prop_price"])
            d3 = st.text_input(t["fields"]["prop_term"])

        address = st.text_area(t["address_lbl"])
        submitted = st.form_submit_button(t["submit"])

    if submitted:
        if org_name and client_name:
            res_col, ai_col = st.columns([2, 1])
            
            with res_col:
                st.markdown("<div class='doc-preview'>", unsafe_allow_html=True)
                
                # Рендеринг ПРЕВЬЮ на выбранном языке
                if doc_id == "labor":
                    st.markdown("<h3 style='text-align:center;'>№ __ ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='display:flex; justify-content:space-between;'><span>Астана қ. / г. Астана</span><span>{now.strftime('%d.%m.%Y')} ж/г.</span></p>", unsafe_allow_html=True)
                    k1, k2 = st.columns(2)
                    k1.write(f"**Жұмыс беруші:** {org_name}\n\n**Жұмыскер:** {client_name}\n\nЛауазымы: {d1}")
                    k2.write(f"**Работодатель:** {org_name}\n\n**Работник:** {client_name}\n\nДолжность: {d1}")
                    st.write(f"**Оклад / Жалақы:** {d2} KZT<br>**Мерзімі / Срок:** {d3}", unsafe_allow_html=True)
                    r1, r2 = "Работодатель / Жұмыс беруші", "Работник / Жұмыскер"
                else:
                    titles_preview = {
                        "Русский": {"prop": "ДОГОВОР КУПЛИ-ПРОДАЖИ", "rent": "ДОГОВОР АРЕНДЫ", "serv": "ДОГОВОР ОБ ОКАЗАНИИ УСЛУГ", "car": "ДОГОВОР КУПЛИ-ПРОДАЖИ ТС"},
                        "English": {"prop": "SALE AND PURCHASE AGREEMENT", "rent": "LEASE AGREEMENT", "serv": "SERVICES AGREEMENT", "car": "VEHICLE SALE AGREEMENT"},
                        "Қазақша": {"prop": "САТЫП АЛУ-САТУ ШАРТЫ", "rent": "ЖАЛДАУ ШАРТЫ", "serv": "ҚЫЗМЕТ КӨРСЕТУ ШАРТЫ", "car": "КӨЛІК ҚҰРАЛЫН САТЫП АЛУ-САТУ ШАРТЫ"}
                    }
                    roles_preview = {
                        "Русский": {"prop": ("Продавец", "Покупатель"), "rent": ("Арендодатель", "Арендатор"), "serv": ("Заказчик", "Исполнитель"), "car": ("Продавец", "Покупатель")},
                        "English": {"prop": ("Seller", "Buyer"), "rent": ("Landlord", "Tenant"), "serv": ("Customer", "Contractor"), "car": ("Seller", "Buyer")},
                        "Қазақша": {"prop": ("Сатушы", "Сатып алушы"), "rent": ("Жалға беруші", "Жалға алушы"), "serv": ("Тапсырыс беруші", "Орындаушы"), "car": ("Сатушы", "Сатып алушы")}
                    }
                    
                    r1, r2 = roles_preview[selected_lang][doc_id]
                    st.markdown(f"<h3 style='text-align:center;'>{titles_preview[selected_lang][doc_id]}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='display:flex; justify-content:space-between;'><span>{translations[selected_lang]['city']}</span><span>{now.strftime('%d.%m.%Y')}</span></p>", unsafe_allow_html=True)
                    
                    # Логика текста преамбулы в превью
                    if selected_lang == "Русский":
                        st.markdown(f"<p><b>{org_name}</b> (далее - {r1}), с одной стороны, и <b>{client_name}</b> (далее - {r2}), с другой стороны, заключили настоящий договор:</p>", unsafe_allow_html=True)