from random import randint
import random
import string
import json

# 43 Overall satisfaction 1-10 DI 45
# 44 How inclusive do you think this company is? 1-5 DI 46,
# 47 What is your age?
# 48 How many years have you been involved in company?
# 49 What is your yearly salary?
# 50 I feel save at work on a scale from 1-10.
# I feel as if my company contributes to a better working world. (scale 1-10).


# These parameters will have to be filled in correctly!
# Required Parameters
organisation_pk = 7
esea_account_pk = 6
survey_pk = 7

# pk's shouldn't already exist in the current data!
# Start of your PK's
respondent_pk = 100
questionresponse_pk = 100
surveyresponse_pk = 100
answeroption_pk = 100

def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

jsondata = []

# Create Multiple Respondent Survey Respondents
for i in range(20):
    # Create Respondent
    respondent = {
            "model": "core.respondent",
            "pk": respondent_pk,
            "fields": {
                "organisation": organisation_pk,
                "email": f"{random_char(6)}@gmail.com",
                "first_name": f"{random_char(5)}",
                "last_name_prefix": "",
                "last_name": f"{random_char(8)}"
            }
        }

    jsondata.append(respondent)

    # Create Survey Response
    surveyresponse = {
            "model": "core.surveyresponse",
            "pk": surveyresponse_pk,
            "fields": {
                "survey": survey_pk,
                "esea_account": esea_account_pk,
                "respondent": respondent_pk,
                "token" : "".join(random.choice(string.ascii_letters) for i in range(10)),
                "finished": True
            }
        }

    jsondata.append(surveyresponse)

    # Add the question id's as dictionary keys with the corresponding directindicatorid
    dictionary = {
            '43': {'value': randint(1, 10), 'directindicator': 45},
            '44': {'value': randint(1, 10), 'directindicator': 46},
            '47': {'value': randint(18, 67), 'directindicator': 49},
            '48': {'value': randint(0, 35), 'directindicator': 50},
            '49': {'value': (randint(100, 1200)* 100), 'directindicator': 47},
            '50': {'value': randint(1, 10), 'directindicator': 48},
            '51': {'value': randint(1, 10), 'directindicator': 51}
        }

    # Create random generated Question Responses
    for key in dictionary:
        questionresponse = {
            'model': 'core.questionresponse',
            'pk': questionresponse_pk,
            'fields':
                {
                    'survey_response': surveyresponse_pk,
                    'question': int(key),
                    'direct_indicator_id': dictionary[key]['directindicator'],
                    'value': dictionary[key]['value'],
                    'values': []
                }
        }
        jsondata.append(questionresponse)

        questionresponse_pk += 1
    surveyresponse_pk += 1
    respondent_pk += 1
for item in jsondata:
    print(item)

# Writing to sample.json
with open('app.json', 'w', encoding='utf-8') as f:
    json.dump(jsondata, f, ensure_ascii=False, indent=4)
