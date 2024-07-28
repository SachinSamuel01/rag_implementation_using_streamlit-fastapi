from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os


load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv('API_KEY')

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.3,
    top_p=0.9,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    
)

prompt_template='''
You are an assistant. You are provided with necessary content and previous chat.
You have to answer the question based on the content provided and previous chat is provided to facilitate your response.

Content: {content}

Previous chats: {chat}

Query: {query}
'''

prompt= PromptTemplate.from_template(prompt_template)
parser= StrOutputParser()

chain= prompt | llm | parser

def get_response(query,content,chat ):
    
    res= chain.invoke(
        {
        'content': content,
        'chat': chat,
        'query': query
        }
    )
    return res

