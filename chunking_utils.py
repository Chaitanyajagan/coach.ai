from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=[
            "\n\n",   # paragraphs
            "\n",     # new lines
            ".",      # sentences
            " ",      # words
            ""
        ]
    )

    chunks = splitter.split_text(text)

    return [
        {
            "chunk_id": i + 1,
            "content": chunk
        }
        for i, chunk in enumerate(chunks)
    ]
