import PyPDF2
import re
import io
# Replace with the path to your PDF file
pdf_path = "AllCompanyFolder\ARANK-Annual Report 2023.pdfe"
keyword1 = "Assets"
keyword2 = "Property, plant and equipment"
keyword3 = "non-Current Assets"
keyword4 = "total Assets"
keyword5 = "cash"
keyword_total_assets = keyword4
keyword_cash = keyword5
keyword_borrowings = "borrowings"

keyword_revenue = "revenue"
keyword_pbt = "profit before tax"
keyword_finance_costs = "finance costs"
keyword_expense = "expense"
keyword_group = "group"


def search_revenue_keywords(file_upload, keyword_revenue, keyword_pbt, keyword_finance_costs, keyword_expense, keyword_group):
    results = []
    with io.BytesIO(file_upload) as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page_text = reader.pages[page_num].extract_text()
            if all(keyword.lower() in page_text.lower() for keyword in [keyword_revenue, keyword_pbt, keyword_finance_costs, keyword_expense, keyword_group]):
                results.append(page_num + 1)
    return results


def search_four_keywords(file_upload, keyword1, keyword2, keyword3, keyword4, keyword5):
    results = []
    with io.BytesIO(file_upload) as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page_text = reader.pages[page_num].extract_text()
            if all(keyword.lower() in page_text.lower() for keyword in [keyword1, keyword2, keyword3, keyword4, keyword5]):
                results.append(page_num + 1)
                results.append(page_num + 2)  # Page numbers are 1-indexed
    return results


def extract_text_on_page(file_upload, page_num):
    with io.BytesIO(file_upload) as file:
        reader = PyPDF2.PdfReader(file)
        if 0 < page_num <= len(reader.pages):
            page_text = reader.pages[page_num - 1].extract_text()
            return page_text
        else:
            return "Invalid page number."


def extract_value_with_commas_from_table(text, keyword):
    lines = text.split('\n')
    for line in lines:
        if keyword.lower() in line.lower():
            matches = re.findall(r'(\d{1,3}(?:,\d{3})+)', line)
            if matches:
                return matches[0]
            else:
                return None
    return None


def extract_text_from_pdf_page(pdf_path, page_num):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        if page_num >= 0 and page_num < len(reader.pages):
            text = reader.pages[page_num].extract_text()
    return text


def find_page_2(pdf_path, keyword_revenue, keyword_pbt, keyword_finance_costs, keyword_expense, keyword_group):
    pages_with_both_keywords = search_revenue_keywords(
        pdf_path, keyword_revenue, keyword_pbt, keyword_finance_costs, keyword_expense, keyword_group)
    if pages_with_both_keywords:
        # Store the extracted text from all pages in a single variable
        text = ""
        for page_number in pages_with_both_keywords:
            page_text = extract_text_on_page(pdf_path, page_number)
            text += page_text + "\n"

        return text
    else:
        return "Page Not Found"


def find_page_5(pdf_path, keyword1, keyword2, keyword3, keyword4, keyword5):
    pages_with_both_keywords = search_four_keywords(
        pdf_path, keyword1, keyword2, keyword3, keyword4, keyword5)
    if pages_with_both_keywords:
        # Store the extracted text from all pages in a single variable
        text = ""
        for page_number in pages_with_both_keywords:
            page_text = extract_text_on_page(pdf_path, page_number)
            text += page_text + "\n"

        return text
    else:
        return "Page Not Found"

# Extract the value with commas from the line containing the keyword


def total_revenue_with_commas(text, keyword_revenue):
    value_with_commas_total_assets = extract_value_with_commas_from_table(
        text, keyword_revenue)
    if value_with_commas_total_assets:
        # Remove commas and convert to a numeric value
        numeric_value_total_assets = float(
            value_with_commas_total_assets.replace(",", ""))
        return numeric_value_total_assets

    else:
        return 0


