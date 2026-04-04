import streamlit as st
from datetime import datetime
import pytz
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import streamlit.components.v1 as components
import base64
import os

# ===== 1. НАСТРОЙКИ =====
st.set_page_config(page_title="EasyDoc AI", page_icon="📝", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = "Главная"

def nav_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ===== 2. ПЕРЕВОДЫ =====
translations = {
    "Русский": {
        "nav_title": "Навигация",
        "nav": {"Главная": "Главная", "Генератор": "Генератор", "Отзывы": "Отзывы", "Авторы": "Авторы"},
        "subtitle": "Ваш надежный ИИ-помощник для малого бизнеса.",
        "run_btn": "🚀 ЗАПУСТИТЬ ГЕНЕРАТОР",
        "date": "Дата", "time": "Время",
        "gen_header": "⚙️ Настройка шаблона", "doc_type": "Выберите тип документа:",
        "address": "Юридические адреса, контакты и банковские реквизиты сторон (IBAN, Банк)",
        "submit": "✨ СОЗДАТЬ ДОКУМЕНТ", "download": "📥 СКАЧАТЬ WORD (.DOCX)",
        "feedback": "Обратная связь", "name": "Имя", "review": "Ваш отзыв",
        "send": "Отправить", "thanks": "✅ Спасибо за отзыв!",
        "authors": "Авторы проекта", "city": "г. Астана",
        "features_title": "Возможности",
        "feat1": "5 типов договоров", "feat1_desc": "Трудовые, аренда, купля-продажа и другие",
        "feat2": "3 языка", "feat2_desc": "Русский, English, Қазақша",
        "feat3": "Мгновенно", "feat3_desc": "Генерация DOCX за секунды",
        "parties": "Стороны", "details": "Детали",
        "docs": {
            "labor": "📋 Трудовой договор (Двуязычный Каз/Рус)",
            "prop": "🏠 Договор купли-продажи имущества",
            "rent": "🏢 Договор аренды помещения",
            "serv": "🤝 Договор об оказании услуг",
            "car": "🚗 Договор купли-продажи ТС (Авто)"
        },
        "fields": {
            "p1_labor": "Работодатель (Название + БИН)", "p2_labor": "Работник (ФИО + ИИН)",
            "p1_prop": "Продавец (ФИО/Организация)", "p2_prop": "Покупатель (ФИО/Организация)",
            "p1_rent": "Арендодатель (ФИО/Организация)", "p2_rent": "Арендатор (ФИО/Организация)",
            "p1_serv": "Заказчик (ФИО/Организация)", "p2_serv": "Исполнитель (ФИО/Организация)",
            "p1_car": "Продавец ТС (ФИО + ИИН)", "p2_car": "Покупатель ТС (ФИО + ИИН)",
            "d1_labor": "Должность работника", "d2_labor": "Оклад (цифрами и прописью)", "d3_labor": "Срок договора",
            "d1_prop": "Описание имущества", "d2_prop": "Стоимость имущества", "d3_prop": "Срок передачи",
            "d1_rent": "Адрес помещения", "d2_rent": "Арендная плата", "d3_rent": "Срок аренды",
            "d1_serv": "Описание услуг", "d2_serv": "Сумма договора", "d3_serv": "Срок оказания",
            "d1_car": "Марка, Модель, Год", "d2_car": "Цена авто", "d3_car": "Гос. номер и VIN код"
        }
    },
    "English": {
        "nav_title": "Navigation",
        "nav": {"Главная": "Home", "Генератор": "Generator", "Отзывы": "Feedback", "Авторы": "Authors"},
        "subtitle": "Your reliable AI assistant for small businesses.",
        "run_btn": "🚀 LAUNCH GENERATOR",
        "date": "Date", "time": "Time",
        "gen_header": "⚙️ Template Setup", "doc_type": "Select document type:",
        "address": "Legal addresses, contacts and bank details (IBAN, Bank)",
        "submit": "✨ CREATE DOCUMENT", "download": "📥 DOWNLOAD WORD (.DOCX)",
        "feedback": "Feedback", "name": "Name", "review": "Your review",
        "send": "Submit", "thanks": "✅ Thank you for your feedback!",
        "authors": "Project Authors", "city": "Astana city",
        "features_title": "Features",
        "feat1": "5 document types", "feat1_desc": "Labor, lease, sale and more",
        "feat2": "3 languages", "feat2_desc": "Русский, English, Қазақша",
        "feat3": "Instant", "feat3_desc": "DOCX generation in seconds",
        "parties": "Parties", "details": "Details",
        "docs": {
            "labor": "📋 Labor Contract (Bilingual Kaz/Rus)",
            "prop": "🏠 Property Sale Agreement",
            "rent": "🏢 Lease Agreement",
            "serv": "🤝 Services Agreement",
            "car": "🚗 Vehicle Sale Agreement"
        },
        "fields": {
            "p1_labor": "Employer (Company + BIN)", "p2_labor": "Employee (Name + IIN)",
            "p1_prop": "Seller (Name/Company)", "p2_prop": "Buyer (Name/Company)",
            "p1_rent": "Landlord (Name/Company)", "p2_rent": "Tenant (Name/Company)",
            "p1_serv": "Customer (Name/Company)", "p2_serv": "Contractor (Name/Company)",
            "p1_car": "Seller (Name + IIN)", "p2_car": "Buyer (Name + IIN)",
            "d1_labor": "Position", "d2_labor": "Salary", "d3_labor": "Contract term",
            "d1_prop": "Property description", "d2_prop": "Property cost", "d3_prop": "Transfer deadline",
            "d1_rent": "Premises address", "d2_rent": "Monthly rent", "d3_rent": "Lease term",
            "d1_serv": "Services description", "d2_serv": "Contract amount", "d3_serv": "Deadline",
            "d1_car": "Make, Model, Year", "d2_car": "Car price", "d3_car": "Plate & VIN"
        }
    },
    "Қазақша": {
        "nav_title": "Навигация",
        "nav": {"Главная": "Басты бет", "Генератор": "Генератор", "Отзывы": "Пікірлер", "Авторы": "Авторлар"},
        "subtitle": "Шағын бизнеске арналған сенімді AI көмекшісі.",
        "run_btn": "🚀 ГЕНЕРАТОРДЫ ІСКЕ ҚОСУ",
        "date": "Күні", "time": "Уақыты",
        "gen_header": "⚙️ Үлгіні баптау", "doc_type": "Құжат түрін таңдаңыз:",
        "address": "Заңды мекенжайлар, байланыстар және банк деректемелері (IBAN, Банк)",
        "submit": "✨ ҚҰЖАТТЫ ҚҰРУ", "download": "📥 WORD ЖҮКТЕУ (.DOCX)",
        "feedback": "Кері байланыс", "name": "Атыңыз", "review": "Пікіріңіз",
        "send": "Жіберу", "thanks": "✅ Пікіріңіз үшін рахмет!",
        "authors": "Жоба авторлары", "city": "Астана қ.",
        "features_title": "Мүмкіндіктер",
        "feat1": "5 құжат түрі", "feat1_desc": "Еңбек, жалдау, сатып алу-сату",
        "feat2": "3 тіл", "feat2_desc": "Русский, English, Қазақша",
        "feat3": "Лезде", "feat3_desc": "DOCX бірнеше секундта",
        "parties": "Тараптар", "details": "Мәліметтер",
        "docs": {
            "labor": "📋 Еңбек шарты (Қаз/Орыс)",
            "prop": "🏠 Сатып алу-сату шарты",
            "rent": "🏢 Жалдау шарты",
            "serv": "🤝 Қызмет көрсету шарты",
            "car": "🚗 Көлік сатып алу-сату шарты"
        },
        "fields": {
            "p1_labor": "Жұмыс беруші (Атауы + БСН)", "p2_labor": "Жұмыскер (ТАӘ + ЖСН)",
            "p1_prop": "Сатушы (ТАӘ/Ұйым)", "p2_prop": "Сатып алушы (ТАӘ/Ұйым)",
            "p1_rent": "Жалға беруші (ТАӘ/Ұйым)", "p2_rent": "Жалға алушы (ТАӘ/Ұйым)",
            "p1_serv": "Тапсырыс беруші (ТАӘ/Ұйым)", "p2_serv": "Орындаушы (ТАӘ/Ұйым)",
            "p1_car": "Көлік сатушысы (ТАӘ + ЖСН)", "p2_car": "Көлік сатып алушысы (ТАӘ + ЖСН)",
            "d1_labor": "Лауазымы", "d2_labor": "Жалақы мөлшері", "d3_labor": "Шарт мерзімі",
            "d1_prop": "Мүліктің сипаттамасы", "d2_prop": "Мүліктің құны", "d3_prop": "Тапсыру мерзімі",
            "d1_rent": "Мекенжайы", "d2_rent": "Жалдау ақысы", "d3_rent": "Жалдау мерзімі",
            "d1_serv": "Қызметтер сипаттамасы", "d2_serv": "Шарт сомасы", "d3_serv": "Мерзімі",
            "d1_car": "Маркасы, Моделі, Жылы", "d2_car": "Көлік құны", "d3_car": "Мемлекеттік нөмір және VIN"
        }
    }
}

# ===== 3. CSS ДИЗАЙН (С НОВЫМ ФОНОМ) =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Новые анимации из ваших скриншотов */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes rotateSlow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .stApp {
        background: #050816; /* Глубокий темный фон как основа */
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.15) 0%, transparent 40%);
        background-size: 200% 200%;
        animation: gradientShift 15s ease infinite;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }

    /* Псевдоэлемент для "живого" вращающегося свечения */
    .stApp::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(
            from 0deg,
            rgba(99, 102, 241, 0) 0%,
            rgba(99, 102, 241, 0.05) 25%,
            rgba(139, 92, 246, 0) 50%,
            rgba(59, 130, 246, 0.05) 75%,
            rgba(99, 102, 241, 0) 100%
        );
        animation: rotateSlow 20s linear infinite;
        z-index: -1;
        pointer-events: none;
    }

    section[data-testid="stSidebar"] {
        background: rgba(10, 15, 30, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }

    /* Остальные стили */
    .main-title {
        font-size: 4.5rem; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 50%, #818cf8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0; letter-spacing: -0.03em;
    }
    .main-sub {
        text-align: center; font-size: 1.25rem; color: #94a3b8;
        margin-bottom: 3rem;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: 0.4s;
    }
    .feature-card:hover {
        background: rgba(99, 102, 241, 0.05);
        border-color: rgba(99, 102, 241, 0.3);
        transform: translateY(-5px);
    }

    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== 4. ГЕНЕРАЦИЯ WORD =====
def create_docx(doc_id, data, lang):
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    date_str = datetime.now().strftime('%d.%m.%Y')

    if doc_id == "labor":
        heading = doc.add_heading("ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР", level=1)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in heading.runs:
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(0, 0, 0)
        p = doc.add_paragraph()
        p.add_run("Астана қ. / г. Астана").bold = True
        p.add_run(f"\t\t\t\t\t\t{date_str} ж/г.")
        doc.add_paragraph("")
        p2 = doc.add_paragraph()
        p2.add_run("Работодатель / Жұмыс беруші: ").bold = True
        p2.add_run(data.get('p1', ''))
        p3 = doc.add_paragraph()
        p3.add_run("Работник / Жұмыскер: ").bold = True
        p3.add_run(data.get('p2', ''))
        doc.add_paragraph("")
        h2 = doc.add_heading('1. Предмет / Шарттың мәні', level=2)
        for run in h2.runs:
            run.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph(f"Принять на работу на должность / Лауазымы: {data.get('d1', '')}")
        h3 = doc.add_heading('2. Оплата и Сроки / Төлем және Мерзімдері', level=2)
        for run in h3.runs:
            run.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph(f"Оклад / Жалақы: {data.get('d2', '')} KZT.")
        doc.add_paragraph(f"Срок / Мерзімі: {data.get('d3', '')}")
    else:
        titles = {
            "Русский": {"prop": "ДОГОВОР КУПЛИ-ПРОДАЖИ", "rent": "ДОГОВОР АРЕНДЫ", "serv": "ДОГОВОР ОБ ОКАЗАНИИ УСЛУГ", "car": "ДОГОВОР КУПЛИ-ПРОДАЖИ ТС"},
            "English": {"prop": "SALE AND PURCHASE AGREEMENT", "rent": "LEASE AGREEMENT", "serv": "SERVICES AGREEMENT", "car": "VEHICLE SALE AGREEMENT"},
            "Қазақша": {"prop": "САТЫП АЛУ-САТУ ШАРТЫ", "rent": "ЖАЛДАУ ШАРТЫ", "serv": "ҚЫЗМЕТ КӨРСЕТУ ШАРТЫ", "car": "КӨЛІК ҚҰРАЛЫН САТЫП АЛУ-САТУ ШАРТЫ"}
        }
        heading = doc.add_heading(titles[lang][doc_id], level=1)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in heading.runs:
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(0, 0, 0)
        city_name = translations[lang]['city']
        p = doc.add_paragraph()
        p.add_run(city_name).bold = True
        p.add_run(f"\t\t\t\t\t\t{date_str}")
        roles = {
            "Русский": {"prop": ("Продавец", "Покупатель"), "rent": ("Арендодатель", "Арендатор"), "serv": ("Заказчик", "Исполнитель"), "car": ("Продавец", "Покупатель")},
            "English": {"prop": ("Seller", "Buyer"), "rent": ("Landlord", "Tenant"), "serv": ("Customer", "Contractor"), "car": ("Seller", "Buyer")},
            "Қазақша": {"prop": ("Сатушы", "Сатып алушы"), "rent": ("Жалға беруші", "Жалға алушы"), "serv": ("Тапсырыс беруші", "Орындаушы"), "car": ("Сатушы", "Сатып алушы")}
        }
        r1, r2 = roles[lang][doc_id]
        doc.add_paragraph("")
        p2 = doc.add_paragraph()
        if lang == "Русский":
            p2.add_run(f"{data.get('p1', '')} (далее — {r1}), с одной стороны, и {data.get('p2', '')} (далее — {r2}), с другой стороны, заключили настоящий договор о нижеследующем:")
        elif lang == "English":
            p2.add_run(f"{data.get('p1', '')} (hereinafter — {r1}), on the one part, and {data.get('p2', '')} (hereinafter — {r2}), on the other part, have concluded this agreement as follows:")
        else:
            p2.add_run(f"Бір тараптан {data.get('p1', '')} (бұдан әрі — {r1}), және екінші тараптан {data.get('p2', '')} (бұдан әрі — {r2}), осы шартты жасасты:")
        doc.add_paragraph("")
        h2a = doc.add_heading('1. Предмет', level=2)
        for run in h2a.runs:
            run.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph(data.get('d1', ''))
        h2b = doc.add_heading('2. Условия', level=2)
        for run in h2b.runs:
            run.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph(data.get('d2', ''))
        doc.add_paragraph(data.get('d3', ''))
        if data.get('addr'):
            h2c = doc.add_heading('3. Реквизиты сторон', level=2)
            for run in h2c.runs:
                run.font.color.rgb = RGBColor(0, 0, 0)
            doc.add_paragraph(data.get('addr', ''))

    doc.add_paragraph("")
    sig = doc.add_paragraph()
    sig.add_run("___________________ / ")
    sig.add_run(data.get('p1', ''))
    doc.add_paragraph("")
    sig2 = doc.add_paragraph()
    sig2.add_run("___________________ / ")
    sig2.add_run(data.get('p2', ''))

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ===== 5. SIDEBAR =====
tz = pytz.timezone('Asia/Almaty')
now = datetime.now(tz)

with st.sidebar:
    st.markdown("### 📝 EasyDoc AI")
    selected_lang = st.selectbox("🌐 Язык / Language", ["Русский", "English", "Қазақша"])
    t = translations[selected_lang]
    st.divider()
    st.caption(f"📅 {t['date']}: {now.strftime('%d.%m.%Y')}")
    st.divider()
    menu_keys = ["Главная", "Генератор", "Отзывы", "Авторы"]
    selected_key = st.radio(
        t["nav_title"],
        menu_keys,
        index=menu_keys.index(st.session_state.page),
        format_func=lambda x: t["nav"][x]
    )
    st.session_state.page = selected_key

# ===== 6. СТРАНИЦЫ =====
if st.session_state.page == "Главная":
    st.markdown('<div class="main-title">EasyDoc AI</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="main-sub">{t["subtitle"]}</div>', unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button(t["run_btn"], use_container_width=True, type="primary"):
            nav_to("Генератор")

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'''<div class="feature-card">
            <div style="font-size:2rem">📋</div>
            <div style="font-weight:700">{t["feat1"]}</div>
            <div style="font-size:0.8rem; color:#94a3b8">{t["feat1_desc"]}</div>
        </div>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<div class="feature-card">
            <div style="font-size:2rem">🌍</div>
            <div style="font-weight:700">{t["feat2"]}</div>
            <div style="font-size:0.8rem; color:#94a3b8">{t["feat2_desc"]}</div>
        </div>''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''<div class="feature-card">
            <div style="font-size:2rem">⚡</div>
            <div style="font-weight:700">{t["feat3"]}</div>
            <div style="font-size:0.8rem; color:#94a3b8">{t["feat3_desc"]}</div>
        </div>''', unsafe_allow_html=True)

elif st.session_state.page == "Генератор":
    st.markdown(f"## {t['gen_header']}")
    doc_options = ["labor", "prop", "rent", "serv", "car"]
    doc_id = st.selectbox(t["doc_type"], doc_options, format_func=lambda x: t["docs"][x])

    with st.form("main_form"):
        c1, c2 = st.columns(2)
        org_name = c1.text_input(t["fields"][f"p1_{doc_id}"])
        client_name = c2.text_input(t["fields"][f"p2_{doc_id}"])
        d1 = st.text_input(t["fields"][f"d1_{doc_id}"])
        d2 = st.text_input(t["fields"][f"d2_{doc_id}"])
        d3 = st.text_input(t["fields"][f"d3_{doc_id}"])
        address = st.text_area(t["address"])
        submitted = st.form_submit_button(t["submit"], use_container_width=True)

    if submitted:
        if org_name and client_name:
            doc_data = {"p1": org_name, "p2": client_name, "d1": d1, "d2": d2, "d3": d3, "addr": address}
            word_buf = create_docx(doc_id, doc_data, selected_lang)
            st.success("Документ готов!")
            st.download_button(label=t["download"], data=word_buf, file_name=f"{doc_id}.docx", use_container_width=True)
        else:
            st.warning("Заполните основные поля!")

elif st.session_state.page == "Отзывы":
    st.markdown(f"## {t['feedback']}")
    st.info("Здесь будут отображаться отзывы пользователей.")

elif st.session_state.page == "Авторы":
    st.markdown(f"## {t['authors']}")
    st.markdown("""
    <div style="text-align:center; padding: 40px; background: rgba(255,255,255,0.05); border-radius: 20px;">
        <h2>Yeraly & Ramazan</h2>
        <p>8 класс | Астана, Казахстан</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center; padding: 20px; color:#475569">EasyDoc AI © {now.year}</div>', unsafe_allow_html=True)
