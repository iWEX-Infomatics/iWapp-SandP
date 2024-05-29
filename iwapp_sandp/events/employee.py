def before_save(doc, method):
    monthly_salary = doc.custom_gross_salary or 0
    # # Calculate the ctc
    doc.ctc = monthly_salary  * 12
    # # Calculate the salary per day
    doc.custom_salary_per_day = monthly_salary / 30
