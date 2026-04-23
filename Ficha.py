from pypdf import PdfReader

def listar_campos(ruta_pdf):
    try:
        reader = PdfReader(ruta_pdf)
        campos = reader.get_fields()
        
        if not campos:
            print("\n❌ No se encontraron campos interactivos.")
            print("Esto significa que el PDF es 'plano'. Tendremos que usar el metodo de coordenadas (x, y).")
            return

        print(f"\n{'NOMBRE DEL CAMPO':<30} | {'TIPO':<15}")
        print("-" * 50)
        for nombre, info in campos.items():
            # El tipo /FT nos dice si es texto, checkbox, etc.
            tipo = info.get('/FT', 'Desconocido')
            print(f"{nombre:<30} | {tipo:<15}")
            
    except Exception as e:
        print(f"❌ Error al abrir el archivo: {e}")

# Aquí es donde se pone el nombre de tu archivo entre comillas
listar_campos("FichaTecnica.pdf")