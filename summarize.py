import nlpcloud


def text_summarize(text, count):

    api_token = ["0a4707f867bf3cc1530c44a91f48be031f2501ee", "48a237e5bb45a88a88020a6f40c8804faa2b05df", "cf6753ac3c78000009c3317f52b2011506338f1d",
                 "a60d97ba791b445f1208af0c1e35ed35c26a006e", "a1ba2e2450eed7debe4c409eead140772d180fc4"]

    client = nlpcloud.Client(
        "bart-large-cnn", api_token[count % 5], False)
    result = client.summarization(text)
    return result['summary_text']
