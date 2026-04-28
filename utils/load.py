from sqlalchemy import create_engine

def load_to_postgres(data, table_name, connector):
    try:
        engine = create_engine(connector)
        while engine.connection() as con:
            data.to_sql(table_name, con=engine, if_exist='replace',index=False)
            print(f"Data loaded to database succesfully")
    except Exception as e:
        print(f"Error occurs during loading: {e}")    
