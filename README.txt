to use the ordering system, import the app.py module into your application
the below functions are recommended for quick use

app.getallitems()
function used to retrieve items list
takes no arguments

app.orderC()
class object must be initialised to use ordering system
takes no arguments

app.orderC.additem()
this method populates the order with items
takes PRODUCT ID as required argument, QUANTITY as optional argument

app.orderC.clearitem()
this method removes an item from the order
takes PRODUCT ID as required argument

app.orderC.clearorder()
wipes the order of all items
takes no arguments

app.orderC.processpayment()
calculates totals, confirms order, processes payment, logs order
takes no arguments