from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, HallucinationMetric
from test.view_golden import read_json

dataset = read_json("dataset/20240415_114301.json")

easy_question = "Buymed là công ty lĩnh vực nào?"

easy_bad_output = "Buymed là công ty bất động sản"
easy_good_output = "Buymed là công ty start-up về chăm sóc sức khỏe"

# def test_answer_relevancy():
#     answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)
#     test_case = LLMTestCase(
#         input="What if these shoes don't fit?",
#         # Replace this with the actual output of your LLM application
#         actual_output="We offer a 30-day full refund at no extra cost."
#     )
#     assert_test(test_case, [answer_relevancy_metric])

def test_answer_hallucination():
    metric_params = dict(
        threshold = 0.5, 
        model = 'gpt-3.5-turbo-0125', 
    )
    hallucination = HallucinationMetric(**metric_params)
    answer_relevancy = AnswerRelevancyMetric(**metric_params)
    metrics = [HallucinationMetric(**metric_params), 
               AnswerRelevancyMetric(**metric_params),
               ]
    # good test case
    test_case = LLMTestCase(
        input=easy_question,
        actual_output = easy_good_output, 
        context = context, 
    )

    # bad test case
    bad_case = LLMTestCase(
        input=easy_question,
        actual_output = easy_bad_output, 
        context = context, 
    )
    print(bad_case.expected_output)

    # assert_test(test_case, [hallucination, answer_relevancy])
    # assert_test(bad_case, [hallucination, answer_relevancy])
    for metric in metrics: 
        result = metric.measure(bad_case)
        print(result)

    return bad_case

print(test_answer_hallucination())