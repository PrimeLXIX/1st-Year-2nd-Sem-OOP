class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name

    @property
    def citizen_id(self):
        return self.__citizen_id

    @property
    def full_name(self):
        return self.__name

class Account:
    def __init__(self, account_number: str, owner: User, initial_balance: float = 0.0):
        self.__account_number = account_number
        self.__owner = owner
        self.__balance = initial_balance
        self.__transactions = []

    @property
    def account_number(self):
        return self.__account_number

    @property
    def owner(self):
        return self.__owner

    @property
    def balance(self):
        return self.__balance

    @property
    def transactions(self):
        return self.__transactions

    @balance.setter
    def balance(self, balance: float):
        self.__balance = balance

    def add_transaction(self, transaction):
        self.__transactions.append(transaction)

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount
        else:
            return "Invalid Amount"

    def withdraw(self, amount: float):
        if amount > 0 and self.__balance > 0:
            self.balance -= amount
        return "Invalid Amount"

class ATMCard:
    def __init__(self, card_number: str, account: Account, pin: str = "0000"):
        self.__card_number = card_number
        self.__account = account
        self.__pin = pin

    @property
    def card_number(self):
        return self.__card_number

    @property
    def account(self):
        return self.__account

    @property
    def pin(self):
        return self.__pin

    @property
    def balance(self):
        return self.__account.balance

    @property
    def account_number(self):
        return self.__account.account_number

    @property
    def owner(self):
        return self.__account.owner

    def add_transaction(self, transaction):
        self.__account.add_transaction(transaction)

class ATMMachine:
    ANNUAL_FEE: int = 150
    MAXIMUM_WITHDRAWAL: int = 40000

    def __init__(self, machine_id: str, initial_amount: float = 1000000):
        self.__machine_id = machine_id
        self.__atm_balance = initial_amount# Class Code

    @property
    def machine_id(self):
        return self.__machine_id

    @property
    def atm_balance(self):
        return self.__atm_balance

## TODO 2: Write a method to insert an ATM card into the machine. It should accept two parameters:
## TODO: 1) Bank instance 2) ATM card number.
## TODO: If the card is valid, return the account instance; if not, return None.
## TODO: This should be a method of the ATM machine.

    def insert_card(self, card_number: str, pin: str):
        card = bank.find_card(card_number)
        if card and card.pin == pin:
            return card
        return "Invalid PIN."

## TODO 3: Write a method to deposit money. It should accept three parameters:
## TODO: 1) ATM machine instance, 2) Account instance, 3) Deposit amount.
## TODO: The method should increase the account balance and log the transaction in the account.
## TODO: Return "success" if the transaction is successful, otherwise return "error."
## TODO: Validate the input, e.g., the amount must be greater than 0.

    def deposit(self, account: Account, amount: float):
        if amount <= 0:
            return "Error"
        account.deposit(amount)
        self.__atm_balance += amount
        account.add_transaction(Transaction("D", amount, account.balance, self.__machine_id))

## TODO 4: Write a method to withdraw money. It should accept three parameters:
## TODO: 1) ATM machine instance, 2) Account instance, 3) Withdrawal amount.
## TODO: The method should decrease the account balance and log the transaction in the account.
## TODO: Return "success" if the transaction is successful, otherwise return "error."
## TODO: Validate the input, e.g., the amount must be greater than 0 and not exceed the account balance.

    def withdraw(self, account: Account, amount: float):
        if amount > self.__atm_balance:
            return "ATM has insufficient funds"

        if amount > self.MAXIMUM_WITHDRAWAL:
            return f"Exceeds daily maximum withdrawal limit of {self.MAXIMUM_WITHDRAWAL:,} baht"

        if amount > account.balance:
            return "Error."

        if amount <= 0:
            return "Withdrawal amount must be positive"

        account.balance -= amount
        self.__atm_balance -= amount
        account.add_transaction(Transaction("W", amount, account.balance, self.__machine_id))

## TODO 5: Write a method to transfer money. It should accept four parameters:
## TODO: 1) ATM machine instance, 2) Sender account instance, 3) Recipient account instance, 4) Transfer amount.
## TODO: The method should decrease the sender's balance, increase the recipient's balance, and log the transaction.
## TODO: Return "success" if the transaction is successful, otherwise return "error."
## TODO: Validate the input, e.g., the amount must be greater than 0 and not exceed the sender's balance.
    
    def transfer(self, sender: Account, receiver: Account, amount: float):
        if amount > sender.balance:
            return "Insufficient sender account balance."

        if amount <= 0:
            return "Amount must be positive."

        sender.balance -= amount
        receiver.balance += amount
        sender.add_transaction(Transaction("TW", amount, sender.balance, self.__machine_id, receiver.account_number))
        receiver.add_transaction(Transaction("TD", amount, receiver.balance, self.__machine_id, sender.account_number))

