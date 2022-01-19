from django.shortcuts import get_object_or_404

from .calculate_indicators import map_responses_by_indicator, calculate_indicators, calculate_absolute_weights
from ..models import EseaAccount, DirectIndicator, IndirectIndicator, SurveyResponse, QuestionResponse
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
     

def calculate_scoring_scheme(eseaaccount_pk):
    eseaaccount = get_object_or_404(EseaAccount, pk=eseaaccount_pk)
    print(eseaaccount)
    try:
        certification_indicator = IndirectIndicator.objects.get(method=eseaaccount.method, type='certification')
        print(certification_indicator)
    except IndirectIndicator.DoesNotExist:
        return('There is no Certification Indicator!')

    # Get Method Indicators
    indirect_indicators = IndirectIndicator.objects.filter(method=eseaaccount.method)
    direct_indicators = DirectIndicator.objects.filter(method=eseaaccount.method)


    indicators_dict = {}
    for indirect_indicator in indirect_indicators:
        indicators_dict[indirect_indicator.key] =  indirect_indicator
    
    for direct_indicator in direct_indicators:
        indicators_dict[direct_indicator.key] = direct_indicator

    # indicators = calculate_indicator(certification_indicator, indicators_dict)

    required_indicators = find_connected_indicators(certification_indicator, indicators_dict)

    directindicators, indirectindicators = [], []
    for key in required_indicators:
        try:
            directindicators.append(DirectIndicator.objects.get(method=eseaaccount.method, key=key))
        except:
            try:
                indirectindicators.append(IndirectIndicator.objects.get(method=eseaaccount.method, key=key))
            except:
                print(key)

    print('++', json.dumps(calculate_absolute_weights(indicators_dict['total_organisation_score'], indicators_dict), sort_keys=True, indent=4))


    respondents = SurveyResponse.objects.filter(esea_account=eseaaccount_pk) #Respondent.objects.filter(organisation__esea_accounts=74)
    responses = SurveyResponse.objects.filter(esea_account=eseaaccount_pk, finished=True)

    question_responses = QuestionResponse.objects.filter(survey_response__esea_account=eseaaccount_pk, survey_response__finished=True)
    map_responses_by_indicator(direct_indicators, question_responses)

    indicators2 = calculate_indicators(indirect_indicators, direct_indicators)

    '''
    print(indirect_indicators)
    indicators = 
    for indicator in indicators.values():
        try:
            print('>>', indicator.expression, '-------->', indicator.value) #  indicator.calculation
        except:
            pass
    print('>>>>>>>>>>>>>>>>>>', indicators)
    '''
    indicators_dict2 = {}
    for indic in indicators2.values():
        print(indic.calculation)
        pass
        indicators_dict2[indic.key] = indic
    
    # print('====', indicators_dict['total_organisation_score'].formula)

    # print(calculate_absolute_weights(indicators_dict['total_organisation_score'], indicators_dict))
    print('++', json.dumps(calculate_absolute_weights(indicators_dict2['total_organisation_score'], indicators_dict2), sort_keys=True, indent=4))
    # print(json.dumps(calculate_absolute_weights(indicators_dict['total_organisation_score'], indicators_dict), sort_keys=True, indent=4))

    #for indicator in absolute_weights:
    #    
    return 'check'

    # indicators that aren't used for the certification_indicator
    #print(list(set(indicators_dict.keys()) - required_indicators))
    # calculate_indicators()

    # print(IndirectIndicator.objects.get(type='certification'))
    # check if certification indicator is present in method indicators
    # if yes --> get certification indicator
    # get list of connected indicators
    # get absolute weights
    # sort descending from absolute weights
    # 0.5 * 1, 0.4 * 10
    # loop through all indicators and omit them one by one and check if certification threshold is still 
    '''

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

