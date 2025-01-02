# Python backend for QuizBot 
# Usage Instructions:
# 1. Set the OPENAI_API_KEY environment variable to your OpenAI API key using the following or similar syntax:
#       export OPENAI_API_KEY="your-api-key"
# 2. Run the code using the following command:
#       python simple-nobel-laureates-chatbot.py --port 8080

############################################################################################################

import openai
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def check_open_ai_key():
    if "OPENAI_API_KEY" in os.environ:
        print("OpenAI API key is set")
    else:
        print("OpenAI API key is not set\n")
        print("Please set the OPENAI_API_KEY environment variable to your OpenAI API key using the following or similar syntax:")   
        print(">export OPENAI_API_KEY=\"your-api-key\"")
        exit()


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # temperature controls the randomness of the model's responses (0 = most deterministic, 
                                  # 0.5 = more creative, less deterministic, 1 = maximum creativity)
    )
    return response.choices[0].message["content"]

@app.route('/quiz', methods=['POST'])
def quiz():
    data = request.json
    prompt = data.get('prompt', '')
    context.append({'role': 'user', 'content': prompt})
    model = "gpt-3.5-turbo"
    response = get_completion_from_messages(context, model, 0.5)
    context.append({'role': 'assistant', 'content': response})
    return jsonify({'response': response})

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

if __name__ == '__main__':
    check_open_ai_key()
    app.run(host='0.0.0.0', port=8080)
