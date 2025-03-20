from ..utils.parse import extract_pdf_content

def rag(questions):
    pdf_path = "mon_document.pdf"
    content = extract_pdf_content(pdf_path)
    chunks = chunk_text(content)
    embed_chunks(chunks, embedder, index)
    results_semantic = semantic_search(question, chunks)
    results_vector = vector_search(question, chunks)
    merged_results = results_semantic + results_vector
    merged_results_sorted = sorted(merged_results, key=lambda x: x[1], reverse=True)
    best_chunks = [chunk for chunk, _ in merged_results_sorted[:3]]
    answer, score = generate_response(question, best_chunks, merged_results_sorted[0][1])