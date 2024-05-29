def before_save(doc, method):
    if doc.base:
        doc.variable = doc.base / 30