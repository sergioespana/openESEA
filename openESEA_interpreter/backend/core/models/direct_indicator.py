from django.db import models
from django.utils.translation import gettext_lazy as  _

from .question import Question
from .answer_option import AnswerOption


class directIndicatorManager(models.Manager):

    def create(self, method, key, name, datatype="Text", topic=None, description="", pre_unit="", post_unit="", question=None, answer_options=None, survey=None, wizard=False,
        answertype="TEXT", isMandatory=True, instruction="", default="", min_number=None, max_number=None, options=None):

        # If method creation wizard is used
        if wizard:
            question = Question.objects.create(name=name, isMandatory=isMandatory, answertype=answertype, topic=topic, description=description, instruction=instruction, default=default, min_number=min_number, max_number=max_number, options=options)

        direct_indicator = DirectIndicator(method=method, key=key, name=name, description=description, question=question, topic=topic, pre_unit=pre_unit, post_unit=post_unit, datatype=datatype)
        # magic save function that saves the indicator to the database
        direct_indicator.save()

        # if question is single/multiple choice
        if answer_options:
            for option in answer_options:
                answer_option, _ = AnswerOption.objects.get_or_create(order=option['Order'], text=option['Text'].lower())
                direct_indicator.options.add(answer_option.id)
                
        direct_indicator.save()

        if survey:
            survey.questions.add(direct_indicator)

        return direct_indicator


class DirectIndicator(models.Model):
    objects = directIndicatorManager()
    question = models.ForeignKey("Question", related_name="direct_indicator", on_delete=models.SET_NULL, null=True) # One to One field? question2 = models.OneToOneField("Question", on_delete=models.CASCADE, null=True, primary_key=False)
    method = models.ForeignKey("Method", related_name="direct_indicators", on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey("Topic", related_name="direct_indicators", on_delete=models.SET_NULL, blank=True, null=True)
    # options

    key = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True, default="")
    pre_unit = models.CharField(max_length=30, blank=True, default="") # Examples pre_unit: $,€.
    post_unit = models.CharField(max_length=30, blank=True, default="") #  Examples post_unit: %, points, persons
    cut_off_lower_limit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    cut_off_upper_limit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    TEXT = "text"
    INTEGER = "integer"
    DOUBLE = "double"
    DATE = "date"
    BOOLEAN = "boolean"
    SINGLECHOICE = "singlechoice" # UI: RadioButton, Scale, Dropdown
    MULTIPLECHOICE = "multiplechoice" # UI: Checkbox, Scale (1-3 on 1:10 scale for example)

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

    responses = []
    value = None
    calculation_keys = None
    calculation = None
    critical_impact_by = {}

    class Meta:
        verbose_name = _("direct_indicator")
        verbose_name_plural = _("direct_indicators")

    @property
    def question_name(self):
        if self.question:
            return self.question.name
        return ''

    def __str__(self):
        return self.name

    def update(self, key, name, answertype, topic=None, isMandatory=True, options=None, description=None, instruction=None, default=None, min_number=None, max_number=None, pre_unit="", post_unit="", cut_off_lower_limit=None, cut_off_upper_limit=None): # Add datatype?
        self.key = key
        self.topic = topic
        self.pre_unit = pre_unit
        self.post_unit = post_unit
        self.cut_off_lower_limit = cut_off_lower_limit
        self.cut_off_upper_limit = cut_off_upper_limit
        self.question = self.question.update(name=name, answertype=answertype, isMandatory=isMandatory, options=options, description=description, instruction=instruction, default=default, min_number=min_number, max_number=max_number)

        self.save()
        return self

    # Processes responses belonging to a single direct indicator
    def filter_responses(self, responses):
        self.responses = []

        for response in responses:
            if response.direct_indicator_id == self.id:
                if len(response.values.all()):
                    self.responses.append(response.values.all())
                else: 
                    self.responses.append(response.value)

        self.value = self.get_average(self.responses)

    # Processes responses dependent on the direct indicator's datatype
    def get_average(self, responses=[]):
        response_values = responses
        if not len(responses):
            return "0"

        if (
            self.datatype == self.SINGLECHOICE
            or self.datatype == self.BOOLEAN
            or self.datatype == self.MULTIPLECHOICE
        ):
            response_values = self.checkbox_values(responses)
            return response_values

        if (
            self.datatype == self.DATE or self.datatype == self.TEXT
        ) :
            newdict = {}
            for index, response  in enumerate(responses):
                newdict[index] = response
            return newdict


        return self.average_calculation(response_values)

    def average_calculation(self, responses):
        numbers = [int(r) for r in responses]
        return sum(numbers) / len(numbers)

    def checkbox_values(self, responses):
        valuesdict = {}

        for option in self.options.all():
            valuesdict[option.text] = 0
        for response in responses:
            if response:
                if self.datatype == self.MULTIPLECHOICE:
                    for item in response:
                        question_option = self.options.get(text=item.text)
                        valuesdict[question_option.text] += 1
                else:
                    try:
                        question_option = self.options.get(text=response)
                        valuesdict[question_option.text] += 1
                    except:
                        print('doesnt exist')
                        
        # Return single value if datatype is either singlechoice or boolean
        if (self.datatype == self.SINGLECHOICE or self.datatype == self.BOOLEAN):
            if self.question.section.survey.response_type == 'single':
                return max(valuesdict, key=valuesdict.get) if valuesdict else None
        return valuesdict



'''
- Should response_values not be returned to self.value (or self.values)?  [FIXED]

question (FK) - Should be change to 1to1
topic (FK)
key
name (= self.question.name)
indicator_name
(description)
(pre_unit)
(post_unit)
datatype
'''