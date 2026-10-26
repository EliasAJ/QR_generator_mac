import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode

def generar_y_guardar():
    enlace = entrada_url.get().strip()
    
    # 1. Validación de seguridad: Evitar generar QR vacíos
    if not enlace:
        messagebox.showwarning("Introduce un enlace válido.")
        return
    
    # 2. Corrección automática de protocolo para evitar la "trampa del texto plano"
    if not enlace.startswith("http://") and not enlace.startswith("https://"):
        enlace = "https://" + enlace
    
    # 3. Configuración blindada: Nivel de corrección H (30% de tolerancia al daño)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # <-- Protección máxima
        box_size=10,
        border=4
    )
    
    qr.add_data(enlace)
    qr.make(fit=True)
    
    # 4. Generación de la imagen en alta calidad
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 5. Ventana nativa de macOS para elegir dónde guardar
    ruta = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Imagen PNG", "*.png")],
        title="Guardar como..."
    )
    
    if ruta:
        img.save(ruta)
        messagebox.showinfo(
            "", 
            "Tu código QR fue generado y guardado correctamente."
        )

# --- Configuración de la interfaz gráfica (Ventana principal) ---
ventana = tk.Tk()
ventana.title("Generador de Códigos QR")
ventana.resizable(False, False)

# --- LÓGICA PARA CENTRAR LA VENTANA EN LA PANTALLA ---
ancho_ventana = 440
alto_ventana = 190

# Obtener las dimensiones totales de la pantalla de tu Mac
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calcular las coordenadas X e Y exactas para el centro
pos_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
pos_y = int((alto_pantalla / 2) - (alto_ventana / 2))

# Aplicar geometría: "anchoxalto+X+Y"
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
# ------------------------------------------------------

# Elementos de la interfaz
tk.Label(
    ventana, 
    text="Introduce o pega el enlace de tu web:", 
    font=("Arial", 12)
).pack(pady=(15, 5))

entrada_url = tk.Entry(ventana, width=42, font=("Arial", 11))
entrada_url.pack(pady=5)
entrada_url.focus()

boton_generar = tk.Button(
    ventana, 
    text="Generar y Guardar QR", 
    command=generar_y_guardar, 
    font=("Arial", 11, "bold")
)
boton_generar.pack(pady=15)

# Bucle principal para mantener la aplicación en ejecución
ventana.mainloop()