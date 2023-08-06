# coding: utf-8
"""Módulo para procesar documentos y crear corpus."""

from gensim.corpora import Dictionary
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Span, Token
import pandas as pd


class Documentos:
    """Colección de documentos spaCy procesados."""

    def __init__(self, lang, datos, tk=0, filtros=None, grupos=None, entes=None):
        """Define parámetros de inicio.

        Parameters
        ----------
        lang : spacy.language.Language
            Modelo de lenguaje spaCy.
        datos : Iterable (str, dict)
            Información de cada documento (texto, metadata).
        tk : int, optional
            Filtro para número mínimo de tokens en frases.
        filtros : dict, optional
            Filtros a evaluar en cada token.
        grupos : dict (str: set)
            Grupos de listas de palabras a identificar.
        entes : dict (str: set)
            Grupos de expresiones a considerar como entidades.
        """
        self.lang = lang
        self.datos = datos
        self.tk = tk
        self.filtros = filtros
        self.grupos = grupos
        self.entes = entes

        self.exts_doc = []
        self.exts_span = ["ok_span"]
        self.exts_token = ["ok_token"]

        if self.grupos:
            for grupo in self.grupos:
                self.exts_token.append(grupo)

        self.fijar_extensiones()
        self.fijar_pipes()

        self.docs = [doc for doc in self.crear_docs(datos)]

    def __len__(self):
        return len(self.docs)

    def __repr__(self):
        return f"{self.__len__()} documentos procesados."

    def __iter__(self):
        """Itera documentos procesados."""
        yield from self.docs

    @staticmethod
    def token_cumple(token, filtros=None):
        """Determina si token pasa los filtros.

        Parameters
        ----------
        token : spacy.tokens.Token
            Token a evaluar.
        filtros : dict, optional
            (is_alpha, stopwords, postags, entities, chars)

        Returns
        -------
        bool
            Si token pasa los filtros o no.
        """
        if not filtros:
            return True

        stopwords = filtros.get("stopwords")
        postags = filtros.get("postags")
        entities = filtros.get("entities")
        chars = filtros.get("chars", 0)

        cumple = True if not filtros.get("is_alpha") else token.is_alpha
        if cumple:
            cumple = len(token) > chars
        if cumple:
            cumple = True if not stopwords else token.lower_ not in stopwords
        if cumple:
            cumple = True if not postags else token.pos_ not in postags
        if cumple:
            cumple = True if not entities else token.ent_type_ not in entities

        return cumple

    def fijar_extensiones(self):
        """Fija extensiones globalmente."""
        if not Span.has_extension("ok_span"):
            Span.set_extension("ok_span", getter=lambda x: len(x) > self.tk)

        if not Token.has_extension("ok_token"):
            Token.set_extension("ok_token", default=True)

        if self.grupos:
            for grupo in self.grupos:
                if not Token.has_extension(grupo):
                    Token.set_extension(grupo, default=False)

    def fijar_pipes(self):
        """Fija componentes adicionales del Pipeline de procesamiento."""
        if not self.lang.has_pipe("evaluar_tokens"):
            self.lang.add_pipe(self.evaluar_tokens, name="evaluar_tokens", last=True)

        if self.grupos:
            if not self.lang.has_pipe("tokens_presentes"):
                self.lang.add_pipe(
                    self.tokens_presentes, name="tokens_presentes", last=True
                )

        if self.entes:
            if not self.lang.has_pipe("entes"):
                patterns = [
                    {"label": k, "pattern": v}
                    for k in self.entes
                    for v in self.entes.get(k)
                ]

                ruler = EntityRuler(self.lang, phrase_matcher_attr="LOWER")
                ruler.add_patterns(patterns)

                self.lang.add_pipe(ruler, name="entes", before="ner")

    def evaluar_tokens(self, doc):
        """Cambia valores durante componente evaluar_tokens si falla filtros.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        doc : spacy.tokens.Doc
        """
        for token in doc:
            if not self.token_cumple(token, filtros=self.filtros):
                token._.set("ok_token", False)

        return doc

    def tokens_presentes(self, doc):
        """Cambia valores durante componente tokens_presentes si en grupos.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        spacy.tokens.Doc
        """
        for grupo in self.grupos:
            palabras = self.grupos.get(grupo)
            for token in doc:
                if token.lower_ in palabras:
                    token._.set(grupo, True)

        return doc

    def crear_docs(self, datos):
        """Crea documentos spaCy a partir de textos y su metadata.

        Parameters
        ----------
        datos : Iterable[Tuple(str, dict)]
            Texto y Metadata de cada documento.

        Yields
        ------
        spacy.tokens.Doc
        """
        for doc, meta in self.lang.pipe(datos, as_tuples=True):
            for ext in meta.keys():
                if ext not in self.exts_doc:
                        self.exts_doc.append(ext)

                if not Doc.has_extension(ext):
                    Doc.set_extension(ext, default=None)

                if meta.get(ext):
                    doc._.set(ext, meta.get(ext))

            yield doc

    def df_docs(self, texto=False):
        """Estadísticas de los Documentos.

        Returns
        -------
        pd.DataFrame
            Estadísticas de cada documento.
        """
        cols = self.exts_doc + self.exts_span + self.exts_token
        if self.entes:
            tipos = list(self.entes.keys())
            cols = cols + tipos
        if texto:
            cols = cols + ["texto"]

        data = []
        for doc in self.docs:
            fila = [doc._.get(ext) for ext in self.exts_doc]
            for ext in self.exts_span:
                fila.append(sum(sent._.get(ext) for sent in doc.sents))
            for ext in self.exts_token:
                fila.append(sum(tok._.get(ext) for tok in doc))

            if self.entes:
                for tipo in tipos:
                    fila.append(sum((ent.label_ == tipo for ent in doc.ents)))

            if texto:
                fila.append(doc.text)

            data.append(fila)

        return pd.DataFrame(data=data, columns=cols)

    def df_tokens(self):
        """Tokens de los Documentos.

        Returns
        -------
        pd.DataFrame
            Estadisticas de cada token.
        """
        cols = ["doc_id", "sent_id", "tok_id", "word", "pos"]
        columnas = cols + self.exts_token

        items = []
        for doc in self.docs:
            sent_id = 1
            for sent in doc.sents:
                if sent._.get("ok_span"):
                    tok_id = 1
                    tokens = [tok for tok in sent if tok._.get("ok_token")]

                    for tok in tokens:
                        fila = [
                            doc._.get("doc_id"),
                            sent_id,
                            tok_id,
                            tok.lower_,
                            tok.pos_,
                        ]
                        for ext in self.exts_token:
                            fila.append(tok._.get(ext))
                        tok_id += 1

                        items.append(fila)

                    sent_id += 1

        return pd.DataFrame(items, columns=columnas)

    def df_frases(self):
        """Frases de Documentos.

        Returns
        -------
        pd.DataFrame
            Estadísticas de cada frase.
        """
        cols = ["doc_id", "sent_id", "frase"]
        columnas = cols + self.exts_span + self.exts_token
        if self.entes:
            tipos = list(self.entes.keys())
            columnas = columnas + tipos

        items = []
        for doc in self.docs:
            sent_id = 1
            for sent in doc.sents:
                fila = [doc._.get("doc_id"), sent_id, sent.text]
                for ext in self.exts_span:
                    fila.append(sent._.get(ext))
                for ext in self.exts_token:
                    fila.append(sum(tok._.get(ext) for tok in sent))

                if self.entes:
                    for tipo in tipos:
                        fila.append(sum((ent.label_ == tipo for ent in sent.ents)))

                items.append(fila)
                sent_id += 1

        return pd.DataFrame(items, columns=columnas)


