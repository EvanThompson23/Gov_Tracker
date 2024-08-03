class Trade:
    def __init__(self, person, purchase_date, filed_date, stock, action, amount):
        self._person = person
        self._purchase_date = purchase_date
        self._filed_date = filed_date
        self._stock = stock
        self._action = action
        self._amount = amount

    # Getter and Setter for person
    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, value):
        self._person = value

    # Getter and Setter for purchase_date
    @property
    def purchase_date(self):
        return self._purchase_date

    @purchase_date.setter
    def purchase_date(self, value):
        self._purchase_date = value

    # Getter and Setter for filed_date
    @property
    def filed_date(self):
        return self._filed_date

    @filed_date.setter
    def filed_date(self, value):
        self._filed_date = value

    # Getter and Setter for stock
    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value

    # Getter and Setter for action
    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    # Getter and Setter for range
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value
        
    def print_all(self):
        print([self._person, self._purchase_date, self._filed_date, self._stock, self._action, self._amount])
