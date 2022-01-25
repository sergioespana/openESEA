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


def recursive_weight_calculator(weight_dict, level=0, number=1, absolute_weights=[]):
    #print('-->', weight_dict.keys())
    
    level += 1
    #print('i, item', i, item)
    for indicator in weight_dict:
        #print('ind', weight_dict)

        if level == 1:
            number = 1

        try:
            weight = float(weight_dict[indicator]['weight'])
            # print(f'level {level}: {indicator}: {number} * {weight}')
            outcome = number*weight
            
            absolute_weights.append({'indicator': indicator, 'absolute': round(outcome, 3), 'level': level})
        except:
            weight=1
            absolute_weights.append({'indicator': indicator, 'level': level})
        # Checks if there's a sub indicator`
        
        if isinstance(weight_dict[indicator], dict) and len(weight_dict[indicator]['child'].keys()) > 1:
            number=weight
            new_dict = weight_dict[indicator]['child']  
            recursive_weight_calculator(new_dict, level, number, absolute_weights)

    level -= 1
            
    return absolute_weights


def calculate_scoring_scheme(eseaaccount_pk, indicators_dict=[], verbose=False):
    eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)

    if eseaaccount.method.certification_theshold is None:
        return(f"Method '{eseaaccount.method.name}' has no certification threshold!")
    '''
    if not indicators_dict:
        # Get Data
        indirect_indicators = IndirectIndicator.objects.filter(method=eseaaccount.method)
        direct_indicators = DirectIndicator.objects.filter(method=eseaaccount.method)
        
        indicators_dict = {}
        for indirect_indicator in indirect_indicators:
            indicators_dict[indirect_indicator.key] =  indirect_indicator

        for direct_indicator in direct_indicators:
            indicators_dict[direct_indicator.key] = direct_indicator

        # Get Responses
        question_responses = QuestionResponse.objects.filter(survey_response__esea_account=eseaaccount_pk, survey_response__finished=True)
        map_responses_by_indicator(direct_indicators, question_responses)

        # Calculate Indicators
        calculate_indicators(indirect_indicators, direct_indicators)
    '''

    # Find indirect indicator of type scoring that is not included in other scoring indicators
    total_score_indicator = indicators_dict['total_organisation_score']

    # Calculate Absolute Weights
    #json.dumps(weight_dict, sort_keys=True, indent=4)
    weight_dict = calculate_absolute_weights(total_score_indicator, indicators_dict)
    print(json.dumps(weight_dict, sort_keys=True, indent=4))
    absolute_weights = recursive_weight_calculator(weight_dict)
    print(json.dumps(absolute_weights, sort_keys=True, indent=4))

    #sorted_absolute_weights = sorted(absolute_weights, key = lambda i: i['absolute'], reverse=True)

    total_score = total_score_indicator.value
    for indicator in absolute_weights:
        if 'absolute' in indicator.keys():
            indicator_impact = indicator['absolute']*float(indicators_dict[indicator['indicator']].value)
            indicators_dict[indicator['indicator']].indicator_impact = indicator_impact
            indicators_dict[indicator['indicator']].scoring_level = indicator['level']
            indicators_dict[indicator['indicator']].absolute = indicator['absolute']
            indicators_dict


            corrected_total_score = total_score - indicator_impact
            if corrected_total_score < eseaaccount.method.certification_theshold:
                indicators_dict[indicator['indicator']].critical_impact = True

                # What indicators 

            if True: 
                print(f"impact = {total_score} - {indicator['absolute']} * {indicators_dict[indicator['indicator']].value}.")
                print(f"{indicator['indicator']} in level ({indicator['level']}) has an impact of {indicator_impact} on the total score({total_score}), corrected total score: {corrected_total_score}!")
                print(indicators_dict[indicator['indicator']].formula_keys)

    indicators_to_return = {}
    for indicator in indicators_dict:
        if (isinstance(indicators_dict[indicator], DirectIndicator) and (indicators_dict[indicator].question.section.survey.response_type == 'single')) or (isinstance(indicators_dict[indicator], IndirectIndicator) and (indicators_dict[indicator].type == 'performance')):
            indicators_to_return[indicator] = indicators_dict[indicator]

    return indicators_to_return




    '''
    # threshold = 3
    # filterThreshold = 0.5
    # <5 --> {1,2,3} {1,4} {3,4}
    # 1   8 - 1.2
    # 2   8 - 0.7
    # 3   8 - 1.4
    # 4   8 - 2.2
    # 5   8 - 0.2

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

