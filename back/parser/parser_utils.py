from pathlib import Path


def parse_file_parameters(filepath: Path):
    discriminator = Path(filepath).name[:2]
    if discriminator == "01":
        # Fichero de CONTROL de los ficheros que componen el proceso electoral.
        widths = (2, 4, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        names = ( "tipo", "anho", "mes", "vuelta", "flag01", "flag02", "flag03", "flag04", "flag05", "flag06", "flag07", "flag08", "flag09", "flag10", "flag011104", "flag1204", "flag0510", "flag0610", "flag0710", "flag0810")  # fmt: skip
        tablename = "control"
    if discriminator == "02":
        # Fichero de IDENTIFICACION del proceso electoral.
        widths = (2, 4, 2, 1, 1, 2, 2, 2, 4, 5, 5, 5, 5)
        names = ( "tipo", "anho", "mes", "vuelta", "tipo_ambito", "ambito", "fecha_dia", "fecha_mes", "fecha_anho", "hora_apertura", "hora_cierre", "hora_primer_avance", "hora_segundo_avance")  # fmt: skip
        tablename = "identificacion"
    if discriminator == "03":
        # Fichero de CANDIDATURAS.
        widths = (2, 4, 2, 6, 50, 150, 6, 6, 6)
        names = ( "tipo", "anho", "mes", "codigo_candidatura", "siglas", "denominacion", "codigo_candidatura_provincial", "codigo_candidatura_autonomico", "codigo_candidatura_nacional")  # fmt: skip
        tablename = "candidaturas"
    if discriminator == "04":
        # Fichero de RELACION DE CANDIDATOS.
        widths = (2, 4, 2, 1, 2, 1, 3, 6, 3, 1, 25, 25, 25, 1, 2, 2, 4, 10, 1)
        names = ( "tipo", "anho", "mes", "vuelta", "ine_provincia", "distrito_electoral", "ine_municipio", "codigo_candidatura", "orden_candidato", "tipo_candidato", "nombre", "primer_apellido", "segundo_apellido", "sexo", "fecha_nac_dia", "fecha_nac_mes", "fecha_nac_anho", "dni", "elegido")  # fmt: skip
        tablename = "candidatos"
    if discriminator == "05":
        widths = (2, 4, 2)
        names = ( "tipo", "anho", "mes", )  # fmt: skip
    if discriminator == "06":
        widths = (2, 4, 2)
        names = ( "tipo", "anho", "mes", )  # fmt: skip
    if discriminator == "07":
        widths = (2, 4, 2)
        names = ( "tipo", "anho", "mes", )  # fmt: skip
    if discriminator == "08":
        widths = (2, 4, 2)
        names = ( "tipo", "anho", "mes", )  # fmt: skip
    if discriminator == "09":
        widths = (2, 4, 2)
        names = ( "tipo", "anho", "mes", )  # fmt: skip
    if discriminator == "10":
        widths = (2, 4, 2)
        names = ( "tipo", "anho", "mes", )  # fmt: skip

    return widths, names, tablename
