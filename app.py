from flask import Flask, request,jsonify
import requests

app = Flask(__name__)

@app.route('/webhook',methods = ['GET','POST'])
def webhook():

    data = request.get_json(silent=True)
    if data['queryResult']['intent']['displayName'] == 'testimonial-yes':
        data = testimonials(data)
        return jsonify(data)
    
def testimonials(data):
    try:
        question1 = data['queryResult']['parameters']['question1']
        sessionIDName = data['queryResult']['outputContexts'][0]['name']
        # print(sessionIDName)
        sessionID = sessionIDName.split('sessions/')[1].split('/')[0]
        # print(sessionID)
        iteration = int(data['queryResult']['parameters']['iteration'])
        # print(question1)
        hopeKeywords = ['attitude','leadership','socialization','bullying','self esteem','focus','confidence','adhd','discipline','respect','self control']
        for keyword in hopeKeywords:
            if keyword in question1:
                url = "https://sheetdb.io/api/v1/zpz9l2516955c"
                payload = {}
                headers = {}
                response = requests.request("GET", url, headers=headers, data=payload)
                result = response.json()
                keywordList = []
                for res in result:
                    for key, val in res.items():
                        if key == keyword:
                            keywordList.append(val)
        # print(keywordList)
        print(iteration)
        # print(len(keywordList))
        # Check if the intent has been triggered 3 times in a row
        if iteration >= len(keywordList):
            # Perform any necessary actions or store the count value wherever you need
            # Reset the count
            iteration = 0
            reply = {
            'fulfillmentText': 'No more testimonials available'
            }
        else:
            response = keywordList[iteration]
            # Increment the count
            iteration += 1
            print(iteration)
            reply = {
                "fulfillmentMessages": [
                    # {
                    #     "text": {
                    #         "text": [response]
                    #     }
                    # },
                    {
                        "text": {"text": [response]}
                    },
                    {
                        "text": {
                            "text": [
                                f"Would you like to read another testimonial about {question1}"
                            ]
                        }
                    },
                    {
                        "payload": {
                            "richContent": [
                                [
                                    {
                                        "title": "Choose from below.."
                                    },
                                    {
                                        "options": [
                                            {
                                                "text": "Yes"
                                            },
                                            {
                                                "text": "No"
                                            }
                                        ],
                                        "type": "chips"
                                    }
                                ]
                            ]
                        }
                    }
                ]
                ,
                "outputContexts": [{
                    "name": f"projects/mastery-brwr/agent/sessions/{sessionID}/contexts/yes-newques",
                    "lifespanCount": 5,
                    "parameters": {
                        "iteration":iteration
                    }
                }]
            }

    except Exception as e:
        print(e)
    return reply

if __name__ == '__main__':
    app.run()
