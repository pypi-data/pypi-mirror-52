# coding: utf-8
"""Módulo para crear modelos de transformación de texto."""
import warnings

from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel
import pandas as pd


class Ldas:
    """Modelos LDA de tópicos."""

    def __init__(self, bow, kas, params, medida="c_v"):
        """Inicializa clase.

        Parameters
        ----------
        bow : banrep.corpus.Bow
            Corpus previamente inicializado con documentos.
        kas: list (int)
            Diferentes k tópicos para los cuales crear modelo.
        params: dict
            Parámetros requeridos en modelos LDA.
        medida : str
            Medida de Coherencia a usar (u_mass, c_v, c_uci, c_npmi).
        """
        self.bow = bow
        self.kas = kas
        self.params = params
        self.medida = medida

        self.modelos = sorted(
            [lda for lda in self.modelar()], key=lambda x: x.get("score"), reverse=True
        )

    def __repr__(self):
        best = self.modelos[0]
        fmstr = f"Mejor k={best.get('k')} con Score={best.get('score'):.3f}"
        return f"Modelos LDA para k en {self.kas}: {fmstr}"

    def __iter__(self):
        """Iterar devuelve cada modelo en orden de kas."""
        yield from self.modelos

    def crear_modelo(self, k):
        """Crea modelo LDA de k tópicos.

        Returns
        -------
        gensim.models.ldamodel.LdaModel
            Modelo LDA de k tópicos.
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            modelo = LdaModel(
                self.bow, num_topics=k, id2word=self.bow.id2word, **self.params
            )

        return modelo

    def evaluar_modelo(self, modelo, textos):
        """Calcula Coherence Score de modelo de tópicos.

        Parameters
        ----------
        modelo : gensim.models.ldamodel.LdaModel
        textos : Iterable (list[str])
            Palabras de cada documento en un corpus.

        Returns
        -------
        float
            Coherencia calculada.
        """
        cm = CoherenceModel(
            model=modelo,
            texts=textos,
            dictionary=self.bow.id2word,
            coherence=self.medida,
        )

        return cm.get_coherence()

    def modelar(self):
        """Crea y evalua modelos LDA para diferente número de tópicos.

        Yields
        ------
        dict (k:int, modelo: gensim.models.ldamodel.LdaModel, score: float)
        """
        textos = [palabras for palabras in self.bow.obtener_palabras()]
        for k in self.kas:
            modelo = self.crear_modelo(k)
            score = self.evaluar_modelo(modelo, textos)

            yield dict(k=k, modelo=modelo, score=score)


class Topicos:
    """Topicos resultantes de modelo LDA"""

    def __init__(self, modelo, bow):
        """Inicialización de instancias.

        Parameters
        ----------
        modelo : gensim.models.ldamodel.LdaModel
        bow : banrep.corpus.Bow
            Corpus bow previamente inicializado con documentos.
        """
        self.modelo = modelo
        self.bow = bow

        self.dfm = self.doc_topico()

    def doc_topico(self):
        """Distribución de probabilidad de tópicos en cada documento.

        Returns
        -------
        pd.DataFrame
            Distribución de probabilidad de tópicos x documento.
        """
        data = (dict(doc) for doc in self.modelo[self.bow])
        index = [doc._.get("doc_id") for doc in self.bow.docs]

        return pd.DataFrame(data=data, index=index)

    def prevalencia(self):
        """Prevalencia de cada tópico en corpus.

        Returns
        -------
        pd.DataFrame
            Prevalencia de tópicos.
        """
        dom = self.dfm.idxmax(axis=1).value_counts(normalize=True)
        dom.index.name = "topico"

        return dom.to_frame(name='domina').reset_index()

    def palabras_probables(self, n=15):
        """Distribución de probabilidad de palabras en tópicos.

        Parameters
        ----------
        n : int
            Cuantas palabras obtener.

        Returns
        -------
        pd.DataFrame
            Palabras probables de cada tópico y sus probabilidades.
        """
        dfs = []
        for topico in range(self.modelo.num_topics):
            data = self.modelo.show_topic(topico, n)
            df = pd.DataFrame(data=data, columns=["palabra", "probabilidad"])
            df = df.sort_values(by="probabilidad", ascending=False)
            df["topico"] = topico
            dfs.append(df)

        return pd.concat(dfs, ignore_index=True)

    def distancia(self, anno=True):
        """Distancia entre tópicos del modelo.

        Parameters
        ----------
        anno : bool
            Cuantas palabras obtener.
        """
        diff, annos = self.modelo.diff(
            self.modelo, distance="hellinger", annotation=anno
        )

        return diff, annos
