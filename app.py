from flask import Flask,request,jsonify
import pandas as pd
from flask import json
from flask import request
import requests

df=pd.read_csv('dig.csv')
h_df=pd.read_csv('dig_hosptal.csv')
#print(df.head(1))

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    print(data)

    if 'zip-code' in data['queryResult']['parameters']:
        zip = data['queryResult']['parameters']['zip-code']
        hospital_list = h_df[h_df['pincode'] == int(zip)].iloc[:, 0:2].values
        hospital = []
        rank = 0
        for i in hospital_list:
            rank += 1
            lis = (rank, ', '.join(map(str, i.flatten())))
            hospital.append(lis)
        )
        response = {
            'fulfillmentText': "List of Hospital in Your Pin code\n\n{}".format(hospital)
        }
        return jsonify(response)


    #nam = data['queryResult']['parameters']['given_name']
    if  'health_insurance' in data['queryResult']['parameters']:
        age = data['queryResult']['parameters']['number-integer']
        smoking = data['queryResult']['parameters']['tobacco']
        adult = data['queryResult']['parameters']['Adult']
        city = data['queryResult']['parameters']['geo-city']
        city_list = ['Hyderabad', 'Delhi', 'Mumbai', 'thane', 'navi Mumbai', 'kalyan']
        print(age)
        print(smoking)
        print(adult)


        slot = ''
        tob = 0
        member_total = ''
        cit = 0

        if adult == '1 Adult':
            member_total = '1A'
        if adult == '2 Adult':
            member_total = '2A'
        if adult == '2 Adult And 1 Child':
            member_total = '2A1C'
        if adult == '2 Adult And 2 Child':
            member_total = '2A2C'

        if smoking == 'No' or smoking == 'no':
            tob = 0.05
        if smoking == 'Yes' or smoking == 'yes':
            tob = 0

        if city in city_list:
            cit = 0
        if city not in city_list:
            cit = .10

        if age < 66:
            if age < 35:
                slot = '0-35'
            if age > 35 and age < 46:
                slot = '36-45'
            if age > 45 and age < 51:
                slot = '46-50'
            if age > 50 and age < 56:
                slot = '51-55'
            if age > 55 and age < 61:
                slot = '56-60'
            if age > 60 and age < 66:
                slot = '61-65'

            if age > 65:
                slot = 'Sorry your Age is Outof Our Plan'

            a=df[(df.age == slot)&(df.member==member_total)].iloc[:,1:].values

            print(a)

            da = {'5 lakh': '  ' + str(a[0][0]) + ' Rs' + '  ',
                  '10 lakh': '  ' + str(a[0][1]) + ' Rs' + '  ',
                  '15 lakh': '  ' + str(a[0][2]) + ' Rs' + '  ',
                  '25 lakh': '  ' + str(a[0][3]) + ' Rs' + '  ',
                  '50 lakh': '  ' + str(a[0][4]) + ' Rs' + '  ',
                  '100 lakh': '  ' + str(a[0][5]) + ' Rs'+' '
                  }
            print(da)
            dis = {'5 lakh': '  ' + str(round(a[0][0] * (1 - (tob + cit)),2)) + ' Rs' + '  ',
                   '10 lakh': '  ' + str(round(a[0][1] * (1 - (tob + cit)),2))+ ' Rs' + '  ',
                   '15 lakh': '  ' + str(round(a[0][2] * (1 - (tob + cit)),2)) + ' Rs' + '  ',
                   '25 lakh': '  ' + str(round(a[0][3] * (1 - (tob + cit)),2)) + ' Rs' + '  ',
                   '50 lakh': '  ' + str(round(a[0][4] * (1 - (tob + cit)),2)) + ' Rs' + '  ',
                   '100 lakh': '  ' + str(round(a[0][5] * (1 - (tob + cit)),2)) + ' Rs'
                   }

            print(dis)

            #print('Congratulation You get 15% Discount\n', dis)
            discount =  round(100 * (tob + cit))
            response = {
                'fulfillmentText': "{}\n\n Congratulation You get {}% Discount\n\n{}".format(da,discount,dis)
            }
            # response ={
            #     'fulfillmentText': "{} Congratulation You get {}% Discount\n\n {}".format(da, discount, dis)
            # }#Thank You {} For Visit Us\n\n
            return jsonify(response)
        if age > 65:
            response = {
                'fulfillmentText': "Sorry your Age is not Available in Our Plan"
            }
            return jsonify(response)
if __name__ == "__main__":
    app.run(debug=True)