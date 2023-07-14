class Category:
  #initialize the object
  def __init__(self, name):
    self.name = name
    self.ledger = []

  # create a method for depositing money and what for (appending it to the ledger)
  def deposit(self, amount, description=""):
    self.ledger.append({"amount" : amount, "description": description})

  # create a method for withdrawing money. if there is money left, subtract it and show what for in the ledger
  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.ledger.append({"amount": -amount, "description": description})
      return True
    return False

  # get balance
  def get_balance(self):
    return sum(item["amount"] for item in self.ledger)

  # transfer money from self to category
  def transfer(self, amount, category):
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {category.name}")
      category.deposit(amount, f"Transfer from {self.name}")
      return True
    return False

  # check balance
  def check_funds(self, amount):
    return amount <= self.get_balance()

  # save outputs as a string
  def __str__(self):
    # create title centered in 30 spaces with * around it (* is filling character, ^ is to center it, 30 is length)
    title = f"{self.name:*^30}\n"
    items = ""
    total = 0
    for item in self.ledger:
        # each description for each item should be no longer than 23 characters, 7.2f means max character length of 7, up to 2 decimal places, float value
        items += f"{item['description'][:23]:23}" + f"{item['amount']:7.2f}\n"
        total += item["amount"]
    output = title + items + "Total: " + str(total)
    return output


# function to make spending chart
def create_spend_chart(categories):
    category_names = []
    spent_percentages = []

    # for each category, calculate the sum of all items
    for category in categories:
        total_withdrawals = sum(
            item["amount"]
            for item in category.ledger
            if item["amount"] < 0
        )

        # add the amount withdrawn over the total balance for that category to a spent percentages
        spent_percentages.append(total_withdrawals / sum(
            item["amount"]
            for category in categories
            for item in category.ledger
            if item["amount"] < 0
        ))
        category_names.append(category.name)

    # create the chart
    chart = "\nPercentage spent by category\n"
    # in increments of -10, starting from 100. 3d represents a width of 3, d = integer 
    for percentage in range(100, -10, -10):
        chart += f"{percentage:3d}| "
        for spent_percentage in spent_percentages:
            if spent_percentage * 100 >= percentage:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Find the longest category name
    max_name_length = max(len(name) for name in category_names)

    # Add category names vertically
    for i in range(max_name_length):
        chart += "    "
        for name in category_names:
            if i < len(name):
                chart += name[i] + "  "
            else:
                chart += "   "
        chart += "\n"

    return chart
