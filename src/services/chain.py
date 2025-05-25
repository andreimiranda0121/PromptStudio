from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import CSVLoader, PyMuPDFLoader
from langchain_core.runnables import RunnableLambda,RunnableBranch

class Chain:
    def __init__(self, model_settings: dict):
        self.model_settings = model_settings
    
    def select_model(self,model,temperature,top_p):
        if "gpt" in model.lower():
            return ChatOpenAI(
                model = model.lower(),
                temperature=temperature,
                top_p= top_p
            )
        else:
            return ChatGoogleGenerativeAI(
                model = model.lower(),
                temperature=temperature,
                top_p= top_p
            )

    def chain_context(self):
        model = self.select_model(self.model_settings['model'],self.model_settings['temperature'],self.model_settings['top_p'])
        context = "test"
        
    def chain_no_context(self):
        pass

    def main(self):
        use_context = self.model_settings['use_context']

        if use_context:
            pass
        else:
            pass