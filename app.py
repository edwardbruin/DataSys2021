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

import mysqlapp
import paymentprocess
from datetime import datetime

tablename = 'items'

def checkstock(product_id, quantity=False):
    foo = ItemC(product_id).checkstock(quantity)
    return foo

class ItemC:
    def __init__(self, product_id, quantity=0):
        self.product_id = product_id
        self.quantity = quantity

    # 11 digit unique ID
    product_id = 00000000000
    # quantity in order and to be subtracted
    quantity = 0

    # sends a request to the database to subtract the corresponding stock value
    def checkstock(self, quantity=False):
        testvar = mysqlapp.main(f'SELECT Stock_Amt FROM {tablename} WHERE Prod_ID={self.product_id}')[0][0]
        # print('checking corresponding stock values')
        # print(testvar, self.quantity)
        if quantity != False:
            return testvar >= quantity
        else:
            return testvar

    # sends a request to the database to subtract the corresponding stock value

    def substock(self):
        if self.checkstock():
            testvar = mysqlapp.main(f'UPDATE {tablename} SET Stock_Amt = Stock_Amt - {self.quantity} WHERE Prod_ID={self.product_id}', True)
        print('subtracting corresponding stock values')
        print(self.product_id)
        print(self.quantity)
        print(testvar)

    # fetches the value of the item
    def getprice(self):
        testvar = mysqlapp.main(f'SELECT Prod_Price FROM {tablename} WHERE Prod_ID={self.product_id}')[0][0]
        # print(f'fetching price of item: {self.product_id}')
        return testvar

    def calcprice(self):
        return self.quantity * self.getprice()

    # fetches the name of the item
    def getname(self):
        testvar = mysqlapp.main(f'SELECT Prod_name FROM {tablename} WHERE Prod_ID={self.product_id}')[0][0]
        # print(f'fetching name of item: {self.product_id}')
        return testvar

    # fetches the image file of the item
    def getimg(self):
        print(f'fetching image file of item: {self.product_id}')

class OrderC:
    items = []

    def confirmorder(self):
        while True:
            self.displayorder()
            bar = input('Does this order match your request? type Y or N')
            if bar.upper() == 'Y':
                return True
            if bar.upper() == 'N':
                return False

    def processpayment(self):
        if self.confirmorder():
            if paymentprocess.main():
                self.logorder()
                print('substracting stock amounts!')
                # self.subtractstocks()
                # TO DO clear the order object so that it can no longer be used

    def logorder(self):
        foo = datetime.now()
        myfile = open(f'orderlog_{foo.day}_{foo.month}_{foo.year}.txt', 'a')
        myfile.write(str(foo.time()))
        myfile.write('\n')

        for x in self.items:
            myfile.write(str(x.product_id))
            myfile.write(', ')
        myfile.write('\n')

        for x in self.items:
            myfile.write(str(x.quantity))
            myfile.write(', ')
        myfile.write('\n')

        myfile.close()

        myfile = open(f'revenue_{foo.day}_{foo.month}_{foo.year}.txt', 'a')
        myfile.write(str(foo.time()))
        myfile.write('\n')
        myfile.write(str(self.calcprices()))
        myfile.write('\n')
        myfile.close()

    def additem(self, product_id, quantity=0):
        match = False
        for x in self.items:
            if x.product_id == product_id:
                match = True
                x.quantity = x.quantity + quantity
        if not match:
            self.items.append(ItemC(product_id, quantity))

    def clearitem(self, product_id):
        match = False
        print(product_id)
        for x in self.items:
            if x.product_id == product_id:
                match = True
                self.items.remove(x)
        if not match:
            print('no match found')

    def clearorder(self):
        self.items = []

    def calcprices(self):
        total = 0
        for x in self.items:
            total = total + x.calcprice()
        return total

    # returns 0 if all items are available
    def checkstocks(self):
        total = 0
        for x in self.items:
            total += not x.checkstock()
        return total

    def subtractstocks(self):
        for x in self.items:
            x.substock()

    def displayorder(self):
        for x in self.items:
            print(x.getname(), end=', ')
        print('')
        for x in self.items:
            print(x.product_id, end=', ')
        print('')
        for x in self.items:
            print(x.quantity, end=', ')
        print('')
        print(f'TOTAL: {self.calcprices()}')

    def serialise(self, mode=1):
        foo = []

        if mode == 1:
            for x in self.items:
                foo.append([x.product_id, x.getname(), x.checkstock(), x.quantity, x.checkstock(x.quantity), x.calcprice(), x.getprice()])
        if mode == 2:
            bar = []
            for x in self.items:
                bar.append(x.product_id)
            foo.append(bar)

            bar = []
            for x in self.items:
                bar.append(x.getname())
            foo.append(bar)

            bar = []
            for x in self.items:
                bar.append(x.checkstock())
            foo.append(bar)

            bar = []
            for x in self.items:
                bar.append(x.quantity)
            foo.append(bar)

            bar = []
            for x in self.items:
                bar.append(x.checkstock(x.quantity))
            foo.append(bar)

            bar = []
            for x in self.items:
                bar.append(x.calcprice())
            foo.append(bar)

            bar = []
            for x in self.items:
                bar.append(x.getprice())
            foo.append(bar)
        return foo

def getallitems():
    testvar = mysqlapp.main(f'SELECT Prod_Name, Prod_ID FROM {tablename} WHERE Stock_Amt>0')
    return testvar
