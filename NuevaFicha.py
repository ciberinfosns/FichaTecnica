from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def crear_pdf_personalizado(datos, nombre_archivo):
    c = canvas.Canvas(nombre_archivo, pagesize=A4)
    ancho, alto = A4

    # --- ESTILO DE FUENTE ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, alto - 50, "FICHA TÉCNICA DE INSTALACIÓN - GS CONTROL")
    
    # Línea decorativa superior
    c.setStrokeColor(colors.black)
    c.line(50, alto - 60, 540, alto - 60)

    # --- SECCIÓN 1: DATOS DE CABECERA ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, alto - 90, "1. IDENTIFICACIÓN")
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, alto - 110, f"Código Instalador: {datos.get('cod_instalador', '')}")
    c.drawString(250, alto - 110, f"D.G.P.: {datos.get('dgp', '')}")
    c.drawString(400, alto - 110, f"Fecha: {datos.get('fecha', '')}")
    c.drawString(50, alto - 125, f"Nº Abonado: {datos.get('n_abonado', '')}")

    # --- SECCIÓN 2: DATOS DEL CLIENTE ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, alto - 160, "2. DATOS DEL CLIENTE / INSTALACIÓN")
    
    c.setFont("Helvetica-Bold", 10)
    y = alto - 180
    c.drawString(50, y, f"Empresa / Nombre: {datos.get('nombre_abonado', '')}")
    c.drawString(50, y - 20, f"Dirección: {datos.get('direccion', '')}")
    c.drawString(50, y - 40, f"Población: {datos.get('poblacion', '')}")
    c.drawString(250, y - 40, f"Provincia: {datos.get('provincia', '')}")
    c.drawString(450, y - 40, f"C.P.: {datos.get('cp', '')}")
    c.drawString(50, y - 60, f"Email: {datos.get('email', '')}")
    c.drawString(50, y - 80, f"Tipo: {datos.get('tipo', '')}")
    c.drawString(250, y - 80, f"Coordenadas: {datos.get('coordenadas', '')}")

    # --- SECCIÓN 3: EQUIPAMIENTO ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 120, "3. DATOS DE LA CENTRAL")
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y - 140, f"S/N o Panel ID: {datos.get('sn_panel', '')}")
    c.drawString(250, y - 140, f"Modelo Central: {datos.get('modelo_central', '')}")

    # --- SECCIÓN 4: TABLA DE ZONAS (Ejemplo de diseño limpio) ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 180, "4. CONFIGURACIÓN DE ZONAS")
    
    c.setFont("Helvetica-Bold", 9)
    y_zonas = y - 200
    zonas = datos.get("zonas", {})
    
    # Crear dos columnas de zonas
    for i in range(1, 9):
        # Columna 1
        c.drawString(60, y_zonas, f"Z{i}: {zonas.get(f'Z{i}', '__________')}")
        # Columna 2
        c.drawString(300, y_zonas, f"Z{i+8}: {zonas.get(f'Z{i+8}', '__________')}")
        y_zonas -= 15

    # Pie de página
    c.setFont("Helvetica", 8)
    c.drawString(50, 30, "Documento generado automáticamente por Sistema GS Control.")

    c.save()
    print(f"✅ ¡Ficha propia creada: {nombre_archivo}!")

# --- DATOS PARA RELLENAR ---
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
    "tipo": "NEGOCIO",
    "coordenadas": "37.98, -1.13",
    "sn_panel": "SN-882211",
    "modelo_central": "PARADOX EVO",
    "zonas": {"Z1": "ENTRADA", "Z2": "VOL. SALÓN", "Z9": "TECLADO"}
}

crear_pdf_personalizado(mis_datos, "MiNuevaFicha_GS.pdf")