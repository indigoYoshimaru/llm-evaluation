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
        prompt = f"""I want you act as a copywriter. Based on the given context, which is list of strings, please generate a list of JSON objects with a `input` key.
            The `input` must be a question that can be addressed by the given context. 

            **
            IMPORTANT: Please make sure to only return in JSON format, with the 'data' key as a list of JSON objects.
            You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting reptitive.

            Example context: ["Einstein đạt giải Nobel nhờ phát hiện ra penicillin.", "Einstein đạt giải Nobel vào năm 1968."] 
            Example max goldens per context: 2
            Example JSON:
            {{
                "data": [
                    {{
                        "input": "Einstein nổi tiếng nhờ gì?"
                    }},
                    {{
                        "input": "Einstein đạt giải Nobel năm nào?"
                    }}
                ]  
            }}

            `input` MUST be in VIETNAMESE, if not, please translate it to VIETNAMESE!
            Kết quả trả về phải ở tiếng Việt!!
            You should NOT incorporate any prior knowledge you have and take each context at face value.
            You MUST include at least one question as the input.
            `input` MUST be a STRING.
            You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting reptitive.
            **

            Max Goldens Per Context:
            {max_goldens_per_context}

            Context:
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
