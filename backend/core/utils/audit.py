import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import os
from pprint import pprint
import warnings

from django.shortcuts import get_object_or_404

from .calculate_indicators import map_responses_by_indicator, calculate_indicators, merge_indicators
from .audit_benfords_law import calculate_benfords_law
from .audit_scoring_scheme import calculate_scoring_scheme
from .audit_iso_forest import calculate_iso_forest
from .audit_outlier_detection import outlier_detection
from ..models import EseaAccount, SurveyResponse, Question, QuestionResponse, IndirectIndicator, DirectIndicator


def audit_data(eseaaccount_pk, verbose=False, boxplot=False):
    eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)
    eseaaccount21 = get_object_or_404(EseaAccount, pk=21) # hardcoded esea accounts for now

    df = pd.DataFrame({})

    # Right now only there's only one other hardcoded esea account, should contain all esea accounts belonging to an esea method
    other_organisations = [eseaaccount21] # eseaaccount21
    organisation_list = other_organisations + [eseaaccount] # eseaaccount21

    for organisation in organisation_list:
        print('\n----------->----------->', organisation)

        # Get Data
        direct_indicators = DirectIndicator.objects.filter(method=organisation.method)
        indirect_indicators = IndirectIndicator.objects.filter(method=organisation.method)
        question_responses = QuestionResponse.objects.filter(survey_response__esea_account=organisation.pk, survey_response__finished=True)

        # Run Scripts on Data
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

    plotspath = os.getcwd() + '/uploadedfiles/plots/'
    
    # 'recommended audit' per question that has numerical values
    warnings.filterwarnings('ignore')
    for indicator in indicators.values():
        if indicator.datatype in ['integer', 'double']:
            try:
                if indicator.datatype == 'integer':
                    indicator_array = df.loc[:, indicator.key].astype(int)
                if indicator.datatype == 'double':
                    indicator_array = df.loc[:, indicator.key].astype(float)
            except ValueError as error:
                print('audit.py - type conversion', error)

            if verbose:
                print('>>>', df.loc[:, indicator.key])
                print(indicator.key, indicator.datatype, '\n')
            
            # Boxplot
            if boxplot:
                sns.boxplot(x=indicator_array)
                plt.savefig(plotspath + f'{indicator.key}.png')
                plt.close()
            
            # Outliers
            outliers = outlier_detection(eseaaccount.organisation, indicator, indicator_array, verbose=verbose)
            indicators[indicator.key].outliers = outliers

    warnings.filterwarnings('default')

    # Calculate Scoring Scheme
    result = calculate_scoring_scheme(eseaaccount_pk, indicators_dict=indicators, verbose=verbose)

    return result