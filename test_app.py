import chainlit as cl
import pandas as pd
import os
import openai

# Set your correct API key here
openai.api_key = "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"

# Automatically determine the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the dataset
file_path = os.path.join(current_dir, "Final_List_Test.csv")
data = pd.read_csv(file_path)

print(data)

# Define a list of questions
questions_list = [
    "What is the popular item?",
    "Who are the top buyers?",
    "What is the highest bid item?",
    "List questions (to see this list again)",
    "Analyze data using LLM (type your query)",
    "Top 3 purchase item"
]


# Helper Function: Create Markdown Table
def create_markdown_table(dataframe, title):
    """
    Generate a markdown table from a pandas DataFrame.
    """
    return f"### {title}\n\n" + dataframe.to_markdown(index=False)


@cl.on_chat_start
async def show_questions():
    """
    Display a list of questions when the chat starts.
    """
    questions = "Welcome! Here are some questions you can ask:\n" + "\n".join(f"- {q}" for q in questions_list)
    await cl.Message(content=questions).send()


@cl.on_message
async def main(message: cl.Message):
    """
    Handle incoming user messages and process the dataset.
    """
    user_message = message.content.lower().strip()
    print(f"User said: {user_message}")

    # Handle "exit" or "quit" command
    if user_message in ["exit", "quit"]:
        await cl.Message(content="Goodbye! Thank you for using the chatbot.").send()
        return

    # Route user message to appropriate function
    try:
        if "list questions" in user_message:
            await display_questions()
        elif "popular item" in user_message:
            await find_popular_item()
        elif "top buyers" in user_message:
            await find_top_buyers()
        elif "highest bid" in user_message:
            await find_highest_bid()
        elif "top 3 purchase item" in user_message or "top three purchased items" in user_message:
            await find_top_three_purchased_items()
        else:
            await analyze_with_llm(user_message)
    except Exception as e:
        await cl.Message(content=f"An error occurred: {e}").send()


async def display_questions():
    """
    Display the list of available questions.
    """
    questions = "Here are some questions you can ask:\n" + "\n".join(f"- {q}" for q in questions_list)
    await cl.Message(content=questions).send()


async def find_popular_item():
    """
    Find the most popular item in the dataset and display it as a table.
    """
    try:
        popular_item = data["item_name"].value_counts().idxmax()
        popular_count = data["item_name"].value_counts().max()

        # Create a DataFrame for table display
        popular_item_df = pd.DataFrame({"item_name": [popular_item], "count": [popular_count]})
        response = create_markdown_table(popular_item_df, "Most Popular Item")
        await cl.Message(content=response).send()

    except Exception as e:
        await cl.Message(content=f"An error occurred while finding the popular item: {e}").send()


async def find_top_buyers():
    """
    Find the top buyers based on purchase counts and display as a table.
    """
    try:
        top_buyers = data[data["interaction"] == "purchased"]["purchaser"].value_counts().head(3)
        top_buyers_df = top_buyers.reset_index()
        top_buyers_df.columns = ["buyer", "purchase_count"]
        response = create_markdown_table(top_buyers_df, "Top Buyers")
        await cl.Message(content=response).send()

    except Exception as e:
        await cl.Message(content=f"An error occurred while finding the top buyers: {e}").send()


async def find_highest_bid():
    """
    Find the item with the highest bid and display it as a table.
    """
    try:
        highest_bid_item = data.loc[data["highest_bid"].idxmax(), ["item_name", "highest_bid"]]
        highest_bid_df = pd.DataFrame([highest_bid_item])
        response = create_markdown_table(highest_bid_df, "Item with the Highest Bid")
        await cl.Message(content=response).send()

    except Exception as e:
        await cl.Message(content=f"An error occurred while finding the highest bid: {e}").send()


async def find_top_three_purchased_items():
    """
    Find the top three most purchased items and display them as a table.
    """
    try:
        purchased_items = data[data["interaction"] == "purchased"]["item_name"].value_counts()
        top_items = purchased_items.nlargest(3)

        if top_items.empty:
            response = "No purchase data available."
        else:
            # Convert the results to a DataFrame for table display
            top_items_df = top_items.reset_index()
            top_items_df.columns = ["item_name", "purchase_count"]
                
             # Convert to markdown table
            response = create_markdown_table(top_items_df, "Top 3 Purchased Items by Quantity")

        await cl.Message(content=response).send()

    except Exception as e:
        await cl.Message(content=f"An error occurred while finding the top purchased items: {e}").send()


async def analyze_with_llm(query):
    """
    Use OpenAI's GPT API to analyze the dataset based on the user's query.
    """
    try:
        dataset_preview = data.to_string(index=False)
        
        prompt = f"""
        You are a data analysis assistant. Here is a preview of the dataset:
        {dataset_preview}

        The user asked: "{query}"

        Please analyze the dataset and provide a meaningful answer. If the query is unclear, ask the user for clarification.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.5
        )
        llm_response = response["choices"][0]["message"]["content"]
        await cl.Message(content=llm_response).send()

    except Exception as e:
        await cl.Message(content=f"An error occurred while processing your query: {e}").send()
