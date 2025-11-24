# 🤖 Desafio Cloudwalk Nimbus - Nível 1 (Chatbot RAG)

Este projeto é uma solução para o Nível 1 do desafio Nimbus, que consiste em criar um chatbot RAG (Retrieval-Augmented Generation) para responder perguntas sobre a Cloudwalk.

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python
* **Orquestração RAG:** LangChain
* **LLM (Chat Model):** Ollama com Llama 3.2 (100% GRATUITO e LOCAL! 🎉)
* **Embeddings:** Hugging Face `all-MiniLM-L6-v2` (via `sentence-transformers`)
* **Vector Store:** ChromaDB
* **Interface Web:** Streamlit

## ⚙️ Como Executar

### 📋 **Pré-requisitos:**
- Python 3.10 ou superior
- Git
- Conexão à internet (apenas para instalação)

---

### 🚀 **Passo a Passo Completo:**

#### **1. Instale o Ollama (LLM Gratuito):**
   
   **Linux/WSL:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
   
   **macOS:**
   ```bash
   brew install ollama
   ```
   
   **Windows:** Baixe em https://ollama.com/download

#### **2. Inicie o Ollama e baixe o modelo Llama 3.2:**
   ```bash
   # Inicia o servidor Ollama (deixe rodando)
   ollama serve
   ```
   
   Em **outro terminal**, execute:
   ```bash
   # Baixa o modelo Llama 3.2 (~2GB)
   ollama pull llama3.2
   ```

#### **3. Clone o repositório:**
   ```bash
   git clone [URL-DO-SEU-REPO]
   cd chatbot-cloudwalk
   ```

#### **4. Instale o Python 3.10-venv (se necessário - Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install python3.10-venv -y
   ```

#### **5. Crie e ative o ambiente virtual:**
   ```bash
   # Criar ambiente virtual
   python3 -m venv venv
   
   # Ativar (Linux/macOS)
   source venv/bin/activate
   
   # Ativar (Windows CMD)
   .\venv\Scripts\activate
   
   # Ativar (Windows PowerShell)
   .\venv\Scripts\Activate.ps1
   ```

#### **6. Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
   
   ⏱️ *Este passo pode levar alguns minutos (várias bibliotecas serão instaladas).*

#### **7. Processe os documentos (Execute apenas uma vez):**
   ```bash
   python ingest.py
   ```
   
   ✅ *Isso criará o banco de dados vetorial na pasta `chroma_db/`*

#### **8. Execute o chatbot:**
   ```bash
   streamlit run app.py
   ```

#### **9. Acesse no navegador:**
   
   Após executar o comando acima, você verá algo como:
   ```
   Agora você pode visualizar seu aplicativo Streamlit no seu navegador.
   
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```
   
   **Abra seu navegador** e acesse:
   - 🌐 **http://localhost:8501**
   
   Ou copie e cole a URL mostrada no terminal.

---

### 🎮 **Para parar a aplicação:**
   - Pressione **Ctrl + C** no terminal onde o Streamlit está rodando

---

### 🔄 **Para executar novamente:**
   ```bash
   # 1. Certifique-se de que o Ollama está rodando
   ollama serve
   
   # 2. Em outro terminal, ative o ambiente virtual
   cd chatbot-cloudwalk
   source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
   
   # 3. Execute o chatbot
   streamlit run app.py
   ```

---

## 💬 3 Amostras de Conversa (Exigência do Desafio)

**Amostra 1:**
* **Usuário:** O que é a Cloudwalk?
* **Chatbot:** A Cloudwalk é uma fintech (empresa de tecnologia financeira) brasileira, fundada em 2013 e sediada em São Paulo. Ela é a empresa controladora da popular marca InfinitePay e foca em revolucionar o sistema financeiro usando IA e blockchain.

**Amostra 2:**
* **Usuário:** Qual a missão da empresa?
* **Chatbot:** A missão principal da Cloudwalk é "democratizar o acesso a serviços financeiros inovadores", com o objetivo de criar uma rede global de pagamentos mais rápida, fácil e segura.

**Amostra 3:**
* **Usuário:** O que é o InfiniteTap?
* **Chatbot:** O InfiniteTap (Tap to Pay) é uma solução da InfinitePay (marca da Cloudwalk) que transforma o celular (Android e iOS) em uma maquininha de cartão.
