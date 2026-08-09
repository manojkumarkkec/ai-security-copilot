class PromptBuilder:


    def build(

        self,

        question: str,

        context: list,

        history: list | None = None,

    ) -> list[dict]:


        messages = []


        messages.append(

            {
                "role": "system",
                "content": (
                    "You are an AI security assistant. "
                    "Answer only using provided context."
                ),
            }

        )


        if history:

            messages.extend(history)



        context_text = "\n\n".join(

            [

                document.content

                for document in context

            ]

        )


        messages.append(

            {
                "role": "user",

                "content": f"""

Context:

{context_text}


Question:

{question}

""",

            }

        )


        return messages