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

            các câu hỏi ở `input` PHẢI ĐƯỢC VIẾT BẰNG TIẾNG VIỆT VÀ CHỈ BẰNG TIẾNG VIỆT.
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


class VietnamEvolutionTemplate:
    base_instruction = """I want you to act as an input rewriter.
    Your object is the rewrite a given `input` and must be factually correct according to the supporting information in `Context`. Rewritten input MUST be written in Vietnamese ONLY!
    You MUST complicate the given `Input` using the following method:"""

    @staticmethod
    def multi_context_evolution(input, context):
        return (
            VietnamEvolutionTemplate.base_instruction
            + f"""
            1. `Input` should be rewritten to require readers to use information from all elements of `Context`. 
            2. `Rewritten Input` must be fully answerable from information in `Context`. 
            3. `Rewritten Input` should be concise and understandable by humans.
            4. `Rewritten Input` should not contain phrases like  'based on the provided context' or 'according to the context'.
            5. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.
            
            **
            EXAMPLES

            Example context:
            ["Vaccines introduce a weakened or dead form of the pathogen to the human body.", "This exposure helps the immune system learn to recognize and fight the pathogen in the future."]
            Example input:
            How do vaccines work?
            Example rewritten input:
            How does the introduction of a modified pathogen prepare the immune system for future encounters?

            --------------------------
            
            Example context:
            ["Plants perform photosynthesis, using sunlight to convert carbon dioxide and water into glucose and oxygen.", "Chlorophyll in plant leaves absorbs sunlight, initiating the photosynthesis process.", "Oxygen is a by-product of the photosynthesis process and is released into the atmosphere."]
            Example input:
            Explain how plants produce oxygen.
            Example rewritten input: 
            Considering chlorophyll's role in sunlight absorption and photosynthesis, how is oxygen produced and released by plants?

            --------------------------

            Example context:
            ["The gravitational pull of the moon on the Earth influences the tides.", "The position of the sun relative to the Earth and the moon also affects tidal patterns."]
            Example input:
            Tell me about high tides.
            Example rewritten input:
            Explain how the combined gravitational effects of the moon and the sun's relative positioning influence Earth's tidal phenomena.
            **

            Context:
            {context}
            Input:
            {input}
            Rewritten Input:            
            """
        )

    @staticmethod
    def reasoning_evolution(input, context):
        return (
            VietnamEvolutionTemplate.base_instruction
            + f"""
            1. If `Input` can be solved with just a few simple thinking processes, you can rewrite it to explicitly request multiple-step reasoning.
            2. `Rewritten Input` should require readers to make multiple logical connections or inferences.
            3. `Rewritten Input` should be concise and understandable by humans.
            4. `Rewritten Input` should not contain phrases like  'based on the provided context' or 'according to the context'.
            5. `Rewritten Input` must be fully answerable from information in `Context`. 
            6. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

            **
            EXAMPLES

            Example context:
            Chlorophyll allows plants to absorb energy from light, and this energy is used to convert carbon dioxide and water into glucose and oxygen, a process known as photosynthesis.
            Example input:
            Why are plants green?
            Example rewritten input:
            How does chlorophyll's role in absorbing light relate to plants' green color and their ability to produce glucose?
        
            --------------------------
            
            Example context:
            The greenhouse effect occurs when the Earth's atmosphere traps solar radiation, caused by gases such as carbon dioxide, methane, and water vapor. This process maintains the planet's temperature but can lead to increased global temperatures when exacerbated by human activities.
            Example input:
            What causes seasons to change?
            Example rewritten input: 
            Given the trapping of solar radiation by atmospheric gases, explain how the enhanced activity impact Earth's climate.

            --------------------------

            Example context:
            Economic theories suggest that market demand and supply determine prices, but government policies can also influence market dynamics through regulations, taxes, and subsidies.
            Example input:
            Identify the primary factors that determine the price of goods in a market.
            Example rewritten input:
            Examine how the interplay of market demand, supply dynamics, and government policy interventions collectively shape the pricing mechanism of goods within a market ecosystem.
            **

            Context:
            {context}
            Input:
            {input}
            Rewritten Input:            
            """
        )

    @staticmethod
    def concretizing_evolution(input, context):
        return (
            VietnamEvolutionTemplate.base_instruction
            + f"""
            1. Rewrite `Input` by replacing general concepts/inquiries with more specific ones.
            2. `Rewritten Input` should be concise and understandable by humans.
            3. `Rewritten Input` should not contain phrases like  'based on the provided context' or 'according to the context'.
            4. `Rewritten Input` must be fully answerable from information in `Context`.  
            5. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

            **
            EXAMPLES
            Example context:
            Rainforests are home to over half of the world's plant and animal species, making them key to maintaining global biodiversity. The variety of life found in these ecosystems contributes to genetic diversity, which is crucial for adaptation and survival amid changing environmental conditions. This biodiversity also supports ecosystem resilience, enabling forests to recover from disturbances.
            The biodiversity in rainforests plays a significant role in human well-being, providing essential services such as air and water purification, disease control, and pollination of crops. Additionally, many medicines are derived from rainforest plants, highlighting the importance of these ecosystems for medical research and healthcare.
            Example input: 
            Why is the biodiversity of rainforests important?
            Example rewritten input:
            How does the extensive biodiversity found in rainforests, encompassing over half of the world's plant and animal species, contribute to global biodiversity maintenance, and what role does this diversity play in enhancing ecosystem resilience, human health through disease control, crop pollination, and the development of medicines derived from rainforest plants?

            --------------------------

            Example context:
            Bees play a critical role in pollinating flowering plants, including many fruits and vegetables, contributing to the diversity of plant life and the production of crops. Their activity supports the growth of trees, flowers, and other plants, which serve as food and shelter for numerous animals, thus maintaining ecosystem balance.
            Beyond their impact on food crops, bees contribute to wild plant growth by pollinating a wide range of plants outside of agricultural settings. This pollination is vital for the reproduction of many plants, affecting entire ecosystems' health and sustainability.
            Example input: 
            What is the role of bees in ecosystems?
            Example rewritten input:
            How do bees, through their pollination of flowering plants, including a multitude of fruits and vegetables, significantly influence the diversity of plant life and agricultural productivity, and in what ways do their activities extend beyond agricultural settings to support the growth of trees, flowers, and other plants, thereby providing essential resources for various animal species and contributing to the overall balance and sustainability of ecosystems?

            --------------------------

            Example context:
            Solar power generation relies on photovoltaic cells to convert sunlight into electricity. These cells are made of materials that exhibit the photovoltaic effect, which occurs when light photons are absorbed by the material, causing the generation of electrical current.
            Solar panels, composed of many photovoltaic cells, collect sunlight and convert it into electrical power. This energy can then be used directly or stored in batteries for later use, providing a renewable and sustainable source of power with minimal environmental impact.
            Example input: 
            What are the principles behind solar power generation?
            Example rewritten input:
            How do photovoltaic cells work to convert sunlight into electrical power, and what role do solar panels play in this process, including energy storage for sustainable use?
            **

            Input:
            {input}
            Context:
            {context}
            Rewritten Input:
            """
        )

    @staticmethod
    def constrained_evolution(input, context):
        return (
            VietnamEvolutionTemplate.base_instruction
            + f"""
            1. Rewrite `Input` by adding at least one more constraints/requirements.
            2. `Rewritten Input` must be fully answerable from information in `Context`. 
            5. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

            **
            EXAMPLES
            Example context:
            Rainforests are home to over half of the world's plant and animal species, making them key to maintaining global biodiversity. The variety of life found in these ecosystems contributes to genetic diversity, which is crucial for adaptation and survival amid changing environmental conditions. This biodiversity also supports ecosystem resilience, enabling forests to recover from disturbances.
            The biodiversity in rainforests plays a significant role in human well-being, providing essential services such as air and water purification, disease control, and pollination of crops. Additionally, many medicines are derived from rainforest plants, highlighting the importance of these ecosystems for medical research and healthcare.
            Example input: 
            Why is the biodiversity of rainforests important?
            Example rewritten input:
            How does the biodiversity of rainforests contribute to ecosystem resilience and recovery from disturbances, and in what ways does it impact human well-being through services such as air and water purification, disease control, and crop pollination?

            --------------------------

            Example context:
            Bees play a critical role in pollinating flowering plants, including many fruits and vegetables, contributing to the diversity of plant life and the production of crops. Their activity supports the growth of trees, flowers, and other plants, which serve as food and shelter for numerous animals, thus maintaining ecosystem balance.
            Beyond their impact on food crops, bees contribute to wild plant growth by pollinating a wide range of plants outside of agricultural settings. This pollination is vital for the reproduction of many plants, affecting entire ecosystems' health and sustainability.
            Example input: 
            What is the role of bees in ecosystems?
            Example rewritten input:
            Considering the pivotal role bees play in pollinating both agricultural crops and wild plants, thereby contributing to the diversity of plant life and supporting the foundation of food chains, analyze how bees influence the growth and sustainability of various ecosystems.

            --------------------------

            Example context:
            Solar power generation relies on photovoltaic cells to convert sunlight into electricity. These cells are made of materials that exhibit the photovoltaic effect, which occurs when light photons are absorbed by the material, causing the generation of electrical current.
            Solar panels, composed of many photovoltaic cells, collect sunlight and convert it into electrical power. This energy can then be used directly or stored in batteries for later use, providing a renewable and sustainable source of power with minimal environmental impact.
            Example input: 
            What are the principles behind solar power generation?
            Example rewritten input:
            Examine the significance of rainforest biodiversity in sustaining ecosystem resilience and providing essential services such as disease control and crop pollination, alongside its critical role in medical research and the development of new medicines. Consider the broader implications of biodiversity loss on global ecological balance and human health.
            **

            Context:
            {context}
            Input:
            {input}
            Rewritten Input:
            """
        )

    @staticmethod
    def comparative_question_evolution(input, context):
        return (
            VietnamEvolutionTemplate.base_instruction
            + f"""
            1. Rewrite `Input` to focus on comparing two or more entities, concepts, or processes.
            2. `Rewritten Input` should encourage a detailed comparison that highlights similarities and differences.
            3. `Rewritten Input` must be fully answerable from information in `Context`. 
            4. `Rewritten Input` should be concise and understandable by humans.
            5. `Rewritten Input` should not contain phrases like  'based on the provided context' or 'according to the context'.
            6. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

            **
            EXAMPLES
            Example context:
            "Water boils at 100°C (212°F) at sea level, but boiling point decreases with altitude due to lower atmospheric pressure. In contrast, alcohol boils at about 78°C (172°F)."
            Example input: 
            What happens to water as it boils?
            Example rewritten input:
            How does the boiling point of water at sea level compare to that of alcohol, and how does altitude affect water's boiling point?

            --------------------------

            Example context:
            "Photosynthesis in plants involves converting carbon dioxide and water into glucose and oxygen, using sunlight. Cellular respiration in animals converts glucose and oxygen back into carbon dioxide and water, releasing energy."
            Example input: 
            How do plants and animals process energy?
            Example rewritten input:
            Compare the processes of photosynthesis in plants and cellular respiration in animals, focusing on inputs and outputs of each process.

            --------------------------

            Example context:
            "The Renaissance was a period of significant cultural, artistic, and scientific rebirth that began in the 14th century, primarily in Italy. The Enlightenment, occurring mainly in the 18th century, centered around reason, science, and individualism, significantly influencing European thought."
            Example input: 
            What was the Renaissance?
            Example rewritten input:
            Contrast the main focuses and impacts of the Renaissance and the Enlightenment on European thought and culture.

            --------------------------

            Context:
            {context}
            Input:
            {input}
            Rewritten Input:
            """
        )

    @staticmethod
    def hypothetical_scenario_evolution(input, context):
        return (
            VietnamEvolutionTemplate.base_instruction
            + f"""
            1. Rewrite `Input` to include a hypothetical or speculative scenario that is relevant to the `Context`.
            2. `Rewritten Input` should encourage the reader to apply knowledge from the `Context` to imagine or deduce outcomes.
            3. `Rewritten Input` should be concise, clear, and understandable by humans.
            4. `Rewritten Input` should not contain phrases like 'based on the provided context' or 'according to the context'.
            5. `Rewritten Input` must be fully answerable from information in `Context`.
            6. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.
            7. `Rewritten Input` must still be a question

            **
            EXAMPLES

            Example context:
            The greenhouse effect is a natural process where the Earth's atmosphere traps some of the Sun's energy, warming the planet to a temperature that supports life. Human activities, particularly the emission of greenhouse gases like carbon dioxide and methane, have intensified this effect, leading to global warming and climate change.
            Example input:
            What are the consequences of the greenhouse effect?
            Example rewritten input:
            Imagine a world where greenhouse gas emissions were doubled overnight. How might this intensified greenhouse effect impact global climate patterns and ecosystems?

            --------------------------

            Example context:
            Antibiotics are drugs used to treat bacterial infections. They work by killing bacteria or preventing their growth. However, overuse and misuse of antibiotics have led to the development of antibiotic-resistant bacteria, which are harder to treat because they can withstand the drugs designed to kill them.
            Example input:
            How do antibiotics work?
            Example rewritten input:
            In a scenario where a new antibiotic-resistant superbug emerges, how would the principles of antibiotic action and resistance influence our approach to treatment?

            --------------------------

            Example context:
            Quantum computing relies on the principles of quantum mechanics to process information, utilizing quantum bits or qubits. These qubits can exist in multiple states simultaneously, allowing quantum computers to perform complex calculations much faster than traditional computers.
            Example input:
            What is quantum computing?
            Example rewritten input:
            Suppose a quantum computer was tasked with solving a problem that currently takes traditional computers centuries to solve. How might the unique capabilities of quantum computing change the outcome?
            **

            Context:
            {context}
            Input:
            {input}
            Rewritten Input:
            """
        )

    @staticmethod
    def in_breadth_evolution(input, context):
        return (
            VietnamEvolutionTemplate.base_instruction
            + f"""
            1. Rewrite `Input` to create a brand new prompt.
            2. `Rewritten Input` should belong to the same domain as the `input` but be even more rare.
            3. `Rewritten Input` should be concise, clear, and understandable by humans.
            4. `Rewritten Input` should not contain phrases like 'based on the provided context' or 'according to the context'.
            5. `Rewritten Input` should not contain more than 15 words. Use abbreviation wherever possible.

            **
            EXAMPLES

            Example context:
            Wearable technology has revolutionized personal health monitoring, allowing individuals to track vital signs and activity levels in real time.
            Example input:
            Explore the impact of wearable technology on personal health management.
            Example rewritten input:
            Delve into the development of implantable health devices and their potential to transform chronic disease management.

            --------------------------

            Example context:
            Quantum computing leverages the principles of quantum mechanics to process information, offering significant advancements over traditional computing methods.
            Example input:
            How is quantum computing different from traditional computing?
            Example rewritten input:
            Explore the potential of quantum cryptography in enhancing cybersecurity measures beyond current encryption standards

            --------------------------

            Example context:
            Virtual reality (VR) offers immersive learning experiences, transforming educational methodologies by providing interactive and engaging ways to acquire knowledge, especially in fields requiring practical skills.
            Example input:
            What impact does virtual reality (VR) have on education?
            Example rewritten input:
            Investigate the use of VR simulations in medical training to enhance practical skills and decision-making under pressure.
            **

            Context:
            {context}
            Input:
            {input}
            Rewritten Input:
            """
        )
