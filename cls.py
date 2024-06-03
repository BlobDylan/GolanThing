import os
import google.generativeai as geni

def classify(msg):
    key = os.environ.get('GEMINI_API_KEY')

    geni.configure(api_key=key)

    instruction = (
        """Given an input I want you to classify it into one of the following classes:
        housing_expenses,
        gift_expenses,
        transportation_expenses,
        food_and_groceries,
        healthcare_expenses,
        entertainment_and_leisure,
        clothing_and_personal_care,
        education_and_childcare,
        savings_and_investments,
        miscellaneous_expenses,
        operational_expenses,
        employee_expenses,
        marketing_and_advertising,
        professional_services,
        inventory_and_supplies,
        insurance,
        research_and_development,
        taxes_and_licenses,
        depreciation_and_amortization,
        miscellaneous_business_expenses.
        Do not explain your categorization give only the categorie you think fits best.
        If you think the input does not fit any categorie well simply respond with no_fit.
        """
    )
    model = geni.GenerativeModel('gemini-1.5-flash',system_instruction=instruction)
    response = model.generate_content(msg)
    return response.text

