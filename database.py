# from sqlalchemy import create_engine
# from sqlalchemy import text

# server = "DESKTOP-42M7LI5\SQLEXPRESS"
# database = "student"

# connection_string = ("mssql+pyodbc://@" + server + "/" + database + "?driver=ODBC+Driver+17+for+SQL+Server")
    


# engine = create_engine(connection_string)



# with engine.connect() as connection:
#     result = connection.execute(text("SELECT GETDATE()"))
#     print(result.fetchone())