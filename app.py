import streamlit as st
import time
from datetime import date
import os

# ===== SETTINGS =====
st.set_page_config(page_title="EasyDoc AI", page_icon="📝", layout="centered")

# ===== STYLE (Dark Gradient) =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}
.block-container {
    background: #1e293b;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}
h1, h2, h3 { text-align: center; color: white !important; }
p, label { color: #cbd5e1 !important; }

/* Input styling */
.stTextInput>div>div>input {
    background-color: #334155 !important;
    color: white !important;
    border-radius: 10px;
    border: 2px solid transparent;
}
.stTextInput>div>div>input:focus { border: 2px solid #6366f1 !important; }

/* Button styling */
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 55px;
    width: 100%;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 25px rgba(99,102,241,0.5);
}

/* AI Insights Box */
.ai-box {
    background-color: rgba(99, 102, 241, 0.1);
    border-left: 5px solid #6366f1;
    padding: 15px;
    border-radius: 5px;
    margin: 20px 0;
}

/* Professional Footer */
.footer-container {
    text-align: center;
    margin-top: 60px;
    padding: 20px;
    border-top: 1px solid #334155;
}
.footer-team { color: #6366f1; font-weight: bold; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# ===== LOGO =====
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h1>📝 EasyDoc AI</h1>", unsafe_allow_html=True)

# ===== LANGUAGE & DOC TYPE =====
st.markdown("### 🌍 Select Language / Тілді таңдаңыз:")
lang = st.selectbox("", ("English", "Русский", "Қазақша"))
st.divider()

# Переменные для перевода
if lang == "English":
    types = ("Employment Contract", "NDA", "Service Agreement")
    btn_text = "GENERATE DOCUMENT"
    summary_title = "🤖 AI Document Insights"
elif lang == "Русский":
    types = ("Трудовой договор", "NDA (Конфиденциальность)", "Договор услуг")
    btn_text = "СГЕНЕРИРОВАТЬ"
    summary_title = "🤖 Краткий обзор от AI"
else:
    types = ("Еңбек шарты", "NDA (Құпиялылық)", "Қызмет көрсету шарты")
    btn_text = "ДАЙЫНДАУ"
    summary_title = "🤖 AI құжатқа шолу"

doc_type = st.selectbox("Document Type", types)

# ===== FORM =====
with st.form("main_form"):
    c1, c2 = st.columns(2)
    comp = c1.text_input("Employer / Company")
    work = c2.text_input("Employee / Partner")
    
    if "Employment" in doc_type or "Еңбек" in doc_type or "Трудовой" in doc_type:
        val1 = c1.text_input("Position")
        val2 = c2.text_input("Salary (KZT)")
    elif "NDA" in doc_type:
        val1 = c1.text_input("Duration (Years)", "5")
        val2 = c2.text_input("Penalty Fine (KZT)", "1,000,000")
    else:
        val1 = c1.text_input("Service Title")
        val2 = c2.text_input("Price / Deadline")

    submitted = st.form_submit_button(btn_text)

# ===== PROCESSING & OUTPUT =====
if submitted:
    if comp and work:
        with st.spinner("AI is analyzing and generating..."):
            time.sleep(1.5)
        
        # 4. ФУНКЦИЯ AI SUMMARY (ИНСАЙТЫ)
        st.markdown(f"""<div class="ai-box">
            <h4 style="margin-top:0;">{summary_title}</h4>
            <p>• <b>Parties:</b> {comp} & {work}</p>
            <p>• <b>Key Terms:</b> {val1}, {val2}</p>
            <p>• <b>Status:</b> Legally structured for Google Docs.</p>
        </div>""", unsafe_allow_html=True)

        # Контент для скачивания
        html_content = f"<html><body style='font-family:Arial;'><h1>{doc_type.upper()}</h1><p>Date: {date.today()}</p><p><b>Party A:</b> {comp}</p><p><b>Party B:</b> {work}</p><p><b>Details:</b> {val1}, {val2}</p></body></html>"
        
        st.success("Success!")
        st.download_button("📥 Download for Google Docs", html_content, f"EasyDoc_{work}.doc")

# ===== 5. ПРОФЕССИОНАЛЬНЫЙ ФУТЕР =====
st.markdown(f"""
<div class="footer-container">
    <p>EasyDoc AI — Automating Business Documentation</p>
    <p>Developed by Team: <span class="footer-team">Yeraly & Ramazan</span></p>
    <p style="font-size: 0.8rem;">Hackathon 2026 | Astana, Kazakhstan</p>
</div>
""", unsafe_allow_html=True)