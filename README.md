# Laptop Shop Management
This Python program allows you to manage the inventory of a laptop shop. You can view the available laptops, sell laptops to customers, purchase new laptops, and exit the program.
## Prerequisites
* Python 3.7 or higher
* tabulate module (install with `pip install tabulate`)
* reportlab module (install with `pip install reportlab`)
* PyPDF2 module (install with `pip install PyPDF2`)
## Getting Started
1. Clone or download the repository to your local machine.
2. Navigate to the directory where the program files are stored.
3. Run the following command to start the program:
```bash
python laptop_shop.py
```
4.You should see the main menu displayed in your terminal:
```bash
================ Laptop Shop Management ================
1. Display available laptops
2. Sell a laptop
3. Purchase a laptop
4. Exit
```
5. Follow the prompts to interact with the program.
## Usage
#### Display Available Laptops
To view the available laptops in the inventory, select option 1 from the main menu. The program will display a table of all the laptops, including the name, brand, price, quantity, processor, and graphics card.
### Sell a Laptop
To sell a laptop to a customer, select option 2 from the main menu. You will be prompted to enter the buyer's name, email address, the laptop's name, and the quantity to sell.

If the laptop is in stock and the quantity requested is available, the program will generate an invoice in PDF format and deduct the sold quantity from the inventory. Otherwise, an appropriate error message will be displayed.
### Purchase a Laptop
To purchase new laptops for the inventory, select option 3 from the main menu. You will be prompted to enter the laptop's name, brand, price, quantity, processor, and graphics card.

The program will add the new laptops to the inventory and display a message indicating the number of laptops added.
### Exit
To exit the program, select option 4 from the main menu. The program will save the updated inventory to the `inventory.pdf` file and exit.
## Notes
* You need to create empty `inventory.pdf` and `invoice_template.pdf` files in the same directory where you store this program.
## Author 
* Pushparaj Mehta
## Acknowledgmehts
This program was creades as a project for the Python programming course
## Copyright
© 2023 Pushparaj Mehta. All rights reserved.
