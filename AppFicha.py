import streamlit as st
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

def crear_capa_texto(datos):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 10)

    # Coordenadas ajustadas a la derecha según tus pruebas anteriores
    # Cabecera
    can.drawString(500, 785, datos.get("cod_instalador", "")) 
    can.drawString(500, 770, datos.get("dgp", ""))            
    can.drawString(500, 755, datos.get("fecha", ""))          
    can.drawString(510, 725, datos.get("n_abonado", ""))      

    # Datos Instalación
    can.drawString(220, 695, datos.get("nombre_abonado", "")) 
    can.drawString(160, 680, datos.get("direccion", ""))      
    can.drawString(160, 665, datos.get("poblacion", ""))      
    can.drawString(360, 665, datos.get("provincia", ""))      
    can.drawString(500, 665, datos.get("cp", ""))             
    can.drawString(160, 650, datos.get("email", ""))          

    # Conexión
    can.drawString(160, 595, datos.get("sn_panel", ""))       
    can.drawString(180, 565, datos.get("modelo_central", "")) 

    can.save()
    packet.seek(0)
    return packet

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Generador de Fichas GS Control", layout="wide")
st.title("📄 Rellenar Ficha Técnica - GS Control")

with st.form("formulario_pdf"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Datos de Cabecera")
        cod = st.text_input("Código Instalador")
        dgp = st.text_input("D.G.P.")
        fecha = st.text_input("Fecha (DD/MM/AAAA)")
        n_abonado = st.text_input("Nº ABONADO")

    with col2:
        st.subheader("Datos de Instalación")
        nombre = st.text_input("Empresa / Nombre Abonado")
        dir_inst = st.text_input("Dirección")
        pob = st.text_input("Población")
        prov = st.text_input("Provincia")
        cp = st.text_input("C.P.")
        mail = st.text_input("E-mail")

    st.subheader("Datos de Conexión")
    sn = st.text_input("S/N o Panel ID")
    modelo = st.text_input("Modelo y Marca de Central")

    submit = st.form_submit_button("Generar y Descargar PDF")

if submit:
    mis_datos = {
        "cod_instalador": cod, "dgp": dgp, "fecha": fecha, "n_abonado": n_abonado,
        "nombre_abonado": nombre, "direccion": dir_inst, "poblacion": pob,
        "provincia": prov, "cp": cp, "email": mail, "sn_panel": sn, "modelo_central": modelo
    }
    
    # Procesamiento del PDF
    reader = PdfReader("FichaTecnica.pdf")
    writer = PdfWriter()
    
    capa = crear_capa_texto(mis_datos)
    capa_pdf = PdfReader(capa)
    
    pagina = reader.pages[0]
    pagina.merge_page(capa_pdf.pages[0])
    writer.add_page(pagina)
    
    if len(reader.pages) > 1:
        writer.add_page(reader.pages[1])
        
    # Guardar en memoria para descarga inmediata
    output = io.BytesIO()
    writer.write(output)
    
    st.success("✅ PDF generado correctamente")
    st.download_button(
        label="⬇️ Descargar Ficha Rellena",
        data=output.getvalue(),
        file_name=f"Ficha_{n_abonado}.pdf",
        mime="application/pdf"
    )