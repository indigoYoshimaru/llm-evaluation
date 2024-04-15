from typing import Text
from loguru import logger


class QATemplate:

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

            `input` MUST be in VIETNAMESE, if not, please translate to VIETNAMESE!
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
        logger.info(f"Creating synthesis dataset using {prompt=}")

        return prompt


class MQCTemplate:

    @staticmethod
    def generate_synthetic_data(context: Text, max_goldens_per_context: Text):
        prompt = f"""I want you act as a copywriter. Based on the given context, which is list of strings, please generate a list of JSON objects with a `input` key.
            The `input` must be a multiple choice question that include 4 multiple choice answers and can be addressed by the given context. 

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

            `input` MUST be in VIETNAMESE, if not, please translate to VIETNAMESE!
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
        logger.info(f"Creating synthesis dataset using {prompt=}")

        return prompt
