import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


today = datetime.date.today()
age = 0

### Functionality Helper Functions ###
def parse_float(n):
    """
    Securely converts a non-numeric value to float.
    """
    try:
        return float(n)
    except ValueError:
        return float("nan")
        
        
def calculate_age(birthday):
    current_date = datetime.now()
    try:
        birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
        age = current_date.year - birthday.year
        # Check if the birth month and day have already occurred this year
        if (current_date.month, current_date.day) < (birthday.month, birthday.day):
            age -= 1
        return age
    except ValueError:
        return "Invalid date format. Please provide the date in the format: YYYY-MM-DD"
        
def calculate_future_date(current_age, target_age):
    current_date = datetime.now()
    # Calculate the remaining years until the target age
    remaining_years = target_age - current_age
    # Calculate the future date by adding the remaining years to the current date
    future_date = current_date + timedelta(days=remaining_years*365)
    return future_date
        
def build_validation_result(is_valid, violated_slot, message_content):
    """
    Defines an internal validation message structured as a python dictionary.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }

def validate_data(close_friend, self_eval, would_you_rather, risk_define, willingness, intent_request):
    """
    Validates the data provided by the user.
    """

    # Validate the amount, it should be > 0
    for response in close_friend, self_eval, would_you_rather, risk_define, willingness:
        
        if response is not None:
            response = parse_float(
                response
            )  # Since parameters are strings it's important to cast values
            if response <= 0 or > 4:
                return build_validation_result(
                    False,
                    "amount",
                    "The amount should be a number between 1 and 4, "
                    "please provide a correct response.",
                )

    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)
   
 ## Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response
     

def aggregate_client_score():
    close_friend, self_eval, would_you_rather, risk_define, willingness = client_risk_tolerance_info()
    return sum([close_friend, self_eval, would_you_rather, risk_define, willingness])
    
    
def client_risk_tolerance():
    risk_sum = aggregate_client_score()
    if isinstance(risk_sum, float) and 1 <= risk_sum <= 20:
        return risk_sum / 20
    else:
        return print("Your answers are not applicable, please input a value between 1-4 for each question")


def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
