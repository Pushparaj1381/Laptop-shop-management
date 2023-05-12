# Author: Pushparaj Mehta
# Date created: 2023-05-12
import datetime
import os
from tabulate import tabulate
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
import PyPDF2
from PyPDF2 import PdfReader

def main():
    inventory_file = 'inventory.pdf'
    laptops = read_inventory_file(inventory_file)

    while True:
        print('================ Laptop Shop Management ================')
        print('1. Display available laptops')
        print('2. Sell a laptop')
        print('3. Purchase a laptop')
        print('4. Exit')

        choice = input('Enter your choice (1-4): ')
        if choice == '1':
            display_laptops(laptops)
        elif choice == '2':
            sell_laptop(laptops)
        elif choice == '3':
            purchase_laptop(laptops)
        elif choice == '4':
            write_inventory_file(inventory_file, laptops)
            laptops = read_inventory_file(inventory_file) # call read_inventory_file() to update laptops list
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Try again.')


def read_inventory_file(file_path):
    """
    Reads the inventory file and returns a list of dictionaries
    containing laptop information
    """
    laptops = []
    with open(file_path, 'rb') as file:
        try:
            pdf_reader = PyPDF2.PdfReader(file)
        except PyPDF2.errors.EmptyFileError:
            print('File is empty')
            return laptops
        for page in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page]
            content = page_obj.extract_text()
            if content:
                for line in content.strip().split('\n'):
                    laptop_data = line.strip().split(', ')
                    laptop = {
                        'name': laptop_data[0],
                        'brand': laptop_data[1],
                        'price': float(laptop_data[2].replace('$', '')),
                        'quantity': int(laptop_data[3]),
                        'processor': laptop_data[4],
                        'graphics_card': laptop_data[5]
                    }
                    laptops.append(laptop)
    return laptops

def write_inventory_file(file_path, laptops):
    """
    Writes the updated laptop information to the inventory file
    """
    with open(file_path, 'wb') as file:
        pdf_canvas = canvas.Canvas(file)
        y = 700
        for laptop in laptops:
            laptop_data = [
                laptop['name'], laptop['brand'],
                f"${laptop['price']}", str(laptop['quantity']),
                laptop['processor'], laptop['graphics_card'] if 'graphics_card' in laptop else ''
            ]
            line = ', '.join(laptop_data)
            pdf_canvas.drawString(100, y, line)
            y -= 20
        pdf_canvas.save()

def display_laptops(laptops):
    """
        Displays available laptops
    """
    if laptops:
        table_headers = ['Name', 'Brand', 'Price', 'Quantity', 'Processor', 'Graphics Card']
        table_data = [[
            laptop['name'], laptop['brand'],
            f"${laptop['price']}", f"{laptop['quantity']} ",
            laptop['processor'], laptop['graphics_card']
        ] for laptop in laptops]

        table = tabulate(table_data, headers=table_headers, tablefmt='grid')
        print(table)
    else:
        print('No laptops found in inventory!')


