from flask import Flask, request, send_file, jsonify
from pypdf import PdfReader, PdfWriter
import io
import os

app = Flask(__name__)

# Ruta al PDF en blanco (debe estar en el mismo directorio)
PDF_TEMPLATE = os.path.join(os.path.dirname(__file__), "DR_CONVENIO_MODELO_blanco.pdf")

# Mapeo fijo de campos del formulario
FIELD_MAP = {
    # --- PUNTO 4 ---
    "punto4_denominacion": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-3[0].CUERPO[0].apart3[0].s[0].c[0]",
        "page": 2
    },
    "punto4_responsable": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-3[0].CUERPO[0].apart3[0].s[1].c[0]",
        "page": 2
    },
    "punto4_lugar": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-3[0].CUERPO[0].apart3[0].s[2].c[0]",
        "page": 2
    },

    # --- PUNTO 5.2 ---
    "p52_nombre": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].DATOS-PERSONALES[0].BLOQUE[0].NOMBRE[0]",
        "page": 3
    },
    "p52_apellido1": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].DATOS-PERSONALES[0].BLOQUE[0].APELLIDO1[0]",
        "page": 3
    },
    "p52_apellido2": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].DATOS-PERSONALES[0].BLOQUE[0].APELLIDO2[0]",
        "page": 3
    },
    "p52_dni": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].DATOS-PERSONALES[0].BLOQUE[0].DNI-NIE-NIF[0]",
        "page": 3
    },
    "p52_sexo": {
        # "/0" = Hombre, "/1" = Mujer
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].DATOS-PERSONALES[0].BLOQUE[0].SEXO[0].OPCIONES[0].unode[0]",
        "page": 3
    },
    "p52_pais_nacionalidad": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].datos[0].cuerpo-3[0].cue[0].s[0].c[0]",
        "page": 3
    },
    "p52_pais_nacimiento": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].datos[0].cuerpo-3[0].cue[0].s[0].c[1]",
        "page": 3
    },
    "p52_fecha_dia": {
        # Valores válidos: "01" a "31"
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].datos[0].cuerpo-3[0].cue[0].s[0].FECHA-INICIO[0].DIA[0]",
        "page": 3
    },
    "p52_fecha_mes": {
        # Valores válidos: "01" a "12"
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].datos[0].cuerpo-3[0].cue[0].s[0].FECHA-INICIO[0].mes[0]",
        "page": 3
    },
    "p52_fecha_ano": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].datos[0].cuerpo-3[0].cue[0].s[0].FECHA-INICIO[0].ANO[0]",
        "page": 3
    },
    "p52_provincia_nacimiento": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].datos[0].cuerpo-3[0].cue[0].s[1].c[0]",
        "page": 3
    },
    "p52_poblacion_nacimiento": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].datos[0].cuerpo-3[0].cue[0].s[1].c[1]",
        "page": 3
    },
    "p52_nombre_padre": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].datos[0].cuerpo-3[0].cue[0].s[3].c[0]",
        "page": 3
    },
    "p52_nombre_madre": {
        "field_id": "form1[0].ANEXO[0].ANEXO[0].APARTADO-5[0].CUERPO[0].PROFESOR1[0].datos[0].cuerpo-3[0].cue[0].s[4].c[0]",
        "page": 3
    },
}


def fill_pdf(data: dict) -> bytes:
    """Rellena el PDF con los datos recibidos y devuelve los bytes del PDF."""
    reader = PdfReader(PDF_TEMPLATE)
    writer = PdfWriter(clone_from=reader)

    # Agrupar valores por página
    fields_by_page = {}
    for key, value in data.items():
        if key not in FIELD_MAP:
            continue
        field_info = FIELD_MAP[key]
        page = field_info["page"]
        field_id = field_info["field_id"]
        if page not in fields_by_page:
            fields_by_page[page] = {}
        fields_by_page[page][field_id] = value

    # Aplicar valores al PDF
    for page, field_values in fields_by_page.items():
        writer.update_page_form_field_values(
            writer.pages[page - 1],
            field_values,
            auto_regenerate=False
        )

    writer.set_need_appearances_writer(True)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output.read()


@app.route("/fill-pdf", methods=["POST"])
def fill_pdf_endpoint():
    """
    Endpoint principal. Recibe JSON con los datos y devuelve el PDF rellenado.

    Ejemplo de JSON:
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
    """
    if not request.is_json:
        return jsonify({"error": "El body debe ser JSON"}), 400

    data = request.get_json()

    try:
        pdf_bytes = fill_pdf(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="convenio_rellenado.pdf"
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
