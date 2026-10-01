import mysql.connector

class QueryBuilder:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self._reset_query_state()

    def _reset_query_state(self):
        self._select_sql = ""
        self._join_sql = ""
        self._where_sql = ""
        self._order_sql = ""
        self._limit_sql = ""
        self._where_params = []

    def select(self, table_name, columns="*"):
        self._reset_query_state()
        if isinstance(columns, list):
            cols_str = ", ".join([f"`{c.split('.')[0]}`.`{c.split('.')[1]}`" if "." in c else f"`{c}`" for c in columns])
        else:
            cols_str = columns
            
        self._select_sql = f"SELECT {cols_str} FROM `{table_name}`"
        return self

    def join(self, table, first_column, operator, second_column, join_type="INNER"):
        """Adds a JOIN clause safely mapping table columns."""
        allowed_types = {"INNER", "LEFT", "RIGHT", "OUTER", "CROSS"}
        allowed_operators = {"=", "!=", "<", ">", "<=", ">="}

        join_type_upper = join_type.upper()
        if join_type_upper not in allowed_types:
            raise ValueError(f"Invalid join type: {join_type}")
            
        if operator not in allowed_operators:
            raise ValueError(f"Invalid operator: {operator}")

        col1 = ".".join([f"`{part}`" for part in first_column.split(".")])
        col2 = ".".join([f"`{part}`" for part in second_column.split(".")])

        self._join_sql += f" {join_type_upper} JOIN `{table}` ON {col1} {operator} {col2}"
        return self

    def left_join(self, table, first_column, operator, second_column):
        return self.join(table, first_column, operator, second_column, join_type="LEFT")

    def right_join(self, table, first_column, operator, second_column):
        return self.join(table, first_column, operator, second_column, join_type="RIGHT")

    def where(self, columns, values, operators=None):
        if operators is None:
            operators = ["="] * len(columns)

        if not (len(columns) == len(values) == len(operators)):
            raise ValueError("Columns, values, and operators length mismatch.")

        allowed_operators = {"=", "!=", "<", ">", "<=", ">=", "LIKE"}
        conditions = []
        
        for col, op in zip(columns, operators):
            if op.upper() not in allowed_operators:
                raise ValueError(f"Invalid operator: {op}")
            
            formatted_col = ".".join([f"`{part}`" for part in col.split(".")])
            conditions.append(f"{formatted_col} {op} %s")

        self._where_sql = " WHERE " + " AND ".join(conditions)
        self._where_params = values
        return self

    def order_by(self, column, direction="ASC"):
        """Adds ORDER BY clause with strict direction validation."""
        direction_upper = direction.upper()
        if direction_upper not in {"ASC", "DESC"}:
            raise ValueError("Direction must be 'ASC' or 'DESC'")

        formatted_col = ".".join([f"`{part}`" for part in column.split(".")])
        self._order_sql = f" ORDER BY {formatted_col} {direction_upper}"
        return self

    def limit(self, limit, offset=None):
        """Adds LIMIT and optional OFFSET clause using integers."""
        if not isinstance(limit, int) or limit < 0:
            raise ValueError("Limit must be a non-negative integer")

        if offset is not None:
            if not isinstance(offset, int) or offset < 0:
                raise ValueError("Offset must be a non-negative integer")
            self._limit_sql = f" LIMIT {limit} OFFSET {offset}"
        else:
            self._limit_sql = f" LIMIT {limit}"
            
        return self

    def find(self):
        sql = (
            self._select_sql
            + self._join_sql
            + self._where_sql
            + self._order_sql
            + self._limit_sql
        )
        
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(sql, self._where_params)
            results = cursor.fetchall()

        self._reset_query_state()
        return results