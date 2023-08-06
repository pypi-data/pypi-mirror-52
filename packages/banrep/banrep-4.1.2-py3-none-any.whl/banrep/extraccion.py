# coding: utf-8
"""Modulo para extraer texto de archivos binarios."""
from pathlib import Path
import json

from tika import parser
import bs4

from banrep.io import guardar_texto
from banrep.preprocesos import filtrar_cortas, limpiar_extraccion
from banrep.utils import crear_directorio, iterar_rutas


def extraer_info(archivo):
    """Extrae contenido y metadata de archivo.

    Parameters
    -------------
    archivo : str | Path
        Ruta del archivo del cual se quiere extraer texto y metadata.

    Returns
    ---------
    tuple (str, dict)
        Content y Metadata.
    """
    ruta = Path(archivo).resolve()

    if ruta.is_file():
        try:
            info = parser.from_file(str(ruta), xmlContent=True)

        except Exception:
            print(f"No pudo extraerse información de {ruta.name}.")
            info = dict()
    else:
        print(f"{ruta.name} no es un archivo.")
        info = dict()

    content = info.get("content")
    metadata = info.get("metadata")

    return content, metadata


def procesar_xhtml(content, basura=None, chars=0):
    """Procesa texto contenido en xhmtl.

    Parameters
    ----------
    content : str
        xhtml que contiene texto.
    basura : Iterable
        Caracteres a eliminar.
    chars : int
        Mínimo número de caracteres en una línea de texto.

    Returns
    -------
    str
        Texto procesado.
    """
    parsed = ""
    sopa = bs4.BeautifulSoup(content, "lxml")

    for p in sopa.find_all("p"):
        texto = p.get_text(strip=True)
        texto = limpiar_extraccion(texto, basura=basura)
        if texto:
            parsed += texto + "\n"

    if parsed:
        parsed = filtrar_cortas(parsed, chars=chars)

    return parsed


def extraer_todos(dirin, dirout, recursivo=False, exts=None, basura=None, chars=0):
    """Extrae y guarda texto y metadata de archivos.

    Parameters
    -------------
    dirin : str | Path
        Directorio donde están los documentos originales.
    dirout : str | Path
        Directorio donde se quiere guardar texto extraído.
    recursivo: bool
        Iterar recursivamente.
    exts: Iterable
        Solo considerar archivos con estas extensiones.
    basura : Iterable
        Caracteres a eliminar.
    chars : int
        Mínimo número de caracteres en una línea de texto.

    Returns
    ---------
    int
        Número de documentos procesados.
    """
    dirdocs = Path(dirin).resolve()
    dirtextos = Path(dirout).resolve()
    dirmeta = crear_directorio(dirtextos.joinpath("metadata"))

    nparts = len(dirdocs.parts)

    n = 0
    for ruta in iterar_rutas(dirdocs, recursivo=recursivo, exts=exts):
        partes = ruta.parent.parts[nparts:]
        dirtexto = dirtextos.joinpath(*partes)
        if not dirtexto.exists():
            dirtexto = crear_directorio(dirtexto)

        archivo = dirtexto.joinpath(f"{ruta.stem}.txt")
        if not archivo.exists():
            content, metadata = extraer_info(ruta)
            texto = procesar_xhtml(content, basura=basura, chars=chars)
            if texto:
                guardar_texto(texto, archivo)

                metaout = dirmeta.joinpath(*partes)
                if not metaout.exists():
                    metaout = crear_directorio(metaout)

                metafile = metaout.joinpath(f"{ruta.stem}.json")
                with open(metafile, "w", encoding="utf-8") as out:
                    json.dump(metadata, out, ensure_ascii=False)
                n += 1

    return n


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="""Extrae y guarda texto y metadata de archivos."""
    )

    parser.add_argument("dirin", help="Directorio de archivos originales.")
    parser.add_argument("dirout", help="Directorio para almacenar texto extraido.")
    parser.add_argument(
        "--recursivo",
        default=False,
        action="store_true",
        help="Visitar subdirectorios si se incluye. (%(default)s) Ej: --recursivo",
    )
    parser.add_argument(
        "--exts",
        action="append",
        required=False,
        help="Extraer solo de este tipo de archivo. Ej: --exts pdf --exts docx",
    )
    parser.add_argument(
        "--basura",
        action="append",
        help="Eliminar estos caracteres. Ej: --basura '<>!#' --basura � ",
    )
    parser.add_argument(
        "--chars",
        default=0,
        type=int,
        help="Eliminar texto con pocos caracteres. (%(default)s). Ej: --chars 10",
    )

    args = parser.parse_args()

    dirin = args.dirin
    dirout = Path(args.dirout).resolve()
    recursivo = args.recursivo
    exts = args.exts
    basura = args.basura
    chars = args.chars

    n = extraer_todos(
        dirin, dirout, recursivo=recursivo, exts=exts, basura=basura, chars=chars
    )
    print(f"{n} nuevos archivos guardados en directorio {str(dirout)}")


if __name__ == "__main__":
    main()
