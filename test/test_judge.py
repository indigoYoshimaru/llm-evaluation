from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, HallucinationMetric

easy_question = "Buymed là công ty lĩnh vực nào?"

easy_bad_output = "Buymed là công ty bất động sản"
easy_good_output = "Buymed là công ty start-up về chăm sóc sức khỏe"

context = ["""# Công ty Buymed

## a. Giới thiệu

Công ty TNHH Buymed được thành lập vào năm 2017, là một start-up hướng đến mục tiêu cách mạng hóa ngành chăm sóc sức khỏe trên toàn Châu Á. Buymed bắt đầu sứ mệnh của mình từ một văn phòng nhỏ tại Singapore và chỉ sau một thời gian ngắn, chúng tôi đã mở rộng thành một tổ chức đa quốc gia trong khu vực Đông Nam Á với quy mô hơn 500 nhân viên. Chúng tôi phát triển mạng lưới phân phối dược phẩm, sản phẩm chăm sóc sức khỏe và trang thiết bị vật tư y tế với nguồn cung 100% đến từ các nhà sản xuất uy tín trên toàn bộ Việt Nam và Đông Nam Á.

## b. Tầm nhìn

Trở thành nền tảng công nghệ y tế lớn nhất Đông Nam Á, tiên phong trong ứng dụng và phát triển công nghệ vào hệ thống y tế vì sức khỏe cộng đồng. Việc tiếp cận toàn cầu với dịch vụ chăm sóc sức khỏe chất lượng cao và chi phí hiệu quả là bước đệm đầu tiên hướng tới một tương lai phát triển hệ thống Y Tế tốt đẹp và bền vững. Chúng tôi tin vào tiềm năng của chuyển đổi kỹ thuật số đối với xã hội, điều này có thể được thực hiện hóa bằng cách kết hợp công nghệ vào chăm sóc sức khỏe.

## c. Sứ mệnh

Ứng dụng mô hình hiện đại nhất để giải quyết vấn đề y tế một cách nhanh chóng và chất lượng. Đối với khách hàng: Sử dụng công nghệ cung cấp các giải pháp đặt hàng dược phẩm và được giải quyết vấn đề nhanh chóng, chất lượng với các cam kết về nguồn gốc sản phẩm và hiệu quả chi phí. Đối với các đối tác: Cung cấp giải pháp nâng cao nhận diện thương hiệu và cơ hội mở rộng thị trường, giảm thiểu chi phí kho bãi, vận chuyển.
"""]

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