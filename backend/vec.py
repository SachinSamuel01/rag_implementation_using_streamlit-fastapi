from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from backend.llm import embeddings

def rele_data(dir):
    print(dir)
    loader= DirectoryLoader(f'./{dir}', glob='./*.pdf',loader_cls=PyPDFLoader)
    documents= loader.load()

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    docs=text_splitter.split_documents(documents)
    vectordb=Chroma.from_documents(documents=docs,
                                    embedding=embeddings)
        
    retriever=vectordb.as_retriever()
    return retriever



def get_content(retriever,query):
    docs=retriever.get_relevant_documents(query)
    
    content= f'{str(docs[0])}\n{str(docs[1])}\n{str(docs[2])}\n{str(docs[3])}'
    
    return content