from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text):
    # Split text into chunks of 1024 tokens
    max_chunk = 1024
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    return " ".join(summaries)