import pandas as pd
import numpy as np
import os

from django.shortcuts import get_object_or_404

from .calculate_indicators import map_responses_by_indicator, calculate_indicators, merge_indicators
from .audit_benfords_law import calculate_benfords_law
from .audit_scoring_scheme import calculate_scoring_scheme
from .audit_iso_forest import calculate_iso_forest
from .audit_outlier_detection import outlier_detection
from ..models import EseaAccount, SurveyResponse, Question, QuestionResponse, IndirectIndicator, DirectIndicator



def audit_data(eseaaccount_pk):
    print('this works!', eseaaccount_pk)

    eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)

    direct_indicators = DirectIndicator.objects.filter(method=eseaaccount.method)
    indirect_indicators = IndirectIndicator.objects.filter(method=eseaaccount.method)
    indicators = merge_indicators(direct_indicators, indirect_indicators)

    df = pd.DataFrame({indicator.key: [] for indicator in indicators.values()}) 

    # Right now only has the esea account itself, should contain all esea accounts belonging to an esea method
    organisation_list = [eseaaccount]

    for organisation in organisation_list:
        question_responses = QuestionResponse.objects.filter(survey_response__esea_account=eseaaccount_pk, survey_response__finished=True)
        map_responses_by_indicator(direct_indicators, question_responses)
        indicators = calculate_indicators(indirect_indicators, direct_indicators)

        account_dict = dict()
        for indicator in indicators.values():
            if not indicator.value:
                value = np.nan
            else:    
                value = indicator.value

            account_dict[indicator.key] = value

        account_dict['organisation_id'] = organisation.organisation
        df = df.append(account_dict, ignore_index=True)

    df = df.set_index('organisation_id')
    print('===>', df)

    ## Use outlier detection methods on the above created dataframe

    if False:
        pathname = os.getcwd() + '/uploadedfiles/XES_esea.csv'
        df = pd.read_csv(pathname, delimiter=';', quotechar='|')
        df = df.set_index('Org')
        
        eseaaccount = print(df.index[0])

    # per esea method (all esea accounts + indicators)
    # iso_df = calculate_iso_forest()

    iso_df = df
    iso_row = []
    if (iso_df.index == eseaaccount.organisation).any():
        iso_row = iso_df.loc[eseaaccount.organisation]

    def create_boxplot(data):
        # create boxplot
        return boxplot

    indicators = direct_indicators + indirect_indicators

    # For now, with our dummy .csv dataset
    
    indicators = df.columns[1:]

    print('---->', df[indicators[0]])
    # 'recommended audit' per question that has numerical values
    for indicator in indicators:
        if indicator.datatype in ['integer', 'double']:
            boxplot = create_boxplot(data[indicator])
            
            benfordslaw = calculate_benfords_law(data[indicator_column])
            outliers = outlier_detection(data[indicator.key])

            # Check if indicator/company combination is found in iso dataframe
            iso_forest = True if indicator.key in iso_row.index else False 
            scoring_scheme = calculate_scoring_scheme()

        # return indicators with for each (boxplot, benfordslaw, outliers, iso_forest, scoring_scheme)
        indicators =  [
            {
                'indicator': 1,
                'boxplot': 'boxplot_image',
                'benfordslaw': {
                        'value': 'Bool (1 or 0)',
                        'image': 'benfordslaw_image'
                    },
                'outliers': 'outliers (= 1 or 0)',
                'iso_forest': 'iso_forest (= 1 or 1)',
                'scoring_scheme': '' # ID of indicator with highest absolute score if it impacts total score and thus certification indicator
            }
        ]









    '''
    # Get eseaaccount
    eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)

    # Get filled in survey responses
    survey_responses = SurveyResponse.objects.filter(esea_account=eseaaccount, finished=True)

    # Get question responses
    question_responses = QuestionResponse.objects.filter(survey_response__esea_account=eseaaccount, survey_response__finished=True)
    
    # indirect_indicators = IndirectIndicator.objects.filter(method=eseaaccount.method)
    # direct_indicators = DirectIndicator.objects.filter(method=eseaaccount.method)
    questions = Question.objects.filter(method=eseaaccount.method)

    # map_responses_by_indicator(direct_indicators, question_responses)

    df = pd.DataFrame(columns = [ question.name for question in questions])
    df.insert(0, 'Response_id', [int(survey_response.id) for survey_response in survey_responses])
    df.insert(1, 'Survey', [survey_response.survey.name for survey_response in survey_responses])
    # df.set_index('Respondent_id', inplace=True)
    for survey_response in survey_responses:
        questionresponses = QuestionResponse.objects.filter(survey_response=survey_response, survey_response__finished=True)
        for questionresponse in questionresponses:
            print(questionresponse.question.name, questionresponse.value)
            df.loc[df['Response_id'] == int(survey_response.id), [questionresponse.question.name]] = questionresponse.value
            # print(df[questionresponse.question.name])

    # pd.set_option('display.width', 20, 'max_colwidth', 800)
    print(df)
   
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


        anomalies = []
    '''