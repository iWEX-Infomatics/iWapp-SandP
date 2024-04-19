def after_insert(doc, method):
    if doc.expenses:
        for exp in doc.expenses:
            if exp.amount:
                exp.sanctioned_amount = exp.amount