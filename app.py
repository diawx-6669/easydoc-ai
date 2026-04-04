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

# ===== 3. CSS ДИЗАЙН =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background: radial-gradient(ellipse at 20% 50%, rgba(99,102,241,0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 20%, rgba(139,92,246,0.06) 0%, transparent 50%),
                    radial-gradient(ellipse at 50% 80%, rgba(59,130,246,0.05) 0%, transparent 50%),
                    linear-gradient(160deg, #050816 0%, #0a0f1e 30%, #0d1326 60%, #080c1a 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10,15,30,0.98) 0%, rgba(15,20,40,0.95) 100%) !important;
        backdrop-filter: blur(24px);
        border-right: 1px solid rgba(99,102,241,0.12);
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stRadio > div {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(99,102,241,0.1); }
        50% { box-shadow: 0 0 40px rgba(99,102,241,0.2), 0 0 60px rgba(99,102,241,0.05); }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes pulseGlow {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 0.8; }
    }

    .main-title {
        font-size: 4.5rem; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 40%, #a5b4fc 60%, #818cf8 100%);
        background-size: 200% auto;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: fadeInUp 1s ease-out, shimmer 4s linear infinite;
        margin-bottom: 0; letter-spacing: -0.03em; line-height: 1.1;
    }
    .main-sub {
        text-align: center; font-size: 1.25rem; color: #64748b;
        margin-bottom: 3rem; font-weight: 400;
        animation: fadeInUp 1s ease-out 0.2s both;
    }

    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
        backdrop-filter: blur(24px);
        border: 1px solid rgba(99,102,241,0.1);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
        animation: fadeInUp 0.6s ease-out both;
    }
    .glass-card:hover {
        border-color: rgba(99,102,241,0.3);
        box-shadow: 0 8px 40px rgba(99,102,241,0.1), 0 0 0 1px rgba(99,102,241,0.05);
        transform: translateY(-3px);
    }

    .feature-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(139,92,246,0.04) 100%);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 20px;
        padding: 32px 24px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
        animation: fadeInUp 0.6s ease-out both;
    }
    .feature-card:hover {
        background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.08) 100%);
        border-color: rgba(99,102,241,0.4);
        transform: translateY(-6px);
        box-shadow: 0 20px 50px rgba(99,102,241,0.15);
    }
    .feature-icon {
        font-size: 2.5rem; margin-bottom: 16px;
        animation: float 3s ease-in-out infinite;
    }
    .feature-title { font-size: 1.05rem; font-weight: 700; color: #e2e8f0; margin-bottom: 6px; }
    .feature-desc { font-size: 0.82rem; color: #64748b; line-height: 1.5; }

    .doc-preview {
        background: linear-gradient(135deg, #fefefe, #f8fafc);
        color: #1a1a2e !important;
        padding: 44px;
        font-family: 'Times New Roman', Georgia, serif;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.08);
        box-shadow: 0 25px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05);
        line-height: 1.8;
        animation: fadeInUp 0.5s ease-out;
    }
    .doc-preview p, .doc-preview div, .doc-preview b, .doc-preview h3, .doc-preview span { color: #1a1a2e !important; }

    .ai-sidebar {
        background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.05));
        border: 1px solid rgba(99,102,241,0.2);
        padding: 28px; border-radius: 20px;
        animation: fadeIn 0.6s ease-out 0.3s both;
    }

    .feedback-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        backdrop-filter: blur(16px);
        padding: 24px; border-radius: 16px; margin-bottom: 16px;
        border-left: 3px solid #6366f1;
        border-top: 1px solid rgba(99,102,241,0.08);
        border-right: 1px solid rgba(99,102,241,0.08);
        border-bottom: 1px solid rgba(99,102,241,0.08);
        transition: all 0.4s ease;
        animation: slideInLeft 0.5s ease-out both;
    }
    .feedback-card:hover {
        border-left-color: #818cf8;
        box-shadow: 0 8px 30px rgba(99,102,241,0.12);
        transform: translateX(4px);
    }

    .author-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.06), rgba(139,92,246,0.03));
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 24px;
        padding: 48px 40px;
        text-align: center;
        animation: fadeInUp 0.8s ease-out, glow 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    .author-card::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(99,102,241,0.03) 0%, transparent 70%);
        animation: pulseGlow 4s ease-in-out infinite;
    }
    .author-photo {
        width: 140px; height: 140px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid rgba(99,102,241,0.3);
        box-shadow: 0 8px 30px rgba(99,102,241,0.2);
        margin: 0 auto 20px;
        display: block;
        animation: fadeIn 1s ease-out 0.3s both;
    }

    .stButton > button {
        border-radius: 16px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.03em;
        transition: all 0.4s cubic-bezier(0.4,0,0.2,1) !important;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(99,102,241,0.35) !important;
    }
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #7c3aed, #8b5cf6) !important;
        color: white !important; border: none !important; border-radius: 16px !important;
        font-weight: 700 !important; padding: 14px 28px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.2) !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(99,102,241,0.4) !important;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        border-radius: 14px !important;
        border-color: rgba(99,102,241,0.15) !important;
        background: rgba(255,255,255,0.03) !important;
        transition: all 0.3s ease !important;
        color: #e2e8f0 !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(99,102,241,0.5) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.08), 0 0 20px rgba(99,102,241,0.05) !important;
    }

    hr { border-color: rgba(99,102,241,0.08) !important; }

    .footer {
        text-align: center; color: #334155; font-size: 0.85rem;
        padding: 40px 0; margin-top: 80px;
        border-top: 1px solid rgba(99,102,241,0.08);
        animation: fadeIn 1s ease-out;
    }

    .section-header {
        font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.15em; color: #6366f1; margin-bottom: 16px;
        padding-bottom: 8px; border-bottom: 1px solid rgba(99,102,241,0.15);
    }

    .orb {
        position: fixed; border-radius: 50%; pointer-events: none;
        filter: blur(80px); opacity: 0.15; z-index: 0;
    }
    .orb-1 { width: 400px; height: 400px; background: #6366f1; top: 10%; left: 5%; animation: float 8s ease-in-out infinite; }
    .orb-2 { width: 300px; height: 300px; background: #8b5cf6; bottom: 20%; right: 10%; animation: float 6s ease-in-out infinite 1s; }
    .orb-3 { width: 250px; height: 250px; background: #3b82f6; top: 60%; left: 40%; animation: float 10s ease-in-out infinite 2s; }
</style>
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>
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
    clock_html = f"""
    <div style="font-family: 'Inter', monospace; font-size: 13px; color: #94a3b8; padding: 4px 0;">
        🕒 {t['time']}: <span id="clock"></span>
    </div>
    <script>
        function updateClock() {{
            const now = new Date().toLocaleTimeString('ru-RU', {{timeZone: 'Asia/Almaty'}});
            const el = document.getElementById('clock');
            if (el) el.textContent = now;
        }}
        updateClock();
        setInterval(updateClock, 1000);
    </script>
    """
    components.html(clock_html, height=30)
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
    st.markdown("")
    st.markdown("")
    st.markdown('<div class="main-title">EasyDoc AI</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="main-sub">{t["subtitle"]}</div>', unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button(t["run_btn"], use_container_width=True, type="primary"):
            nav_to("Генератор")

    st.markdown("")
    st.markdown("")
    st.markdown(f"#### ✦ {t['features_title']}")
    st.markdown("")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'''<div class="feature-card" style="animation-delay: 0.1s;">
            <div class="feature-icon">📋</div>
            <div class="feature-title">{t["feat1"]}</div>
            <div class="feature-desc">{t["feat1_desc"]}</div>
        </div>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<div class="feature-card" style="animation-delay: 0.3s;">
            <div class="feature-icon">🌍</div>
            <div class="feature-title">{t["feat2"]}</div>
            <div class="feature-desc">{t["feat2_desc"]}</div>
        </div>''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''<div class="feature-card" style="animation-delay: 0.5s;">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">{t["feat3"]}</div>
            <div class="feature-desc">{t["feat3_desc"]}</div>
        </div>''', unsafe_allow_html=True)

elif st.session_state.page == "Генератор":
    st.markdown(f"## {t['gen_header']}")
    st.markdown("")

    doc_options = ["labor", "prop", "rent", "serv", "car"]
    doc_id = st.selectbox(t["doc_type"], doc_options, format_func=lambda x: t["docs"][x])

    with st.form("main_form"):
        st.markdown(f'<div class="section-header">1. {t["parties"]}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        org_name = c1.text_input(t["fields"][f"p1_{doc_id}"])
        client_name = c2.text_input(t["fields"][f"p2_{doc_id}"])

        st.markdown("")
        st.markdown(f'<div class="section-header">2. {t["details"]}</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        d1 = col3.text_input(t["fields"][f"d1_{doc_id}"])
        d2 = col4.text_input(t["fields"][f"d2_{doc_id}"])
        d3 = st.text_input(t["fields"][f"d3_{doc_id}"])
        address = st.text_area(t["address"])

        submitted = st.form_submit_button(t["submit"], use_container_width=True, type="primary")

    if submitted:
        if org_name and client_name:
            res_col, ai_col = st.columns([2, 1])
            with res_col:
                st.markdown('<div class="doc-preview">', unsafe_allow_html=True)
                if doc_id == "labor":
                    st.markdown("<h3 style='text-align:center; color:#1a1a2e!important;'>ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:#1a1a2e!important;'><b>Работодатель / Жұмыс беруші:</b> {org_name}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:#1a1a2e!important;'><b>Работник / Жұмыскер:</b> {client_name}</p>", unsafe_allow_html=True)
                else:
                    titles_preview = {
                        "Русский": {"prop": "ДОГОВОР КУПЛИ-ПРОДАЖИ", "rent": "ДОГОВОР АРЕНДЫ", "serv": "ДОГОВОР ОБ ОКАЗАНИИ УСЛУГ", "car": "ДОГОВОР КУПЛИ-ПРОДАЖИ ТС"},
                        "English": {"prop": "SALE AND PURCHASE AGREEMENT", "rent": "LEASE AGREEMENT", "serv": "SERVICES AGREEMENT", "car": "VEHICLE SALE AGREEMENT"},
                        "Қазақша": {"prop": "САТЫП АЛУ-САТУ ШАРТЫ", "rent": "ЖАЛДАУ ШАРТЫ", "serv": "ҚЫЗМЕТ КӨРСЕТУ ШАРТЫ", "car": "КӨЛІК ҚҰРАЛЫН САТЫП АЛУ-САТУ ШАРТЫ"}
                    }
                    st.markdown(f"<h3 style='text-align:center; color:#1a1a2e!important;'>{titles_preview[selected_lang][doc_id]}</h3>", unsafe_allow_html=True)
                if d1:
                    st.markdown(f"<p style='color:#1a1a2e!important;'>🔹 {d1}</p>", unsafe_allow_html=True)
                if d2:
                    st.markdown(f"<p style='color:#1a1a2e!important;'>🔹 {d2}</p>", unsafe_allow_html=True)
                if d3:
                    st.markdown(f"<p style='color:#1a1a2e!important;'>🔹 {d3}</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                doc_data = {"p1": org_name, "p2": client_name, "d1": d1, "d2": d2, "d3": d3, "addr": address}
                word_buf = create_docx(doc_id, doc_data, selected_lang)
                st.markdown("")
                st.download_button(
                    label=t["download"], data=word_buf,
                    file_name=f"{doc_id}_{client_name}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            with ai_col:
                st.markdown(f"""
                <div class="ai-sidebar">
                    <p style="font-size: 1.15rem; margin-bottom: 10px;">🤖 <b>EasyDoc AI</b></p>
                    <p style="color: #94a3b8; font-size: 0.9rem;">Документ подготовлен на языке: <b>{selected_lang}</b></p>
                    <p style="color: #64748b; font-size: 0.8rem; margin-top: 14px;">✅ Проверьте данные перед использованием.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Заполните обе стороны договора!")

elif st.session_state.page == "Отзывы":
    st.markdown(f"## {t['feedback']}")
    st.markdown("")
    st.markdown("""
    <div class="feedback-card">
        <div style="margin-bottom: 10px;">
            <span style="font-weight: 600; font-size: 1rem;">👤 Айдос, ИП "AlmatyTech"</span>
            <span style="color: #eab308;"> ⭐⭐⭐⭐⭐</span>
        </div>
        <p style="color: #cbd5e1; margin-bottom: 10px; line-height: 1.6;">Отличный генератор! Сэкономил кучу времени на договорах аренды.</p>
        <p style="color: #818cf8; font-size: 0.85rem;">💡 Добавьте возможность загружать свои собственные шаблоны.</p>
    </div>
    <div class="feedback-card" style="animation-delay: 0.15s;">
        <div style="margin-bottom: 10px;">
            <span style="font-weight: 600; font-size: 1rem;">👤 Елена, HR-менеджер</span>
            <span style="color: #eab308;"> ⭐⭐⭐⭐⭐</span>
        </div>
        <p style="color: #cbd5e1; margin-bottom: 10px; line-height: 1.6;">Трудовые договоры на двух языках (Каз/Рус) — это просто спасение!</p>
        <p style="color: #818cf8; font-size: 0.85rem;">💡 Было бы здорово сохранять базу сотрудников.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("##### ✍️ Оставить свой отзыв:")
    with st.form("feed"):
        name_input = st.text_input(t["name"])
        review_input = st.text_area(t["review"])
        if st.form_submit_button(t["send"], type="primary"):
            if name_input and review_input:
                st.success(t["thanks"])
            else:
                st.warning("⚠️ Заполните все поля!")

elif st.session_state.page == "Авторы":
    st.markdown(f"## {t['authors']}")
    st.markdown("")
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        # Фото авторов
        photo_html = ""
        if os.path.exists("authors.jpg"):
            with open("authors.jpg", "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            photo_html = f'<img class="author-photo" src="data:image/jpeg;base64,{img_data}" alt="Yeraly & Ramazan" />'
        else:
            photo_html = '<div style="font-size: 4rem; margin-bottom: 20px; animation: float 3s ease-in-out infinite;">👨‍💻</div>'

        st.markdown(f"""
        <div class="author-card">
            {photo_html}
            <h2 style="margin-bottom: 6px; font-weight: 800; font-size: 1.8rem; position: relative; z-index: 1;">Yeraly & Ramazan</h2>
            <p style="color: #a5b4fc; font-size: 1.05rem; font-weight: 500; position: relative; z-index: 1;">8 класс</p>
            <p style="color: #64748b; font-size: 0.9rem; margin-top: 10px; position: relative; z-index: 1;">📍 Астана, Казахстан</p>
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(99,102,241,0.15); position: relative; z-index: 1;">
                <p style="color: #475569; font-size: 0.85rem; line-height: 1.6;">Разработчики проекта EasyDoc AI</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f'<div class="footer">EasyDoc AI © {now.year} | Astana, Kazakhstan 🇰🇿</div>', unsafe_allow_html=True)
