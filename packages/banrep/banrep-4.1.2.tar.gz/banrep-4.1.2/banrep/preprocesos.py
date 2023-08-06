# coding: utf-8
"""Módulo para funciones de preprocesamiento de texto."""
import re


def filtrar_cortas(texto, chars=0):
    """Filtra líneas en texto de longitud chars o inferior.

    Parameters
    ----------
    texto : str
        Texto que se quiere filtrar.
    chars : int
        Mínimo número de caracteres en una línea de texto.

    Returns
    -------
    str
       Texto filtrado.
    """
    filtrado = ""
    for linea in texto.splitlines():
        if len(linea) > chars:
            filtrado += linea + "\n"

    return filtrado


def eliminar_chars(texto, basura=None):
    """Elimina caracteres en texto.

    Parameters
    ----------
    texto : str
    basura : Iterable
        Caracteres a eliminar.

    Returns
    -------
    str
       Texto sin caracteres.
    """
    if basura:
        texto = re.sub(f"[{''.join(basura)}]", '', texto)

    return texto


def unir_fragmentos(texto):
    """Une fragmentos de palabras partidas por final de línea.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto con palabras de fin de línea unidas si estaban partidas.
    """
    # Asume ord('-') == 45
    nuevo = re.sub(r'-\n+', '', texto)

    return re.sub(r'-(\r\n)+', '', nuevo)


def eliminar_newlines(texto):
    """Elimina caracteres de fin de línea.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto sin caracteres de fin de línea.
    """
    return ' '.join(texto.split())


def separar_guiones(texto):
    """Separa guiones de primera y última palabra de fragmentos de texto.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto con guiones de fragmentos separados de las palabras.
    """
    # Asume ord('–') == 8211
    nuevo = re.sub(r'(\W)–([A-Za-zÀ-Üà-ü]+)', r'\1– \2', texto)

    return re.sub(r'([A-Za-zÀ-Üà-ü]+)–(\W)', r'\1 –\2', nuevo)


def separar_numeros(texto):
    """Separa números de palabras que los tienen.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto con números separados de palabras.
    """
    nuevo = re.sub(r'(\d+)([A-Za-zÀ-Üà-ü]{2,}?|\()', r'\1 \2', texto)

    return re.sub(r'([A-Za-zÀ-Üà-ü]{2,}?|\))(\d+)', r'\1 \2', nuevo)


def limpiar_extraccion(texto, basura=None):
    """Limpieza de texto extraido.

    Parameters
    ----------
    texto : str
    basura : Iterable
        Caracteres a eliminar.

    Returns
    -------
    str
       Texto procesado.
    """
    limpio = eliminar_chars(texto, basura=basura)
    if limpio:
        limpio = unir_fragmentos(limpio)
        limpio = separar_guiones(limpio)
        limpio = separar_numeros(limpio)

    limpio = eliminar_newlines(limpio)

    return limpio
