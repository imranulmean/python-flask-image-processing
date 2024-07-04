import pandas as pd
import cx_Oracle
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# app instance
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/generateReport', methods=['POST'])
def generateReport():
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    # Debug: print start_date and end_date
    print("Start Date:", start_date)
    print("End Date:", end_date)
    
    # Connect to the database
    dsn_tns = cx_Oracle.makedsn('10.20.3.35', '16122', service_name='PDBIB')
    conn = cx_Oracle.connect(user='ICT_ANIKA', password='ICT_ANIKA', dsn=dsn_tns)
    
    # Create cursor
    cursor = conn.cursor()

    # Define the queries with parameterized dates
    sql_branch = """ 
        SELECT FT_CHANNEL, COUNT(*) AS NO_OF_TRXN, SUM(TRAMOUNT) AS TOTAL_AMOUNT_OF_TRXN
        FROM TRANSACTIONRECORD
        WHERE trdate BETWEEN TO_DATE(:start_date, 'DD-MON-YYYY') AND TO_DATE(:end_date, 'DD-MON-YYYY')
        AND trstatus IN ('SUCCESS', 'PENDING')
        AND FT_CHANNEL IN ('EFT', 'RTGS', 'NPSB')
        GROUP BY FT_CHANNEL"""

    sql_acc = """ 
        SELECT COUNT(*) AS NO_OF_TRXN, SUM(TRAMOUNT) AS TOTAL_AMOUNT_OF_TRXN 
        FROM TRANSACTIONRECORD 
        WHERE trdate BETWEEN TO_DATE(:start_date, 'DD-MON-YYYY') AND TO_DATE(:end_date, 'DD-MON-YYYY')
        AND trstatus IN ('SUCCESS', 'PENDING')"""

    sql_user = "SELECT COUNT(USER_NAME) AS IB_USER FROM CLIENT_USER_INFO"

    sql_sms = "SELECT COUNT(*) AS TOTAL_SMS_ACC FROM NTFY_CLIENT_CF@PDBSMS_DBLINK"

    # Execute the queries and fetch the results
    cursor.execute(sql_branch, start_date=start_date, end_date=end_date)
    df_branch = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

    cursor.execute(sql_acc, start_date=start_date, end_date=end_date)
    df_acc = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

    cursor.execute(sql_user)
    df_user = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

    cursor.execute(sql_sms)
    df_sms = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

    # Combine the results into a single DataFrame
    values = [
        df_user["IB_USER"].values[0], 
        df_acc["NO_OF_TRXN"].values[0], 
        df_acc["TOTAL_AMOUNT_OF_TRXN"].values[0], 
        df_branch[df_branch['FT_CHANNEL'] == 'EFT'][['NO_OF_TRXN', 'TOTAL_AMOUNT_OF_TRXN']].values.flatten().tolist(), 
        df_branch[df_branch['FT_CHANNEL'] == 'RTGS'][['NO_OF_TRXN', 'TOTAL_AMOUNT_OF_TRXN']].values.flatten().tolist(), 
        df_branch[df_branch['FT_CHANNEL'] == 'NPSB'][['NO_OF_TRXN', 'TOTAL_AMOUNT_OF_TRXN']].values.flatten().tolist(),
        0, 0,  # Fraud through Internet Banking
        df_sms["TOTAL_SMS_ACC"].values[0]
    ]

    # Flatten nested lists
    flattened_values = [item for sublist in values for item in (sublist if isinstance(sublist, list) else [sublist])]

    df_combined = pd.DataFrame({
        "Category": ["Internet Banking"] + 
                    ["Internet Banking Transactions"]*2 + 
                    ["EFT Transactions initiated through Internet Banking"]*2 + 
                    ["RTGS Transactions initiated through Internet Banking"]*2 + 
                    ["NPSB Transactions initiated through Internet Banking"]*2 +
                    ["Fraud through Internet Banking"]*2 +
                    ["SMS Banking"],
        "Details": ["Total No. of Internet Banking Customers"] + 
                   ["No. of Transaction", "Value of Transaction"] + 
                   ["No. of Transaction", "Value of Transaction"] + 
                   ["No. of Transaction", "Value of Transaction"] + 
                   ["No. of Transaction", "Value of Transaction"] + 
                   ["No. of Transaction", "Value of Transaction"] + 
                   ["Total No. of A/C facilitated with SMS Banking"],
        "Values": flattened_values,
        "Menu" : [
            "Internet Banking",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "SMS Banking"
        ],
        "Remarks": [
            "Internet Banking As on Reporting Date",
            "For Reporting Month Only",
            "For Reporting Month Only",
            "For Reporting Month Only",
            "For Reporting Month Only",
            "For Reporting Month Only",
            "For Reporting Month Only",
            "For Reporting Month Only",
            "For Reporting Month Only",
            "For Reporting Month Only",
            "For Reporting Month Only",
            "SMS Banking As on Reporting Date"
        ]
    })

 # Ensure the uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Define the output file path
    output_file = os.path.join(app.config['UPLOAD_FOLDER'], f"monthly_trxn_report_{start_date}_to_{end_date}.xlsx")

    # Save the result to an Excel file
    df_combined.to_excel(output_file, index=False)
      # Close the database connection
    cursor.close()
    conn.close()

    return jsonify({
        "msg": "File Uploaded Successfully",
        "file_path": output_file
    })

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True, host="172.23.1.217", port=8080)