class Transaction:
    def __init__(self, transaction_type: str, amount: float, balance: float, atim_id: str, account_number: str = None):
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__balance = balance
        self.__atm_id = atim_id
        self.__account_number = account_number

    def __str__(self):
        if self.__transaction_type in ("TW", "TD"):
            return f"{self.__transaction_type}-ATM : {self.__atm_id}-{self.__amount}-{self.__balance}"
        return f"{self.__transaction_type}-ATM : {self.__atm_id}-{self.__amount}-{self.__balance}"

class Bank:
    def __init__(self):
        self.__users = []
        self.__accounts = []
        self.__cards = []
        self.__atms = []

    def add_user(self, user: User):
        self.__users.append(user)

    def add_account(self, account: Account):
        self.__accounts.append(account)

    def add_card(self, card: ATMCard):
        self.__cards.append(card)

    def add_atm(self, atm: ATMMachine):
        self.__atms.append(atm)

    def get_atm(self, machine_id: str):
        for atm in self.__atms:
            if atm.machine_id == machine_id:
                return atm

    def find_card(self, card_number: str):
        for card in self.__cards:
            if card.card_number == card_number:
                return card

    def find_account(self, account_number: str):
        for account in self.__accounts:
            if account.account_number == account_number:
                return account

##################################################################################


## Define the format of the user as follows:
## {Citizen ID: [Name, Account Number, ATM Card Number, Account Balance]}

user_data ={'1-1101-12345-12-0':['Harry Potter','1234567890','12345',20000],
       '1-1101-12345-13-0':['Hermione Jean Granger','0987654321','12346',1000]}

atm_data ={'1001':1000000,'1002':200000}

bank = Bank()

for citizen_id, data in user_data.items():
    user = User(citizen_id, data[0])
    account = Account(data[1], user, data[3])
    card = ATMCard(data[2], account, "1234")

    bank.add_user(user)
    bank.add_account(account)
    bank.add_card(card)


for machine_id, balance in atm_data.items():
    atm = ATMMachine(machine_id, balance)
    bank.add_atm(atm)
    
## TODO 1: From the user data, create instances with the following details:
## TODO: key:value, where the key is the Citizen ID, and the value contains
## TODO: [Name, Account Number, ATM Card Number, Account Balance].
## TODO: Return the instance of the bank and create two ATM instances.


print("--------------------------")
print("     Start Test Cases     ")
print("--------------------------")


## Test case #1: Test inserting Harry's ATM card into ATM machine #1
## and call the corresponding method.
## Expected result: Print Harry's account number and ATM card number correctly.
## Ans: 12345, 1234567890, Success
# print("-------------------------")

print()
print("------ Test Case 1 ------")
print("Expected Output: 12345, 1234567890, Success")
atm = bank.get_atm('1001')
card = atm.insert_card('12345', '1234')
print()
print(f"{card.card_number}, {card.account.account_number}, Success")
print("-------------------------")

## Test case #2: Test depositing 1000 Baht into Hermione's account using ATM machine #2.
## Call the deposit method.
## Expected result: Display Hermione's balance before and after the deposit, along with the transaction.
## Hermione's account before test: 1000
## Hermione's account after test: 2000
# print("-------------------------")

print()
print("------ Test Case 2 ------")
print("Expected Output: Hermione's account before test: 1000")
print("Expected Output: Hermione's account after test: 2000")
print()
atm = bank.get_atm('1002')
card = atm.insert_card('12346', '1234')
print(f'Hermione account balance before: {card.account.balance}')
atm.deposit(card.account, 1000)
print(f'Hermione account balance after: {card.account.balance}')
print("-------------------------")

## Test case #3: Test depositing -1 Baht into Hermione's account using ATM machine #2.
## Expected result: Display "Error."
# print("-------------------------")

print()
print("------ Test Case 3 ------")
print("Expected Output: Error")
atm = bank.get_atm('1002')
account = atm.insert_card('12346', '1234')
print()
print(atm.deposit(account, -1))
print("-------------------------")

## Test case #4: Test withdrawing 500 Baht from Hermione's account using ATM machine #2.
## Call the withdrawal method.
## Expected result: Display Hermione's balance before and after the withdrawal, along with the transaction.
## Hermione's account before test: 2000
## Hermione's account after test: 1500
# print("-------------------------")

print()
print("------ Test Case 4 ------")
print("Expected Output: Hermione's account before test: 2000")
print("Expected Output: Hermione's account after test: 1500")
atm = bank.get_atm('1002')
card = atm.insert_card('12346', '1234')
print()
print(f'Hermione account balance before: {card.account.balance}')
atm.withdraw(card.account, 500)
print(f'Hermione account balance after: {card.account.balance}')
print("-------------------------")

## Test case #5: Test withdrawing 2000 Baht from Hermione's account using ATM machine #2.
## Expected result: Display "Error."
# print("-------------------------")

