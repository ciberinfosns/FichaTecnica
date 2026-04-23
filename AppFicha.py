import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
import io

def generar_pdf_sofisticado(datos):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    ancho, alto = A4

    # --- CONFIGURACI¨®N DE COLORES (Azul corporativo oscuro) ---
    color_principal = colors.HexColor("#1B2631")
    color_linea = colors.HexColor("#D5D8DC")

    # --- ENCABEZADO ---
    c.setFillColor(color_principal)
    c.rect(0, alto - 80, ancho, 80, fill=1, stroke=0) # Barra superior
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, alto - 50, "GS CONTROL")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, alto - 65, "SISTEMAS DE SEGURIDAD Y CONTROL DE ACCESOS")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(ancho - 50, alto - 50, "FICHA TECNICA")
    c.setFont("Helvetica", 9)
    c.drawRightString(ancho - 50, alto - 65, f"No. Registro: {datos['n_abonado']}")

    # --- CUERPO DEL DOCUMENTO ---
    y_inicial = alto - 120

    def dibujar_seccion(titulo, y_pos):
        c.setFillColor(color_principal)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y_pos, titulo.upper())
        c.setStrokeColor(color_linea)
        c.setLineWidth(1)
        c.line(50, y_pos - 5, ancho - 50, y_pos - 5)
        return y_pos - 25

    # 1. INFORMACION GENERAL
    y = dibujar_seccion("1. Informacion General", y_inicial)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    
    # Grid de datos
    c.drawString(50, y, "Cod. Instalador:"); c.setFont("Helvetica", 10); c.drawString(150, y, datos['cod_instalador'])
    c.setFont("Helvetica-Bold", 10); c.drawString(300, y, "D.G.P.:"); c.setFont("Helvetica", 10); c.drawString(360, y, datos['dgp'])
    y -= 18
    c.setFont("Helvetica-Bold", 10); c.drawString(50, y, "Fecha Emision:"); c.setFont("Helvetica", 10); c.drawString(150, y, datos['fecha'])
    c.setFont("Helvetica-Bold", 10); c.drawString(300, y, "Abonado:"); c.setFont("Helvetica", 10); c.drawString(360, y, datos['n_abonado'])

    # 2. LOCALIZACION Y CONTACTO
    y = dibujar_seccion("2. Localizacion y Contacto", y - 35)
    
    datos_cliente = [
        ("Titular / Empresa", datos['nombre']),
        ("Direccion", datos['direccion']),
        ("Poblacion", f"{datos['poblacion']} ({datos['provincia']})"),
        ("Cod. Postal", datos['cp']),
        ("Email", datos['email']),
        ("Tipo Instalacion", datos['tipo']),
        ("Coordenadas GPS", datos['coordenadas'])
    ]

    for label, valor in datos_cliente:
        c.setFont("Helvetica-Bold", 10); c.drawString(60, y, f"{label}:")
        c.setFont("Helvetica", 10); c.drawString(180, y, str(valor))
        y -= 18

    # 3. ESPECIFICACIONES TECNICAS
    y = dibujar_seccion("3. Especificaciones Tecnicas de Central", y - 20)
    
    c.setFont("Helvetica-Bold", 10); c.drawString(60, y, "Modelo de Central:")
    c.setFont("Helvetica", 10); c.drawString(180, y, datos['modelo'])
    y -= 18
    c.setFont("Helvetica-Bold", 10); c.drawString(60, y, "Numero de Serie:")
    c.setFont("Helvetica", 10); c.drawString(180, y, datos['sn'])

    # --- PIE DE P¨¢GINA ---
    c.setStrokeColor(color_linea)
    c.line(50, 50, ancho - 50, 50)
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.gray)
    c.drawString(50, 35, "Este documento es confidencial y para uso exclusivo de GS Control y el cliente titular.")
    c.drawRightString(ancho - 50, 35, "Pagina 1 de 1")

    c.save()
    packet.seek(0)
    return packet

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="GS Control - Generador Pro", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #F8F9F9; }
    .stButton>button { width: 100%; background-color: #1B2631; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("?? Generador de Fichas Profesionales")
st.info("Complete el formulario para generar el PDF con dise?o corporativo.")

with st.form("main_form"):
    col1, col2, col3 = st.columns(3)
    with col1: cod = st.text_input("Cod. Instalador")
    with col2: dgp = st.text_input("D.G.P.")
    with col3: fecha = st.text_input("Fecha")
    
    n_abonado = st.text_input("Numero de Abonado")
    
    st.divider()
    
    nombre = st.text_input("Nombre Titular / Empresa")
    direccion = st.text_input("Direccion")
    
    c_pob, c_prov, c_cp = st.columns([2, 2, 1])
    poblacion = c_pob.text_input("Poblacion")
    provincia = c_prov.text_input("Provincia")
    cp = c_cp.text_input("C.P.")
    
    c_em, c_tp = st.columns(2)
    email = c_em.text_input("Email")
    tipo = c_tp.selectbox("Tipo", ["Vivienda", "Negocio", "Industrial"])
    coordenadas = st.text_input("Coordenadas GPS")
    
    st.divider()
    
    c_sn, c_mod = st.columns(2)
    sn = c_sn.text_input("S/N Panel ID")
    modelo = c_mod.text_input("Modelo Central")
    
    boton = st.form_submit_button("GENERAR DOCUMENTO PROFESIONAL")

if boton:
    datos = {
        "cod_instalador": cod, "dgp": dgp, "fecha": fecha, "n_abonado": n_abonado,
        "nombre": nombre, "direccion": direccion, "poblacion": poblacion,
        "provincia": provincia, "cp": cp, "email": email, "tipo": tipo,
        "coordenadas": coordenadas, "sn": sn, "modelo": modelo
    }
    pdf = generar_pdf_sofisticado(datos)
    st.success("Documento generado con exito.")
    st.download_button("?? Descargar PDF Corporativo", data=pdf, file_name=f"Ficha_GS_{n_abonado}.pdf")