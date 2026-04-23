from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

def crear_capa_texto(datos):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 10)

    # --- CABECERA (Lado derecho superior) ---
    # He subido el valor X a 500 para que escriba bien a la derecha
    can.drawString(500, 785, datos.get("cod_instalador", "")) 
    can.drawString(500, 770, datos.get("dgp", ""))            
    can.drawString(500, 755, datos.get("fecha", ""))          
    
    # Nº ABONADO (Está un poco más abajo)
    can.drawString(510, 725, datos.get("n_abonado", ""))      

    # --- DATOS DE LA INSTALACIÓN ---
    # Ajustamos X para que no tape los títulos "Dirección:", "Población:", etc.
    can.drawString(220, 695, datos.get("nombre_abonado", "")) # Al lado de Empresa/Nombre
    can.drawString(160, 680, datos.get("direccion", ""))      # Al lado de Dirección
    can.drawString(160, 665, datos.get("poblacion", ""))      # Al lado de Población
    can.drawString(360, 665, datos.get("provincia", ""))      # Al lado de Provincia
    can.drawString(500, 665, datos.get("cp", ""))             # Al lado de C.P.
    can.drawString(160, 650, datos.get("email", ""))          # Al lado de E-mail

    # --- DATOS DE CONEXIÓN ---
    can.drawString(160, 595, datos.get("sn_panel", ""))       
    can.drawString(180, 565, datos.get("modelo_central", "")) 

    can.save()
    packet.seek(0)
    return packet

def procesar_ficha():
    archivo_entrada = "FichaTecnica.pdf"
    archivo_salida = "Ficha_Final_Ajustada.pdf"
    
    try:
        reader = PdfReader(archivo_entrada)
        writer = PdfWriter()

        # Datos que quieres insertar
        mis_datos = {
            "cod_instalador": "9999",
            "dgp": "12345",
            "fecha": "23/04/2026",
            "n_abonado": "AB-500",
            "nombre_abonado": "JUAN PEREZ S.L.",
            "direccion": "AVENIDA PRINCIPAL 123",
            "poblacion": "MURCIA",
            "provincia": "MURCIA",
            "cp": "30001",
            "email": "cliente@correo.com",
            "sn_panel": "SN-882211",
            "modelo_central": "PARADOX EVO"
        }

        # Generar capa y fusionar
        capa = crear_capa_texto(mis_datos)
        capa_pdf = PdfReader(capa)
        
        pagina = reader.pages[0]
        pagina.merge_page(capa_pdf.pages[0])
        writer.add_page(pagina)

        # Añadir página 2 sin cambios
        if len(reader.pages) > 1:
            writer.add_page(reader.pages[1])

        with open(archivo_salida, "wb") as f:
            writer.write(f)
        
        print(f"✨ ¡Listo! Revisa '{archivo_salida}'")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    procesar_ficha()