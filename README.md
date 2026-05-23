# ETL Fashion Studio Case Study

A comprehensive case study project demonstrating an ETL (Extract, Transform, Load) pipeline that scrapes fashion product data from a fashion-themed website and loads it into multiple destinations.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Pipeline Architecture](#pipeline-architecture)
- [Project Modules](#project-modules)
- [Testing](#testing)
- [Requirements](#requirements)
- [License](#license)

## 🎯 Overview

This project implements a complete ETL pipeline that:
1. **Extracts** fashion product data from `https://fashion-studio.dicoding.dev`
2. **Transforms** the raw data into a structured, clean dataset with currency conversions
3. **Loads** the processed data into multiple destinations:
   - CSV file format
   - PostgreSQL database
   - Google Sheets

The project demonstrates best practices in data engineering, including error handling, modular design, and data validation through comprehensive testing.

## 📁 Project Structure

```
ETL_Fashion_Studio_Case/
├── main.py                    # Main ETL pipeline orchestrator
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── utils/                     # Utility modules
│   ├── extract.py            # Data extraction module
│   ├── transform.py          # Data transformation module
│   └── load.py               # Data loading module
└── tests/                     # Test suite
    ├── test_extract.py       # Extract module tests
    ├── test_transform.py     # Transform module tests
    └── test_load.py          # Load module tests
```

## ✨ Features

- **Web Scraping**: Extracts fashion product data using BeautifulSoup
- **Data Transformation**: Cleans and transforms data with Pandas, including currency conversion
- **Multi-destination Loading**: Supports CSV, PostgreSQL, and Google Sheets
- **Error Handling**: Comprehensive try-catch blocks for robust error management
- **Unit Testing**: Full test coverage with pytest
- **Modular Design**: Clean separation of concerns (Extract, Transform, Load)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL (if loading to database)
- Google Sheets API credentials (if loading to Google Sheets)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ichsan4Fa/ETL_Fashion_Studio_Case.git
   cd ETL_Fashion_Studio_Case
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### PostgreSQL Connection

To enable PostgreSQL loading, update the connection string in `main.py`:

```python
load_to_postgres(transform_df, "products", "postgresql://[username]:[password]@localhost:[port]/[dbname]")
```

Replace the placeholders:
- `[username]`: Your PostgreSQL username
- `[password]`: Your PostgreSQL password
- `[port]`: PostgreSQL port (default: 5432)
- `[dbname]`: Your database name

### Google Sheets Integration

To load data to Google Sheets:

1. Set up Google Sheets API credentials
2. Update the credentials in `main.py`:
   ```python
   load_to_google_sheets(transform_df, "[spreadsheets_id]", "Sheet1", "google-sheets-api.json")
   ```

Replace:
- `[spreadsheets_id]`: Your Google Sheets document ID
- `google-sheets-api.json`: Path to your credentials JSON file

## 🔄 Usage

### Running the Pipeline

Execute the main ETL pipeline:

```bash
python main.py
```

### Expected Output

```
Scraped data:
(n_rows, n_columns)
Transformed data: 
   product_name  original_price  converted_price  ...
0  ...           ...              ...              ...
(n_rows, n_columns)
Data loaded to CSV successfully.
```

### Output Files

- **products.csv**: CSV file containing the processed data

## 🏗️ Pipeline Architecture

### Extract Phase (`utils/extract.py`)
- Connects to the fashion studio website
- Scrapes product information (name, price, description, etc.)
- Handles network errors and invalid responses

### Transform Phase (`utils/transform.py`)
- Converts raw scraped data into a Pandas DataFrame
- Validates data quality
- Performs currency conversion (IDR to other currencies)
- Cleans and standardizes product information

### Load Phase (`utils/load.py`)
- Exports transformed data to CSV
- Writes data to PostgreSQL database
- Uploads data to Google Sheets

## 📦 Project Modules

### `main.py`
The main orchestrator that ties together the Extract, Transform, and Load phases. Includes comprehensive error handling for each phase.

### `utils/extract.py`
Handles all data extraction logic:
- `fetch_data()`: Generic data fetching function
- `scrape_products()`: Scrapes products from the website
- `extract_fashion_data()`: Extracts fashion-specific data

### `utils/transform.py`
Handles data transformation:
- `transform_to_dataframe()`: Converts raw data to DataFrame
- `transform_data()`: Applies transformations including currency conversion

### `utils/load.py`
Handles data loading:
- `load_to_csv()`: Saves data to CSV format
- `load_to_postgres()`: Loads data into PostgreSQL
- `load_to_google_sheets()`: Uploads data to Google Sheets

## 🧪 Testing

The project includes comprehensive test coverage for all modules.

### Running Tests

```bash
pytest
```

### Running Tests with Coverage Report

```bash
pytest --cov=utils --cov-report=html
```

### Test Modules

- **`tests/test_extract.py`**: Tests for data extraction functionality
- **`tests/test_transform.py`**: Tests for data transformation logic
- **`tests/test_load.py`**: Tests for data loading operations

## 📚 Requirements

```
python-crontab ~= 3.2
sqlalchemy~=2.0
psycopg2-binary~=2.9
pandas~=2.2
requests~=2.32
beautifulsoup4~=4.12
google-auth ~=2.36
google-api-python-client ~=2.152
pytest-cov ~=6.0
gspread ~=6.2.1
```

### Key Dependencies

- **pandas**: Data manipulation and analysis
- **requests**: HTTP library for web requests
- **beautifulsoup4**: HTML parsing for web scraping
- **sqlalchemy**: SQL toolkit and ORM
- **psycopg2-binary**: PostgreSQL adapter
- **google-auth, google-api-python-client, gspread**: Google Sheets integration
- **pytest-cov**: Testing framework with coverage

## 📝 License

This project is provided as-is for educational and case study purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📧 Contact

For questions or inquiries, please reach out to [@Ichsan4Fa](https://github.com/Ichsan4Fa)
