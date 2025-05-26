from langchain_core.prompts import ChatPromptTemplate

class Template:
    @staticmethod
    def chat_prompt(template):
        return ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", "{input}")
        ])
    @staticmethod
    def context_template(template):
        return ChatPromptTemplate.from_messages(
            [
                ("system", template),
                ("human", "{input}")
            ]
        )