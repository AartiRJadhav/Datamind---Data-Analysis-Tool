import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
import plotly.express as px
import json

from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI  # Or `from langchain_openai import ChatOpenAI` depending on version

# Load environment variables from .env file
load_dotenv()

# Retrieve API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize ChatOpenAI model
llm = ChatOpenAI(
    model="gpt-4o",  # Or "gpt-4o-mini" if supported by your version
    openai_api_key=openai_api_key,
    temperature=0.7,
)


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None

# Prompt templates
visualization_prompt_template = PromptTemplate(
    input_variables=["user_query", "csv_preview", "chat_history"],
    template="""
    Previous conversation:
    {chat_history}
    
    Dataset preview:
    {csv_preview}
    
    Your response should ONLY be the python code [NOTHING ELSE is allowed]. 
    Keep in mind that the data is already read using pandas as st.session_state.csv_data. Make sure to import streamlit. Create a temporary copy onto another variable copy_data for your needs.

    You are free to perform any data cleaning to resolve issues - like badly named columns, column data types, etc.
    
    Please ONLY use Plotly for creating the chart. Exclude fig.show() at the end of the code.

    Query: {user_query}
    """
)

textual_prompt_template = PromptTemplate(
    input_variables=["user_query", "csv_preview", "chat_history"],
    template="""
    Previous conversation:
    {chat_history}
    
    Dataset preview:
    {csv_preview}
    
    Your response should ONLY be the python code [NOTHING ELSE is allowed].
    Keep in mind that the data is already read using pandas as st.session_state.csv_data. Make sure to import streamlit. Create a temporary copy onto another variable copy_data for your needs.

    You are free to perform any data cleaning to resolve issues - like badly named columns, column data types, etc.
    
    The code should perform the required analysis and store the final output in a variable called 'markdown_output'.
    The markdown_output should be properly formatted with markdown syntax for better presentation.
    
    Query: {user_query}
    """
)

decision_prompt_template = PromptTemplate.from_template(
    """
    Analyze this query and determine needed actions. 
    1. Visualization for creating charts and graphs {{\"visualization\": true, \"textual\": false}}
    2. Textual analysis for explanations for answers which do NOT require graphs at all {{\"visualization\": false, \"textual\": true}}
    3. Both for comprehensive analysis if both graphs and textual answers are required {{\"visualization\": true, \"textual\": true}}
    
    If both visualization and textual are required, attempt to split the query into a visualization part and a textual part. Return the result in the format:
    {{
        \"visualization\": true,
        \"textual\": true,
        \"split_query\": {{
            \"visualization_query\": \"<query for visualization>\",
            \"textual_query\": \"<query for textual analysis>\"
        }}
    }}

    If splitting is not possible, return {{\"visualization\": true, \"textual\": true, \"split_query\": null}}.

    Return ONLY a JSON object like {{\"visualization\": true, \"textual\": true, \"split_query\": {{\"visualization_query\": \"...\", \"textual_query\": \"...\"}}}} No other text.

    Query: {user_query}
    """
)

def create_visualization_agent():
    def visualization_tool(user_query, csv_data):
        # print(st.session_state.messages)
        chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]])
        print(chat_history)
        csv_preview = csv_data.head().to_string(index=False)
        prompt = visualization_prompt_template.format(
            user_query=user_query,
            csv_preview=csv_preview,
            chat_history=chat_history
        )
        response = llm([HumanMessage(content=prompt)])
        return response.content

    return Tool(
        name="VisualizationAgent",
        func=visualization_tool,
        description="Generates Python code for visualizations using Plotly."
    )

def create_textual_agent():
    def textual_tool(user_query, csv_data):
        # print(st.session_state.messages)
        chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]])
        print(chat_history)
        csv_preview = csv_data.head().to_string(index=False)
        prompt = textual_prompt_template.format(
            user_query=user_query,
            csv_preview=csv_preview,
            chat_history=chat_history
        )
        response = llm([HumanMessage(content=prompt)])
        return response.content

    return Tool(
        name="TextualAgent",
        func=textual_tool,
        description="Generates Python code for data analysis with markdown output."
    )

def decide_agents(user_query):
    decision_prompt = decision_prompt_template.format(user_query=user_query)
    response = llm([HumanMessage(content=decision_prompt)])
    try:
        decision = json.loads(response.content.strip())
        if not isinstance(decision, dict):
            raise ValueError("Decision output is not a dictionary.")
        return {
            "visualization": decision.get("visualization", False),
            "textual": decision.get("textual", False),
            "split_query": decision.get("split_query")
        }
    except Exception as e:
        st.error(f"Error parsing decision response: {e}")
        return {"visualization": False, "textual": False, "split_query": None}

def main():
    st.title("Interactive Data Analysis Chat")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        st.session_state.csv_data = pd.read_csv(uploaded_file)
        st.write("Preview of the uploaded data:")
        st.dataframe(st.session_state.csv_data.head())
        
        # Display chat messages
        for idx, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                if "code" in message:
                    st.code(message["code"], language="python")
                if "visualization" in message:
                    st.plotly_chart(message["visualization"], key=f"viz_{idx}")
                if "analysis" in message:
                    st.markdown(message["analysis"])
                if "content" in message:
                    st.markdown(message["content"])

        # Chat input
        user_query = st.chat_input("Ask about your data...")
        
        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)
            st.session_state.messages.append({"role": "user", "content": user_query})

            with st.spinner("Processing..."):
                decision = decide_agents(user_query)
                
                if decision.get("visualization") or decision.get("textual"):
                    split_query = decision.get("split_query")
                    visualization_query = split_query.get("visualization_query", user_query) if split_query else user_query
                    textual_query = split_query.get("textual_query", user_query) if split_query else user_query

                    if decision.get("visualization"):
                        visualization_agent = create_visualization_agent()
                        vis_response = visualization_agent.func(visualization_query, st.session_state.csv_data)
                        
                        try:
                            local_context = {"csv_data": st.session_state.csv_data, "pd": pd, "px": px}
                            exec(vis_response.strip("```").lstrip("python"), local_context)
                            
                            with st.chat_message("assistant"):
                                st.code(vis_response, language="python")
                                st.plotly_chart(local_context["fig"], key=f"chart_{len(st.session_state.messages)}")
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": vis_response,
                                "visualization": local_context["fig"]
                            })
                        except Exception as e:
                            with st.chat_message("assistant"):
                                st.error(f"Error executing the visualization code: {e}")

                    if decision.get("textual"):
                        textual_agent = create_textual_agent()
                        text_response = textual_agent.func(textual_query, st.session_state.csv_data)
                        
                        try:
                            local_context = {"csv_data": st.session_state.csv_data, "pd": pd}
                            exec(text_response.strip("```").lstrip("python"), local_context)
                            
                            with st.chat_message("assistant"):
                                st.code(text_response, language="python")
                                st.markdown(local_context["markdown_output"])
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": text_response,
                                "analysis": local_context["markdown_output"]
                            })
                        except Exception as e:
                            with st.chat_message("assistant"):
                                st.error(f"Error executing the analysis code: {e}")

if __name__ == "__main__":
    main()
