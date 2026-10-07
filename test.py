from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("SELECT GETDATE()"))
    print(result.fetchone())