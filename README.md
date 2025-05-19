# DataMind

## Overview

**DataMind** is an advanced interactive data analysis tool that leverages cutting-edge AI technologies to provide intuitive data exploration and visualization. Built with Streamlit and LangChain, this application implements **multi-agent systems with chain-of-thought prompting**, enabling dynamic decision-making and task routing. It features **stateful memory management** with chat history injection, **interactive data visualization** using Plotly, and a conversational AI system designed for seamless user interaction.

Future enhancements include **planned integration of vector databases** for efficient data retrieval and **agent swarm architecture** for enhanced scalability and capabilities.

This project is a work in progress. I'm planning to learn the functioning of several agentic frameworks, prompting techniques and RAG systems through this project. Always accepting contributions!

---

## Features

### Core Features
- **Multi-Agent System**: Implements dynamic agent routing through decision prompts, enabling specialized agents for visualization and textual analysis.
- **Chain-of-Thought Prompting**: Enhances reasoning capabilities by breaking down complex queries into logical steps.
- **Interactive Data Visualization**: Generates Plotly charts and graphs based on natural language queries.
- **Textual Analysis**: Provides detailed explanations and insights in Markdown format.
- **Stateful Memory Management**: Maintains chat history and context for coherent multi-turn conversations.

### Technical Highlights
- **Dynamic Agent Routing**: Uses decision prompts to determine whether to route queries to visualization or textual analysis agents.
- **Chat History Injection**: Injects conversation history into prompts for context-aware responses.
- **Interactive UI**: Built with Streamlit for a seamless and user-friendly experience.
- **Dynamic Code Execution**: Executes generated Python code on-the-fly for real-time analysis and visualization.

### Future Enhancements
- **Vector Database Integration**: Planned integration for efficient data storage and retrieval.
- **Agent Swarm Architecture**: Scalable multi-agent framework for handling complex queries and large datasets.
- **Enhanced Visualization**: Support for additional chart types and customization options.

---

## Current Architecure

![system arch  -1](https://github.com/user-attachments/assets/5865d685-8fc3-4546-a3ce-ccdd9fa034f9)

---
## Installation

To run **DataMind** locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/zubairatha/DataMind.git
   cd datamind
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key to the `.env` file:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key_here
     ```

5. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. **Upload a CSV file**: Use the file uploader to upload your dataset.
2. **Ask questions**: Use the chat interface to ask questions about your data. For example:
   - "Show me a bar chart of sales by region."
   - "What is the average age of the customers?"
   - "Explain the trends in monthly revenue."
3. **View results**: The application will generate visualizations and textual analysis based on your queries.

---


## Code Structure

- **app.py**: The main Streamlit application script.
- **requirements.txt**: Lists all the required Python packages.
- **.env**: Stores environment variables like the OpenAI API key.

---

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.
