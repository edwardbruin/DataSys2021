import mysqlapp


def main():
    # get list of items (without levels) DONE
    # present list to user DONE
    # select products from list DONE
    # check if requested levels are present DONE
    #   if unavailable, cancel order
    # calculate price total
    # hold order until user verifies correct
    #   if user doesn't verify, cancel order
    # pass price value to tendering function
    # wait for completed payment
    #   if payment fails, cancel order
    # record the sale
    # send corresponding stock amounts to be subtracted from database
    foo = 'hello'
    return foo


class ItemC:
    def __init__(self, product_id, quantity):
        self.product_ID = product_id
        self.quantity = quantity

    # 11 digit unique ID
    product_ID = 00000000000
    # quantity in order and to be subtracted
    quantity = 0

    # sends a request to the database to subtract the corresponding stock value
    def checkstock(self):
        testvar = mysqlapp.main(f'SELECT Stock_Amt FROM parramatta WHERE Prod_ID={self.product_ID}')[0][0]
        print('checking corresponding stock values')
        print(testvar, self.quantity)
        return testvar >= self.quantity

    # sends a request to the database to subtract the corresponding stock value

    def substock(self):
        if self.checkstock():
            testvar = mysqlapp.main(f'UPDATE parramatta SET Stock_Amt = Stock_Amt - {self.quantity} WHERE Prod_ID={self.product_ID}', True)
        print('subtracting corresponding stock values')
        print(self.product_ID)
        print(self.quantity)
        print(testvar)

    # fetches the value of the item
    def getprice(self):
        testvar = mysqlapp.main(f'SELECT Prod_Price FROM parramatta WHERE Prod_ID={self.product_ID}')[0][0]
        print(f'fetching price of item: {self.product_ID}')
        return testvar

    # fetches the name of the item
    def getname(self):
        print(f'fetching name of item: {self.product_ID}')

    # fetches the image file of the item
    def getimg(self):
        print(f'fetching image file of item: {self.product_ID}')


class OrderC:
    items = []

    def additem(self, product_id, quantity):
        match = False
        for x in self.items:
            if x.product_ID == product_id:
                match = True
                x.quantity = x.quantity + quantity
        if not match:
            self.items.append(ItemC(product_id, quantity))

    def clearitem(self, product_id):
        match = False
        print(product_id)
        for x in self.items:
            if x.product_ID == product_id:
                match = True
                self.items.remove(x)
        if not match:
            print('no match found')

    def clearorder(self):
        self.items = []

    def calcprices(self):
        total = 0
        for x in self.items:
            itemprice = x.getprice()
            total = total + itemprice * x.quantity
        return total

    def checkstocks(self):
        total = 0
        for x in self.items:
            total += not x.checkstock()
        return total

    def subtractstocks(self):
        for x in self.items:
            x.substock()


def displayorder():
    print('hello')


def getallitems():
    testvar = mysqlapp.main('SELECT Prod_Name, Prod_ID FROM parramatta WHERE Stock_Amt>0')
    return testvar
