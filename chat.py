# chat.py

import chainlit as cl
from coverage_tracker import CoverageTracker
from langchain.llms import CTransformers
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Initialize LLM
llm = CTransformers(
    model="marella/gpt-2-ggml",
    model_file="ggml-model.bin",
    model_type="gpt2",
    config={"max_new_tokens": 256, "temperature": 0.8}
)

# Initialize Coverage Tracker
tracker = CoverageTracker()

# Prompt template
template = """You are a QA automation assistant helping a user write test cases.

User's input:
{user_input}

Respond helpfully, suggesting clear test ideas or strategies.
"""
prompt = PromptTemplate(input_variables=["user_input"], template=template)
chain = LLMChain(llm=llm, prompt=prompt)

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content

    # Update test coverage
    feature, updated_state = tracker.update_coverage(user_input)

    # Maintain session-level coverage state
    cl.user_session.set("coverage_state", tracker.get_coverage_state())

    # Run the LLM chain for the main response
    response = chain.run(user_input=user_input)

    # Get any missing test types and build nudge
    missing = tracker.get_missing_categories(feature)
    if missing:
        categories = ", ".join(missing)
        nudge = f"\n\n💡 P.S. We haven't covered **{categories}** tests for *{feature.replace('_', ' ')}*. Want suggestions?"
        response += nudge

    # Send final response
    await cl.Message(content=response).send()
