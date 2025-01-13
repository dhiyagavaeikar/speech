from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate


from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate

from langchain.prompts import PromptTemplate



# model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, convert_system_message_to_human=True, google_api_key="AIzaSyAX63WnRPbEJ7963mdjvY5kvBJesg4EqDE")
llama=ChatGroq(model_name="llama3-70b-8192", temperature=0, groq_api_key = "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")
# flash = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, convert_system_message_to_human=True, google_api_key="AIzaSyDeI_eDWwNWX-erwNkKxDreyqDdLAfZk3s")

gemini_generation_prompt = PromptTemplate(
    template="""You are an expert in generating the response based on the following user question : {question}
        """,
    input_variables=["question"],
)

gemini_generator = gemini_generation_prompt | llama | StrOutputParser()
print(gemini_generator)
refined_question = gemini_generator.invoke({'question': "what is ml"})