def sell_laptop(laptops):
    if not laptops:
        print("Sorry, there are no laptops available for sale.")
        return

    buyer_name = ""
    while not buyer_name:
        buyer_name = input("Enter buyer name: ")
    
    buyer_email = ""
    while not buyer_email:
        buyer_email = input("Enter buyer email: ")

    laptop_name = ""
    while not laptop_name:
        laptop_name = input("Enter laptop name: ")
    
    quantity = 0
    while quantity <= 0:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Invalid quantity. Quantity must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    
    # Check if the laptop is in stock
    laptop = next((laptop for laptop in laptops if laptop['name'] == laptop_name), None)
    if not laptop:
        print("Sorry, we don't have that laptop in stock.")
        return

    # Check if there are enough laptops in stock
    if quantity > laptop["quantity"]:
        print(f"Sorry, we only have {laptop['quantity']} {laptop['name']} laptop(s) in stock.")
        return

    # Calculate the total price
    total_price = laptop["price"] * quantity

    # Reduce the quantity of laptops in stock
    laptop["quantity"] -= quantity

    # Get the current date and time
    current_time = datetime.datetime.now()


    # Check if the quantity is zero, and remove the laptop from inventory
    if laptop["quantity"] == 0:
        laptops.remove(laptop)
        print(f"{laptop['name']} has been removed from inventory as it has 0 quantity.")

    # Create a new PDF file for the invoice
    file_name = f"{buyer_name}_{laptop_name}_{current_time.strftime('%Y%m%d%H%M%S')}.pdf"
    my_canvas = Canvas(file_name, pagesize=LETTER)

      # Generate the purchase invoice
    invoice = f"\n===================================================\nSALES INVOICE\n===================================================\nBuyer Name: {buyer_name}\nBuyer Email: {buyer_email}\nLaptop Name: {laptop_name}\nQuantity: {quantity}\nPrice: ${laptop['price']}\nTotal Price: ${total_price}\nDate: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\nFeatures:\n{'-'*62}\n"
    invoice += f"Processor: {laptop['processor']}\n"
    if laptop['graphics_card']:
        invoice += f"graphics_card: {laptop['graphics_card']}\n"
        invoice += "===================================================\n"
    print(invoice)
    # Set the font and font size for the invoice text
    font_name = 'Helvetica'
    font_size = 12

      # Add the sales invoice header to the PDF
    my_canvas.setFont(font_name, 24)
    my_canvas.drawString(250, 750, "Sales Invoice")
    my_canvas.line(50, 740, 550, 740)
    
    my_canvas.setFont(font_name, font_size)
    
    # Add the buyer name to the PDF
    my_canvas.drawString(50, 710, f"Buyer Name: {buyer_name}")

    # Add the buyer email to the PDF
    my_canvas.drawString(50, 690, f"Buyer Email: {buyer_email}")

    # Add the laptop name to the PDF
    my_canvas.drawString(50, 670, f"Laptop Name: {laptop_name}")

    # Add the quantity to the PDF
    my_canvas.drawString(50, 650, f"Quantity: {quantity}")

    # Add the price per piece to the PDF
    my_canvas.drawString(50, 630, f"Price per piece: ${laptop['price']}")

    # Add the total price to the PDF
    my_canvas.drawString(50, 610, f"Total Price: ${total_price}")

    # Add the date and time to the PDF
    my_canvas.drawString(50, 590, f"Date and Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add the features of the laptop to the PDF
    my_canvas.setFont(font_name, font_size+2)
    my_canvas.drawString(50,570 , "Features:")
    my_canvas.setFont(font_name, font_size)
    my_canvas.drawString(60, 550, f"Processor : {laptop['processor']}")
    my_canvas.drawString(60, 530, f"Graphics card {laptop['graphics_card']}")
    my_canvas.drawString(390, 510, f"Sell By:")
    my_canvas.drawString(370, 490, f"Pushparaj Mehta")
    my_canvas.setLineWidth(1) # Set the width of the line
    my_canvas.line(350, 480, 500, 480) # Draw the line

                         

    # Save the PDF file
    my_canvas.save()
    
    #Update the inventory file
    write_inventory_file('inventory.pdf', laptops)

    print(f"{quantity} {laptop_name} laptop(s) sold to {buyer_name} for a total price of ${total_price}. Invoice saved as {file_name}.")
    print('Inventory Updated')
    return laptops

def purchase_laptop(laptops):
    """
    Allows the user to purchase a laptop by adding it to the inventory
    """
    seller_name = ""
    while not seller_name:
        seller_name = input("Enter seller name: ")

    seller_email = ""
    while not seller_email:
        seller_email = input("Enter seller email: ")

    laptop_name = ""
    while not laptop_name:
        laptop_name = input("Enter laptop name: ")

    brand = ""
    while not brand:
        brand = input("Enter brand: ")

    price = 0
    while price <= 0:
        try:
            price = float(input("Enter price: "))
            if price <= 0:
                print("Invalid price. Price must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    quantity = 0
    while quantity <= 0:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Invalid quantity. Quantity must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    processor = ""
    while not processor:
        processor = input("Enter processor: ")

    graphics_card = input("Enter graphics card (optional): ")

    existing_laptop = next((laptop for laptop in laptops if laptop['name'] == laptop_name and laptop['brand'] == brand and laptop['price'] == price and laptop['processor'] == processor and laptop['graphics_card'] == graphics_card), None)

    if existing_laptop:
        existing_laptop['quantity'] += quantity
        print("Laptop quantity updated successfully!")
    else:
        laptop = {
            'name': laptop_name,
            'brand': brand,
            'price': price,
            'quantity': quantity,
            'processor': processor,
            'graphics_card': graphics_card if graphics_card else None
        }
        laptops.append(laptop)

        write_inventory_file('inventory.pdf', laptops)

    # Get the current date and time
    current_time = datetime.datetime.now()

    # Generate the purchase invoice
    invoice = f"\n===================================================\nPURCHASE INVOICE\n===================================================\nSeller Name: {seller_name}\nSeller Email: {seller_email}\nLaptop Name: {laptop_name}\nQuantity: {quantity}\nPrice per piece: ${price}\nTotal Price: ${price * quantity}\nDate: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\nFeatures:\n{'-'*60}\n"
    invoice += f"Processor: {processor}\nGraphics Card: {graphics_card}\n"
    invoice += "===================================================\n"
    print(invoice)

    #Create a New Pdf
    file_name = f"{seller_name}_{laptop_name}_{current_time.strftime('%Y%m%d%H%M%S')}.pdf"
    my_canvas = Canvas(file_name, pagesize=LETTER)
    
    # Set the font and font size for the invoice text
    font_name = 'Helvetica'
    font_size = 12

      # Add the sales invoice header to the PDF
    my_canvas.setFont(font_name, 24)
    my_canvas.drawString(235, 750, "Purchase Invoice")
    my_canvas.line(50, 740, 550, 740)
    
    my_canvas.setFont(font_name, font_size)
    
    # Add the buyer name to the PDF
    my_canvas.drawString(50, 710, f"Seller Name: {seller_name}")

    # Add the buyer email to the PDF
    my_canvas.drawString(50, 690, f"Seller Email: {seller_email}")

    # Add the laptop name to the PDF
    my_canvas.drawString(50, 670, f"Laptop Name: {laptop_name}")

    # Add the quantity to the PDF
    my_canvas.drawString(50, 650, f"Quantity: {quantity}")

    # Add the price per piece to the PDF
    my_canvas.drawString(50, 630, f"Price per piece: ${price}")

    # Add the total price to the PDF
    my_canvas.drawString(50, 610, f"Total Price: ${price}*{quantity}")

    # Add the date and time to the PDF
    my_canvas.drawString(50, 590, f"Date and Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add the features of the laptop to the PDF
    my_canvas.setFont(font_name, font_size+2)
    my_canvas.drawString(50,570 , "Features:")
    my_canvas.setFont(font_name, font_size)
    my_canvas.drawString(60, 550, f"Processor : {processor}")
    my_canvas.drawString(60, 530, f"Graphics card {graphics_card}")
    my_canvas.drawString(390, 510, f"Purchased By:")
    my_canvas.drawString(370, 490, f"Pushparaj Mehta")
    my_canvas.setLineWidth(1) # Set the width of the line
    my_canvas.line(350, 480, 500, 480) # Draw the line

                         

    # Save the PDF file
    my_canvas.save()

    #Update the inventory file
    write_inventory_file('inventory.pdf', laptops)

    print(f"{quantity} {laptop_name} laptop(s) purchase from {seller_name} for a total price of ${price*quantity}. Invoice saved as {file_name}.")

    return laptops



if __name__ == '__main__':
    main()
