# API Relleno de PDF - Convenio Formación en Prácticas

## Archivos necesarios
- `app.py` — el servidor
- `requirements.txt` — dependencias
- `DR_CONVENIO_MODELO_blanco.pdf` — el PDF en blanco (debe estar en la misma carpeta)

## Despliegue en Render.com (gratis)

1. Sube estos 3 archivos a un repositorio de GitHub
2. Ve a https://render.com y crea una cuenta gratuita
3. Nuevo servicio → "Web Service" → conecta tu repositorio
4. Configura:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free
5. Render te dará una URL tipo: `https://tu-app.onrender.com`

## Uso desde Base44

Haz una llamada POST a:
`https://tu-app.onrender.com/fill-pdf`

Con este JSON en el body:

```json
{
    "punto4_denominacion": "GRUPO SCOUT SAN JOSÉ AXARQUÍA (VÉLEZ MÁLAGA)",
    "punto4_responsable": "Rosa María Díaz Verdejo  52585402L",
    "punto4_lugar": "C/. Camino de Algarrobo 38",
    "p52_nombre": "ROSA MARÍA",
    "p52_apellido1": "MARTÍN",
    "p52_apellido2": "VERDEJO",
    "p52_dni": "52585402L",
    "p52_sexo": "/1",
    "p52_pais_nacionalidad": "ESPAÑA",
    "p52_pais_nacimiento": "ESPAÑA",
    "p52_fecha_dia": "20",
    "p52_fecha_mes": "05",
    "p52_fecha_ano": "1973",
    "p52_provincia_nacimiento": "MÁLAGA",
    "p52_poblacion_nacimiento": "VÉLEZ MÁLAGA",
    "p52_nombre_padre": "JOSE ESTEBAN",
    "p52_nombre_madre": "ROSA"
}
```

La respuesta es directamente el archivo PDF rellenado.

## Notas
- `p52_sexo`: "/1" = Mujer, "/0" = Hombre
- `p52_fecha_dia` y `p52_fecha_mes`: siempre con 2 dígitos ("01", "09", etc.)
- Solo se rellenan los campos que envíes; el resto queda en blanco
