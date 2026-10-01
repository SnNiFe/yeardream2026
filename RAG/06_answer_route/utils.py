def retrieve_to_text(docs):
    text = ''
    for doc in docs:
        text += doc.page_content+'\n'
    return text