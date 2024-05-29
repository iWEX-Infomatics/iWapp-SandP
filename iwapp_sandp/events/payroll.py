def before_save(doc, method):
    if doc.posting_date:
        doc.posting_date = doc.end_date