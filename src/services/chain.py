from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import CSVLoader, PyMuPDFLoader
from langchain_core.runnables import RunnableLambda,RunnableBranch
from langchain_core.output_parsers import StrOutputParser
from src.utils.template import Template
from .rag import VectorStore
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self, model_settings: dict):
        self.model_settings = model_settings
        self.template = Template()
    
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

    def chain_context(self, input):
        # 1. Load vector store
        vector_store = VectorStore(
            model=self.model_settings['model'],
            email=self.model_settings['email'],
            prompt_id=self.model_settings['prompt_id'],
            file_path=self.model_settings['file_path']
        )
        db = vector_store.create_vector_store()
        retriever = db.as_retriever(search_kwargs={"k": 3})

        # 2. Retrieve relevant documents based on input query
        relevant_docs = retriever.get_relevant_documents(input)

        # 3. Extract text from documents (depends on doc format)
        context_texts = "\n".join([doc.page_content for doc in relevant_docs])

        # 4. Build prompt template with context
        prompt_template_str = self.model_settings['prompt_template']
        
        # Assuming your template supports placeholders like {context} and {input}
        prompt_str = prompt_template_str.format(context=context_texts, input=input)
        
        # 5. Prepare LangChain prompt
        template = self.template.chat_prompt(prompt_str)
        
        # 6. Select model
        model = self.select_model(self.model_settings['model'], self.model_settings['temperature'], self.model_settings['top_p'])

        # 7. Create chain and parse output
        chain = template | model | StrOutputParser()
        
        response = chain.invoke({"input": input})  # Or pass input if needed by prompt

        return response

        
    def chain_no_context(self, input):
        model = self.select_model(self.model_settings['model'],self.model_settings['temperature'],self.model_settings['top_p'])
        template = self.template.chat_prompt(self.model_settings['prompt_template'])

        chain = template | model | StrOutputParser()
        
        response = chain.invoke({"input": input})

        return response

    def run(self, input):
        use_context = self.model_settings['use_context']

        if use_context.lower() == 'yes':
            response = self.chain_context(input)
            return {"response": response}
        else:
            response = self.chain_no_context(input)
            print(self.model_settings['prompt_template'])
            return {"response": response}
