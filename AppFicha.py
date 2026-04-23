import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io

def generar_pdf_completo(datos):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    ancho, alto = A4

    # --- ESTILO Y ENCABEZADO ---
    color_azul = colors.HexColor("#1B2631")
    c.setFillColor(color_azul)
    c.rect(0, alto - 80, ancho, 80, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, alto - 45, "GS CONTROL - FICHA TECNICA")
    c.setFont("Helvetica", 9)
    c.drawString(50, alto - 60, "CRA - SEGURIDAD MAR MENOR | REV. AGOSTO 2019")

    # --- SECCION 1: IDENTIFICACION ---
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    y = alto - 110
    c.drawString(50, y, "1. IDENTIFICACION DEL RESPONSABLE")
    c.line(50, y-3, 540, y-3)
    
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, f"Cod. Instalador: {datos['cod_inst']}")
    c.drawString(200, y, f"D.G.P.: {datos['dgp']}")
    c.drawString(350, y, f"Fecha: {datos['fecha']}")
    y -= 15
    c.drawString(50, y, f"Empresa Instaladora: {datos['emp_inst']}")
    c.drawString(300, y, f"Tecnico Responsable: {datos['tecnico']}")

    # --- SECCION 2: DATOS DEL ABONADO ---
    y -= 35
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "2. DATOS DE LA INSTALACION / ABONADO")
    c.line(50, y-3, 540, y-3)
    
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, f"No. ABONADO: {datos['n_abonado']}")
    c.drawString(250, y, f"Tipo: {datos['tipo']}")
    y -= 15
    c.drawString(50, y, f"Nombre/Empresa: {datos['nombre']}")
    y -= 15
    c.drawString(50, y, f"Direccion: {datos['dir']}")
    y -= 15
    c.drawString(50, y, f"Poblacion: {datos['pob']}")
    c.drawString(250, y, f"Provincia: {datos['prov']}")
    c.drawString(450, y, f"C.P.: {datos['cp']}")
    y -= 15
    c.drawString(50, y, f"E-mail: {datos['email']}")
    c.drawString(300, y, f"Coordenadas: {datos['gps']}")

    # --- SECCION 3: DATOS TECNICOS Y CONEXION ---
    y -= 35
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "3. DATOS DE LA CENTRAL Y EQUIPO")
    c.line(50, y-3, 540, y-3)
    
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, f"Modelo/Marca: {datos['modelo']}")
    c.drawString(300, y, f"S/N - ID Panel: {datos['sn']}")
    y -= 15
    c.drawString(50, y, f"No. Teclados: {datos['teclados']}")
    c.drawString(180, y, f"No. Sirenas: {datos['sirenas']}")
    c.drawString(310, y, f"No. Detectores: {datos['det']}")
    c.drawString(450, y, f"Fotoverif.: {datos['foto']}")
    y -= 15
    c.drawString(50, y, f"Via Transmision: {datos['via']}")
    c.drawString(300, y, f"IMEI: {datos['imei']}")

    # --- SECCION 4: CONTACTOS ---
    y -= 35
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "4. CONTACTOS Y SERVICIO ACUDA")
    c.line(50, y-3, 540, y-3)
    y -= 20
    c.setFont("Helvetica", 9)
    c.drawString(60, y, "Se notificara en el orden indicado a los telefonos proporcionados.")

    # Pie de pagina
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 30, "Documento digitalizado - GS Control Sistemas de Seguridad")
    
    c.save()
    packet.seek(0)
    return packet

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="GS Control - Editor")
st.title("Generador de Ficha Tecnica")

with st.form("ficha_completa"):
    # Fila 1
    col1, col2, col3 = st.columns(3)
    cod_inst = col1.text_input("Cod. Instalador")
    dgp = col2.text_input("D.G.P.")
    fecha = col3.text_input("Fecha")
    
    # Fila 2
    e_inst = st.text_input("Empresa Instaladora", value="GS CONTROL")
    tecnico = st.text_input("Tecnico Responsable")
    
    st.divider()
    
    # Fila 3: Abonado
    n_abonado = st.text_input("No. Abonado (Ej: AB-500)")
    nombre = st.text_input("Nombre Abonado / Empresa")
    dir_inst = st.text_input("Direccion de la Instalacion")
    
    c_p, c_pr, c_cp = st.columns([2,2,1])
    pob = c_p.text_input("Poblacion")
    prov = c_pr.text_input("Provincia")
    cp = c_cp.text_input("C.P.")
    
    c_em, c_gps, c_ti = st.columns(3)
    email = c_em.text_input("E-mail")
    gps = c_gps.text_input("Coordenadas")
    tipo = c_ti.selectbox("Tipo", ["Vivienda", "Negocio"])
    
    st.divider()
    
    # Fila 4: Tecnico
    c_mo, c_sn = st.columns(2)
    modelo = c_mo.text_input("Modelo y Marca Central")
    sn = c_sn.text_input("S/N o Panel ID")
    
    c_t, c_s, c_d, c_f = st.columns(4)
    teclados = c_t.text_input("No. Teclados")
    sirenas = c_s.text_input("No. Sirenas")
    det = c_d.text_input("No. Detectores")
    foto = c_f.text_input("Fotoverific.")
    
    c_via, c_im = st.columns(2)
    via = st.selectbox("Via Transmision CRA", ["GPRS/GSM", "IP/Network", "RTC/RTB", "Radio"])
    imei = st.text_input("IMEI / No. SIM")

    boton = st.form_submit_button("GENERAR PDF CON TODOS LOS CAMPOS")

if boton:
    # Recopilar todos los datos
    res = {
        "cod_inst": cod_inst, "dgp": dgp, "fecha": fecha, "emp_inst": e_inst,
        "tecnico": tecnico, "n_abonado": n_abonado, "nombre": nombre,
        "dir": dir_inst, "pob": pob, "prov": prov, "cp": cp, "email": email,
        "gps": gps, "tipo": tipo, "modelo": modelo, "sn": sn,
        "teclados": teclados, "sirenas": sirenas, "det": det, "foto": foto,
        "via": via, "imei": imei
    }
    pdf_file = generar_pdf_completo(res)
    st.success("PDF generado exitosamente.")
    st.download_button("Descargar Ficha Completa", data=pdf_file, file_name=f"Ficha_{n_abonado}.pdf")