import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io

# Funcion para generar el PDF
def generar_pdf_sofisticado(datos):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    ancho, alto = A4

    # Colores y estilo
    color_principal = colors.HexColor("#1B2631")
    
    # Encabezado
    c.setFillColor(color_principal)
    c.rect(0, alto - 80, ancho, 80, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, alto - 50, "GS CONTROL")
    c.setFont("Helvetica", 10)
    c.drawString(50, alto - 65, "SISTEMAS DE SEGURIDAD")

    # Cuerpo
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    y = alto - 120
    c.drawString(50, y, "DATOS DEL ABONADO")
    c.line(50, y-5, ancho-50, y-5)
    
    y -= 30
    c.setFont("Helvetica", 10)
    campos = [
        ("Nombre", datos['nombre']),
        ("Direccion", datos['direccion']),
        ("Poblacion", datos['poblacion']),
        ("Email", datos['email']),
        ("No. Abonado", datos['n_abonado'])
    ]
    
    for label, valor in campos:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, f"{label}:")
        c.setFont("Helvetica", 10)
        c.drawString(180, y, str(valor))
        y -= 20

    c.save()
    packet.seek(0)
    return packet

# Interfaz de Usuario
st.title("Generador de Fichas GS")

with st.form("formulario"):
    nombre = st.text_input("Nombre / Empresa")
    direccion = st.text_input("Direccion")
    poblacion = st.text_input("Poblacion")
    email = st.text_input("Email")
    n_abonado = st.text_input("Numero de Abonado")
    
    boton = st.form_submit_button("CREAR PDF")

if boton:
    datos = {
        "nombre": nombre, "direccion": direccion, 
        "poblacion": poblacion, "email": email, "n_abonado": n_abonado
    }
    pdf = generar_pdf_sofisticado(datos)
    st.success("Documento listo")
    st.download_button("Descargar", data=pdf, file_name="Ficha.pdf")