import mysql.connector 

class QueryBuilder:
    def __init__(self, database_host, database_username, database_password, database_name):
        self.database_connection = mysql.connector.connect(host=database_host, user=database_username,password=database_password, database=database_name)
        
    def create_table(self, callback):
        definitions = callback()
        table_definitions = ""
        for i in definitions:
            table_definitions += "\n" + i + " " + " ".join(definitions[i]) + ","
        self.table = f"CREATE TABLE (\n{table_definitions}\n)"
        print(self.table) 
        return self
    
    def table(self, table_name):
        self.table = table_name
        return self
    
qb = QueryBuilder("localhost", "root", "", "nyathi")   

def definitions():
    return {
        "id": ["not null"],
        "name": ["not null"]
    }
    
qb.table("patrick").create_table(definitions)