import pytest

from pdftalk_summarize import split_sentences, summarize


def test_split_sentences_basic():
    text = "Hola. Esto es una prueba. Funciona bien!"
    assert split_sentences(text) == ["Hola.", "Esto es una prueba.", "Funciona bien!"]


def test_split_sentences_empty():
    assert split_sentences("   ") == []


def test_summarize_empty_raises():
    with pytest.raises(ValueError):
        summarize("   ")


def test_summarize_invalid_ratio_raises():
    with pytest.raises(ValueError):
        summarize("Una oracion. Otra oracion.", ratio=0)


def test_summarize_single_sentence_returns_as_is():
    assert summarize("Una sola oracion sin punto final", ratio=0.2) == "Una sola oracion sin punto final"


def test_summarize_keeps_most_relevant_sentences():
    text = (
        "El cambio climático afecta a los ecosistemas de todo el planeta. "
        "El aumento de temperatura global altera los patrones de lluvia en muchas regiones. "
        "Mi gato favorito duerme en la ventana durante las tardes soleadas. "
        "Los ecosistemas marinos sufren por el aumento de temperatura del océano. "
        "El clima y la temperatura global son temas centrales del cambio climático actual."
    )
    summary = summarize(text, ratio=0.4)
    sentences = split_sentences(summary)

    assert 1 <= len(sentences) <= 3
    assert "gato" not in summary.lower()


def test_summarize_respects_max_sentences():
    text = " ".join(f"Esta es la oracion numero {i} sobre el tema principal." for i in range(10))
    summary = summarize(text, ratio=1.0, max_sentences=3)
    assert len(split_sentences(summary)) <= 3
