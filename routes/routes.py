from fastapi import APIRouter, HTTPException, UploadFile
from services.fileservice import total_assets_with_commas, cash_with_commas, calculate_debt_ratio_final, find_non_and_current, non_current_with_commas, current_with_commas, calculate_cash_ratio_final, find_page_2, total_revenue_with_commas, find_page_5


# Replace with the path to your PDF file
keyword1 = "Assets"
keyword2 = "Property, plant and equipment"
keyword3 = "non-Current Assets"
keyword4 = "total Assets"
keyword5 = "cash"
keyword_total_assets = keyword4
keyword_cash = keyword5
keyword_borrowings = "borrowings"

keyword_revenue = "revenue"
keyword_pbt = "before tax"
keyword_finance_costs = "other"
keyword_expense = "expense"
keyword_group = "group"


router = APIRouter()


@router.post('/validate')
async def validateFile(file_upload: UploadFile):
    try:
        fileName = file_upload.filename
        fileContent = await file_upload.read()

        text_assets = find_page_5(fileContent, keyword1, keyword2,
                                  keyword3, keyword4, keyword5)
        text_revenue = find_page_2(fileContent, keyword_revenue, keyword_pbt,
                                   keyword_finance_costs, keyword_expense, keyword_group)
        revenue = total_revenue_with_commas(text_revenue, keyword_revenue)
        profit_before_tax = total_revenue_with_commas(
            text_revenue, keyword_pbt)
        total_assets = total_assets_with_commas(text_assets, keyword4)
        total_cash = cash_with_commas(text_assets, keyword4)
        ratio_cash = calculate_cash_ratio_final(total_cash, total_assets)

        non_current_liab, current_liab = find_non_and_current(text_assets)
        non_current_value = non_current_with_commas(
            non_current_liab, keyword_borrowings)
        current_value = current_with_commas(current_liab, keyword_borrowings)
        ratio_debt = calculate_debt_ratio_final(
            current_value, non_current_value, total_assets)

        print(ratio_cash, ratio_debt)
        print(revenue, profit_before_tax)
        total_debt = non_current_value + current_value

        return {
            'message': fileName,
            'ratio': {
                'ratio_cash': ratio_cash,
                'ratio_debt': ratio_debt
            },
            'title': {
                'revenue': revenue,
                'pbt': profit_before_tax,
                'total_assets': total_assets
            },
            'total': {
                'total_cash': total_cash,
                'total_debt': total_debt
            },
            'debt': {
                'current': current_value,
                'non_current': non_current_value
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error due to {e}')
