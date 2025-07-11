# oops.py

#############
# 1. Classes, objects, constructors (__init__)
#############

class BankAccount:
    """
    Represents a simple bank account with deposit, withdraw, and transaction tracking.

    Use case:
        - Track an individual's bank balance and transaction history.
        - Perform deposits and withdrawals.
        - Compare accounts and combine balances.

    Usage example:
        acc = BankAccount("Alice", 100)
        acc.deposit(50)
        acc.withdraw(30)
        print(acc)  # BankAccount(owner=Alice, balance=120)
    """
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        """
        Deposit a positive amount to the account.

        Usage example:
            acc.deposit(100)
        """
        if amount > 0:
            self.balance += amount
            self.transactions.append(('DEPOSIT', amount))
            return True
        return False

    def withdraw(self, amount):
        """
        Withdraw an amount if sufficient balance exists.

        Usage example:
            acc.withdraw(50)
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(('WITHDRAW', amount))
            return True
        return False

    def __str__(self):
        """
        String representation of the account.

        Usage example:
            print(acc)
        """
        return f"BankAccount(owner={self.owner}, balance={self.balance})"

    # Operator overloading: add two accounts' balances
    def __add__(self, other):
        """
        Add balances of two BankAccount objects.

        Usage example:
            total = acc1 + acc2
        """
        if isinstance(other, BankAccount):
            return self.balance + other.balance
        return NotImplemented

    # Dunder method for equality
    def __eq__(self, other):
        """
        Check if two accounts are equal by owner and balance.

        Usage example:
            acc1 == acc2
        """
        if isinstance(other, BankAccount):
            return self.owner == other.owner and self.balance == other.balance
        return False

#############
# 2. Inheritance, mixins, method overriding
#############

class InterestMixin:
    """
    Mixin to add interest calculation to an account.

    Use case:
        - Extend account classes to support interest accrual.

    Usage example:
        class MyAccount(BankAccount, InterestMixin): pass
        acc = MyAccount("Eve", 1000)
        acc.add_interest(0.05)
    """
    def add_interest(self, rate):
        interest = self.balance * rate
        self.deposit(interest)
        self.transactions.append(('INTEREST', interest))

class SavingsAccount(BankAccount, InterestMixin):
    """
    A bank account with interest and withdrawal limits.

    Use case:
        - Savings account with a withdrawal limit and interest accrual.

    Usage example:
        sav = SavingsAccount("Bob", 500)
        sav.deposit(200)
        sav.add_interest(0.1)
        sav.withdraw(100)
    """
    def __init__(self, owner, balance=0):
        self.owner = owner; 
        self.balance = balance
        # super().__init__(owner, balance)

    # Overriding withdraw to limit withdrawals
    def withdraw(self, amount):
        """
        Withdraw with a maximum limit of 1000 per transaction.

        Usage example:
            sav.withdraw(1200)  # Will print warning and return False
        """
        InterestMixin.add_interest(self, 0.05)  # Add interest before withdrawal
        # Check if withdrawal exceeds limit
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        elif self.balance < amount:
            print("Insufficient funds for withdrawal.")
        if amount > 1000:
            print("Withdrawal limit exceeded for SavingsAccount.")
            return False
        return super().withdraw(amount)

#############
# 3. Mini patterns for Django (factory, singleton)
#############

# Factory pattern
def account_factory(account_type, owner, balance=0):
    """
    Factory function to create different types of accounts.

    Use case:
        - Dynamically create account objects based on type.

    Usage example:
        acc = account_factory('savings', 'Dana', 400)
    """
    if account_type == 'savings':
        return SavingsAccount(owner, balance)
    elif account_type == 'basic':
        return BankAccount(owner, balance)
    else:
        raise ValueError("Unknown account type")

# Singleton pattern
class Bank:
    """
    Singleton class to manage all accounts in a bank.

    Use case:
        - Ensure only one instance of Bank exists.
        - Track all accounts and total funds.

    Usage example:
        bank = Bank()
        bank.add_account(acc)
        print(bank.total_funds())
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.accounts = []
        return cls._instance

    def add_account(self, account):
        """
        Add an account to the bank.

        Usage example:
            bank.add_account(acc)
        """
        self.accounts.append(account)

    def total_funds(self):
        """
        Calculate total funds in the bank.

        Usage example:
            total = bank.total_funds()
        """
        return sum(acc.balance for acc in self.accounts)

#############
# 4. Hands-on: Test cases
#############

def test_bank_account():
    """
    Test BankAccount functionality.

    Usage example:
        test_bank_account()
    """
    acc = BankAccount("Alice", 100)
    assert acc.deposit(50)
    assert acc.balance == 150
    assert acc.withdraw(70)
    assert acc.balance == 80
    assert not acc.withdraw(1000)
    print("BankAccount tests passed.")

def test_savings_account():
    """
    Test SavingsAccount functionality.

    Usage example:
        test_savings_account()
    """
    sav = SavingsAccount("Bob", 500)
    assert sav.deposit(200)
    assert sav.balance == 700
    sav.add_interest(0.1)
    assert sav.balance == 770
    assert not sav.withdraw(2000)
    print("SavingsAccount tests passed.")

def test_factory_and_singleton():
    """
    Test account_factory and Bank singleton.

    Usage example:
        test_factory_and_singleton()
    """
    bank = Bank()
    acc1 = account_factory('basic', 'Charlie', 300)
    acc2 = account_factory('savings', 'Dana', 400)
    bank.add_account(acc1)
    bank.add_account(acc2)
    assert bank.total_funds() == 700
    print("Factory and Singleton tests passed.")

if __name__ == "__main__":
    test_bank_account()
    test_savings_account()
    test_factory_and_singleton()