from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

class Output:
    def __init__(self, db, conversation_history):
        self.db = db
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)   
        self.conversation_history = conversation_history
        self.prompt_template = PromptTemplate(
            template="""
            You are an AI assistant designed to help users understand and interact with documentation from their base URLs. If the question is not related to the base URL, ask the user to share base URL to help them better.
            
            This are the base urls you have in your database:
            {base_urls}

            If no question is asked, offer a context overview and suggest possible questions.
            If you don't know the answer, only ask user to be more specific with the question.
            
            Use the following context, retrieved for semantic similarity with user input:
            {context}

            Your goals are to answer questions, provide relevant code snippets, explain concepts, and offer guidance on implementing documentation content.

            To maintain conversation context, and provide answers to following questions, you can refer to the chat history:
            {chat_history}

            Behavior Guidelines:
            1. Be helpful, friendly, and concise.
            2. Provide code snippets and explanations when requested.
            3. Answer questions based on context only even.
            4. Guide users to find information if their questions exceed the documentation.
            5. Use technical language only when necessary; prioritize simplicity.
            6. Provide brief yet comprehensive explanations for overviews or summaries.
            

            Human: {user_input}
            AI: """,
            input_variables=["context", "user_input", "base_urls"]
        )

        # Initialize the RetrievalQA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.db.as_retriever(search_kwargs={"k": 10}),
            chain_type="stuff",
            return_source_documents=False,
        )


    def response(self, user_input, base_urls):

        chat_history = "\n".join([f"Assistant: {assistant}\nUser: {user}" for user, assistant in self.conversation_history[-6:]])
        
        # Retrieve relevant documents using DeepLake's similarity search
        relevant_docs = self.db.similarity_search(user_input, k=5)

        # Text splitting for long documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(relevant_docs)

        # Extract text content from the retrieved documents to form the context
        context = "\n\n".join([doc.page_content for doc in split_docs])

        print("User input: ", user_input)
        print("Relevant docs: ", len(relevant_docs))

        # Format the prompt with context and user input
        formatted_prompt = self.prompt_template.format(
            context=context, 
            user_input=user_input, 
            base_urls=base_urls,
            chat_history=chat_history
        )

        print("chat_history: ", chat_history)
        # Run the QA chain
        response = self.qa_chain({"query": formatted_prompt})

        
        return response['result']