# Succes
# ..from models import specificmodel

# import pandas as pd


def audit_data(eseaaccount):
    print('this works!', eseaaccount)
    # Create a little bit of everything multiple respondent survey questions
        # -What is your avg. monthly salary?
        # -What is your avg. yearly salary?
        # -What is your age?
        # -How many years are you involved in X company?
        # -Satisfaction level? (1 to 10)
    # Create 100 Respondents/Survey Response with randomised values throug a script (or the shell)

    # ESEA Account belongs to an ESEA method (through a campaign)
    # All Surveys belonging to the Method
    # All questions belonging to a survey
    # All accountant responses belonging to single response survey
    # All respondent responses belonging to a multi respondent survey

    # Create Aggregrated data for the csv

    # for indicator in indicators.values():
    #     print(indicator.name, indicator.value)

        # DirectIndicator.objects.filter(datatype=)

    # eseaaccount.objects.get(organisation=organisation_id, campaign=campaign_id)
    # sr_list = surveyresponse.objects.filter(eseaaccount=eseaaccount)
    # for sr in sr_list:
    #     question_list = question.objects.filter(survey=sr.survey)
    #     for question in question_list:
    #         questionresponse.objects.filter(question__survey=survey)

    #         question_response > question > survey