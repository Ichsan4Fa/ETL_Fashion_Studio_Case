import gspread

from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials

def load_to_csv(data, file_path):
    data.to_csv(file_path, index=False)

def load_to_postgres(data, table_name, connector):
    try:
        engine = create_engine(connector)
        with engine.connect() as connection:
            data.to_sql(table_name, con=engine, if_exists='replace', index=False)
            print(f"Data loaded to database succesfully")
    except Exception as e:
        print(f"Error occurs during loading: {e}")

def load_to_google_sheets(data, spreadsheet_id, sheet_name, credentials):
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(credentials, scopes=scope)
        client = gspread.authorize(creds)

        # Convert datetime/Timestamp columns to strings to ensure JSON serializability
        data_copy = data.copy()
        for col in data_copy.columns:
            if data_copy[col].dtype == 'object' or str(data_copy[col].dtype).startswith('datetime'):
                try:
                    data_copy[col] = data_copy[col].astype(str)
                except Exception:
                    pass

        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        sheet.clear()
        sheet.update([data_copy.columns.values.tolist()] + data_copy.values.tolist())
        print(f"Data loaded to Google Sheets successfully.")
    except Exception as e:
        print(f"Error occurs during loading to Google Sheets: {e}")    
