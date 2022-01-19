from typing import Dict, List
from ..models import DirectIndicator, IndirectIndicator
from ..classes import Indicator

import re


def calculate_indicators(direct_indicators) -> Dict[str, Indicator]:
    indicators = {}

    for direct_indicator in direct_indicators:
        indicators[direct_indicator.key] = direct_indicator.value
        #for response in direct_indicator.responses:
            # print(response.all())
        #indicators[direct_indicator.key] = direct_indicator.responses
    return indicators


def calculate_indicators(indirect_indicators: List[IndirectIndicator], direct_indicators: List[DirectIndicator],) -> Dict[str, Indicator]:
    indicators = merge_indicators(indirect_indicators, direct_indicators)
    # for indicator in indicators.values():
    #     calculate_indicator(indicator, indicators)
    
    #print(type(indicators))
    for indicator in indicators.values():
        if indicator.value is None:
            calculate_indicator(indicator, indicators)

    for indicator in indicators.values():
        if indicator.value is None:
            calculate_indicator(indicator, indicators)

    for indicator in indicators.values():
        calculate_absolute_weights(indicator, indicators)

        # if indicator.key == 'organisation_certification':
        #     print('>>>>>>>>>>>>>>>>>>>>>>> expression', indicator.absolute_weights)

    # for indicator in indicators.values():
    #     if indicator.value is None:
    #         calculate_indicator(indicator, indicators)

    return indicators


# Recursive formula that calculates an indicator based on its formula while finding the indicator values that are required in the formula
def calculate_indicator(indicator, value_list) -> str:
    if indicator.value:
        return indicator.value
        
    elif isinstance(indicator, DirectIndicator):
        print('this is a direct indicator')
    elif not len(indicator.calculation_keys):
        return indicator.calculate()
    else:
        values = {}

        for calculation_key in indicator.calculation_keys:
            child_indicator = value_list[calculation_key]
            values[child_indicator.key] = calculate_indicator(
               child_indicator, value_list
            )

        indicator.find_values(values)
        outcome = indicator.calculate()

        return outcome


def calculate_absolute_weights(indicator, indicator_list) -> str:
    weight_dict = {}

    if isinstance(indicator, IndirectIndicator) and len(indicator.formula_keys):
        weight_finder_regex = re.compile(r"0.\d*\s*\*\s*\[.*?\]") # [0-9].?\d*\s*\*\s*\[.*?\]
        
        indicatorweights = re.findall(weight_finder_regex, indicator.expression)

        for indicatorweight in indicatorweights:
            weight, indicatorkey = indicatorweight.split("*")
            indicatorkey = indicatorkey.strip()[1:-1]
            weight_dict[indicatorkey] = {'indicator': indicatorkey, 'weight': weight }
            child_indicator = indicator_list[indicatorkey]

            weight_dict[indicatorkey]['child'] = calculate_absolute_weights(child_indicator, indicator_list)
        
        absolute_weights = indicator.find_weights(weight_dict)

        return absolute_weights


def map_responses_by_indicator(direct_indicators, question_responses) -> None:
    for direct_indicator in direct_indicators:
        direct_indicator.filter_responses(question_responses)


# TODO: Remove function when direct and indirect indicators are merged.
def merge_indicators(
    indirect_indicators: List[IndirectIndicator],
    direct_indicators: List[DirectIndicator],
) -> Dict[str, Indicator]:
    indicators = {}

    for indirect_indicator in indirect_indicators:
        indicators[indirect_indicator.key] = indirect_indicator

    for direct_indicator in direct_indicators:
        indicators[direct_indicator.key] = direct_indicator

    return indicators