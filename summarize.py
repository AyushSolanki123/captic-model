import nlpcloud

def text_summarize(text):
    client = nlpcloud.Client("bart-large-cnn", "50e8d5cfaf6e0287b24bb7ebe5f6de027388386b", False)
    result = client.summarization(text)
    return result['summary_text']