import pandas as pd
from django.shortcuts import get_object_or_404

from .calculate_indicators import map_responses_by_indicator
from ..models import EseaAccount, SurveyResponse, Question, QuestionResponse, IndirectIndicator, DirectIndicator

# import pandas as pd


def audit_data(eseaaccount_pk):
    print('this works!', eseaaccount_pk)

    # Get eseaaccount
    eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)

    # Get filled in survey responses
    survey_responses = SurveyResponse.objects.filter(esea_account=eseaaccount, finished=True)

    # Get question responses
    question_responses = QuestionResponse.objects.filter(survey_response__esea_account=eseaaccount, survey_response__finished=True)
    
    # indirect_indicators = IndirectIndicator.objects.filter(method=eseaaccount.method)
    # direct_indicators = DirectIndicator.objects.filter(method=eseaaccount.method)
    questions = DirectIndicator.objects.filter(method=eseaaccount.method)

    # map_responses_by_indicator(direct_indicators, question_responses)

    df = pd.DataFrame(columns = [ question.name for question in questions])
    df.insert(0, 'Respondent_id', [int(survey_response.respondent.id) for survey_response in survey_responses])
    # df.set_index('Respondent_id', inplace=True)
    for survey_response in survey_responses:
        questionresponses = QuestionResponse.objects.filter(survey_response=survey_response, survey_response__finished=True)
        for questionresponse in questionresponses:
            df.loc[df['Respondent_id'] == int(survey_response.respondent.id), [questionresponse.question.name]] = questionresponse.value
            
    pd.set_option('display.width', 40)
   
    print(df.tail(5))

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