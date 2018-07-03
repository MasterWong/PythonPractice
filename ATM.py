class ATM:
    def __init__(self, owner, balance=0):

        self.owner = owner
        self.balance = balance

    def deposit(self, dep_amt):

        self.balance += dep_amt
        print("Added {} to the balance".format(dep_amt))
        print("Current balance is {}".format(self.balance))

    def withdraw(self, wd_amt):

        if self.balance >= wd_amt:
            self.balance -= wd_amt
            print("{} has been withdrew from balance".format(wd_amt))
        else:
            print("Not enough funds in current balance")

    def __str__(self):
        return "Owner is {}, \nBalance is {}.".format(self.owner, self.balance)

    def input_check(self, letter, df_letter):

        if letter not in df_letter:
            raise Exception("Wrong letter input!", letter)

user = input("Welcome to use ATM, Please enter User Name: ")
print("User is {}".format(user))

a = ATM(user)

while True:
    i = input("Quit system: Y/N ")
    try:
        a.input_check(i, ["Y", "y", "N", "n"])
        print(i)
        if i == ("Y" or "y"):
            print("Quiting system")
            break
    except:
        print("Wrong input, please try again!")
        continue
    else:
        while True:
            k = input("Enter 'W' for withdraw, 'D' for deposit: ")

            try:
                a.input_check(k, ["W", "w", "D", "d"])
            except:
                print("Wrong input, please try again!")
                continue
            else:
                break

        if k == "W" or k == "w":
            wd = int(input("Please enter withdraw amount: "))
            a.withdraw(wd)
        elif k == "D" or k == "d":
            de = int(input("Please enter deposit amount: "))
            a.deposit(de)
        else:
            print("Wrong word put!")

