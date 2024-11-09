# One-Day Tour Planning Assistant: A Langchain-Powered Interactive Solution

## Project Introduction

This project is an implementation of a **One-Day Tour Planning Assistant** in response to the provided assignment requirements for Attentions.ai. Using the Langchain library within a Streamlit framework, this project serves as an interactive tool designed to help users plan personalized, dynamic itineraries for city tours based on their preferences. This solution leverages memory to adjust to evolving preferences throughout the interaction, creating a responsive and user-centric experience.

## Problem Overview

The assignment specifies the development of an application that assists users in crafting a one-day tour plan for any selected city. The system remembers and adapts to user preferences continuously, ensuring a tailored itinerary that aligns with specific interests and constraints such as budget, time, and transportation modes.

Key requirements of the solution include:
- Collecting user details like the city to visit, preferred timings, budget, and interests (e.g., culture, food, shopping).
- Starting from a provided or default location, with recommended places based on user interests and location.
- A dynamically updated itinerary that incorporates changes as users interact, with options for lunch spots, preferred attractions, and weather-informed suggestions.
- Memory integration for continuity, stored in a graph database using LLM-based memory agents for real-time, context-aware updates.

## Solution Features

The Tour Planning Assistant employs various APIs to address the assignment’s requirements:

- **Geographical Information**: OpenStreetMap (via Geopy) for location geocoding.
- **Route and Transit Options**: Bing Maps API for route creation, supporting multiple waypoints and transportation modes (e.g., walking, taxis).
- **Attractions and Places of Interest**: Foursquare API for real-time details about nearby attractions.
- **General Information**: Wikipedia and weather APIs to provide localized information and weather updates.

This assistant uses OpenAI's `gpt-3.5-turbo` as the language model, though alternative LLMs can be integrated. 

## System Agents

In line with the assignment requirements, the following agents are implemented:
- **User Interaction Agent**: Collects user preferences and initiates itinerary planning.
- **Itinerary Generation Agent**: Drafts a route based on user preferences and adjusts according to new inputs.
- **Optimization Agent**: Optimizes travel paths based on the user’s budget and time constraints.
- **Weather and News Agents**: Provides weather information and relevant local updates.
- **Memory Agent**: Maintains user preferences to ensure personalized future suggestions, structured using Neo4j for graph-based data storage.

## Instructions to Run the Application

To execute this application locally:
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```
4. Access the app via the displayed local URL.

### Notes:
Ensure valid API keys for OpenAI, Bing Maps, and FourSquare are available in your environment.

## Features Demonstration

### Key Functionalities:
- **Personalized Recommendations**: As the conversation progresses, the assistant suggests attractions based on user interests.
- **Itinerary Adjustment**: Dynamically adapts to new user inputs, such as budget changes, additional stops, or lunch preferences.
- **Memory-Based Adaptation**: Retains user preferences across sessions, allowing a consistent experience with memory-backed itinerary updates.
- **Weather and Real-Time Updates**: Integrates weather updates and local news events that could impact the travel plan.

