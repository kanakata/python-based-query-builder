import mysql.connector 

class QueryBuilder:
    def __init__(self, database_host, database_username, database_password, database_name):
        self.database_connection = mysql.connector.connect(host=database_host, user=database_username,password=database_password, database=database_name)
        
    def instance(self):
        return self.database_connection.cursor()
        
    def create_table(self,table_name, callback):
        try:
            definitions = callback()
            _def = ""
            count = 1
            for x in definitions:
                if count == len(definitions):
                    _def += f"{x} {" ".join(definitions[x])}"
                else:
                    _def += f"{x} {" ".join(definitions[x])},"
                count += 1
                
            sql = f"CREATE TABLE {table_name} ({_def})"
            self.instance().execute(sql)
        except:
            print("error")
    
    def insert(self, table_name, columns, data):
        try:
            bindings = []
            for x in data:
                bindings.append("%s")
            sql = f"INSERT INTO {table_name} ({",".join(columns)}) VALUES ({",".join(bindings)})"
            self.instance().execute(sql, data)
            self.database_connection.commit()
        except:
            print('Error')
            
    def select(self, table_name, columns = "*"):
        if columns == "*":
            self.select_sql = f"SELECT * FROM {table_name}"
        else:
            self.select_sql = f"SELECT {",".join(columns)} FROM"
        return self
    
    def where(self, columns, data, operators):
        if len(columns) == len(data) == len(operators):
            sql = " WHERE "
            for x in range(len(columns)):
                if x == len(columns)-1:
                    sql += f"`{columns[x]}`{operators[x]}%s"
                else:
                    sql += f"`{columns[x]}`{operators[x]}%s and"
                
            self.where_sql = sql
        else:
            raise Exception("Column to data to operator miss match")
        
        return self
        
    def find(self):
        sql = self.select_sql + self.where_sql
        print(sql)
        pass


qb = QueryBuilder("localhost", "root", "", "nyathi")
qb.select("patrick", ["name", "email"]).where(["name", "email"], ["jane doe", "jane@gmail.com"], ["=", "="]).find()