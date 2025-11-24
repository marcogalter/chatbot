# 🚀 Guia Rápido - Chatbot Cloudwalk (100% GRATUITO!)

## ✅ O que já está pronto:

- ✅ Ollama instalado e rodando
- ✅ Modelo Llama 3.2 baixado (2GB)
- ✅ Ambiente virtual criado
- ✅ Todas as dependências instaladas
- ✅ Banco de dados vetorial criado

## 🎯 Para executar o chatbot:

### 1. Ative o ambiente virtual:
```bash
cd /home/marcogalter/chatbot-cloudwalk
source venv/bin/activate
```

### 2. Execute o Streamlit:
```bash
streamlit run app.py
```

### 3. Abra no navegador:
O Streamlit abrirá automaticamente em: **http://localhost:8501**

---

## 💡 Perguntas que você pode fazer:

- "O que é a Cloudwalk?"
- "Qual a missão da Cloudwalk?"
- "Quais são os produtos da InfinitePay?"
- "O que é o InfiniteTap?"
- "Quando a Cloudwalk foi fundada?"
- "Quem fundou a Cloudwalk?"

---

## 🔧 Se precisar reprocessar os dados:

```bash
python ingest.py
```

---

## 🎉 Vantagens desta solução:

- ✅ **100% GRATUITO** - Sem custos de API!
- ✅ **Funciona OFFLINE** - Não precisa de internet (exceto para baixar o modelo)
- ✅ **Privado** - Seus dados ficam no seu computador
- ✅ **Rápido** - Llama 3.2 é otimizado para performance

---

## 🆘 Resolução de Problemas:

### Se o Ollama não estiver rodando:
```bash
sudo systemctl start ollama
```

### Para verificar se o Ollama está ativo:
```bash
ollama list
```

### Para parar o Streamlit:
Pressione `Ctrl + C` no terminal
