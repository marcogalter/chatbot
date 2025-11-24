import streamlit as st
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- Configuração da Página ---
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖"
)

# --- Configuração ---
# Ollama é 100% GRATUITO e roda localmente!
# Não precisa de API key 🎉

# --- Constantes ---
DB_PATH = "chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Template de Prompt Customizado para RAG ---
# Instruímos o modelo a focar APENAS no contexto
prompt_template = ChatPromptTemplate.from_template("""
Use estritamente o contexto a seguir para responder à pergunta. 
Se a resposta não estiver no contexto, diga apenas "Desculpe, não tenho informações sobre isso no meu banco de dados."
Não tente inventar uma resposta.

Contexto:
{context}

Pergunta:
{question}

Resposta:
""")

# --- Função de CSS Customizado ---

def apply_custom_css():
    """
    Aplica o CSS customizado para o tema "Hacker Terminal" da Cloudwalk.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ===== PALETA DE CORES MODERNA ===== */
        :root {
            --bg-primary: #121212;
            --bg-secondary: #1a1a1a;
            --text-primary: #e8e8e8;
            --text-secondary: #a0a0a0;
            --accent-green: #00d964;
            --accent-red: #ff3b30;
            --border-subtle: #2a2a2a;
        }

        /* --- Fundo e Tipografia Principal --- */
        html, body, .main {
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }

        /* --- Título Principal Modernizado --- */
        h1 {
            font-family: 'Inter', sans-serif !important;
            font-size: 2.5em !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.5px !important;
            text-shadow: none !important;
            margin-bottom: 8px !important;
        }

        h1 em {
            color: var(--accent-green) !important;
            font-style: normal !important;
        }
        
        /* --- Subtítulo/Legenda --- */
        .stCaption {
            color: var(--text-secondary) !important;
            opacity: 1 !important;
            font-size: 0.95em !important;
            font-weight: 400 !important;
            letter-spacing: 0.2px !important;
        }

        /* === CAIXAS DE MENSAGEM - DESIGN MINIMALISTA === */
        [data-testid="stChatMessage"] {
            background-color: var(--bg-secondary) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        }

        /* Estilo para mensagem do assistente */
        [data-testid="stChatMessage"][data-testid*="assistant"] {
            border-left: 3px solid var(--accent-green) !important;
        }

        /* Estilo para mensagem do usuário */
        [data-testid="stChatMessage"][data-testid*="user"] {
            border-left: 3px solid var(--accent-red) !important;
            background-color: rgba(255, 59, 48, 0.05) !important;
        }
        
        /* --- Texto dentro das mensagens --- */
        [data-testid="stChatMessage"] p {
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1em !important;
            font-weight: 400 !important;
            line-height: 1.6 !important;
        }

        /* --- Ícones do Chat --- */
        [data-testid="stChatMessage"] [data-testid*="avatar"] {
            border-radius: 8px !important;
        }

        /* === CAIXA DE INPUT - DESIGN PREMIUM "PÍLULA" SEM BORDAS (CORREÇÃO DE LAYOUT STREAMLIT) === */

        /* Container Principal - Formato Pílula Suave (data-testid="stChatInput") */
        [data-testid="stChatInput"] {
            /* Forma e Fundo */
            background: linear-gradient(135deg, #2a2a2a 0%, #282828 100%) !important;
            border: none !important;
            border-radius: 50px !important;

            /* Layout e Espaçamento (Ajuste para melhor visualização do texto) */
            /* PADDING aumentado para acomodar melhor o texto */
            padding: 14px 24px 14px 24px !important; 
            display: flex !important;
            align-items: center !important;
            gap: 12px !important; /* Espaçamento aumentado entre o campo de texto e o botão */
            margin: 32px auto !important;
            outline: none !important;
            width: 100% !important;
            max-width: 600px !important; /* Largura máxima para não ficar muito largo */

            /* Efeitos Visuais */
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), inset 0 1px 3px rgba(255, 255, 255, 0.08) !important;
            transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        }

        /* Hover state - aprofunda a sombra */
        [data-testid="stChatInput"]:hover {
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5), inset 0 1px 3px rgba(255, 255, 255, 0.1) !important;
            background: linear-gradient(135deg, #2d2d2d 0%, #2a2a2a 100%) !important;
        }

        /* Estado focado - glow interno verde discreto */
        [data-testid="stChatInput"]:focus-within {
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.5), 
                inset 0 0 20px rgba(0, 255, 128, 0.15) !important; 
            background: linear-gradient(135deg, #2d2d2d 0%, #282828 100%) !important;
        }

        /* Wrapper Interno do Streamlit (CORREÇÃO AGRESSIVA DE ESPAÇAMENTO) */
        /* Este é o elemento que provavelmente injeta o padding indesejado */
        [data-testid="stChatInput"] > div {
            /* Anular qualquer estilo injetado */
            background: transparent !important;
            border: none !important;
            
            /* Essencial: zera padding e margin */
            padding: 0 !important; 
            margin: 0 !important; 
            
            flex: 1 !important;
            display: flex !important;
            align-items: center !important;
        }

        /* === TEXTAREA - CAMPO DE TEXTO ELEGANTE === */
        [data-testid="stChatInput"] textarea {
            background-color: transparent !important;
            color: #e8e8e8 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
            font-size: 1em !important; /* Aumentei um pouco a fonte */
            font-weight: 400 !important;
            border: none !important;
            outline: none !important;
            
            /* Essencial: zera padding/margin para usar o padding do container pai */
            padding: 2px 4px !important; /* Pequeno padding para melhor legibilidade */
            margin: 0 !important;
            
            line-height: 1.6 !important;
            caret-color: #00FF80 !important;
            resize: none !important;
            max-height: 100px !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            letter-spacing: 0.3px !important;
            min-height: 24px !important; /* Altura mínima para acomodar o texto */
        }

        /* Placeholder elegante e legível */
        [data-testid="stChatInput"] textarea::placeholder {
            color: #9a9a9a !important;
            opacity: 1 !important;
        }

        /* === BOTÃO DE ENVIAR - CÍRCULO PERFEITO INTEGRADO === */
        [data-testid="stChatInputSubmitButton"] {
            /* Forma e Fundo */
            background: linear-gradient(135deg, #00FF80 0%, #00dd66 100%) !important;
            border: none !important;
            border-radius: 50% !important;
            width: 44px !important;
            height: 44px !important;
            min-width: 44px !important;
            min-height: 44px !important;
            
            /* Espaçamento */
            padding: 0 !important; 
            margin: 0 !important; /* Zera margem para usar o 'gap' do container pai */
            
            /* Efeitos Visuais */
            outline: none !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 0 4px 12px rgba(0, 255, 128, 0.25) !important;
            flex-shrink: 0 !important;
        }

        /* Ícone, Hover e Active do botão */
        [data-testid="stChatInputSubmitButton"] svg {
            fill: #000 !important;
            width: 22px !important;
            height: 22px !important;
            transition: all 0.25s ease !important;
        }

        [data-testid="stChatInputSubmitButton"]:hover {
            background: linear-gradient(135deg, #00ff99 0%, #00ff80 100%) !important;
            box-shadow: 0 8px 24px rgba(0, 255, 128, 0.4) !important;
            transform: translateY(-2px) scale(1.06) !important;
        }

        [data-testid="stChatInputSubmitButton"]:active {
            transform: translateY(0) scale(0.98) !important;
            box-shadow: 0 2px 8px rgba(0, 255, 128, 0.3) !important;
        }

        /* === SCROLLBAR MINIMALISTA === */
        [data-testid="stChatInput"] textarea::-webkit-scrollbar {
            width: 6px !important;
        }

        [data-testid="stChatInput"] textarea::-webkit-scrollbar-track {
            background: transparent !important;
        }

        [data-testid="stChatInput"] textarea::-webkit-scrollbar-thumb {
            background: #00FF80 !important;
            border-radius: 3px !important;
            opacity: 0.6 !important;
        }

        [data-testid="stChatInput"] textarea::-webkit-scrollbar-thumb:hover {
            opacity: 1 !important;
        }

        /* === REMOVE ELEMENTOS DESNECESSÁRIOS === */
        footer {
            visibility: hidden !important;
        }

        /* === REFINAMENTOS ADICIONAIS === */
        .stMarkdown {
            font-family: 'Inter', sans-serif !important;
        }

        code {
            background-color: var(--bg-secondary) !important;
            color: var(--accent-green) !important;
            border-radius: 4px !important;
            padding: 2px 6px !important;
            font-family: 'SF Mono', monospace !important;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Funções de Cache (para performance) ---

@st.cache_resource
def load_llm():
    """Carrega o modelo de chat (Ollama - Llama 3.2 - GRATUITO!)."""
    try:
        return ChatOllama(
            model="llama3.2",
            temperature=0,
            base_url="http://localhost:11434"
        )
    except Exception as e:
        st.error(f"⚠️ Erro ao conectar com Ollama: {e}")
        st.info("📥 Certifique-se de que o Ollama está rodando. Execute: `ollama serve` e depois `ollama pull llama3.2`")
        st.stop()

@st.cache_resource
def load_embeddings():
    """Carrega o modelo de embeddings (Hugging Face)."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

