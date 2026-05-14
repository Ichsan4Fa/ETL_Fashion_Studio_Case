import gspread

from sqlalchemy import create_engine
from oauth2client.service_account import ServiceAccountCredentials

def load_to_csv(data, file_path):
    data.to_csv(file_path, index=False)

def load_to_postgres(data, table_name, connector):
    try:
        engine = create_engine(connector)
        with engine.connection() as con:
            data.to_sql(table_name, con=engine, if_exist='replace',index=False)
            print(f"Data loaded to database succesfully")
    except Exception as e:
        print(f"Error occurs during loading: {e}")

def load_to_google_sheets(data, spreadsheet_id, sheet_name, credentials):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        sheet.clear()
        sheet.update([data.columns.values.tolist()] + data.values.tolist())
        print(f"Data loaded to Google Sheets successfully.")
    except Exception as e:
        print(f"Error occurs during loading to Google Sheets: {e}")    
