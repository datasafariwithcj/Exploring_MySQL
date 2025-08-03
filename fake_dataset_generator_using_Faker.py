from faker import Faker
import random
import mysql.connector
from datetime import datetime, timedelta

#initialize faker
fake = Faker()

#connect to MySQL finsigle database
conn = mysql.connector.connect(host = 'localhost', user= 'root', password= 'yourpassword', database= 'finsight')
cursor= conn.cursor()

#Predefined currencies for reference
currency_codes = ['USD', 'EUR', 'GBP', 'INR']

def create_customers(num_customers = 1000):
    customers = []
    for _ in range(num_customers):
        customer_type = random.choice(['individual', 'business'])
        if customer_type == 'individual':
            first_name = fake.first_name()
            last_name = fake.last_name()
            business_name = None
            dob = fake.date_of_birth(minimum_age=18, maximum_age= 80).strftime('%Y-%m-%d')
        else:
            first_name = None
            last_name = None
            business_name = fake.company()
            dob = None
        email = fake.unique.email()
        phone = fake.phone_number()
        country = fake.country()
        status = 'active'

        #insert the customers' fake data into database

        insert_customer = '''
        INSERT INTO customers (customer_type, first_name, last_name, business_name, email, phone, date_of_birth, country, status) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_customer,(customer_type, first_name, last_name, business_name, email, phone, dob, country, status))
        customers.append(cursor.lastrowid)
    conn.commit()
    return customers

def create_accounts(customers, max_accounts_per_customer = 3):
    accounts = []
    account_types = ['checking', 'savings', 'investment', 'loan']
    for cust_id in customers:
        num_accounts = random.randint(1, max_accounts_per_customer)
        for _ in range(num_accounts):
            account_type = random.choice(account_types)
            currency_code = random.choice(currency_codes)
            balance = 0.00 #Opening balance set to zero
            status = 'active'
            opened_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d %H:%M:%S')

            insert_account = '''INSERT INTO accounts(customer_id, account_type, currency_code, balance, opened_date, status) VALUES
            (%s, %s, %s, %s, %s, %s)'''
            cursor.execute(insert_account, (cust_id, account_type, currency_code, balance, opened_date, status))
            account_id = cursor.lastrowid

            accounts.append({'account_id': account_id, 'currency_code': currency_code})
    conn.commit()
    return accounts

def insert_transaction(account_id, t_type, amount, currency_code, related_account_id, timestamp, description = None):
    if description is None:
        description = f"Auto-generated {t_type}"
    insert_trx = '''
    INSERT INTO transactions (account_id, type, amount, currency_code, related_account_id, timestamp, description) VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_trx,(account_id, t_type, amount, currency_code, related_account_id, timestamp.strftime('%Y-%m-%d %H:%M:%S'), description))

def create_transactions(accounts, max_transactions_per_account = 20):
    transaction_types = ['deposit', 'withdrawal', 'payment', 'transfer', 'exchange']
    account_balances = {acc['account_id']: 0.0 for acc in accounts} #Running balance per account
    for acc in accounts:
        acc_id = acc['account_id']
        curr_code = acc['currency_code']

        #Initial Deposit
        opening_deposit = round(random.uniform(1000,5000),2)
        insert_transaction(acc_id, 'deposit', opening_deposit, curr_code, None, fake.date_time_between(start_date='-5y', end_date='-4y'))
        account_balances[acc_id] += opening_deposit

        num_transactions = random.randint(10, max_transactions_per_account)

        for _ in range(num_transactions):
            timestamp = fake.date_time_between(start_date='-4y', end_date='now') # Random date spread over last 4 years after opening deposit
            t_type = random.choices(transaction_types, weights=[0.2, 0.3, 0.3, 0.1, 0.1], k=1)[0] #Gets string value from the single value list output of choices.
            if t_type == 'deposit':
                amount = round(random.uniform(500, 3000),2)
                related_account_id = None
                account_balances[acc_id] += amount
            elif t_type == 'withdrawal' or t_type == 'payment':
                max_withdrawable = account_balances[acc_id]
                if max_withdrawable<10:
                    continue
                amount = -round(random.uniform(10, min(max_withdrawable,1000)),2)
                related_account_id = None
                account_balances[acc_id] += amount
            elif t_type == 'transfer':
                max_withdrawable = account_balances[acc_id]
                if max_withdrawable<10 or len(accounts) < 2:
                    continue
                amount = -round(random.uniform(10,min(2000,max_withdrawable)),2)
                related_acc = None
                potential_accounts = [a for a in accounts if a['account_id'] != acc_id and a['currency_code'] == curr_code]
                if not potential_accounts:
                    potential_accounts = [a for a in accounts if a['account_id'] != acc_id]
                if potential_accounts:
                    related_acc = random.choice(potential_accounts)
                else:
                    continue
                related_account_id = related_acc['account_id']
                account_balances[acc_id] += amount
                account_balances[related_account_id] += abs(amount)
            elif t_type == 'exchange':
                amount = round(random.uniform(-1000,1000),2)
                related_account_id = None
                account_balances[acc_id] += amount
            else:
                continue

            #Insert main transaction
            insert_transaction(acc_id, t_type, amount, curr_code, related_account_id, timestamp)

            #Insert reciprocal transaction in related account, for transfer
            if t_type == 'transfer' and related_account_id is not None:
                related_amount = abs(amount)
                related_timestamp = timestamp + timedelta (seconds= 5)
                insert_transaction(related_account_id, t_type,related_amount, curr_code, acc_id, related_timestamp)
    conn.commit()

#Run the steps
print("Generating customers...")
customer_ids = create_customers(num_customers=1000)

print("Generating accounts...")
account_records = create_accounts(customer_ids, max_accounts_per_customer=3)

print("Generating transactions...")
create_transactions(account_records, max_transactions_per_account=20)

print("Operation completed!")

cursor.close()
conn.close()