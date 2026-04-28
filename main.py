import os
import streamlit as st
import pickle
import time
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
import google.generativeai as genai
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms.base import LLM
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Simple URL loader using requests + BeautifulSoup
def load_urls(urls):
    """Load and extract text from URLs"""
    documents = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for url in urls:
        if not url.strip():
            continue
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            
            if text.strip():
                doc = Document(page_content=text, metadata={"source": url})
                documents.append(doc)
        except Exception as e:
            st.error(f"Error loading {url}: {str(e)}")
            continue
    
    return documents

class GeminiLLM(LLM):
    def _call(self, prompt, stop=None, run_manager=None, **kwargs):
        model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-2.5-pro"
        response = model.generate_content(prompt)
        return response.text

    @property
    def _llm_type(self) -> str:
        return "google_gemini"

st.title("News Research Tool 📈")
st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss-store-hf.pkl"

main_placeholder = st.empty()
llm = GeminiLLM()

if process_url_clicked:
    loader_placeholder = st.empty()
    loader_placeholder.text("Data Loading >>> Started >>> ✅✅✅")
    
    data = load_urls(urls)
    
    if not data:
        st.error("No content could be loaded from the provided URLs")
    else:
        loader_placeholder.text(f"Loaded {len(data)} documents >>> ✅✅✅")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        separators=['\n\n', '\n', '.', ' ']
    )

    loader_placeholder.text("Text Splitter >>> Started >>> ✅✅✅")
    docs = text_splitter.split_documents(data)

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
    else:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)
        with open(file_path, "wb") as f:
            pickle.dump(vectorstore, f)

    main_placeholder.text("Embedding Vector Creation >>> ✅✅✅")
    print(f"Embeddings creation completed")
    time.sleep(2)

query = st.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            st.header("Answer")
            st.write(result["answer"])

            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")
                for source in sources_list:
                    st.write(source)
