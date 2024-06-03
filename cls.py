import os
import google.generativeai as geni

key = os.environ.get('GEMINI_API_KEY')
geni.configure(api_key=key)
hist = []

def classify(msg):

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
        Sometimes the input will be associated with a cost, if so respond with the category and cost in the following format:
        {"category" : "<category>", "cost" : "<cost>"} where <category> is the category and <cost> is the cost represented only by a number.
        Do not explain your categorization give only the categorie and cost you think fit best.
        If you think the input does not fit any categorie well simply respond {"category" : "no_fit", "cost" : "<cost>"}.
        If you think a cost wasn't provided simply respond with {"category" : "<category>", "cost" : "no_cost"}.
        """
    )
    model = geni.GenerativeModel('gemini-1.5-flash',system_instruction=instruction)
    response = model.generate_content(msg)
    return response.text

def message_type(msg):

    instruction = (
        """
        You are in charge of responding to an input that may be a generic message or an attempt to report a cash expense
        On the given input respond "generic" if you think the input is a question, otherwise, respond "classify".
        If the input is unclear repspond "not_sure".
        Do not add any information to your response besides "generic", "classify" and "not_sure".
        """
    )
    model = geni.GenerativeModel('gemini-1.5-flash',system_instruction=instruction)
    response = model.generate_content(msg)
    return response.text


def question_response(msg, db):
    instruction = (
        f"""
        Given an input answer based on the following information:
        {db}
        Try to be short and concice.
        """
    )
    hist.append({'role' : 'user', 'parts' : [msg]})
    model = geni.GenerativeModel('gemini-1.5-flash',system_instruction=instruction)
    response = model.generate_content(hist)
    hist.append({'role' : 'model', 'parts' : [response.text]})
    print(hist)
    return response.text
