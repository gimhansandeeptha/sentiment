from dotenv import load_dotenv
import os
from datetime import datetime
from src.database.connectdb import DatabaseConnection
from src.database.createdb import CreateDB
from src.servicenow.data_object import SentimentData

environment_variable_file_path = ".\\src\\database\\.env"
load_dotenv(environment_variable_file_path)

username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
hostname = 'localhost'
username = 'root'
database = 'sentiment'

class Database():
    def __init__(self) -> None:
        self.hostname = hostname
        self.database_name = database
        self.username = username
        self.password = password

    def _check_database_existance(self):
        db=DatabaseConnection(hostname = self.hostname,
                              database = None,
                              username = self.username,
                              password = self.password
                              )
        db.connect()
        check_query = "SHOW DATABASES"
        db_list = db.query(check_query)
        db.disconnect()
        if (self.database_name,) in db_list:
            return True
        else:
            return False


    def create(self):
        if not self._check_database_existance():  
            db=CreateDB(hostname = self.hostname,
                        database_name = self.database_name,
                        username = self.username,
                        password = self.password
                        )
            db.create()
            db.create_schema()
        return 
    
    def insert_gpt_sentiment(self, sentiment_data: SentimentData):
        db=DatabaseConnection(hostname = self.hostname,
                              database = self.database_name,
                              username = self.username,
                              password = self.password
                              )
        db.connect()
        try:
            for case in sentiment_data.cases:
                entries = case.get('entries')
                for comment in entries:
                    text = comment.get("value")
                    sentiment = comment.get("gpt_sentiment", None)
                    created_on = comment.get("created_on", datetime.now())
                    insert_query = f"INSERT INTO gpt (text, sentiment, sys_created_on) VALUES ('{text}','{sentiment}','{created_on}')"
                    db.query(insert_query)
        finally:
            db.disconnect

    
    def insert_cases(self, sentiment_data:SentimentData):
        ''' Value is assumed to be a list with the following format: Incorrect now 
        value = [["case_id 01", "Account_name1",["comment 01","comment 02", ...],["sentiment 01","sentiment 2", ...]], 
                 ["case_id 02", "Account_name2",["comment 01","comment 02", ...],["sentiment 01","sentiment 2", ...]],... 
                ]
        '''
        db=DatabaseConnection(hostname=hostname,
                              database=database,
                              username=username,
                              password=password
                              )
        db.connect()
        try:
            for case in sentiment_data.cases:
                case_id = case.get('case_id')
                account_name = case.get('account')
                sys_created_on = case.get('sys_created_on',datetime.now())
                entries = case.get('entries')

                insert_account = f"INSERT INTO account (case_id, sys_created_on, account_name) VALUES ('{case_id}','{sys_created_on}','{account_name}')"
                db.query(insert_account)
                # Insert into comment table
                for entry in entries:
                    comment = entry.get('value')
                    sentiment = entry.get('sentiment')
                    insert_comment = f"INSERT INTO comment (id, comment, sentiment, account_case_id) VALUES (NULL, '{comment}', '{sentiment}', '{case_id}')"
                    db.query(insert_comment)
            
        finally:
            db.disconnect

    def delete_all_gpt_entries(self):
        db=DatabaseConnection(hostname=hostname,
                              database=database,
                              username=username,
                              password=password
                              )
        db.connect()
        try:
            query_gpt="DELETE FROM gpt"
            db.query(query_gpt)
        finally:
            db.disconnect()

    def delete_all_cases(self):
        db=DatabaseConnection(hostname=hostname,
                              database=database,
                              username=username,
                              password=password
                              )
        db.connect()
        try:
            query_account = "DELETE FROM account"
            query_comment = "DELETE FROM comment"
            db.query(query_comment)
            db.query(query_account)
        finally:
            db.disconnect()

    def get_gpt_entries(self, count):
        result = None
        query = f"""
                WITH RankedData AS (
                SELECT
                    id,
                    text,
                    sentiment,
                    sys_created_on,
                    ROW_NUMBER() OVER (PARTITION BY sentiment ORDER BY sys_created_on DESC) AS rn
                FROM
                    gpt
                )
                SELECT
                    id,
                    text,
                    sentiment,
                    sys_created_on
                FROM
                    RankedData
                WHERE
                    rn <= {count};
                """
        db=DatabaseConnection(hostname=hostname,
                              database=database,
                              username=username,
                              password=password
                              )
        db.connect()
        try:
            result = db.query(query)
        finally:
            db.disconnect()
        return result
        

    def get_cases_by_date(self, start_date, end_date):
        result = ''
        query_by_date = f"""
                            SELECT 
                                a.account_name, 
                                a.case_id, 
                                a.sys_created_on, 
                                c.comment, 
                                c.sentiment
                            FROM account a
                            JOIN comment c ON a.case_id = c.account_case_id
                            WHERE Date(sys_created_on) BETWEEN '{start_date}' AND '{end_date}';
                        """
        db=DatabaseConnection(hostname=hostname,
                              database=database,
                              username=username,
                              password=password
                              )
        db.connect()
        try:
            result = db.query(query_by_date)
        finally:
            db.disconnect()
        return result
    
    def get_sentiment_category_count(self):
        count_query = '''
                    SELECT
                        sentiment,
                        COUNT(*) AS total_count
                    FROM
                        gpt
                    GROUP BY
                        sentiment;
                    '''
        db=DatabaseConnection(hostname=hostname,
                              database=database,
                              username=username,
                              password=password
                              )
        db.connect()
        try:
            result = db.query(count_query)
        finally:
            db.disconnect()
        
        count_dict ={}
        for sentiment_label, count in result:
            count_dict[sentiment_label] = count

        return count_dict
    
    def delete_excessive_gpt_data(self, sentiment_label, count_to_delete:int):
        delete_query = f'''
                        DELETE FROM GPT
                        WHERE sentiment = '{sentiment_label}'
                        AND id IN (
                            SELECT id
                            FROM (
                                SELECT id
                                FROM GPT
                                WHERE sentiment = '{sentiment_label}'
                                ORDER BY sys_created_on ASC
                                LIMIT {count_to_delete}
                            ) AS subquery
                        );
                        '''
        db=DatabaseConnection(hostname=hostname,
                        database=database,
                        username=username,
                        password=password
                        )
        db.connect()
        try:
            result = db.query(delete_query)
        finally:
            db.disconnect()
                
    
    # def get_gpt_entries(self, entry_count):
    #     query1 = f"""
    #             WITH RankedComments AS (
    #             SELECT 
    #                 text,
    #                 sentimet,
    #                 ROW_NUMBER() OVER (PARTITION BY sentimet ORDER BY date_column DESC) AS rn
    #             FROM 
    #                 gpt
    #             )
    #             SELECT 
    #             text,
    #             sentimet
    #             FROM 
    #             RankedComments
    #             WHERE 
    #             rn <= {entry_count//3};
    #         """
    #     result = ''
        
    #     db=DatabaseConnection(hostname=hostname,
    #                           database=database,
    #                           username=username,
    #                           password=password
    #                           )
    #     db.connect()
    #     try:
    #         result = db.query(query1)
    #     finally:
    #         db.disconnect()
    #     # return result
    #     print(result)


