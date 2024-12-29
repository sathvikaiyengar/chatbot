############################################################################################################
# The purpose of this simple chatbot is to simulate a QuizBot that quizzes users on Nobel Laureates.
# It demonstrates an "inverse chat pattern" in which the chatbot asks the user questions and expects  
# the user to answer from a predefined set of answers. This pattern can be useful in implementing user interfaces
# in which users interact with applications or data in a natural language-based conversational manner but are
# guided to provide specific types of responses. This ensures that that the interaction between the user and the
# chatbot is controlled and predictable, making it easier to manage the conversation flow and provide relevant
# information or assistance to the user.
#
# The chatbot uses a small dataset of Nobel Prize winners to ask the user questions about Nobel Prize 
# winners and provides hints if the user gets stuck.
# The chatbot provides the user with 3 chances to answer each question and congratulates the user if 
# they answer correctly.

# This simple chatbot uses the OpenAI API to generate a quiz based on a small subset of Nobel Prizewinners 
# data and to process user responses. It can be extended to handle a larger dataset of Nobel Prize winners and 
# provide more complex interactions with the user by converting it to use a RAG or an agentic RAG model based 
# on a vectorized dataset of Nobel Prize winners.

# To use the chatbot, run as a Panel app from the command line (in Windows) or terminal (in Mac or Linux).
# 1. Set the OPENAI_API_KEY environment variable to your OpenAI API key using the following or similar syntax:
#   >export OPENAI_API_KEY="your-api-key"
# 2. Run the code using the following command:
#    >panel serve simple-nobel-laureates-chatbot.py --port 8080 --dev
# 3. Open the browser and type the following URL to interact with the chatbot:
#    http://localhost:8080/simple-nobel-laureates-chatbot

# Notes:
# 1. This chatbot uses an older version of the OpenAI API and it is necessary to install it using the command:
#    >pip install openai==0.28.0
# 2. It also needs the following libraries to be installed:
#    >pip install panel==1.5.4
# 3. The chatbot does not use a RAG model or an agentic RAG model to generate responses. It uses a simple GPT-3.5 
#    model. Hence it may hallucinate or provide incorrect information in some cases.
#
#
# Effect of temperature on the model's responses:
# -----------------------------------------------
# The temperature parameter controls the randomness of the model's responses. A temperature of 0 results in the most likely response,
# while higher temperatures result in more random responses. The following experiments were carried out with various temperature
# settings:
# 1. Temperature = 0: This setting corresponds to the most deterministic responses from the model and it resulted in very terse
# responses from the model. Specifically, the hints provided were abstract and not that helpful. Also, the model kept repeating
# the same hints since it was deterministic, and this would not be helpful to the user.
# 2. Temperature = 0.5: This setting made the model's responses more creative and less deterministic. Diverse hints were provided were more
# specific and helpful to the user. However, the model abandoned the quiz format and started making "out-of-band" conversations like 
# "That is incorrect. Would you like a hint or would you like to try again?" instead of showing the quiz menu. 
# 3. Temperature = 1: This setting made the models responses more creative (as compared with temparature = 0). The model provided
# more detailed hints and responses to the user's prompts. 
############################################################################################################

import openai
import panel as pn #library for creating interactive dashboards
import os

# First, we set the OpenAI API key. This key is necessary to authenticate requests to OpenAI's servers.
openai.api_key = os.getenv("OPENAI_API_KEY")

def check_open_ai_key():
    if "OPENAI_API_KEY" in os.environ:
        print("OpenAI API key is set")
    else:
        print("OpenAI API key is not set\n")
        print("Please set the OPENAI_API_KEY environment variable to your OpenAI API key using the following or similar syntax:")   
        print(">export OPENAI_API_KEY=\"your-api-key\"")
        exit()

# This function calls the OpenAI API to generate a response to a user's prompt.
# It simulates a chat by passing a message with the role "user" and the user's content.
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.1,  # Low temperature results in more deterministic and less random responses
    )
    return response.choices[0].message["content"]

# This function is similar to get_completion but takes a list of messages for the conversation history.
# It's useful for maintaining context in a conversation.
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # A temperature of 0 results in the most likely response
    )
    return response.choices[0].message["content"]

