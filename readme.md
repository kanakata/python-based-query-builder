# python based query-builder

## creating a table
```python
qb = QueryBuilder("database_host", "database_username", "database_password", "database_name")   
def definitions():
    return {
        "id": ["int"],
        "name": ["varchar(255)"],
        "email": ["varchar(255)"]
    }
qb.create_table("table_name", definitions)
```

## inserting data
```python 
qb = QueryBuilder("database_host", "database_username", "database_password", "database_name")  
qb.insert("table_name", ["column_1","column_2"], ["column_1_data", "column_2_data"])
```