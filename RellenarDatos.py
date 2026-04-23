from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

def crear_capa_texto(datos):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # CAMBIO AQUÍ: Usamos 'Helvetica-Bold' para que la letra sea más oscura
    # También puedes subir el tamaño de 10 a 11 si quieres que resalte más
    can.setFont("Helvetica-Bold", 10)
    
    # Para que sea EXTREMADAMENTE oscura, podemos usar un color negro puro
    can.setFillColorRGB(0, 0, 0) 

    # --- CABECERA ---
    can.drawString(500, 785, datos.get("cod_instalador", "")) 
    can.drawString(500, 770, datos.get("dgp", ""))            
    can.drawString(500, 755, datos.get("fecha", ""))          
    can.drawString(510, 725, datos.get("n_abonado", ""))      

    # --- DATOS DE LA INSTALACIÓN ---
    can.drawString(220, 695, datos.get("nombre_abonado", "")) 
    can.drawString(160, 680, datos.get("direccion", ""))      
    can.drawString(160, 665, datos.get("poblacion", ""))      
    can.drawString(360, 665, datos.get("provincia", ""))      
    can.drawString(500, 665, datos.get("cp", ""))             
    can.drawString(160, 650, datos.get("email", ""))          

    # --- DATOS DE CONEXIÓN ---
    can.drawString(160, 595, datos.get("sn_panel", ""))       
    can.drawString(180, 565, datos.get("modelo_central", "")) 

    # --- CONTACTOS ---
    y_contacto = 445
    contactos = datos.get("contactos", [])
    for i, contacto in enumerate(contactos[:5]):
        can.drawString(85, y_contacto - (i * 18), contacto.get("nombre", ""))
        can.drawString(450, y_contacto - (i * 18), contacto.get("telefono", ""))

    # --- ZONAS ---
    # Columna Izquierda
    y_zona = 318
    zonas = datos.get("zonas", {})
    for i in range(1, 9):
        can.drawString(85, y_zona, zonas.get(f"Z{i}", ""))
        y_zona -= 14.5

    # Columna Derecha
    y_zona = 318
    for i in range(9, 17):
        can.drawString(365, y_zona, zonas.get(f"Z{i}", ""))
        y_zona -= 14.5

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