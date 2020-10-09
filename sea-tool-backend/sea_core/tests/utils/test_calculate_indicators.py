from rest_framework.test import APITestCase
from typing import Dict
from sea_core.models import (
    IndirectIndicator,
    Topic,
    DirectIndicator,
    QuestionResponse,
    Question,
)
from sea_core.utils.calculate_indicators import calculate_indicators
from sea_core.classes import Indicator


class SurveyResponseTestCase(APITestCase):
    def test_calculate_indicators(self):
        indirect_indicator_1 = IndirectIndicator(
            id=1,
            topic=Topic(id=1),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] + [question_2]",
        )
        indirect_indicator_2 = IndirectIndicator(
            id=2,
            topic=Topic(id=1),
            name="calc_2",
            description="description of calc_2",
            formula="[question_3] * [question_4]",
        )
        indirect_indicator_3 = IndirectIndicator(
            id=3,
            topic=Topic(id=1),
            name="calc_3",
            description="description of calc_3",
            formula="[question_5] / [question_1]",
        )
        indirect_indicator_4 = IndirectIndicator(
            id=4,
            topic=Topic(id=1),
            name="calc_4",
            description="description of calc_4",
            formula="[question_2] - [question_4]",
        )
        indirect_indicator_5 = IndirectIndicator(
            id=5,
            topic=Topic(id=1),
            name="calc_5",
            description="description of calc_5",
            formula="[question_3] + [calc_1]",
        )

        direct_indicator_1 = DirectIndicator(
            id=1,
            topic=Topic(id=1),
            key="question_1",
            question=Question(id=1, type="NUMBER", name="question 1"),
        )
        direct_indicator_2 = DirectIndicator(
            id=2,
            topic=Topic(id=1),
            key="question_2",
            question=Question(id=1, type="NUMBER", name="question 2"),
        )
        direct_indicator_3 = DirectIndicator(
            id=3,
            topic=Topic(id=1),
            key="question_3",
            question=Question(id=1, type="NUMBER", name="question 3"),
        )
        direct_indicator_4 = DirectIndicator(
            id=4,
            topic=Topic(id=1),
            key="question_4",
            question=Question(id=1, type="NUMBER", name="question 4"),
        )
        direct_indicator_5 = DirectIndicator(
            id=5,
            topic=Topic(id=1),
            key="question_5",
            question=Question(id=1, type="NUMBER", name="question 5"),
        )
        indirect_indicators = [
            indirect_indicator_1,
            indirect_indicator_2,
            indirect_indicator_3,
            indirect_indicator_4,
            indirect_indicator_5,
        ]
        direct_indicators = {
            direct_indicator_1,
            direct_indicator_2,
            direct_indicator_3,
            direct_indicator_4,
            direct_indicator_5,
        }

        question_responses = {
            QuestionResponse(id=1, direct_indicator_id=1, value=0),
            QuestionResponse(id=2, direct_indicator_id=1, value=5),
            QuestionResponse(id=3, direct_indicator_id=1, value=10),
            QuestionResponse(id=5, direct_indicator_id=2, value=4),
            QuestionResponse(id=6, direct_indicator_id=2, value=6),
            QuestionResponse(id=7, direct_indicator_id=2, value=8),
            QuestionResponse(id=8, direct_indicator_id=3, value=4),
            QuestionResponse(id=9, direct_indicator_id=3, value=5),
            QuestionResponse(id=10, direct_indicator_id=3, value=6),
            QuestionResponse(id=11, direct_indicator_id=4, value=8),
            QuestionResponse(id=12, direct_indicator_id=4, value=9),
            QuestionResponse(id=13, direct_indicator_id=5, value=10),
            QuestionResponse(id=14, direct_indicator_id=5, value=20),
            QuestionResponse(id=15, direct_indicator_id=5, value=30),
        }

        expected_result = {
            "calc_1": {
                "calculation": "5.0 + 6.0",
                "value": 11,
                "responses": None,
            },
            "calc_2": {
                "calculation": "5.0 * 8.5",
                "value": 42.5,
                "responses": None,
            },
            "calc_3": {
                "calculation": "20.0 / 5.0",
                "value": 4,
                "responses": None,
            },
            "calc_4": {
                "calculation": "6.0 - 8.5",
                "value": -2.5,
                "responses": None,
            },
            "calc_5": {
                "calculation": "5.0 + 11.0",
                "value": 16,
                "responses": None,
            },
            "question_1": {
                "value": 5,
                "responses": [0, 5, 10],
                "calculation": None,
            },
            "question_2": {
                "value": 6,
                "responses": [4, 6, 8],
                "calculation": None,
            },
            "question_3": {
                "value": 5,
                "responses": [4, 5, 6],
                "calculation": None,
            },
            "question_4": {
                "value": 8.5,
                "responses": [8, 9],
                "calculation": None,
            },
            "question_5": {
                "value": 20,
                "responses": [10, 20, 30],
                "calculation": None,
            },
        }

        for direct_indicator in direct_indicators:
            direct_indicator.filter_responses(question_responses)

        result: Dict[str, Indicator] = calculate_indicators(
            indirect_indicators, direct_indicators
        )

        for key in expected_result.keys():
            self.assertEqual(
                result[key].calculation, expected_result[key]["calculation"]
            )
            self.assertEqual(result[key].value, expected_result[key]["value"])
            self.assertEqual(
                result[key].responses, expected_result[key]["responses"]
            )
