import os
import glob
from pathlib import Path
from functools import partial
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


knowledgebase = str(Path(__file__).parent.parent / "knowledge-base")
vectorDB = str(Path(__file__).parent.parent / "vectorstore")

embeddings = HuggingFaceEmbeddings(model_name="multi-qa-MiniLM-L6-cos-v1")

def fetching():
    documents = []
    folder = glob.glob(knowledgebase)
    for files in folder:
        docType = os.path.basename(files)
        loader = DirectoryLoader(
            files,
            glob="**/*.md",
            loader_cls=partial(TextLoader, encoding="utf-8"),
        )
        fileDocs = loader.load()
        for doc in fileDocs:
            doc.metadata["docType"] = docType
            documents.append(doc)
    return documents

def splitter(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=80)
    chunks = text_splitter.split_documents(documents)
    return chunks

def vectorize(chunks):
    if os.path.exists(vectorDB):
        Chroma(persist_directory=vectorDB, embedding_function=embeddings).delete_collection()
    vectors = Chroma.from_documents( 
        documents=chunks,
        embedding=embeddings,
        persist_directory=vectorDB,
    )
    return vectors

if __name__ == "__main__":
    documents = fetching()
    print(f"fetched {len(documents)} documents")
    chunks = splitter(documents)
    print(f"split into {len(chunks)} chunks")
    vectors = vectorize(chunks)
    print("ingestion completed")