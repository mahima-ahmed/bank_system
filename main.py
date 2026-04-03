import pandas as pd

class Bank:
    def __init__(self, account_holder, bank, balance, pin):
        self.account_holder = account_holder
        self._bank = bank
        self.__balance = balance
        self.__pin = pin

    def authenticate(self, name, bank, pin):
        return name == self.account_holder and bank == self._bank and pin == self.__pin

    def get_balance(self):
        print(f'Balance: {self.__balance}€')

    def deposit(self):
        amount = float(input('Enter amount to deposit: '))
        if amount > 0:
            self.__balance += amount
            print(f'{amount}€ deposited successfully.')
        else:
            print('Invalid amount. Try again.')

    def withdraw(self):
        pin = int(input('Enter PIN: '))
        if pin != self.__pin:
            print('The pin is incorrect. Try again')
            return
        amount = float(input('Enter amount to withdraw: '))
        if amount <= 0:
            print('The amount is not valid.')
        elif amount >= self.__balance:
            print(f'Insufficient amount. Available balance: {self.__balance}€')
        else:
            self.__balance -= amount
            print(f'{amount}€ withdrawn successfully. New balance: {self.__balance}€')

    def menu(self):
        while True:
            print('\n----MENU----')
            print('1. Balance')
            print('2. Deposit')
            print('3. Withdraw')
            print('4. Exit')

            choice = int(input('Choose an option: '))
            if choice == 1:
                self.get_balance()
            elif choice == 2:
                self.deposit()
            elif choice == 3:
                self.withdraw()
            elif choice == 4:
                print('Exiting...')
                break
            else:
                print('Invalid option')

accounts = []
while True:
    create = input('Do you want to create an account? (yes/no): ')
    if create.lower() == 'no':
        break
    name = input('Enter account holder name: ')
    bank = input('Enter bank name: ')
    balance = float(input('Enter balance: '))
    pin = int(input('Enter PIN: '))

    accounts.append({
        'Name': name,
        'Bank': bank,
        'Balance': balance,
        'PIN': pin
    })
df = pd.DataFrame(accounts)
df.to_csv('accounts.csv', index=False)
print('Account saved to CSV successfully.')

max_attempts = 3
attempts = 0

while attempts < max_attempts:
    print("\n--- LOGIN ---")
    name = input("Enter your name: ")
    bank = input("Enter your bank: ")
    pin = int(input("Enter your PIN: "))

    user = df[
        (df["Name"] == name) &
        (df["Bank"] == bank) &
        (df["PIN"] == pin)
    ]

    if not user.empty:
        print('ACCESS GRANTED.')

        row_data = user.iloc[0]
        account = Bank(row_data['Name'], row_data['Bank'], row_data['Balance'], row_data['PIN'])
        account.menu()
        index = user.index[0]
        df.loc[index, 'Balance'] = account._Bank__balance
        df.to_csv('accounts.csv', index=False)
        print('Data updated in CSV.')
        break
    else:
        attempts += 1
        print(f'ACCESS DENIED ({attempts}/{max_attempts}) attempts.')

if attempts == max_attempts:
    print('ACCOUNT BLOCKED. You reached the maximum attempts.')
