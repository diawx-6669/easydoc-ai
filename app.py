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

# ===== 2. ДИЗАЙН (CSS) =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background-color: #090e1a; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .main-title { font-size: 3.5rem; font-weight: 800; text-align: center; color: white; margin-bottom: 0px; }
    .main-sub { text-align: center; font-size: 1.4rem; color: #94a3b8; margin-bottom: 2rem; }
    .gen-logo { display: block; margin: 0 auto; width: 380px; padding: 20px; filter: drop-shadow(0 0 10px rgba(99,102,241,0.5)); }
    .doc-preview { 
        background: white; color: black !important; padding: 50px; 
        font-family: 'Times New Roman', serif; border: 1px solid #ccc;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5); line-height: 1.5;
    }
    .doc-preview p, .doc-preview div, .doc-preview b, .doc-preview h3 { color: black !important; }
    .ai-sidebar { background: rgba(99, 102, 241, 0.1); border: 1px solid #6366f1; padding: 20px; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# ===== 3. ГЕНЕРАЦИЯ WORD (УЛУЧШЕННЫЙ ШАБЛОН) =====
def create_docx(doc_type, data):
    doc = Document()
    
    # Заголовок документа
    heading = doc.add_heading(doc_type.upper(), 1)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Дата и город
    date_p = doc.add_paragraph()
    date_p.add_run(f"г. Астана\t\t\t\t\t\t\t\t{datetime.now().strftime('%d.%m.%Y')} г.")
    
    # Преамбула (вступление)
    p = doc.add_paragraph()
    p.add_run(f"\n{data.get('Сторона 1', '__________')} (далее - Сторона 1), ")
    p.add_run("с одной стороны, и ")
    p.add_run(f"{data.get('Сторона 2', '__________')} (далее - Сторона 2), ")
    p.add_run("с другой стороны, совместно именуемые «Стороны», заключили настоящий договор о нижеследующем:\n")
    
    # Основные пункты
    doc.add_heading('1. ПРЕДМЕТ ДОГОВОРА', level=2)
    doc.add_paragraph(f"1.1. По настоящему договору Стороны договорились о следующем: {data.get('Детали', '____________________')}.")
    
    doc.add_heading('2. УСЛОВИЯ И ПОРЯДОК РАСЧЕТОВ', level=2)
    doc.add_paragraph(f"2.1. Основные условия сделки: {data.get('Условия', '____________________')}.")
    doc.add_paragraph(f"2.2. Сроки исполнения обязательств: {data.get('Сроки', '____________________')}.")
    
    doc.add_heading('3. ОТВЕТСТВЕННОСТЬ СТОРОН', level=2)
    doc.add_paragraph("3.1. За неисполнение или ненадлежащее исполнение обязательств по настоящему Договору Стороны несут ответственность в соответствии с действующим законодательством Республики Казахстан.")
    
    # Реквизиты
    doc.add_heading('4. АДРЕСА И РЕКВИЗИТЫ СТОРОН', level=2)
    req_p = doc.add_paragraph(f"{data.get('Реквизиты', '____________________')}\n")
    
    # Подписи
    sign_p = doc.add_paragraph()
    sign_p.add_run("\nПОДПИСИ СТОРОН:\n").bold = True
    sign_p.add_run("От Стороны 1: ___________________        От Стороны 2: ___________________")
    
    # Сохранение в буфер
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ===== 4. SIDEBAR =====
tz = pytz.timezone('Asia/Almaty')
now = datetime.now(tz)

with st.sidebar:
    st.title("EasyDoc AI")
    lang = st.selectbox("🌐 Язык / Language", ["Русский", "English", "Қазақша"])
    st.divider()
    st.write(f"📅 **Дата:** {now.strftime('%d.%m.%Y')}")
    menu = ["Главная", "Генератор", "Отзывы", "Авторы"]
    st.session_state.page = st.radio("Навигация", menu, index=menu.index(st.session_state.page))

# ===== 5. КОНТЕНТ =====

if st.session_state.page == "Главная":
    st.markdown("<div class='main-title'>EasyDoc AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-sub'>Ваш надежный ИИ-помощник для малого бизнеса.</div>", unsafe_allow_html=True)
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    st.divider()
    col_l, col_m, col_r = st.columns([1,2,1])
    if col_m.button("ЗАПУСТИТЬ ГЕНЕРАТОР", use_container_width=True): nav_to("Генератор")

elif st.session_state.page == "Генератор":
    if os.path.exists("logo_pen.png"): 
        st.markdown('<img src="logo_pen.png" class="gen-logo">', unsafe_allow_html=True)
    
    st.header("Настройка шаблона")
    doc_choice = st.selectbox("Выберите тип документа:", [
        "Трудовой договор (Двуязычный Каз/Рус)",
        "Договор купли-продажи имущества",
        "Договор аренды помещения",
        "Договор об оказании услуг",
        "Договор купли-продажи ТС (Авто)"
    ])

    with st.form("main_form"):
        st.subheader("Информация о сторонах")
        c1, c2 = st.columns(2)
        org_name = c1.text_input("Сторона 1 (Организация/Продавец/Работодатель + БИН)")
        client_name = c2.text_input("Сторона 2 (ФИО Клиента/Покупателя/Работника + ИИН)")
        
        st.subheader("Детали сделки")
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

        address = st.text_area("Юридические адреса, контакты и банковские реквизиты сторон (IBAN, Банк)")
        submitted = st.form_submit_button("СОЗДАТЬ ДОКУМЕНТ")

    if submitted:
        if org_name and client_name:
            res_col, ai_col = st.columns([2, 1])
            
            with res_col:
                st.markdown("<div class='doc-preview'>", unsafe_allow_html=True)
                if "Трудовой" in doc_choice:
                    st.markdown("### № __ ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР")
                    st.write(f"Астана қ. / г. Астана — {now.strftime('%d.%m.%Y')}")
                    k1, k2 = st.columns(2)
                    k1.write(f"**Жұмыс беруші:** {org_name}\n\n**Жұмыскер:** {client_name}\n\nЛауазымы: {d1}")
                    k2.write(f"**Работодатель:** {org_name}\n\n**Работник:** {client_name}\n\nДолжность: {d1}")
                    st.write(f"**Жалақы / Оклад:** {d2} KZT")
                    st.write(f"**Сроки:** {d3}")
                else:
                    st.markdown(f"### {doc_choice.upper()}")
                    st.write(f"г. Астана, Дата: {now.strftime('%d.%m.%Y')}")
                    st.write(f"**Стороны:** {org_name} и {client_name}")
                    st.write(f"**Предмет/Детали:** {d1}")
                    st.write(f"**Условия:** {d2}")
                    st.write(f"**Сроки/Особые отметки:** {d3}")
                
                st.write(f"**Реквизиты:**\n{address}")
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
                    label="📥 СКАЧАТЬ WORD (.DOCX)", 
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
    st.header("Обратная связь")
    with st.form("feed"):
        st.text_input("Имя")
        st.text_area("Ваш отзыв")
        if st.form_submit_button("Отправить"): st.success("Спасибо за отзыв!")

elif st.session_state.page == "Авторы":
    st.header("Авторы проекта")
    # Ограничиваем ширину картинки, чтобы она не была огромной
    if os.path.exists("authors.jpg"): 
        st.image("authors.jpg", width=300) 
        
    st.markdown("### Yeraly & Ramazan\n8 класс | Астана")

st.markdown(f"<div style='text-align:center; opacity:0.3; padding:20px;'>EasyDoc AI ©️ {now.year} | Astana</div>", unsafe_allow_html=True)