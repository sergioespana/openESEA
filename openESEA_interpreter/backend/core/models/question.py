from __future__ import annotations
from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _


class questionManager(models.Manager):

    def create(self,  name, uiComponent, method=None, order=1, section=None, topic=None, indicator=None, isMandatory=True, answertype="TEXT", min_number=1, max_number=5, description="", instruction="", default="", options=None):
        question = Question(isMandatory=isMandatory, name=name, method=method, order=order, uiComponent=uiComponent, section=section, topic=topic, answertype=answertype, description=description, instruction=instruction, default=default, min_number=min_number, max_number=max_number)
        question.save()

        # Allows creation of a question and connection to a direct indicator in 1 go (used in method wizard)
        if indicator:
            from .direct_indicator import DirectIndicator
            indicator.question = question
            indicator.save(update_fields=['question'])

        return question
    
    # Checks if question already exists or creates a new one
    def get_or_create(self, **args):
        question = self.model.findQuestion(**args)
        if not question:
            question = self.model.objects.create(**args)
        return question


class Question(models.Model):
    objects = questionManager()

    method = models.ForeignKey("Method", related_name="questions", on_delete=models.CASCADE, null=True)
    section = models.ForeignKey('Section', related_name='questions', on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey('Topic', related_name="questions_of_topic", on_delete=models.SET_NULL, null=True)
    topics = models.ManyToManyField("Topic", through="DirectIndicator")
    
    order = models.IntegerField(default=1)
    isMandatory = models.BooleanField(default=True)

    name = models.CharField(max_length=511, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    instruction = models.TextField(max_length=1000, blank=True, null=True)

    default = models.CharField(max_length=255, blank=True, default="")
    min_number= models.IntegerField(blank=True, null=True)
    max_number = models.IntegerField(blank=True, null=True)

    TEXT = "Text"
    NUMBER = "Number"
    RADIO = "Radio"
    CHECKBOX = "Checkbox"
    SCALE = "Scale"

    QUESTION_TYPES = (
        (TEXT, "Text"),
        (NUMBER, "Number"),
        (RADIO, "Radio"),
        (CHECKBOX, "checkBox"),
        (SCALE, "scale"),
    )
    
    QUESTION_TYPES_WITH_OPTIONS = [RADIO, CHECKBOX, SCALE]
    answertype = models.CharField(max_length=100, blank=False, choices=QUESTION_TYPES, default="Text")

    FIELD = "field"
    LINE = "line"
    TEXTBOX = "textbox"
    CHECKBOX = "checkbox"
    DROPDOWN = "dropdown"
    RADIOBUTTON = "radiobutton"

    UI_COMPONENT_TYPES = (
        (FIELD, "field"),
        (LINE, "line"),
        (TEXTBOX, "textbox"),
        (CHECKBOX, "checkbox"),
        (DROPDOWN, "dropdown"),
        (RADIOBUTTON, "radiobutton")
    )
    UI_COMPONENTS_FOR_OPTIONS= [CHECKBOX, DROPDOWN, RADIOBUTTON]
    uiComponent = models.CharField(max_length=100, blank=False, choices=UI_COMPONENT_TYPES, default="Field")

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return self.name

    def __repr__(self) -> str:  # -> str?
        return (
            f"<Question id='{self.id}' name='{self.name}' "
            f"answertype='{self.answertype}'>"
        )

    def hasOptions(self, options) -> bool:
        if not self.options.count() == len(options):
            return False

        optionsExists = True
        for inputOption in options:
            for option in self.options.all():
                if inputOption["text"] == option.text:
                    break
            if not option.equal(inputOption):
                optionsExists = False
        return optionsExists

    # Checks if question already exists with the same amount of (answer) options
    def findQuestion(name, answertype, options, description=None) -> Any: # instruction = None
        questions = Question.objects.filter(name=name, answertype=answertype, description=description)
        for question in questions:
            if question.hasOptions(options):
                return question
        return False

    def update(self, isMandatory, name, answertype, options, min_number, max_number, description="", instruction="", default="") -> "Question":
        question: Question = Question.findQuestion(name, answertype, options, description)
        if question and question.id != self.id:
            self.delete()
            return question

        self.isMandatory = isMandatory
        self.name = name
        self.answertype = answertype
        self.description = description
        self.instruction = instruction
        self.default = default
        self.min_number = min_number
        self.max_number = max_number
        self.save()
        return self



    '''
    - Can i savely remove topic(s) fields from this model?
    - Remove answertype, made redundant because of instance.direct_indicator.datatype
    - Change isMandatory to required
    '''