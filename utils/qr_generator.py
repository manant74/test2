"""
QR Code Generator - VibeTheForce
Genera QR codes con colori Star Wars per condivisione URL
"""
import qrcode
from io import BytesIO
from typing import Optional


def generate_qr_code(
    url: str,
    fill_color: str = "#FFE81F",
    back_color: str = "#000428",
    box_size: int = 10,
    border: int = 4
) -> BytesIO:
    """
    Genera un QR code con colori Star Wars
    
    Args:
        url: URL da codificare nel QR code
        fill_color: Colore di riempimento (default: giallo Jedi #FFE81F)
        back_color: Colore di sfondo (default: nero spazio #000428)
        box_size: Dimensione di ogni box del QR code (default: 10)
        border: Dimensione del bordo in boxes (default: 4)
    
    Returns:
        BytesIO buffer contenente l'immagine PNG del QR code
    
    Requisiti: 4.1, 4.2
    """
    # Crea oggetto QR Code
    qr = qrcode.QRCode(
        version=1,  # Controlla dimensione (1 è la più piccola)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # ~7% error correction
        box_size=box_size,
        border=border,
    )
    
    # Aggiungi dati
    qr.add_data(url)
    qr.make(fit=True)
    
    # Crea immagine con colori Star Wars
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Salva in buffer
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return buf


def generate_qr_code_with_logo(
    url: str,
    logo_path: Optional[str] = None,
    fill_color: str = "#FFE81F",
    back_color: str = "#000428"
) -> BytesIO:
    """
    Genera un QR code con logo centrale (opzionale)
    
    Args:
        url: URL da codificare
        logo_path: Percorso al logo da inserire al centro (opzionale)
        fill_color: Colore di riempimento
        back_color: Colore di sfondo
    
    Returns:
        BytesIO buffer contenente l'immagine PNG
    """
    from PIL import Image
    
    # Genera QR code base
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction per logo
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')
    
    # Aggiungi logo se fornito
    if logo_path:
        try:
            logo = Image.open(logo_path)
            
            # Calcola dimensioni logo (max 20% del QR code)
            qr_width, qr_height = img.size
            logo_size = min(qr_width, qr_height) // 5
            
            # Ridimensiona logo
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Calcola posizione centrale
            logo_pos = (
                (qr_width - logo_size) // 2,
                (qr_height - logo_size) // 2
            )
            
            # Incolla logo
            img.paste(logo, logo_pos)
            
        except Exception as e:
            # Se c'è un errore con il logo, continua senza
            print(f"Errore nel caricamento logo: {e}")
    
    # Salva in buffer
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return buf


# Preset colori Star Wars per QR codes
STAR_WARS_QR_PRESETS = {
    'jedi': {
        'fill_color': '#FFE81F',  # Giallo Jedi
        'back_color': '#000428'   # Nero spazio
    },
    'sith': {
        'fill_color': '#FF0000',  # Rosso Sith
        'back_color': '#000000'   # Nero puro
    },
    'empire': {
        'fill_color': '#000000',  # Nero
        'back_color': '#FFFFFF'   # Bianco
    },
    'rebel': {
        'fill_color': '#FF6B35',  # Arancione ribelle
        'back_color': '#004E89'   # Blu
    }
}


def generate_themed_qr_code(url: str, theme: str = 'jedi') -> BytesIO:
    """
    Genera QR code con preset di colori Star Wars
    
    Args:
        url: URL da codificare
        theme: Tema colori ('jedi', 'sith', 'empire', 'rebel')
    
    Returns:
        BytesIO buffer contenente l'immagine PNG
    """
    preset = STAR_WARS_QR_PRESETS.get(theme, STAR_WARS_QR_PRESETS['jedi'])
    
    return generate_qr_code(
        url=url,
        fill_color=preset['fill_color'],
        back_color=preset['back_color']
    )
