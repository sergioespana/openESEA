from django.shortcuts import get_object_or_404

from .calculate_indicators import map_responses_by_indicator, calculate_indicators, calculate_absolute_weights
from ..models import EseaAccount, DirectIndicator, IndirectIndicator, SurveyResponse, QuestionResponse
from pprint import pprint

import json


def find_connected_indicators(indicator, indicators, keys = set()):
    if isinstance(indicator, IndirectIndicator) and len(indicator.calculation_keys):
        for calculation_key in indicator.calculation_keys:
            keys.add(calculation_key)
            values = find_connected_indicators(indicators[calculation_key], indicators, keys)
            set.union(keys, values)
        return keys
    else:
        keys.add(indicator.key)
        return keys


def recursive_weight_calculator(weight_dict, number=1, absolute_weights=[]):
    for i, item in enumerate(weight_dict):
        for indicator in weight_dict[i]:
            weight = float(weight_dict[int(i)][indicator]['weight'])
            
            outcome = number*weight
            print(outcome, 'number', number, 'weight', weight)
            absolute_weights.append({'indicator': indicator, 'absolute': round(outcome, 3)})
            
            # Checks if there's a sub indicator
            if len(weight_dict[i][indicator]['child'][0]) > 1:
                number=weight
                new_dict = weight_dict[i][indicator]['child']
                recursive_weight_calculator(new_dict, number, absolute_weights)
        
            number = 1
            
    return absolute_weights


def calculate_scoring_scheme(eseaaccount_pk):
    eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)

    try:
        certification_indicator = IndirectIndicator.objects.get(method=eseaaccount.method, type='certification')
    except IndirectIndicator.DoesNotExist:
        return('There is no Certification Indicator!')

    # Get Method Indicators
    indirect_indicators = IndirectIndicator.objects.filter(method=eseaaccount.method)
    direct_indicators = DirectIndicator.objects.filter(method=eseaaccount.method)

    # Get Required Indicators
    indicators_dict = {}
    for indirect_indicator in indirect_indicators:
        indicators_dict[indirect_indicator.key] =  indirect_indicator

    for direct_indicator in direct_indicators:
        indicators_dict[direct_indicator.key] = direct_indicator

    required_indicators = find_connected_indicators(certification_indicator, indicators_dict)

    directindicators, indirectindicators = [], []
    for key in required_indicators:
        try:
            directindicators.append(DirectIndicator.objects.get(method=eseaaccount.method, key=key))
        except:
            indirectindicators.append(IndirectIndicator.objects.get(method=eseaaccount.method, key=key))

    # Get Responses
    respondents = SurveyResponse.objects.filter(esea_account=eseaaccount_pk)
    responses = SurveyResponse.objects.filter(esea_account=eseaaccount_pk, finished=True)
    question_responses = QuestionResponse.objects.filter(survey_response__esea_account=eseaaccount_pk, survey_response__finished=True)
    map_responses_by_indicator(direct_indicators, question_responses)

    # Calculate Indicators
    calculate_indicators(indirect_indicators, direct_indicators)

    # Calculate Absolute Weights
    # json.dumps(calculate_absolute_weights(indicators_dict['total_organisation_score'], indicators_dict), sort_keys=True, indent=4)
    weight_dict = calculate_absolute_weights(indicators_dict['total_organisation_score'], indicators_dict)
    absolute_weights = recursive_weight_calculator(weight_dict)
    sorted_absolute_weights = sorted(absolute_weights, key = lambda i: i['absolute'], reverse=True)

    for indicator in sorted_absolute_weights:
        print(indicator)
        # loop through all indicators and omit them one by one and check if certification threshold is still 
    
    return 'check'

    '''
    indicators that aren't used for the certification_indicator
    print(list(set(indicators_dict.keys()) - required_indicators))
    calculate_indicators()

    print(IndirectIndicator.objects.get(type='certification'))
    check if certification indicator is present in method indicators
    if yes --> get certification indicator
    get list of connected indicators
    get absolute weights
    sort descending from absolute weights
    0.5 * 1, 0.4 * 10

    [workplace_quality_score] = (0.3 * TUPLE_PAIR([public_salaries_score], 10)) + 0.3 * TUPLE_PAIR([public_salaries_score])


    total_organisation_score
    ii1 1 ( 0.6 * ii2 + 0.4 * ii3)
        absolute_weights: [ii2: 0.6, ii3: 0.4, ii4: 0,15, ii5: 0,45, ii6: 0,24]
        sorted_weights: [ii2: 0.6, ii5: 0.45, ii3: 0.4, ii6: 0.24, ii4: 0.15]
    - ii2 0.6 (0.25 * ii4 + 0.75 * ii5)
        absolute_weights: [ii4: 0.25, ii5: 0.75]
        sorted_weights: [ii5: 0.75, ii4: 0.25]
        - ii4 0.25
        - ii5 0.75
        - 
    - ii3 0.4 (if company_size > 100 then (0.4 * ii6) else (0.6 * ii6))   --> e.g company_size = 60                 ii6.weight = 0.6, 0.24
        absolute_weights: [ii6: 0.6]
        ii6
    
    # ii7 1 (0.2 * ii2)
    # - ii2 0.2
    '''

