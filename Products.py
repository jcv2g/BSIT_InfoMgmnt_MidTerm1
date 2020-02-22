from tkinter import *
import pyodbc


class Product:
    def __init__(self,name, price, description, quantity, idnum):
        self.__name = name
        self.__price = price
        self.__description = description
        self.__quantity = quantity
        self.__idnum = idnum
    def getName(self):
        return self.__name

    def getPrice(self):
        return self.__price

    def getDescription(self):
        return self.__description

    def getQuantity(self):
        return self.__quantity

    def getIdnumber(self):
        return self.__idnum

    def updateSelf(self, name, price,description, quantity,idnum):
        global products
        self.__name = name
        self.__price = price
        self.__description = description
        self.__quantity = quantity
        btn1['state'] = DISABLED
        btn2['state'] = NORMAL
        name = e1.get()
        price = e2.get()
        description = e3.get()
        size = e4.get()
        cursor.execute("UPDATE products SET name = ('"+name+"'), description = ('"+description+"')  ,size = ('"+size+"'), price = ('"+price+"') WHERE id = ('"+str(idnum)+"')")
        conn.commit()
        viewProducts()

def addProduct():
    global products
    name = e1.get()
    price = e2.get()
    description = e3.get()
    size = e4.get()
    idnum = 0
    cursor.execute("insert into products(name, description,size,price) values('"+name+"','"+description+"','"+size+"','"+price+"')")
    conn.commit()
    product = Product(e1.get(), e2.get(), e3.get(), e4.get(),idnum)
    products.append(product)
    viewProducts()

def deleteProduct(product):
    global products
    cursor.execute("DELETE FROM products WHERE id = ('"+str(product.getIdnumber())+"');")
    conn.commit()
    products.remove(product)
    viewProducts()


def updateProduct(product):
    e1.delete(0, 'end')
    e2.delete(0, 'end')
    e3.delete(0, 'end')
    e4.delete(0, 'end')
    e1.insert(0,product.getName())
    idnum = product.getIdnumber()
    e2.insert(0,product.getPrice())
    e3.insert(0,product.getDescription())
    e4.insert(0,product.getQuantity())
    btn1['state'] = NORMAL
    btn2['state'] = DISABLED
    btn1.configure(command=lambda: product.updateSelf(e1.get(), e2.get(), e3.get(),e4.get(),idnum))
    

def viewProducts():
    global products

    row = 1
    list = separator.grid_slaves()
    for l in list:
        l.destroy()
        
    addHeaders()
    for product in products:
        Label(separator, text=product.getName(), background=color, width=10).grid(row=row, column=0, sticky=W+E+N+S , padx=10, pady=5)
        Label(separator, text=product.getPrice(), background=color, width=10).grid(row=row, column=1, sticky=W+E+N+S , padx=10, pady=5)
        Label(separator, text=product.getQuantity(),background=color, width=10).grid(row=row, column=2, sticky=W+E+N+S , padx=10, pady=5)

        btn_a1 = Button(separator, text="Update", width=7, command=lambda prod=product: updateProduct(prod))
        btn_a2 = Button(separator, text="Delete", width=7, command=lambda prod=product: deleteProduct(prod))

        btn_a1.grid(row=row, column=3, sticky=W, padx=5, pady=5)
        btn_a2.grid(row=row, column=4, sticky=E, padx=5, pady=5)
        row += 1

    e1.delete(0, 'end')
    e2.delete(0, 'end')
    e3.delete(0, 'end')
    e4.delete(0, 'end')

def addHeaders():    
    separator.grid(row=6, column=0, columnspan=5, pady=5, sticky=W+E+N+S)
    Label(separator, text="Name", background=color, width=10).grid(row=0, column=0, sticky=W, padx=10, pady=5)
    Label(separator, text="Price", background=color, width=10).grid(row=0, column=1, sticky=W, padx=10, pady=5)
    Label(separator, text="Quantity",background=color, width=10).grid(row=0, column=2, sticky=W, padx=10, pady=5)
    Label(separator, text="Action", background=color, width=10).grid(row=0, column=3, sticky=W, padx=10, pady=5, columnspan=2)

products = []

conn = pyodbc.connect("Driver={SQL Server};"
                      "Server=DESKTOP-UJ42S5R\SQLSERVER;"
                      "Database=db_clothing_line;"
                      "Trusted_Connection=yes;")

cursor = conn.cursor()
cursor.execute('SELECT * FROM products')

def show():
    for row in cursor:
        products.append(Product(row[1],row[4],row[2],row[3],row[0]))
        viewProducts()

color = "#d9d7d7"

root = Tk()
root.title("Simple Inventory System")
root.geometry("435x400") 
root.resizable(0, 0) 

Label(root, text="Products Information").grid(row=0, column=0, sticky=W, padx=10, pady=5)
Label(root, text="Product Name: ").grid(row=1, column=0, sticky=W, padx=10, pady=5)                       
Label(root, text="Product Price: ").grid(row=2, column=0, sticky=W, padx=10, pady=5)    
Label(root, text="Product Description: ").grid(row=3, column=0, sticky=W, padx=10, pady=5)
Label(root, text="Product Quantity: ").grid(row=4, column=0, sticky=W, padx=10, pady=5)

e1 = Entry(root, width=45)
e2 = Entry(root, width=45)
e3 = Entry(root, width=45)
e4 = Entry(root, width=45)

e1.grid(row=1, column=1, sticky=W, padx=10, pady=5, columnspan=2)
e2.grid(row=2, column=1, sticky=W, padx=10, pady=5, columnspan=2)
e3.grid(row=3, column=1, sticky=W, padx=10, pady=5, columnspan=2)
e4.grid(row=4, column=1, sticky=W, padx=10, pady=5, columnspan=2)

btn1 = Button(root, text="Update Product", width=15, state=DISABLED) 
btn2 = Button(root, text="Add Product", width=15, state=NORMAL, command=addProduct)

btn1.grid(row=5, column=1, sticky=W, padx=10, pady=5)
btn2.grid(row=5, column=2, sticky=E, padx=10, pady=5)

separator = Canvas(root, height=100, width=420, background=color, relief=SUNKEN)
addHeaders()
show()
root.mainloop()