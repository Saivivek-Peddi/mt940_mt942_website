import json
import mt940
import pandas as pd
import openpyxl
from pandas import ExcelWriter
from pandas.io.json import json_normalize

def parse_func(path, filename):

    transactions = mt940.parse(path)

    # with open('combined.json', 'w') as json_file:  
    #     json.dump(transactions, json_file)

    # with open('combined.json') as f:
    #     d = json.load(f)
    d = transactions
    df = json_normalize(transactions)
    df2 = (pd.concat({i: json_normalize(x) for i, x in df.pop('transactions').items()},sort=False)
            .reset_index(level=1, drop=True)
            .join(df,lsuffix='_in_transactions', rsuffix='_if_opening_NA')
            .reset_index(drop=True))
    try:
        df2 = df2[['account_identification', 'date', 'amount.currency', 'amount.amount', 'status', 'customer_reference', 'transaction_reference', 'extra_details', 'transaction_details', 'final_opening_balance.date', 'final_opening_balance.status', 'final_opening_balance.amount.amount', 'final_opening_balance.amount.currency', 'entry_date', 'funds_code', 'guessed_entry_date', 'id', 'available_balance.date', 'available_balance.status', 'available_balance.amount.amount', 'available_balance.amount.currency', 'final_closing_balance.date', 'final_closing_balance.status', 'final_closing_balance.amount.amount', 'final_closing_balance.amount.currency', 'sequence_number', 'statement_number']]
        df2 = df2.rename(columns={'account_identification': 'Bank account no.', 'date': 'Transacton date', 'amount.currency': 'Amount currency', 'amount.amount': 'Amount', 'status': 'Transaction type', 'customer_reference': 'Transaction reference', 'transaction_reference': 'Reference no.', 'extra_details': 'Additional reference', 'transaction_details': 'Remarks', 'final_opening_balance.date': 'Opening balance date', 'final_opening_balance.status': 'Opening balance status', 'final_opening_balance.amount.amount': 'Opening balance amount', 'final_opening_balance.amount.currency': 'Opening balance currency', 'entry_date': 'Entry date', 'funds_code': 'Fund code', 'guessed_entry_date': 'Addl. Entry date', 'id': 'ID', 'available_balance.date': 'Available balance date', 'available_balance.status': 'Available balance type', 'available_balance.amount.amount': 'Available balance', 'available_balance.amount.currency': 'Available balance currency', 'final_closing_balance.date': 'Ledger balance date', 'final_closing_balance.status': 'Ledger balance type', 'final_closing_balance.amount.amount': 'Ledger balance amount', 'final_closing_balance.amount.currency': 'Ledger balance currency', 'sequence_number': 'Sequence no.', 'statement_number': 'Statement no.'})
    except:
        pass
    #print(df2.head(3))
    #print(df2.shape)
    writer = ExcelWriter(filename)
        
    df2.to_excel(writer,sheet_name='Transactional_Data',index = False)
    writer.save()

    try:
        d[:] = [item for item in d if not item['transactions']]
        df = json_normalize(d)
        df = df[['account_identification', 'final_opening_balance.date', 'final_opening_balance.status', 'final_opening_balance.amount.amount', 'final_opening_balance.amount.currency', 'final_closing_balance.date', 'final_closing_balance.status', 'final_closing_balance.amount.amount', 'final_closing_balance.amount.currency', 'available_balance.date', 'available_balance.status', 'available_balance.amount.amount', 'available_balance.amount.currency', 'sequence_number', 'statement_number', 'transaction_reference']]
        df = df.rename(columns={'account_identification': 'Bank account no.', 'final_opening_balance.date': 'Opening balance date', 'final_opening_balance.status': 'Opening balance status', 'final_opening_balance.amount.amount': 'Opening balance amount', 'final_opening_balance.amount.currency': 'Opening balance currency', 'final_closing_balance.date': 'Ledger balance date', 'final_closing_balance.status': 'Ledger balance type', 'final_closing_balance.amount.amount': 'Ledger balance amount', 'final_closing_balance.amount.currency': 'Ledger balance currency', 'available_balance.date': 'Available balance date', 'available_balance.status': 'Available balance type', 'available_balance.amount.amount': 'Available balance', 'available_balance.amount.currency': 'Available balance currency', 'sequence_number': 'Sequence no.', 'statement_number': 'Statement no.', 'transaction_reference': 'Transaction reference'})
#         del df['transactions']

# # print(df.head(3))
        # print(df.shape)
        
        df.to_excel(writer,sheet_name='Non_Transactional_Data',index=False)
        writer.save()
    except:
        pass
    # wb = openpyxl.load_workbook(filename = filename)        
    # try:
    #     for j in range(2):
    #         if j==0:
    #             worksheet = wb['Transactional_Data']
    #         else:
    #             worksheet = wb['Non_Transactional_Data']
    #         for col in worksheet.columns:
    #             max_length = 0
    #             column = col[0].column # Get the column name
    #             for cell in col:
    #                 try: # Necessary to avoid error on empty cells
    #                     if len(str(cell.value)) > max_length:
    #                         max_length = len(cell.value)
    #                 except:
    #                     pass
    #             adjusted_width = (max_length + 2) * 1.2
    #             worksheet.column_dimensions[column].width = adjusted_width
    # except:
    #     pass