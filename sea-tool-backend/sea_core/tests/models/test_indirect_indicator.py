from django.test import TestCase
from typing import Dict
from sea_core.models import IndirectIndicator, Topic


class IndirectIndicatorTestCase(TestCase):
    def test_calculation_keys(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] + [question_2]",
        )

        # outputs
        expected_result = ["question_1", "question_2"]

        # checking result values
        self.assertEqual(indirect_indicator.calculation_keys, expected_result)

    def test_calculation_keys_change(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] + [question_2]",
        )

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_final_calculation_keys = ["question_2"]

        # checking initial values
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.calculation = "1 + [question_2]"

        # checking result values
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_final_calculation_keys,
        )

    def test_find_values(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] + [question_2]",
        )
        question_responses: Dict[str, float] = {
            "question_1": 5,
            "question_2": 5.5,
        }

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_final_calculation_keys = []
        expected_initial_calculation = "[question_1] + [question_2]"
        expected_final_calculation = "5 + 5.5"

        # checking initial values
        self.assertEqual(
            indirect_indicator.calculation, expected_initial_calculation,
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)

        # checking result values
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_final_calculation_keys,
        )
        self.assertEqual(
            indirect_indicator.calculation, expected_final_calculation
        )

    def test_calculate_plus(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] + [question_2]",
        )
        question_responses: Dict[str, float] = {
            "question_1": 5,
            "question_2": 5.5,
        }

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_result_calculation = "5 + 5.5"
        expected_result_calculation_keys = []
        expected_result_value = 10.5
        expected_exception = type(None)

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_minus(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] - [question_2]",
        )
        question_responses: Dict[str, float] = {
            "question_1": 5,
            "question_2": 5.5,
        }

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_result_calculation = "5 - 5.5"
        expected_result_calculation_keys = []
        expected_result_value = -0.5
        expected_exception = type(None)

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_times(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] * [question_2]",
        )
        question_responses: Dict[str, float] = {
            "question_1": 5,
            "question_2": 5.5,
        }

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_result_calculation = "5 * 5.5"
        expected_result_calculation_keys = []
        expected_result_value = 27.5
        expected_exception = type(None)

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_divide(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] / [question_2]",
        )
        question_responses: Dict[str, float] = {
            "question_1": 10,
            "question_2": 5,
        }

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_result_calculation = "10 / 5"
        expected_result_calculation_keys = []
        expected_result_value = 2
        expected_exception = type(None)

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_multiple_operators(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] + [question_2] * [question_3] / [question_4]",
        )
        question_responses: Dict[str, float] = {
            "question_1": 10,
            "question_2": 5,
            "question_3": 5,
            "question_4": 10,
        }

        # outputs
        expected_initial_calculation_keys = [
            "question_1",
            "question_2",
            "question_3",
            "question_4",
        ]
        expected_result_calculation = "10 + 5 * 5 / 10"
        expected_result_calculation_keys = []
        expected_result_value = 12.5
        expected_exception = type(None)

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_condition_company_micro(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula='IF (([total_staff] + 1) < 10) THEN "micro" ELSE IF ([total_staff] < 49) THEN [question_2] ELSE "large"',
        )
        question_responses = {
            "total_staff": 8,
            "question_2": "small",
        }

        # outputs
        expected_initial_calculation_keys = [
            "total_staff",
            "total_staff",
            "question_2",
        ]
        expected_result_calculation = 'if ((8 + 1) < 10) then "micro" else if (8 < 49) then small else "large"'
        expected_result_calculation_keys = []
        expected_has_conditionals = True
        expected_result_value = "micro"
        expected_exception = None

        # checking initial values
        self.assertEqual(
            indirect_indicator.has_conditionals, expected_has_conditionals
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertEqual(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_condition_company_small(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula='IF (([total_staff] + 1) < 10) THEN "micro" ELSE IF ([total_staff] < 49) THEN [question_2] ELSE "large"',
        )
        question_responses = {
            "total_staff": 20,
            "question_2": "small",
        }

        # outputs
        expected_initial_calculation_keys = [
            "total_staff",
            "total_staff",
            "question_2",
        ]
        expected_result_calculation = 'if ((20 + 1) < 10) then "micro" else if (20 < 49) then small else "large"'
        expected_result_calculation_keys = []
        expected_has_conditionals = True
        expected_result_value = "small"
        expected_exception = None

        # checking initial values
        self.assertEqual(
            indirect_indicator.has_conditionals, expected_has_conditionals
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertEqual(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_condition_company_large(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula='IF (([total_staff] + 1) < 10) THEN "micro" ELSE IF ([total_staff] < 49) THEN [question_2] ELSE "large"',
        )
        question_responses = {
            "total_staff": 50,
            "question_2": "small",
        }

        # outputs
        expected_initial_calculation_keys = [
            "total_staff",
            "total_staff",
            "question_2",
        ]
        expected_result_calculation = 'if ((50 + 1) < 10) then "micro" else if (50 < 49) then small else "large"'
        expected_result_calculation_keys = []
        expected_has_conditionals = True
        expected_result_value = "large"
        expected_exception = None

        # checking initial values
        self.assertEqual(
            indirect_indicator.has_conditionals, expected_has_conditionals
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertEqual(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_condition_company_small_multi_line(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula='IF (([total_staff] + 1) < 10)\n THEN "micro"'
            '\n ELSE IF ([total_staff] < 49)\n THEN [question_2] \nELSE "large"',
        )
        question_responses = {
            "total_staff": 30,
            "question_2": "small",
        }

        # outputs
        expected_initial_calculation_keys = [
            "total_staff",
            "total_staff",
            "question_2",
        ]
        expected_result_calculation = 'if ((30 + 1) < 10) then "micro" else if (30 < 49) then small else "large"'
        expected_result_calculation_keys = []
        expected_has_conditionals = True
        expected_result_value = "small"
        expected_exception = None

        # checking initial values
        self.assertEqual(
            indirect_indicator.has_conditionals, expected_has_conditionals
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertEqual(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_divide_by_zero(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] / [question_2]",
        )
        question_responses: Dict[str, float] = {
            "question_1": 10,
            "question_2": 0,
        }

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_result_calculation = f"{question_responses['question_1']} / {question_responses['question_2']}"
        expected_result_calculation_keys = []
        expected_result_value = None
        expected_exception = Exception

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_without_operators(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] [question_2]",
        )
        question_responses: Dict[str, float] = {
            "question_1": 10,
            "question_2": 4,
        }

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_result_calculation = f"{question_responses['question_1']} {question_responses['question_2']}"
        expected_result_calculation_keys = []
        expected_result_value = None
        expected_exception = Exception

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_incorrect_formula(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] +++*/ [question_2]",
        )
        question_responses: Dict[str, float] = {
            "question_1": 10,
            "question_2": 7,
        }

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_result_calculation = f"{question_responses['question_1']} +++*/ {question_responses['question_2']}"
        expected_result_calculation_keys = []
        expected_result_value = None
        expected_exception = Exception

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_missing_response(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="calc_1",
            description="description of calc_1",
            formula="[question_1] + [question_2]",
        )
        question_responses: Dict[str, float] = {
            "question_2": 7,
        }

        # outputs
        expected_initial_calculation_keys = ["question_1", "question_2"]
        expected_result_calculation = (
            f"[question_1] + {question_responses['question_2']}"
        )
        expected_result_calculation_keys = ["question_1"]
        expected_result_value = None
        expected_exception = Exception

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)

    def test_calculate_incomplete_indirect_indicator(self):
        # inputs
        indirect_indicator: IndirectIndicator = IndirectIndicator(
            id=1,
            topic=Topic(id=1, name="test"),
            name="",
            description="",
            formula="",
        )
        question_responses: Dict[str, float] = {
            "question_2": 7,
        }

        # outputs
        expected_initial_calculation_keys = []
        expected_result_calculation = ""
        expected_result_calculation_keys = []
        expected_result_value = None
        expected_exception = Exception

        # checking initial values
        self.assertEqual(indirect_indicator.has_conditionals, False)
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_initial_calculation_keys,
        )

        # calling functions to test
        indirect_indicator.find_values(question_responses)
        indirect_indicator.calculate()

        # checking result values
        self.assertIsInstance(indirect_indicator.exception, expected_exception)
        self.assertEqual(
            indirect_indicator.calculation, expected_result_calculation
        )
        self.assertEqual(
            indirect_indicator.calculation_keys,
            expected_result_calculation_keys,
        )
        self.assertEqual(indirect_indicator.value, expected_result_value)
