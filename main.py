import os
import uuid
import streamlit as st
from langchain.agents import AgentType
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from streamlit_folium import st_folium
from langchain.agents import load_tools

from customAgent import AdvancedTravelAgent
from customCallback import CustomCallbackHandler
from customTools import InterestLocator, RoutePathfinder
from helper import generate_route_map

# Streamlit setup and app configuration
st.set_page_config(page_title="Intelligent Trip Planner", page_icon="🌍", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)

st.title("Intelligent Trip Planner 🌍✨")
st.info(
    "Welcome to your AI-powered travel assistant! Plan your trips with ease.",
    icon="🗺️")

# Initialize chat message history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I assist you in planning your trip today?"}]

# Set up the chat engine with memory and tools
if "chat_engine" not in st.session_state:
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("The OpenAI API key must be set as an environment variable.")

    # Initialize language model with memory and callback handler
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
    memory = ConversationSummaryMemory(memory_key="chat_log", llm=llm, max_token_limit=10, verbose=True)
    callback_handler = CustomCallbackHandler(session_state=st.session_state)
    travel_agent = AdvancedTravelAgent(llm=llm, memory=memory, agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                       verbose=True, handler=callback_handler)

    # Load external tools for use with the travel agent
    wiki_tool = load_tools(['wikipedia'], llm=llm)[0]
    travel_agent.append_tool(InterestLocator())
    travel_agent.append_tool(RoutePathfinder())
    travel_agent.append_tool(wiki_tool)

    st.session_state.chat_engine = travel_agent

# Capture user input and add to chat history
if user_input := st.chat_input("Type your question here"):
    st.session_state.messages.append({"role": "user", "content": user_input})

# Display all prior messages in the chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

    # Display map if 'geocode_points' are available in the message
    if 'geocode_points' in message:
        route_points = message['geocode_points']
        map_key = message['map_key']
        map_view = generate_route_map(route_points)
        _ = st_folium(map_view, key=map_key)

# Generate assistant response if last message is from user
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Processing your request..."):
            response = st.session_state.chat_engine.process_request(user_input)
            
            # Display route map if geocode points are present
            if 'geocode_points' in st.session_state.messages[-1]:
                route_points = st.session_state.messages[-1]['geocode_points']
                map_key = str(uuid.uuid4())
                map_view = generate_route_map(route_points)
                _ = st_folium(map_view, key=map_key)
                st.session_state.messages[-1]['map_key'] = map_key

            # Display and store assistant response
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
