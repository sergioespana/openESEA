from django.db import models
import re
import statistics

from .direct_indicator import DirectIndicator
from .question_response import QuestionResponse


find_square_bracket_keys = re.compile(r"\[(.*?)\]")


class IndirectIndicator(models.Model):
    topic = models.ForeignKey('Topic', related_name='indirect_indicators', on_delete=models.SET_NULL, null=True)
    method = models.ForeignKey("Method", related_name="indirect_indicators", on_delete=models.CASCADE, null=True)
    key = models.CharField(max_length=255, blank=False)
    formula = models.CharField(max_length=1000, unique=False, blank=False)
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(blank=True, null=True)
    pre_unit = models.CharField(max_length=30, blank=True, default="")      # Examples: $,€
    post_unit = models.CharField(max_length=30, blank=True, default="")     # Examples: %, points, persons
    
    TEXT = "text"
    INTEGER = "integer"
    DOUBLE = "double"
    DATE = "date"
    BOOLEAN = "boolean"
    SINGLECHOICE = "singlechoice"
    MULTIPLECHOICE = "multiplechoice"
    

    DATA_TYPES = (
        (TEXT, "text"),
        (INTEGER, "integer"),
        (DOUBLE, "double"),
        (DATE, "date"),
        (BOOLEAN, "boolean"),
        (SINGLECHOICE, "singlechoice"),
        (MULTIPLECHOICE, "multiplechoice")
    )

    datatype = models.CharField(max_length=50, blank=False, choices=DATA_TYPES, default="text")
    
    PERFORMANCE = "performance"
    SCORING = "scoring"

    INDICATOR_TYPES = (
        (PERFORMANCE, "performance"),
        (SCORING, "scoring")
    )
    
    type = models.CharField(max_length=50, blank=False, choices=INDICATOR_TYPES, default="SCORING")

    calculation = ''
    value = None
    has_conditionals = False
    exception = None
    exception_detail = None
    responses = None

    class Meta: 
        unique_together = ['key', 'method']

    def __init__(self, *args, **kwargs):
        super(IndirectIndicator, self).__init__(*args, **kwargs)
        self.calculation = self.formula.replace("\n", "")

        if self.calculation.strip().startswith("IF"):
            self.has_conditionals = True
    
    def __str__(self):
        return self.key
    
    # calculation_keys are all indicators that are used within the formula of this indirect indicator
    @property
    def calculation_keys(self):
        calculation_keys =  re.findall(find_square_bracket_keys, self.calculation)
        calculation_keys_uniques = list(set(calculation_keys))

        if self.key in calculation_keys_uniques:
            calculation_keys_uniques.remove(self.key)
        return calculation_keys_uniques

    # Replaces indicator keys with corresponding value to be able to calculate the indirect indicator (used in 'utils > calculate_indicators')
    def find_values(self, key_value_list):
        calculation = self.calculation
        # print('===', self.key, '--', calculation_key, key_value_list[calculation_key])
        if not None in key_value_list.values():
            for calculation_key in self.calculation_keys:
                if calculation_key in key_value_list:
                    value = key_value_list[calculation_key]
                    if isinstance(value, dict):
                        value = max(value, key=value.get)
                    calculation = calculation.replace(f"[{calculation_key}]", f"{value}")
            self.calculation = calculation
        else:
            print('Missing values in key_value_list!')

    # Calculates indicator formula
    def calculate(self):
        if len(self.calculation_keys) and not self.has_conditionals:
            self.exception = Exception("Not all keys are replaced with values")
            return

        self.exception = None
        self.error = None
        functionList = ['sum(', 'avg(', 'min(', 'max(', 'median(', 'mode(']

        # If there are conditionals
        if self.has_conditionals:
            self.value = None
            value = self.calculate_conditionals()
            self.value = value
        
        # if there's a function
        elif any(func in self.calculation for func in functionList):
            key = re.findall(find_square_bracket_keys, self.formula)
            if len(key):
                question_responses = QuestionResponse.objects.filter(survey_response__esea_account=4, survey_response__finished=True)
                directind = DirectIndicator.objects.filter(method=self.method, key=key[0]).first()
                indirectind = IndirectIndicator.objects.filter(method=self.method, key=key[0]).first()
                if directind is not None:
                    indicator = directind
                    indicator.filter_responses(question_responses)
                    responses = [float(r) for r in indicator.responses]

                    if 'avg(' in self.calculation:
                        print('cheeeeeck', self.calculation)
                        self.value = sum(responses)/len(responses) # int(direct_indicator.value)
                    elif 'sum(' in self.calculation:
                            self.value = sum(responses)
                    elif 'min(' in self.calculation:
                        self.value = min(responses)
                    elif 'max(' in self.calculation:
                        self.value = max(responses)
                    elif 'median(' in self.calculation:
                        self.value = statistics.median(responses)
                    elif 'mode(' in self.calculation:
                        self.value = statistics.mode(responses)
                else:
                    self.value = 1
                    print('There are no responses to calculate the sum with.')
                    return

        # If a regular calculation can be performed
        else:
            try:
                self.value = eval(self.calculation)
                return self.value
            except Exception as e:
                print('error!', self.calculation, self.has_conditionals)
                self.value = None

    # Calculates conditional formulas (IF..THEN..)
    def calculate_conditionals(self):
        formula = self.calculation.replace('IF', '@@IF').replace('ELSE', '##ELSE').replace('THEN', '%%THEN')
        formula = [x.strip() for x in re.split('@@|##|%%', formula)]
        formula = list(filter(lambda x: x != '', formula))
        print(f'\n  {self.key}:::::::::: Start Conditional Calculations... \nformula: {formula}')

        ifs = 1
        elses = 0
        last_if = False
        search_else = False
        val = None

        for cond in formula:
            bracket_keys = list(set(re.findall(find_square_bracket_keys, cond)))

            if self.key in bracket_keys:
                bracket_keys.remove(self.key)
            if len(bracket_keys):
                print('Invalid Partial Condition: ', bracket_keys)
                # raise Exception("invalid partial condition")

            # Skips code till it finds the corresponding then/else statements corresponding to the IF statement that fails or succeeds.
            if search_else:
                if 'IF' in cond:
                    ifs += 1
                if 'ELSE' in cond:
                    elses += 1
                if ifs != elses:
                    continue
                else:
                    search_else = False
                    last_if = True
                    ifs = 1
                    elses = 0

            # Checks whether if statement equates to True
            if 'IF' in cond:
                cond = cond.replace('IF', '').replace('(', '').replace(')', '').replace('"', '').strip()
                last_if = False
                
                if 'AND' in cond:
                    conds = cond.split("AND")
                    conds = self.process_expression(conds)
                    evaluatedconds = [eval(n) for n in conds]

                    if not False in evaluatedconds:
                        last_if = True
                    else:
                        search_else = True
                    continue
                
                if 'OR' in cond:
                    conds = cond.split("OR")
                    conds = self.process_expression(conds)
                   
                    evaluatedconds = [eval(n) for n in conds]      

                    if True in evaluatedconds:
                        last_if = True
                    else:
                        search_else = True
                    continue

                
                cond = self.process_expression(cond)
                
                if eval(cond):
                    last_if = True
                else:
                    search_else = True
                continue

            # Serves conditional outcome
            if (last_if and '=' in cond) or (cond == formula[-1]):
                cond = cond.replace('(', '').replace(')', '')
                [var, val] = cond.split('=')
                var = var.replace('THEN', '').replace('ELSE', '')
                var = var.replace('[', '').replace(']', '').strip()
                if var != self.key:
                    raise Exception('Assignment variable does not match the key of this indirect indicator')
                val = val.replace('"', '')
                try:
                    val = eval(val)
                except:
                    pass

                return str(val)
        
    def process_expression(self, conds):
        allowedOperators = ['<', '<=', '==', '>=', '>', '=']

        if not isinstance(conds, list):
            conds = [conds]

        for index, cond in enumerate(conds):
            # cond = cond.replace('=', '==')
            processed_cond = re.split('(<|<=|==|>=|>|=)', cond)
            for idx, value in enumerate(processed_cond):
                if value not in allowedOperators:
                    # Makes eval() of string equals string possible
                    processed_cond[idx] = f'"{value.strip().lower()}"'
            conds[index] = ''.join(processed_cond)

        if len(conds) == 1:
            conds = conds[0]

        return conds