class Bow:
    """Colección de documentos BOW."""

    def __init__(self, docs, ngrams=None, id2word=None, no_above=0.75):
        """Define parámetros.

        Parameters
        ----------
        docs : banrep.corpus.Documentos
            Documentos spacy.token.Doc ya procesados.
        ngrams : dict, optional (str: gensim.models.phrases.Phraser)
            Modelos de n-gramas (bigrams, trigrams).
        id2word : gensim.corpora.Dictionary, optional
            Diccionario de tokens a considerar.
        no_above : float, optional
            Mantener tokens que no estén en más de esta fracción de docs.
        """
        self.docs = docs
        self.ngrams = ngrams
        self.id2word = id2word
        self.no_above = no_above

        if not self.ngrams:
            self.ngrams = self.model_ngrams()
            print("Modelo de n-gramas ha sido creado...")

        if not self.id2word:
            self.id2word = self.crear_id2word()
            print(f"Diccionario con {len(self.id2word)} términos creado...")

    def __repr__(self):
        return f"Corpus: {self.__len__()} docs y {len(self.id2word)} términos."

    def __len__(self):
        return len(self.docs)

    def __iter__(self):
        """Palabras de cada documento como BOW."""
        for palabras in self.obtener_palabras():
            yield self.id2word.doc2bow(palabras)

    @staticmethod
    def frases_doc(doc):
        """Desagrega documento en frases compuestas por palabras que cumplen.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        list[list(spacy.tokens.Token)]
            Palabras de cada frase en documento.
        """
        frases = []
        for sent in doc.sents:
            if sent._.get("ok_span"):
                tokens = [tok for tok in sent if tok._.get("ok_token")]
                frases.append(tokens)

        return frases

    def iterar_frases(self):
        """Itera todas las frases del corpus.

        Yields
        ------
        Iterable[list(str)]
            Palabras de una frase.
        """
        for doc in self.docs:
            for frase in self.frases_doc(doc):
                yield [tok.lower_ for tok in frase]

    def model_ngrams(self):
        """Crea modelos de ngramas a partir de frases.

        Returns
        -------
        dict
            Modelos Phraser para bigramas y trigramas
        """
        mc = 20
        big = Phrases(self.iterar_frases(), min_count=mc)
        bigrams = Phraser(big)

        trig = Phrases(bigrams[self.iterar_frases()], min_count=mc)
        trigrams = Phraser(trig)

        return dict(bigrams=bigrams, trigrams=trigrams)

    def ngram_frases(self, doc):
        """Frases palabras de un documento, ya con ngramas.

        Parameters
        ----------
        doc : spacy.tokens.Doc

        Returns
        -------
        list[list(str)]
        """
        bigrams = self.ngrams.get("bigrams")
        trigrams = self.ngrams.get("trigrams")

        doc_ = self.frases_doc(doc)
        frases = []
        for frase in doc_:
            frases.append(list(trigrams[bigrams[[t.lower_ for t in frase]]]))

        return frases

    def obtener_palabras(self):
        """Palabras de cada documento, ya con ngramas.

        Yields
        ------
        Iterable[list(str)]
            Palabras de un documento.
        """
        for doc in self.docs:
            frases = self.ngram_frases(doc)
            palabras = [token for frase in frases for token in frase]

            yield palabras

    def crear_id2word(self):
        """Crea diccionario de todas las palabras procesadas del corpus.

        Returns
        -------
        gensim.corpora.dictionary.Dictionary
            Diccionario de todas las palabras procesas y filtradas.
        """
        id2word = Dictionary(palabras for palabras in self.obtener_palabras())
        id2word.filter_extremes(no_below=5, no_above=self.no_above)
        id2word.compactify()

        return id2word

    def df_ngramed(self):
        """Tokens del corpus con ngramas.

        Returns
        -------
        pd.DataFrame
            Estadisticas de cada token del corpus.
        """
        columnas = ["doc_id", "sent_id", "tok_id", "word"]

        items = []
        for doc in self.docs:
            sent_id = 1

            for frase in self.ngram_frases(doc):
                tok_id = 1
                for tok in frase:
                    fila = [doc._.get("doc_id"), sent_id, tok_id, tok]
                    tok_id += 1

                    items.append(fila)

                sent_id += 1

        return pd.DataFrame(items, columns=columnas)
