from flask import Flask, request,jsonify
import requests

app = Flask(__name__)

@app.route('/webhook',methods = ['GET','POST'])
def webhook():

    data = request.get_json(silent=True)
    if data['queryResult']['intent']['displayName'] == 'testimonial-yes':
        data = testimonials(data)
        return jsonify(data)


    # elif data['queryResult']['intent']['displayName'] == 'test':
    #     reply = {
    #         "fulfillmentText": "Test",
    #     }
    #     return jsonify(reply)

def testimonials(data):
    try:
        question1 = data['queryResult']['parameters']['question1']
        print(question1)
        hopeKeywords = ['attitude','leadership','socialization','bullying','self esteem','focus','confidence','adhd','discipline','respect','self control']
        for keyword in hopeKeywords:
            if keyword in question1:
                url = "https://sheetdb.io/api/v1/t916pxx3nsrot"
                payload = {}
                headers = {}
                response = requests.request("GET", url, headers=headers, data=payload)
                # print(response.json())
                result = response.json()
                # res = result[0]
                keywordList = []
                for res in result:
                    for key,val in res.items():
                        if key == keyword:
                            keywordList.append(val)
                print(keywordList)

               
        reply = {}
    except Exception as e:
        print(e)
    return reply

if __name__ == '__main__':
    app.run(debug=True)