print()
print("------ Test Case 5 ------")
print("Expected Output: Error.")
atm = bank.get_atm('1002')
card = atm.insert_card('12346', '1234')
print()
print(atm.withdraw(card.account, 2000))
print("-------------------------")

## Test case #6: Test transferring 10,000 Baht from Harry's account to Hermione's account using ATM machine #2.
## Call the transfer method.
## Expected result: Display Harry's balance before and after the transfer, Hermione's balance before and after the transfer, and the transaction log.
## Harry's account before test: 20000
## Harry's account after test: 10000
## Hermione's account before test: 1500
## Hermione's account after test: 11500
# print("-------------------------")

print()
print("------ Test Case 6 ------")
print("Expected Output: Harry's account before test: 20000")
print("Expected Output: Harry's account after test: 10000")
print("Expected Output: Hermione's account before test: 1500")
print("Expected Output: Hermione's account after test: 11500")
atm = bank.get_atm('1002')
sender_card = atm.insert_card('12345', '1234')
receiver_card = atm.insert_card('12346', '1234')
a = sender_card.account.balance
b = receiver_card.account.balance
atm.transfer(sender_card.account, receiver_card.account, 10000)
c = sender_card.account.balance
d = receiver_card.account.balance
print()
print(f'Harry\'s account before test: {a}')
print(f'Harry\'s account after test: {c}')
print(f'Hermione\'s account before test: {b}')
print(f'Hermione\'s account after test: {d}')
print("-------------------------")

## Test case #7: Display all of Hermione's transactions.
## Expected result:
## Hermione's transaction log:
## D-ATM:1002-1000-2000
## W-ATM:1002-500-1500
## TD-ATM:1002-10000-11500
# print("-------------------------")

print()
print("------ Test Case 7 ------")
print("Expected Output: D-ATM:1002-1000-2000")
print("Expected Output: W-ATM:1002-500-1500")
print("Expected Output: TD-ATM:1002-10000-11500")
atm = bank.get_atm('1001')
card = atm.insert_card('12346', '1234')
print()
for transaction in card.account.transactions:
    print(transaction)
print("-------------------------")

## Test case #8: Test inserting an incorrect PIN.
## Call the method to insert the card and check the PIN.
## atm_machine = bank.get_atm('1001')
## test_result = atm_machine.insert_card('12345', '9999')  # Incorrect PIN
## Expected result: Invalid PIN
# print("-------------------------")

print()
print("------ Test Case 8 ------")
print("Expected Output: Invalid PIN.")
atm = bank.get_atm('1001')
test_result = atm.insert_card('12345', '9999')
print()
print(test_result)
print("-------------------------")

## Test case #9: Test withdrawing more than the daily limit (40,000 Baht).
## atm_machine = bank.get_atm('1001')
## account = atm_machine.insert_card('12345', '1234')  # Correct PIN
## harry_balance_before = account.get_balance()
## print(f"Harry's account before test: {harry_balance_before}")
## print("Attempting to withdraw 45,000 Baht...")
## result = atm_machine.withdraw(account, 45000)
## print(f"Expected result: Exceeds daily withdrawal limit of 40,000 Baht")
## print(f"Actual result: {result}")
## print(f"Harry's account after test: {account.get_balance()}")
# print("-------------------------")

print()
print("------ Test Case 9 ------")
atm_machine = bank.get_atm('1001') 
account = atm_machine.insert_card('12345', '1234') 

harry_balance_before = sender_card.account.balance
print(f"Harry's account before test: {harry_balance_before:,}")

print("Attempting to withdraw 45,000 Baht...")
result = atm_machine.withdraw(account, 45000)
print(f"Expected result: Exceeds daily maximum withdrawal limit of 40,000 Baht")
print(f"Actual result: {result}")

harry_balance_after = sender_card.account.balance
print(f"Harry's account after test: {harry_balance_after:,}")
print("-------------------------")

## Test case #10: Test withdrawing money when the ATM has insufficient funds.
## atm_machine = bank.get_atm('1002')  # Assume machine #2 has 200,000 Baht left
## account = atm_machine.insert_card('12345', '1234')
## print("Test case #10: Test withdrawal when ATM has insufficient funds.")
## print(f"ATM machine balance before: {atm_machine.get_balance()}")
## print("Attempting to withdraw 250,000 Baht...")
## result = atm_machine.withdraw(account, 250000)
## print(f"Expected result: ATM has insufficient funds.")
## print(f"Actual result: {result}")
## print(f"ATM machine balance after: {atm_machine.get_balance()}")
# print("-------------------------")

print()
print("------ Test Case 10 ------")

atm_machine = bank.get_atm('1002')
account = atm_machine.insert_card('12345', '1234')

print(f"ATM machine balance before: {atm_machine.atm_balance:,}")
print("Attempting to withdraw 250,000 baht...")

result = atm_machine.withdraw(account, 250000)

print(f"Actual result: {result}")
print(f"ATM machine balance after: {atm_machine.atm_balance:,}")
print("-------------------------")