# # Unit Testing
# response = [{'case_id': 'CS0431996', 'account': 'Test Customer Account', 'sys_created_on': '2024-03-11 02:16:41', 'entries': [{'value': 'Closed by contributor : Samitha Rathnayake (Intern)  ⓦ', 'created_on': '2024-03-11 02:17:05', 'sentiment': 'Positive'}, {'value': '<br><b> <u>Incident impact description</u> </b><br><p>Testing</p><br><b> <u>Description</u> </b><br><p></p><p>Test Description</p><p></p>', 'created_on': '2024-03-11 02:16:41', 'sentiment': 'Positive'}]}, {'case_id': 'CS0432040', 'account': 'DemoCloud', 'sys_created_on': '2024-03-11 08:41:08', 'entries': [{'value': 'Solution Accepted \n', 'created_on': '2024-03-11 08:45:05', 'sentiment': 'Positive'}, {'value': '<p>agent commented in here with different proposal,</p>', 'created_on': '2024-03-11 08:44:46', 'sentiment': 'Negative'}, {'value': 'Proposed Solution Rejected \nI prefer different solution...', 'created_on': '2024-03-11 08:44:18', 'sentiment': 'Negative'}, {'value': 'Case moved to Waiting on WSO2 \n', 'created_on': '2024-03-11 08:43:16', 'sentiment': 'Neutral'}, {'value': '<p>Customer commented here..</p>', 'created_on': '2024-03-11 08:43:05', 'sentiment': 'Neutral'}, {'value': '<br><b> <u>Description</u> </b><br><p></p><p>Test goes here</p><p></p>', 'created_on': '2024-03-11 08:41:08', 'sentiment': 'Neutral'}]}]

# db = Database()
# db.create()
# db.insert(response)
            
# # Unit testing : Delete
# db = Database()
# db.delete_all()
    
# # Unit testing: get_cases_by_date
# db = Database()
# result = db.get_cases_by_date("2024-03-19","2024-03-19")
# print(result)


# # Unit testing: _check_database_existance
# db = Database()
# result = db._check_database_existance()
# print(result)
        
# # Unit testing for create()
# db = Database()
# db.create()
        
# # Unit testing for _get_sentiment_category_count
# db = Database()
# result = db.get_sentiment_category_count()
# for sentimet_label, count in result:
#     print(f"sentiment: {sentimet_label}             count: {count}")
