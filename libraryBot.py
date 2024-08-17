from flask import Flask, request, jsonify, render_template
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

app = Flask(__name__)

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

embedding_function = OpenAIEmbeddings()
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
model = ChatOpenAI()

def process_query(query_text):
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        return {"response": "My apologies, I am unable to find matching results for your query.", "sources": []}

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    response_text = model.predict(prompt)
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    return {"response": response_text, "sources": sources}

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query_text = data.get('query_text')
    if not query_text:
        return jsonify({"error": "No query_text provided"}), 400
    
    result = process_query(query_text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)