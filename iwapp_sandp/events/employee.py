def before_save(doc, method):
    # Check if any of the properties are None, and set them to 0 if they are
    monthly_salary = doc.custom_monthly_salary_offered or 0
    seniority_allowance = doc.custom_seniority_allowance or 0
    performance_allowance = doc.custom_performance_allowance or 0
    # # Calculate the ctc
    doc.ctc = (monthly_salary + seniority_allowance + performance_allowance) * 12
    # # Calculate the salary per day
    doc.custom_salary_per_day = (monthly_salary + performance_allowance + seniority_allowance) / 30
