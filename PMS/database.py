from pymongo import MongoClient

class Database:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_portfolio(self, portfolio_data):
        self.db.portfolios.insert_one(portfolio_data)

    def find_portfolio(self, portfolio_name):
        return self.db.portfolios.find_one({"name": portfolio_name})

    def update_portfolio(self, portfolio_name, new_transaction):
        self.db.portfolios.update_one({"name": portfolio_name}, {"$push": {"transactions": new_transaction}})

    def delete_portfolio(self, portfolio_name):
        return self.db.portfolios.delete_one({"name": portfolio_name})
