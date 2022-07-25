################################################################################
# Author:      Martin Scheffauer
# MatNr:       51917931
# File:        banking_system.py
# Description: implements classes for a complete banking system 
# Comments:    the banking system provides BankAccounts for user, where user can 
#              subtract money and add money to their account, delete it, create a 
#              new account and transfer money between accounts
#              ibans are created automatically
################################################################################
#%%
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True) 
class User:
    first_name: str
    last_name: str
    address: str
    phone_number: str
    
class BankAccount:
    def __init__(self,user : User,iban : str,bic : str) -> None:
        self._user = user
        self._iban = iban
        self._bic = bic
        self._balance = 0
    #properties
    @property
    def user(self) -> User:
        return self._user
        
    @property
    def bic(self) -> str:
        return self._bic

    @property
    def iban(self) -> str:
        return self._iban

    @property
    def balance(self) -> float:
        return self._balance

    #methods
    def add_money(self,amount : float) -> None:
        self._balance += amount;  
    def retrieve_money(self,amount : float) -> bool:
        if (self._balance >= amount):
            self._balance -= amount; 
            return True
        else:
            print(f"{self.user.first_name} {self.user.last_name} has insufficient balance. Current balance: "\
                  f"{self.balance:.2f}, {(amount - self.balance):.2f} needed")    
            return False   
    def __str__(self) -> str:
        return (f"First Name: {self.user.first_name}\n"
        f"Last Name: {self.user.last_name}\n"
        f"Address: {self.user.address}\n"  
        f"Phone Number: {self.user.phone_number}\n" 
        f"Balance: {self.balance:.2f}\n" 
        f"IBAN: {self.iban}\n"  
        f"BIC: {self.bic}")

class BankingSystem:
   
    def __init__(self, bic : str, country : str,bank_code: Union[int,str,float]) -> None:
        self._bank_code = str(bank_code)
        self._bic = bic
        self._country = country
        self._account_id = 0
        self._accounts = {}
            
    def _user_exist(self,user : User,toggle_suppress : bool) ->bool:
        #toggle with suppress whether error text should be shown.
        if user in self._accounts:
            if toggle_suppress:
                raise ValueError("An account with this user already exists")
            return True
        else:
            if not toggle_suppress:
                raise ValueError("This account does not exist")
            return False
    def _checksum(self,account_number : str) -> str:
        #evaluate the country code
        if len(self._country) > 0:
            _country_code = str(ord(self._country[0])-55)
        if len(self._country) > 1:
            _country_code += str(ord(self._country[1])-55)
        #generate the checknumber and return the checksum
        _checknumber = self._bank_code + account_number + _country_code.ljust(6,'0')
        return (f"{(98-(int(_checknumber)%97)):02}")
        
    def create_user_account(self,user : User) -> None:
        if not self._user_exist(user,True):
            #pad the account id and sum up everything to iban. then create bank account 
            #for new user and add to dict.
            self._account_id += 1
            _new_acc_num = f"{self._account_id:011}"
            _iban = self._country + self._checksum(_new_acc_num) + self._bank_code +_new_acc_num
            _new_bank_account = BankAccount(user,_iban,self._bic)
            self._accounts[user] = _new_bank_account
    def add_money(self,user : User, amount : float) -> None:
        if self._user_exist(user,False):
            self._accounts[user].add_money(amount)

    def retrieve_money(self,user : User,amount : float) -> None:
        if self._user_exist(user,False):
            self._accounts[user].retrieve_money(amount)
    def transfer_money(self,amount : float, retrieving_user : User, receiving_user : User) -> None:   
        if self._user_exist(retrieving_user,False) and self._user_exist(receiving_user,False):
            #only transfer if retrieving has enough money
            if self._accounts[retrieving_user].retrieve_money(amount):
                self._accounts[receiving_user].add_money(amount)
            
    def account_info(self,user : User) -> None: 
        if self._user_exist(user,False):
            print(self._accounts[user])
    def remove_account(self,user : User) -> None:
        if self._user_exist(user,False):
            del self._accounts[user]
    



# %%