from itertools import islice

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from server.models.document import Chunk, Document


def batched(iterable, n, *, strict=False):
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError("batched(): incomplete batch")
        yield batch


def make_document_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    sentences = ["".join(chars) for chars in batched(text, 1024)]
    embeddings = model.encode(sentences)

    chunks = [
        Chunk(text=text, vectors=vectors)
        for text, vectors in zip(sentences, embeddings)
    ]
    document = Document(text=text, chunks=chunks)

    return document
