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
    cut_off_lower_limit = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    cut_off_upper_limit = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    
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
    CERTIFICATION = "certification"

    INDICATOR_TYPES = (
        (PERFORMANCE, "performance"),
        (SCORING, "scoring"),
        (CERTIFICATION, "certification")
    )
    
    type = models.CharField(max_length=50, blank=False, choices=INDICATOR_TYPES, default="scoring")

    calculation = ''
    absolute_weights = []
    indicator_impact = None
    value = None
    has_conditionals = False
    exception = None
    exception_detail = None
    responses = None
    
    # used to find absolute weights
    expression = ''

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
        calculation_keys =  re.findall(find_square_bracket_keys, self.calculation) #self.formula.replace("\n", ""))
        # print('*****************************', self.formula, self.calculation, calculation_keys)
        calculation_keys_uniques = list(set(calculation_keys))

        if self.key in calculation_keys_uniques:
            calculation_keys_uniques.remove(self.key)
        return calculation_keys_uniques


    # Used for calculation of absolute weights
    @property
    def formula_keys(self):
        formula_keys = re.findall(find_square_bracket_keys, self.formula)
        calculation_keys_uniques = list(set(formula_keys)) 

        if self.key in calculation_keys_uniques:
            calculation_keys_uniques.remove(self.key)
        return calculation_keys_uniques

    def find_weights(self, weight_dict):
        print('---->', self.key, weight_dict)
        self.absolute_weights = [weight_dict]

        return self.absolute_weights

        # # (0.3 * [gender_equity_score]) + (0.4 *[environmental_impact_score]) + (0.3 *[workplace_quality_score])
        # # re.compile(r"\* \[(.*?)\]")
        # weight_finder_regex = re.compile(r"[0-9].?\d*\s*\*\s*\[.*?\]")

        # indicatorweights = re.findall(weight_finder_regex, self.formula)

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
                self.expression = self.formula
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

        full_formula = self.formula.replace('IF', '@@IF').replace('ELSE', '##ELSE').replace('THEN', '%%THEN')
        full_formula = [x.strip() for x in re.split('@@|##|%%', full_formula)]
        full_formula = list(filter(lambda x: x != '', full_formula))

        ifs = 1
        elses = 0
        last_if = False
        search_else = False
        val = None

        for i, cond in enumerate(formula):
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
                
                print('====', self.key, val)
                if self.key == 'workplace_quality_score':
                    print('---->', full_formula[i])
                self.expression = full_formula[i]
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