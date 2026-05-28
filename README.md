# Generative AI Equity Research Tool

A beginner-friendly project scaffold for a RAG-based equity research assistant.

## What this starter contains

- Python virtual environment setup
- Streamlit frontend scaffold
- FastAPI entry point scaffold
- Jupyter notebook folder
- Local vector store and data folders
- OpenAI environment variable setup
- RAG-ready dependency list

## Project structure

```text
project/
├── .venv/
├── notebooks/
├── app/
├── frontend/
├── vectorstore/
├── data/
├── requirements.txt
├── .env
├── main.py
└── README.md
```

## Step-by-step setup commands

1. Create the virtual environment:

```powershell
cd d:\GenAiProject1
C:/Users/cheta/AppData/Local/Programs/Python/Python313/python.exe -m venv .venv
```

2. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

5. Start the FastAPI placeholder entry point later with:

```powershell
uvicorn main:app --reload
```

6. Start the Streamlit frontend later with:

```powershell
streamlit run frontend\streamlit_app.py
```

7. Open notebooks from the `notebooks/` folder in VS Code and pick the `.venv` interpreter when prompted.

## Environment variables

Add your OpenAI API key to `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

## Notes

- `main.py` and `frontend/streamlit_app.py` are only placeholders for now.
- The vector database folder is ready for ChromaDB storage.
- The structure is ready for article scraping, chunking, embeddings, semantic retrieval, and question answering.
