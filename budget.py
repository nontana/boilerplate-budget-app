class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = []

  def __repr__(self):
    header = self.name.center(30, "*") + "\n"
    bill = ""
    total_cash = 0.0
    for cash in self.ledger:
      ## 23 and 24 are heuristic value
      bill += f"{cash['description'][:23]:24}" + f"{cash['amount']:.2f}" + "\n"
      total_cash += cash["amount"]
    out = header + bill + "Total: " + str(total_cash)
    return out

  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      ## Return the negative value
      self.ledger.append({"amount": -amount, "description": description})
      return True
    else:
      return False

  def get_balance(self):
    balance = 0.0
    for cash in self.ledger:
      balance += cash["amount"]
    return balance

  def transfer(self, amount, category):
    if self.check_funds(amount):
      self.withdraw(amount, "Transfer to " + category.name)
      category.deposit(amount, "Transfer from " + self.name)
      return True
    else:
      return False

  def check_funds(self, amount):
    if self.get_balance() >= amount:
      return True
    else:
      return False


def create_spend_chart(categories):
  ############### Total amount ###############
  cash = []
  for i in range(0, len(categories)):
    spent = 0.0
    size_cat = len(categories[i].ledger)
    for j in range(0, size_cat):
      if categories[i].ledger[j]["amount"] < 0:
        spent += abs(categories[i].ledger[j]["amount"])
    cash.append(spent)
  total_spent = sum(cash)
  ############### Percentage ###############
  percentage_spent = list(map(lambda x: int(x / total_spent * 10) * 10, cash))
  ############### Chart bar ###############
  head = "Percentage spent by category\n"
  chart = ""
  for i in range(100, -1, -10):
    ## Need to adjust the spacing [rjust(3)]
    chart += str(i).rjust(3) + "| "
    for j in percentage_spent:
      if j >= i:
        chart += "o  "
      else:
        chart += "   "
    chart += "\n"
  dash = "    " + "-" * 10 + "\n"
  category_name = list(map(lambda x: x.name, categories))
  max_category_name_length = max(map(lambda x: len(x), category_name))
  ## Adjust string
  new_category_name = list(
    map(lambda x: x.ljust(max_category_name_length), category_name))
  ## Arrange string in vertical form
  for i in zip(*new_category_name):
    dash += "    " + "".join(map(lambda x: x.center(3), i)) + " \n"
  output = head + chart + dash
  ## Delete the last \n
  output = output.rstrip("\n")
  return output
