from django.db import models
from django.utils.translation import gettext_lazy as _
from .question import Question


class directIndicatorManager(models.Manager):
    def create(
        self,
        key,
        topic,
        name,
        type,
        options,
        description=None,
        prefix=None,
        suffix=None,
        default=None,
        max_number=None,
        min_number=None,
    ):
        question = Question.objects.get_or_create(
            name=name,
            type=type,
            options=options,
            description=description,
            prefix=prefix,
            suffix=suffix,
            default=default,
        )

        direct_indicator = DirectIndicator(
            key=key,
            max_number=max_number,
            min_number=min_number,
            question=question,
            topic=topic,
        )
        direct_indicator.save()
        return direct_indicator


class DirectIndicator(models.Model):
    objects = directIndicatorManager()
    key = models.CharField(max_length=45, blank=False)
    max_number = models.IntegerField(null=True)
    min_number = models.IntegerField(null=True)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    topic = models.ForeignKey(
        "Topic", related_name="direct_indicators", on_delete=models.PROTECT
    )
    responses = []
    value = None
    calculation_keys = None
    calculation = None

    class Meta:
        verbose_name = _("direct_indicator")
        verbose_name_plural = _("direct_indicators")

    @property
    def name(self):
        return self.question.name

    def __str__(self):
        return self.question.name

    def update(
        self,
        key,
        topic,
        name,
        type,
        options,
        description=None,
        prefix=None,
        suffix=None,
        default=None,
        max_number=None,
        min_number=None,
    ):
        self.key = key
        self.max_number = max_number
        self.min_number = min_number
        self.topic = topic
        self.question = self.question.update(
            name=name,
            type=type,
            options=options,
            description=description,
            prefix=prefix,
            suffix=suffix,
            default=default,
        )
        self.save()
        return self

    def filter_responses(self, responses):
        self.responses = [
            response.value
            for response in responses
            if response.direct_indicator_id == self.id
        ]
        self.value = self.get_average(self.responses)

    def get_average(self, responses=[]):
        response_values = responses
        if not len(responses):
            return "0"

        if (
            self.question.type == self.question.RADIO
            or self.question.type == self.question.CHECKBOX
        ):
            response_values = self.checkbox_values(responses)

        return self.average_calculation(response_values)

    def average_calculation(self, responses):
        numbers = [int(r) for r in responses]
        return sum(numbers) / len(numbers)

    def checkbox_values(self, responses):
        values = []
        for response in responses:
            options = response.split(",")
            for option in options:
                if option:
                    question_option = self.question.options.filter(text=option)
                    if len(question_option):
                        values.append(question_option[0].value)
        return values