@st.cache_resource
def load_retriever(_embeddings):
    """Carrega o banco de dados vetorial (Chroma) como um 'retriever'."""
    if not os.path.exists(DB_PATH):
        st.error(f"Banco de dados '{DB_PATH}' não encontrado. Você rodou `python ingest.py` primeiro?")
        st.stop()
        
    vectordb = Chroma(persist_directory=DB_PATH, 
                      embedding_function=_embeddings)
    return vectordb.as_retriever()

# --- Carregamento Principal ---
llm = load_llm()
embeddings = load_embeddings()
retriever = load_retriever(embeddings)

# --- Criação da Chain de RAG (método moderno LCEL) ---
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)

# --- Interface do Streamlit ---

st.title("🤖 Cloudwalk Nimbus - Chatbot (Nível 1)")
apply_custom_css()  # Aplica o tema Hacker Terminal
st.caption("Pergunte-me sobre a Cloudwalk, sua missão e produtos (InfinitePay).")

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", 
                                  "content": "Olá! Como posso ajudar você a saber mais sobre a Cloudwalk?"}]

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("O que você quer saber?"):
    # Adiciona a pergunta ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do RAG
    with st.chat_message("assistant"):
        with st.spinner("Pensando na melhor resposta..."):
            answer = rag_chain.invoke(prompt)
            st.markdown(answer)

    # Adiciona a resposta do bot ao histórico
    st.session_state.messages.append({"role": "assistant", "content": answer})
