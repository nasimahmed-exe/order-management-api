from app.model.document import Document
from app.core.embedding import embed_text
from app.db.session import SessionLocal

def test():
    db = SessionLocal()

    text = "PostgreSql is powerful relational database"
    embedding = embed_text(text)
    print(f"Embedding_length: {len(embedding)}")
    print(f"first 5 value: {embedding[:5]}")

    doc = Document(
        title = "Test document",
        content = text,
        embedding = embedding
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    print(f" Stored Embedding in database: {doc(id)}")

    retrieved = db.query(Document).filter(Document.id == doc.id).first()
    print(f"Retrieved: {retrieved.titel}")
    print(f"Embedding exist: {retrieved.embedding is not None}")

    db.close()

    if __name__ == "__main__":
        test()