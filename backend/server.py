import sqlite3
from flask import Flask, request
import flask
from flask_classful import FlaskView, route
from flask_cors import CORS
import requests
import json
from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer 
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app)

db_string = 'postgres://postgres:2310452227@localhost:5432/postgres'
db = create_engine(db_string)

base = declarative_base()

class Contract(base):  
    __tablename__ = 'Contracts'

    Name = Column(String)
    Address = Column(String, primary_key=True)
    FunctionName = Column(String)

class User(base):  
    __tablename__ = 'Users'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String)
    LastName = Column(String)

class UserUtils:

    @staticmethod
    @app.route('/createUser/', methods=['POST'])
    def createUser():
        pass

    @staticmethod
    @app.route('/deleteUser/', methods=['DELETE'])
    def deleteUser():
        pass
    
    @staticmethod
    @app.route('/updateUser/', methods=['PATCH'])
    def updateUser():
        pass

class ContractUtils:

    @staticmethod
    def getLocalContracts():
        f = open('../client/src/contracts/scooterTransactions.json')
        data = json.load(f)
        
        scooterTransactionsAddr = data['networks']['5777']['address']
        print(scooterTransactionsAddr)

        return scooterTransactionsAddr

    @staticmethod
    @app.route('/getContracts/', methods=['GET'])
    def getContracts():
        #
        # Returning all the Contract entries in the db
        #
        # data = request.args.to_dict()
        # print(data)
        Session = sessionmaker(db)  
        session = Session()
        
        contracts = session.query(Contract)
        data = {}
        for contract in contracts:
            data[contract.Address] = {'Name': contract.Name, 'FunctionName': contract.FunctionName, 'Address': contract.Address}
        session.commit()
        
        print(data)
        responseToReact = flask.Response(json.dumps(data))
        responseToReact.headers['Access-Control-Allow-Origin'] = '*'
        return responseToReact



    @staticmethod
    @app.route('/addContract/', methods=['POST'])
    def addContract():
        pass

    @staticmethod
    @app.route('/deleteContract/<address>', methods=['DELETE'])
    def deleteContract(address):
        pass
    
    @staticmethod
    @app.route('/updateContract/', methods=['POST'])
    def updateContract():
        data = request.values.to_dict()
        for key in data.keys():
            formData = json.loads(key)

        print(formData)

        Session = sessionmaker(db)  
        session = Session()

        # Checking if the Contract (address) already exists
        contracts = session.query(Contract)
        for contract in contracts:
            if formData['address'] == contract.Address:
                return 'Contract Already exists'

        genesys = Contract(Name=formData['name'], Address=formData['address'], FunctionName=formData['functionName'])
        session.add(genesys)

        session.commit()
        
        return 'OK'



class APICalls:

    @staticmethod
    @app.route('/getExchangeRates/', methods=['GET'])
    def getExchangeRates():
        #
        # Making an API call to the CoinLayer API
        # to get the current exchange rates
        #
        data = request.args.to_dict()

        coin = data['target']
        COINLAYER_URL = 'http://api.coinlayer.com/live'
        COINLAYER_API_KEY = 'eb3c76bbef63fe4aa71b802bc25bef0c'
        PARAMS = { 'access_key': COINLAYER_API_KEY, 'target': coin }
        HEADERS = {'content-type':'application/json'}
        
        response = requests.get(url=COINLAYER_URL, params=PARAMS, headers=HEADERS)
        data = json.loads(response.text)

        dataToSent = {'ETH': data['rates']['ETH'],
                 'BTC': data['rates']['BTC'],
                 'XRP': data['rates']['XRP']
        }

        responseToReact = flask.Response(json.dumps(dataToSent))
        responseToReact.headers['Access-Control-Allow-Origin'] = '*'
        return responseToReact

        


# Getting the address of the contract
scooterTransactionsAddr = ContractUtils.getLocalContracts()

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

# genesys = Contract(Name='Coffee Story', Address='address02', FunctionName='paymentFunction')
# session.add(genesys)  
session.commit()

users = session.query(User)
for x in users:
    print(x.LastName)

# # Connecting to the database
# db, base = ContractUtils.dbInit()

# # Creating Tables
# ContractUtils.create_tables(db)
    
app.run(debug=True)