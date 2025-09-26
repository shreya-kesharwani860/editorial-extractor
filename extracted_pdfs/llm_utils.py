from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_chunk_len=900):
    sentences = text.split(". ")
    current_chunk = ""
    chunks = []
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chunk_len:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())

    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)

    return " ".join(summaries)

def extract_metadata(text):
    """
    Simple metadata extraction: counts sentences and characters.
    """
    sentences = text.split(". ")
    return {
        "num_sentences": len(sentences),
        "num_characters": len(text)
    }