# Initialize the Panel library for building GUI applications.
pn.extension()

# This list will collect the display components for the conversation.
panels = []

# This function collects messages from the user input, gets responses from the model, and updates the display.
def collect_messages(_):
    prompt = inp.value  # Extract the value the user has entered into the input field.
    inp.value = ''  # Clear the input field for the next message.
    context.append({'role': 'user', 'content': prompt})  # Append the user's message to the context.
    model="gpt-3.5-turbo"
    # response = get_completion_from_messages(context,model,1)  # Get a response from the model based on the conversation context.
    response = get_completion_from_messages(context,model,0.5)  # Get a response from the model based on the conversation context.
    context.append({'role': 'assistant', 'content': response})  # Append the response to the context.

    # Add the user's message and the chatbot's response to the panels list for display.
    panels.append(pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(pn.Row('Assistant:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'})))

    # Return a column of panels to display the conversation.
    return pn.Column(*panels)

# This context variable is a list of messages that gives the chatbot initial information about its role and the data it can use.
# Your chatbot's script and concert data here.
context = [{'role': 'system', 'content': """
You are QuizBot, a quiz loving chatbot that knows all triva about nobel prize winners.\
You first greet the user by saying "Are you ready to get quizzed! I am QuizBot and I'm here to quiz you on Nobel Prize winners. You get \
3 chances to answer each question. If you answer all the questions correctly, you may have a chance to win the Nobel Quiz Prize!\
Type "Go" and click Answer! to start!\

You use the {context} provided to frame a question and show three possible numbered choices including the correct answer. Place the correct answer randomly \
in the choices and wait for the answer from the user. 

If a particular prize has multiple winners, choose only one winner in the list of choices and choose the other two\
winners randomly from the list of prize winners from other years or categories. If the choices contain more than one correct winner, it is ok for the user to\
choose any correct answer.\

Add a 4th choice to each answer that allows the user to request a hint "Give me a hint". If the user selects option 4, then provide a hint and ask them to try again.\
If the user repeatedly asks for hints, provide a different hint each time.\
Add a 5th choice to each question that allows the user to select "Show me the answer". If the user selects option 5, then show the correct answer and move to the next question.\
Add a 6th choice to each question that allows the user to select "Give me additional information about the prize and the winner(s)". If the user selects option 6, then show \
additional general information about the prize and the winners but without revealing the names of the winners.\
Add a 7th choice to each question that allows the user to "Exit Quiz". If the user selects option 7, then thank them for playing and exit.\
            
The user gets 3 chances to answer correctly. If the user answers incorrectly, provide a hint and ask them to try again.\

If the user answers correctly, congratulate them and show them the next question.
            
# Sample nobel_prize_data to be used for the quiz. 
nobel_prize_data = {
    "prizes": [
        {
            "year": "2024",
            "category": "chemistry",
            "laureates": [
                {"id": "1039", "firstname": "David", "surname": "Baker", "motivation": "\"for computational protein design\"", "share": "2"},
                {"id": "1040", "firstname": "Demis", "surname": "Hassabis", "motivation": "\"for protein structure prediction\"", "share": "4"},
                {"id": "1041", "firstname": "John", "surname": "Jumper", "motivation": "\"for protein structure prediction\"", "share": "4"}
            ]
        },
        {
            "year": "2024",
            "category": "economics",
            "laureates": [
                {"id": "1044", "firstname": "Daron", "surname": "Acemoglu", "motivation": "\"for studies of how institutions are formed and affect prosperity\"", "share": "3"},
                {"id": "1045", "firstname": "Simon", "surname": "Johnson", "motivation": "\"for studies of how institutions are formed and affect prosperity\"", "share": "3"},
                {"id": "1046", "firstname": "James", "surname": "Robinson", "motivation": "\"for studies of how institutions are formed and affect prosperity\"", "share": "3"}
            ]
        },
        {
            "year": "2024",
            "category": "literature",
            "laureates": [
                {"id": "1042", "firstname": "Kang", "surname": "Han", "motivation": "\"for her intense poetic prose that confronts historical traumas and exposes the fragility of human life\"", "share": "1"}
            ]
        },
        {
            "year": "2024",
            "category": "peace",
            "laureates": [
                {"id": "1043", "motivation": "\"for its efforts to achieve a world free of nuclear weapons and for demonstrating through witness testimony that nuclear weapons must never be used again\"", "share": "1", "firstname": "Nihon Hidankyo"}
            ]
        },
        {
            "year": "2024",
            "category": "physics",
            "laureates": [
                {"id": "1037", "firstname": "John", "surname": "Hopfield", "motivation": "\"for foundational discoveries and inventions that enable machine learning with artificial neural networks\"", "share": "2"},
                {"id": "1038", "firstname": "Geoffrey", "surname": "Hinton", "motivation": "\"for foundational discoveries and inventions that enable machine learning with artificial neural networks\"", "share": "2"}
            ]
        },
        {
            "year": "2024",
            "category": "medicine",
            "laureates": [
                {"id": "1035", "firstname": "Victor", "surname": "Ambros", "motivation": "\"for the discovery of microRNA and its role in post-transcriptional gene regulation\"", "share": "2"},
                {"id": "1036", "firstname": "Gary", "surname": "Ruvkun", "motivation": "\"for the discovery of microRNA and its role in post-transcriptional gene regulation\"", "share": "2"}
            ]
        },
        {
            "year": "2023",
            "category": "chemistry",
            "laureates": [
                {"id": "1029", "firstname": "Moungi", "surname": "Bawendi", "motivation": "\"for the discovery and synthesis of quantum dots\"", "share": "3"},
                {"id": "1030", "firstname": "Louis", "surname": "Brus", "motivation": "\"for the discovery and synthesis of quantum dots\"", "share": "3"},
                {"id": "1031", "firstname": "Aleksey", "surname": "Yekimov", "motivation": "\"for the discovery and synthesis of quantum dots\"", "share": "3"}
            ]
        },
        {
            "year": "2023",
            "category": "economics",
            "laureates": [
                {"id": "1034", "firstname": "Claudia", "surname": "Goldin", "motivation": "\"for having advanced our understanding of women’s labour market outcomes\"", "share": "1"}
            ]
        },
        {
            "year": "2023",
            "category": "literature",
            "laureates": [
                {"id": "1032", "firstname": "Jon", "surname": "Fosse", "motivation": "\"for his innovative plays and prose which give voice to the unsayable\"", "share": "1"}
            ]
        },
        {
            "year": "2023",
            "category": "peace",
            "laureates": [
                {"id": "1033", "firstname": "Narges", "surname": "Mohammadi", "motivation": "\"for her fight against the oppression of women in Iran and her fight to promote human rights and freedom for all\"", "share": "1"}
            ]
        },
        {
            "year": "2023",
            "category": "physics",
            "laureates": [
                {"id": "1026", "firstname": "Pierre", "surname": "Agostini", "motivation": "\"for experimental methods that generate attosecond pulses of light for the study of electron dynamics in matter\"", "share": "3"},
                {"id": "1027", "firstname": "Ferenc", "surname": "Krausz", "motivation": "\"for experimental methods that generate attosecond pulses of light for the study of electron dynamics in matter\"", "share": "3"},
                {"id": "1028", "firstname": "Anne", "surname": "L’Huillier", "motivation": "\"for experimental methods that generate attosecond pulses of light for the study of electron dynamics in matter\"", "share": "3"}
            ]
        },
        {
            "year": "2023",
            "category": "medicine",
            "laureates": [
                {"id": "1024", "firstname": "Katalin", "surname": "Karikó", "motivation": "\"for their discoveries concerning nucleoside base modifications that enabled the development of effective mRNA vaccines against COVID-19\"", "share": "2"},
                {"id": "1025", "firstname": "Drew", "surname": "Weissman", "motivation": "\"for their discoveries concerning nucleoside base modifications that enabled the development of effective mRNA vaccines against COVID-19\"", "share": "2"}
            ]
        },
        {
            "year": "2022",
            "category": "chemistry",
            "laureates": [
                {"id": "1015", "firstname": "Carolyn", "surname": "Bertozzi", "motivation": "\"for the development of click chemistry and bioorthogonal chemistry\"", "share": "3"},
                {"id": "1016", "firstname": "Morten", "surname": "Meldal", "motivation": "\"for the development of click chemistry and bioorthogonal chemistry\"", "share": "3"},
                {"id": "743", "firstname": "Barry", "surname": "Sharpless", "motivation": "\"for the development of click chemistry and bioorthogonal chemistry\"", "share": "3"}
            ]
        },
        {
            "year": "2022",
            "category": "economics",
            "laureates": [
                {"id": "1021", "firstname": "Ben", "surname": "Bernanke", "motivation": "\"for research on banks and financial crises\"", "share": "3"},
                {"id": "1022", "firstname": "Douglas", "surname": "Diamond", "motivation": "\"for research on banks and financial crises\"", "share": "3"},
                {"id": "1023", "firstname": "Philip", "surname": "Dybvig", "motivation": "\"for research on banks and financial crises\"", "share": "3"}
            ]
        },
        {
            "year": "2022",
            "category": "literature",
            "laureates": [
                {"id": "1017", "firstname": "Annie", "surname": "Ernaux", "motivation": "\"for the courage and clinical acuity with which she uncovers the roots, estrangements and collective restraints of personal memory\"", "share": "1"}
            ]
        },
        {
            "year": "2022",
            "category": "peace",
            "laureates": [
                {"id": "1018", "firstname": "Ales", "surname": "Bialiatski", "motivation": "\"The Peace Prize laureates represent civil society in their home countries. They have for many years promoted the right to criticise power and protect the fundamental rights of citizens. They have made an outstanding effort to document war crimes, human right abuses and the abuse of power. Together they demonstrate the significance of civil society for peace and democracy.\"", "share": "3"},
                {"id": "1019", "motivation": "\"The Peace Prize laureates represent civil society in their home countries. They have for many years promoted the right to criticise power and protect the fundamental rights of citizens. They have made an outstanding effort to document war crimes, human right abuses and the abuse of power. Together they demonstrate the significance of civil society for peace and democracy.\"", "share": "3", "firstname": "Memorial"},
                {"id": "1020", "motivation": "\"The Peace Prize laureates represent civil society in their home countries. They have for many years promoted the right to criticise power and protect the fundamental rights of citizens. They have made an outstanding effort to document war crimes, human right abuses and the abuse of power. Together they demonstrate the significance of civil society for peace and democracy.\"", "share": "3", "firstname": "Center for Civil Liberties"}
            ]
        },
        {
            "year": "2022",
            "category": "physics",
            "laureates": [
                {"id": "1012", "firstname": "Alain", "surname": "Aspect", "motivation": "\"for experiments with entangled photons, establishing the violation of Bell inequalities and pioneering quantum information science\"", "share": "3"},
                {"id": "1013", "firstname": "John", "surname": "Clauser", "motivation": "\"for experiments with entangled photons, establishing the violation of Bell inequalities and pioneering quantum information science\"", "share": "3"},
                {"id": "1014", "firstname": "Anton", "surname": "Zeilinger", "motivation": "\"for experiments with entangled photons, establishing the violation of Bell inequalities and pioneering quantum information science\"", "share": "3"}
            ]
        },
        {
            "year": "2022",
            "category": "medicine",
            "laureates": [
                {"id": "1011", "firstname": "Svante", "surname": "Pääbo", "motivation": "\"for his discoveries concerning the genomes of extinct hominins and human evolution\"", "share": "1"}
            ]
        },
        
    ],
}"""}]

# Define the button for starting the conversation
button_conversation = pn.widgets.Button(name="Answer!")

# Set up the user interface for the chatbot.
# TextInput is where the user will type their messages.
inp = pn.widgets.TextInput(value="Quiz On", placeholder='Enter text here…')

# Binding the collect_messages function to be called when the button is clicked.
interactive_conversation = pn.bind(collect_messages, button_conversation)
# The dashboard puts together the input, button, and conversation display.
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

check_open_ai_key()
dashboard.servable()
#Run the code using: panel serve simple-nobel-laureates-chatbot.py --port 8080 --dev
#Open the browser and type: http://localhost:8080/simple-nobel-laureates-chatbot 