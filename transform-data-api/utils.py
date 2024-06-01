def extract_condition_and_clean_name(name):
    if '(' in name and ')' in name:
        condition = name.split('(')[-1].rstrip(')')
        cleaned_name = name.split('(')[0].rstrip()
    else:
        condition = ""
        cleaned_name = name
    return cleaned_name, condition