def total_assets_with_commas(text, keyword_total_assets):
    value_with_commas_total_assets = extract_value_with_commas_from_table(
        text, keyword_total_assets)
    if value_with_commas_total_assets:
        # Remove commas and convert to a numeric value
        numeric_value_total_assets = float(
            value_with_commas_total_assets.replace(",", ""))
        return numeric_value_total_assets

    else:
        return 0

# Extract the value with commas from the line containing the keyword


def cash_with_commas(text, keyword_total_assets):
    value_with_commas_cash = extract_value_with_commas_from_table(
        text, keyword_cash)

    if value_with_commas_cash:
        # Remove commas and convert to a numeric value
        numeric_value_cash = float(value_with_commas_cash.replace(",", ""))

        return numeric_value_cash
    else:
        return 0


def calculate_cash_ratio_final(numeric_value_cash, numeric_value_total_assets):
    cash_ratio_final = numeric_value_cash / numeric_value_total_assets * 100
    return cash_ratio_final


def find_non_and_current(text):

    titles_non_current, lines_non_current, titles_current, lines_current = find_borrowings_titles(
        text)

    return lines_non_current, lines_current


def non_current_with_commas(lines_non_current, keyword_borrowings):
    value_with_commas_non_current = extract_value_with_commas_from_table(
        lines_non_current[0], keyword_borrowings)
    if value_with_commas_non_current and value_with_commas_non_current != "-":
        # Remove commas and convert to a numeric value
        numeric_value_non_current = float(
            value_with_commas_non_current.replace(",", ""))
        print("hello")
        print(numeric_value_non_current)
        return numeric_value_non_current
    else:
        return 0


def find_borrowings_titles(text):
    lines = text.split('\n')
    borrowings_indices = []

    # Find the indices of the lines containing the word "borrowings"
    for i, line in enumerate(lines):
        if 'borrowings' in line.lower():
            borrowings_indices.append(i)

    if not borrowings_indices:

        return [], []

    titles_non_current = []
    lines_non_current = []
    titles_current = []
    lines_current = []

    # Iterate through each found instance of "borrowings"
    for borrowings_index in borrowings_indices:
        title_found = False
        # Trace back to find the titles "Current liabilities" and "Non-current liabilities"
        for i in range(borrowings_index - 1, max(borrowings_index - 11, 0), -1):
            line_lower = lines[i].lower()
            if "current liabilities" in line_lower or "non-current liabilities" in line_lower:
                if "non-current liabilities" in line_lower:
                    titles_non_current.append(lines[i])
                    lines_non_current.append(lines[borrowings_index])
                else:
                    titles_current.append(lines[i])
                    lines_current.append(lines[borrowings_index])
                title_found = True
                break

        if not title_found:
            # If title not found backward, trace forward
            for i in range(borrowings_index + 1, min(borrowings_index + 11, len(lines))):
                line_lower = lines[i].lower()
                if "current liabilities" in line_lower or "non-current liabilities" in line_lower:
                    if "non-current liabilities" in line_lower:
                        titles_non_current.append(lines[i])
                        lines_non_current.append(lines[borrowings_index])
                    else:
                        titles_current.append(lines[i])
                        lines_current.append(lines[borrowings_index])
                    break

    if not titles_non_current and not titles_current:
        return None
    return titles_non_current, lines_non_current, titles_current, lines_current


def current_with_commas(lines_current, keyword_borrowings):
    value_with_commas_current = extract_value_with_commas_from_table(
        lines_current[0], keyword_borrowings)
    if value_with_commas_current:
        # Remove commas and convert to a numeric value
        numeric_value_current = float(
            value_with_commas_current.replace(",", ""))

        return numeric_value_current
    else:
        return 0


def calculate_debt_ratio_final(numeric_value_current, numeric_value_non_current, numeric_value_total_assets):

    debt_ratio_final = (numeric_value_current +
                        numeric_value_non_current)/numeric_value_total_assets * 100
    return debt_ratio_final
