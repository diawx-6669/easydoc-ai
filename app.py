import streamlit as st
import time
from datetime import date
import os

# ===== 1. НАСТРОЙКИ СТРАНИЦЫ =====
st.set_page_config(page_title="EasyDoc AI | Enterprise", page_icon="📝", layout="centered")

# ===== 2. ДИЗАЙН (DARK PREMIUM) =====
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f172a, #1e293b); color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .block-container { background: #1e293b; padding: 40px; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); }
    h1, h2, h3 { text-align: center; color: white !important; }
    p, label { color: #cbd5e1 !important; }
    .stTextInput>div>div>input { background-color: #334155 !important; color: white !important; border-radius: 10px; border: 2px solid transparent; }
    .stTextInput>div>div>input:focus { border: 2px solid #6366f1 !important; }
    .stSelectbox div[data-baseweb="select"] { background-color: #334155 !important; color: white !important; border-radius: 10px; }
    .stButton>button { background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; font-weight: bold; border-radius: 12px; height: 60px; width: 100%; border: none; transition: 0.4s; text-transform: uppercase; }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 15px 30px rgba(99,102,241,0.4); }
    .ai-card { background: rgba(99, 102, 241, 0.1); border: 1px solid #6366f1; padding: 20px; border-radius: 15px; margin: 25px 0; }
    .footer { text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #334155; }
    .team-name { color: #6366f1; font-weight: bold; font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# ===== 3. ЛОГОТИП =====
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h1>📝 EasyDoc AI</h1>", unsafe_allow_html=True)

# ===== 4. ВЫБОР ЯЗЫКА =====
lang = st.selectbox("🌐 Choose Language", ("English", "Русский", "Қазақша"))

# Переводы интерфейса
translations = {
    "English": ["Document Type", "Generate", "AI Insights", "Astana, Kazakhstan", 
                ("Employment Contract", "NDA", "Service Agreement", "Sales Contract", "Lease Agreement")],
    "Русский": ["Тип документа", "Сгенерировать", "Обзор AI", "Астана, Казахстан", 
                ("Трудовой договор", "NDA", "Договор услуг", "Договор купли-продажи", "Договор аренды")],
    "Қазақша": ["Құжат түрі", "Дайындау", "AI шолуы", "Астана, Қазақстан", 
                ("Еңбек шарты", "NDA", "Қызмет көрсету шарты", "Сату-сатып алу шарты", "Жалдау шарты")]
}

t_labels = translations[lang]
doc_type = st.selectbox(t_labels[0], t_labels[4])
st.divider()

# ===== 5. ФОРМА ВВОДА =====
with st.form("doc_form"):
    c1, c2 = st.columns(2)
    party_a = c1.text_input("Party A (Employer/Seller/Lessor)")
    party_b = c2.text_input("Party B (Employee/Buyer/Lessee)")
    
    # Уникальные поля для каждого типа
    if "Employment" in doc_type or "Еңбек" in doc_type or "Трудовой" in doc_type:
        d1 = c1.text_input("Position")
        d2 = c2.text_input("Salary (KZT/Month)")
    elif "NDA" in doc_type:
        d1 = c1.text_input("Secrecy Term (Years)", "5")
        d2 = c2.text_input("Penalty Fine (KZT)")
    elif "Sales" in doc_type or "Сату" in doc_type or "продажи" in doc_type:
        d1 = c1.text_input("Item Name (e.g. Laptop)")
        d2 = c2.text_input("Total Price (KZT)")
    elif "Lease" in doc_type or "Жалдау" in doc_type or "аренды" in doc_type:
        d1 = c1.text_input("Address of Property")
        d2 = c2.text_input("Monthly Rent (KZT)")
    else: # Service
        d1 = c1.text_input("Service Description")
        d2 = c2.text_input("Contract Value (KZT)")

    submit = st.form_submit_button(t_labels[1])

# ===== 6. ГЕНЕРАЦИЯ ЮРИДИЧЕСКОГО ТЕКСТА =====
if submit:
    if party_a and party_b:
        with st.spinner("AI is drafting..."):
            time.sleep(1.5)
        
        # ЛОГИКА ТЕКСТА
        if "Employment" in doc_type or "Трудовой" in doc_type or "Еңбек" in doc_type:
            title, body = "EMPLOYMENT AGREEMENT", f"<h3>1. SUBJECT</h3><p>Party B is hired as <b>{d1}</b>.</p><h3>2. SALARY</h3><p>Monthly compensation: <b>{d2} KZT</b>.</p>"
        elif "NDA" in doc_type:
            title, body = "NON-DISCLOSURE AGREEMENT", f"<h3>1. CONFIDENTIALITY</h3><p>Protection period: <b>{d1} years</b>.</p><h3>2. PENALTY</h3><p>Breach fine: <b>{d2} KZT</b>.</p>"
        elif "Sales" in doc_type or "Сату" in doc_type or "продажи" in doc_type:
            title, body = "SALES CONTRACT", f"<h3>1. ITEM</h3><p>Seller transfers ownership of: <b>{d1}</b>.</p><h3>2. PRICE</h3><p>Total amount: <b>{d2} KZT</b>.</p>"
        elif "Lease" in doc_type or "Жалдау" in doc_type or "аренды" in doc_type:
            title, body = "LEASE AGREEMENT", f"<h3>1. PROPERTY</h3><p>Located at: <b>{d1}</b>.</p><h3>2. RENT</h3><p>Monthly payment: <b>{d2} KZT</b>.</p>"
        else:
            title, body = "SERVICE CONTRACT", f"<h3>1. SERVICES</h3><p>Scope: <b>{d1}</b>.</p><h3>2. PAYMENT</h3><p>Total: <b>{d2} KZT</b>.</p>"

        # HTML ШАБЛОН
        html = f"""
        <html><body style='font-family:Times New Roman; padding:50px; color:black;'>
            <h1 style='text-align:center;'>{title}</h1>
            <p><b>Date:</b> {date.today()} | <b>Location:</b> {t_labels[3]}</p>
            <hr><p>This Agreement is between <b>{party_a}</b> and <b>{party_b}</b>.</p>
            {body}
            <h3>3. SIGNATURES</h3>
            <p>Party A: _________________ &nbsp;&nbsp;&nbsp;&nbsp; Party B: _________________</p>
        </body></html>
        """

        # AI CARD
        st.markdown(f"""<div class="ai-card"><h3>{t_labels[2]}</h3><p>✅ Type: {doc_type}</p><p>✅ Parties: {party_a} / {party_b}</p></div>""", unsafe_allow_html=True)
        st.download_button("📥 Download Official .DOC", html, f"EasyDoc_{party_b}.doc", "application/msword")

# ===== 7. FOOTER =====
st.markdown(f"""<div class="footer"><p>EasyDoc AI | Team: <span class="team-name">Yeraly & Ramazan</span></p></div>""", unsafe_allow_html=True)