# from deepeval.dataset import EvaluationDataset
# from deepeval.synthesizer import Synthesizer
# from deepeval.synthesizer.template import SynthesizerTemplate
# from deepeval.synthesizer import synthesizer

# class SynthesizerTemplate:
#     @staticmethod
#     def generate_synthetic_data(context, max_goldens_per_context):
#         # provided false example context purposely!
#         prompt= f"""I want you act as a copywriter. Based on the given context, which is list of strings, please generate a list of JSON objects with a `input` key.
#             The `input` must be a question that can be addressed by the given context. 

#             **
#             IMPORTANT: Please make sure to only return in JSON format, with the 'data' key as a list of JSON objects.
#             You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting reptitive.

#             Example context: ["Einstein đạt giải Nobel nhờ phát hiện ra penicillin.", "Einstein đạt giải Nobel vào năm 1968."] 
#             Example max goldens per context: 2
#             Example JSON:
#             {{
#                 "data": [
#                     {{
#                         "input": "Einstein nổi tiếng nhờ gì?"
#                     }},
#                     {{
#                         "input": "Einstein đạt giải Nobel năm nào?"
#                     }}
#                 ]  
#             }}

#             `input` MUST be VIETNAMESE, if not, please translate to VIETNAMESE!
#             You should NOT incorporate any prior knowledge you have and take each context at face value.
#             You MUST include at least one question as the input.
#             `input` MUST be a STRING.
#             You MUST TRY to generate {max_goldens_per_context} data points, unless the `input` is getting reptitive.
#             **

#             Max Goldens Per Context:
#             {max_goldens_per_context}

#             Context:
#             {context}

#             JSON:
#             """
    
#         return prompt

# synthesizer.SynthesizerTemplate = SynthesizerTemplate
# synthesizer = Synthesizer(model="gpt-3.5-turbo-0125")
# dataset = EvaluationDataset()
# dataset.generate_goldens_from_docs(
#     document_paths=["files/chinh_sach_cap_doi_tra_thiet_bi.pdf"],
#     max_goldens_per_document=2,
#     synthesizer=synthesizer,
    
# )
# dataset.save_as(file_type="json", directory="./dataset")


from deepeval.synthesizer import Synthesizer
from deepeval.dataset import EvaluationDataset

# Initialize the Synthesizer
synthesizer = Synthesizer()

# Define a list of contexts for synthetic data generation
contexts = [
    ["The Earth revolves around the Sun.", "Planets are celestial bodies."],
    ["Water freezes at 0 degrees Celsius.", "The chemical formula for water is H2O."],
]

# Generate goldens directly with the synthesizer
synthesizer.generate_goldens(contexts=contexts)
synthesizer.save_as(
    file_type='json',  # The method also supports 'csv'
    path="./synthetic_data"
)

# Generate goldens within an EvaluationDataset
dataset = EvaluationDataset()
dataset.generate_goldens(
    synthesizer=synthesizer,
    contexts=contexts
)
dataset.save_as(
    file_type='json',  # Similarly, this supports 'csv'
    path="./dataset"
)