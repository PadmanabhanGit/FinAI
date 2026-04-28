import os
import streamlit as st
import pickle
import time
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms.base import LLM
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini only if API key is available
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.warning("⚠️ GEMINI_API_KEY not found. Please add it to Streamlit Secrets.")

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
    """Custom LLM wrapper for Google Gemini"""
    
    def _call(self, prompt, stop=None, run_manager=None, **kwargs):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

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

# Only initialize LLM if API key is available
llm = None
if GEMINI_API_KEY:
    llm = GeminiLLM()
else:
    st.error("❌ Cannot initialize LLM. GEMINI_API_KEY is required. Add it in Settings → Secrets.")

if process_url_clicked:
    loader_placeholder = st.empty()
    loader_placeholder.text("Data Loading >>> Started >>> ✅✅✅")
    
    try:
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
            time.sleep(2)
    except Exception as e:
        st.error(f"❌ Error processing URLs: {str(e)}")

query = st.text_input("Question: ")
if query:
    if not llm:
        st.error("❌ LLM not initialized. Please add GEMINI_API_KEY to Secrets first.")
    elif not os.path.exists(file_path):
        st.error("❌ No vectorstore found. Please process URLs first.")
    else:
        try:
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
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")
