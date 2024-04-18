from typing import Text
from loguru import logger
from pydantic import BaseModel


class CustomSynthesizeTemplate(BaseModel):
    @staticmethod
    def generate_synthetic_data(context: Text, max_goldens_per_context: Text):
        pass


class QATemplate(CustomSynthesizeTemplate):

    # I hate this but we need to use static method to map to the deepeval's template :)
    @staticmethod
    def generate_synthetic_data(context: Text, max_goldens_per_context: Text):
        #     prompt = f"""I want you act as a copywriter. Based on the given context, which is list of strings, please generate a list of JSON objects with a `input` key.
        #         The `input` must be a question that can be addressed by the given context.

        #         **
        #         IMPORTANT: Please make sure to only return in JSON format, with the 'data' key as a list of JSON objects.
        #         You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting reptitive.

        #         Example context: ["Einstein đạt giải Nobel nhờ phát hiện ra penicillin.", "Einstein đạt giải Nobel vào năm 1968."]
        #         Example max goldens per context: 2
        #         Example JSON:
        #         {{
        #             "data": [
        #                 {{
        #                     "input": "Einstein nổi tiếng nhờ gì?"
        #                 }},
        #                 {{
        #                     "input": "Einstein đạt giải Nobel năm nào?"
        #                 }}
        #             ]
        #         }}

        #         `input` MUST be in VIETNAMESE, if not, please translate it to VIETNAMESE!
        #         Kết quả trả về phải ở tiếng Việt!!
        #         You should NOT incorporate any prior knowledge you have and take each context at face value.
        #         You MUST include at least one question as the input.
        #         `input` MUST be a STRING.
        #         You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting reptitive.
        #         **

        #         Max Goldens Per Context:
        #         {max_goldens_per_context}

        #         Context:
        #         {context}

        #         JSON:
        #         """

        prompt = f"""Tôi muốn bạn đóng vai trò là một biên tập viên. Dựa trên ngữ cảnh đã cho, là một danh sách các chuỗi, hãy tạo ra một danh sách các đối tượng JSON với một khóa `input`.
            `input` phải là một câu hỏi có thể được đề cập đến trong ngữ cảnh đã cho. Hãy hỏi những câu hỏi mà người dùng thường có thể hỏi nhất. Ví dụ:"Cài đặt voucher như thế nào?", "Buymed có những loại voucher nào?"

            **
            QUAN TRỌNG: Vui lòng đảm bảo chỉ trả về dưới định dạng JSON, với khóa 'data' là một danh sách các đối tượng JSON.
            BẠN PHẢI CỐ GẮNG tạo ra {max_goldens_per_context} dữ liệu, trừ khi `input` trở nên lặp đi lặp lại.

            Ví dụ ngữ cảnh: ["Einstein đạt giải Nobel nhờ phát hiện ra penicillin.", "Einstein đạt giải Nobel vào năm 1968."] 
            Ví dụ số lượng goldens tối đa cho mỗi ngữ cảnh: 2
            Ví dụ JSON:
            {{
                "data": [
                    {{
                        "input": "Einstein nổi tiếng nhờ điều gì?"
                    }},
                    {{
                        "input": "Einstein đạt giải Nobel vào năm nào?"
                    }}
                ]  
            }}

            các câu hỏi ở `input` PHẢI ĐƯỢC VIẾT BẰNG TIẾNG VIỆT, nếu không, vui lòng dịch sang TIẾNG VIỆT!
            Bạn KHÔNG ĐƯỢC KẾT HỢP bất kỳ kiến thức trước đó nào và hãy xem xét mỗi ngữ cảnh một cách đơn giản.
            Bạn PHẢI BAO GỒM ít nhất một câu hỏi làm đầu vào.
            `input` PHẢI LÀ MỘT CHUỖI.
            BẠN PHẢI CỐ GẮNG tạo ra {max_goldens_per_context} điểm dữ liệu, trừ khi `input` trở nên lặp đi lặp lại.
            **

            Số Lượng Goldens Tối Đa Cho Mỗi Ngữ Cảnh:
            {max_goldens_per_context}

            Ngữ Cảnh:
            {context}

            JSON:
            """
        logger.info(f"Creating Q&A dataset using {prompt=}")

        return prompt


class MQCTemplate(CustomSynthesizeTemplate):

    @staticmethod
    def generate_synthetic_data(context: Text, max_goldens_per_context: Text):
        prompt = f"""I want you to act as a copywriter. Based on the given context, which is a list of strings, please generate a multiple-choice question with four options.

        The `input` key must contain the question, and the `options` key must contain a list of four possible answer choices. The correct answer must be indicated by adding an additional key `answer` with the index of the correct option (0-indexed).

        **
        IMPORTANT: Please make sure to only return in JSON format, with the 'data' key as a list of JSON objects.
        You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting repetitive.

        Example context: ["Einstein đạt giải Nobel nhờ phát hiện ra penicillin.", "Einstein đạt giải Nobel vào năm 1968."]
        Example max goldens per context: 2
        Example JSON:
        {{
            "data": [
                {{
                    "input": "Einstein nổi tiếng nhờ gì?",
                    "options": ["A. Phát minh ra vi khuẩn", "B. Phát hiện ra penicillin", "C. Đạt giải Nobel vào năm 1968", "D. Là một nhà toán học"],
                    "answer": 1
                }},
                {{
                    "input": "Einstein đạt giải Nobel năm nào?",
                    "options": ["A. 1968", "B. 1950", "C. 1972", "D. 1990"],
                    "answer": 0
                }}
            ]
        }}

        `options` and `input` must be in VIETNAMESE, if not, please translate to VIETNAMESE!
        You should NOT incorporate any prior knowledge you have and take each context at face value.
        You MUST include at least one question as the input.
        `input` and `options` MUST be strings.
        You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting repetitive.
        **

        Max Goldens Per Context:
        {max_goldens_per_context}

        Context:
        {context}

        JSON:
        """

        logger.info(f"Creating multiple choice dataset using {prompt=}")

        return prompt
