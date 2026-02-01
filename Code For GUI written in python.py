"""
Starter template for programming coursework.

You must build your app by writing code for the functions listed below.

The whole app is a composition of functions.
No GLOBAL variables and button functionality managed by use of lambda functions.

Student Name: [Kosish Adhikari]
Student ID: [w2121985]
"""
import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from functools import partial  # Importing partial to pre-fill function arguments


def load_pizza_prices(csv_file):
    pizza_prices = {}
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                name, price = row
                pizza_prices[name] = float(price)
    except Exception as e:
        print(f"Error reading pizza prices CSV: {e}")
    return pizza_prices 

def save_images(path, image_dict):
    VALID_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    
    if not os.path.exists(path): # Checks if image directory exists
        messagebox.showerror("Error", f"Image directory not found: {path}")
        return
    
    for filename in os.listdir(path): #loops through all files in the directory

        if filename.lower().endswith(VALID_IMAGE_EXTENSIONS): #ensures only valid image files are processed
          
            try:
               
                img_path = os.path.join(path, filename) 
                img = Image.open(img_path) #opens the image
                img = img.resize((75, 75), Image.Resampling.LANCZOS) # resizes the image 
                photo = ImageTk.PhotoImage(img) #converts the image to PhotoImage so it can be used in tkinter

                name = os.path.splitext(filename)[0] #extracts the name of the image without the extension 
                image_dict[name] = photo #stores the image in dictionary with the name as the key

            except Exception as e: #if an  occurs, it prints the error message 
                print(f"Error loading image {filename}: {e}")

    if not image_dict:#if no images are found, it warns the user as the dictornary is empty
        messagebox.showwarning("Error", "No valid images found in the directory.")

def make_pizza_command(name, image, details_frame, order_frame, cart, prices, total_price_label): #defines the command for the button

    def command(): #defines the command function 
        load_image_in_frame(name, image, details_frame, order_frame, cart, prices, total_price_label) #calls the function to load the image in the frame 
    return command #returns the command function so it can be used in the button 

def pizza_images_as_buttons(images, pizza_frame, details_frame, order_frame, cart, prices, total_price_label): # recieves the datato create image based pizza
  
    for widget in pizza_frame.winfo_children(): #clears any previous widgets in the frame
        widget.destroy()

    row, col = 0, 0 #initializes the layout, 4 buttons in a row 

    for name, img in images.items():

        btn = tk.Button( #create a button with image
            pizza_frame,
            image=img,

            command=make_pizza_command( # calls the function to create the command for the button
                name, img, details_frame, order_frame, cart, prices,
                total_price_label
            )
        )

        btn.image = img # refereneces the image so that garbage is not collected
        btn.grid(row=row, column=col, padx=5, pady=5)

        tk.Label(pizza_frame, text=name).grid(row=row+1, column=col) # adds a label with pizza name under image

        col += 1 # moves to next column, wraps to new row after 4 columns
        if col >= 4:
            col = 0
            row += 2

def load_image_in_frame(name, image, details_frame, order_frame, cart, prices, total_price_label): 
    
    for widget in details_frame.winfo_children(): 
        widget.destroy()

    details_frame.grid_rowconfigure(0, weight=1) # comfigures the grid so content can be cantered for user convenience
    details_frame.grid_columnconfigure(0, weight=1)

    inner_frame = tk.Frame(details_frame, bg="black") # creates a frame to center the content and applies a black background  
    inner_frame.grid(row=0, column=0)

    img_label = tk.Label(inner_frame, image=image, bg="black") # displays the image in frame selcted by the user
    img_label.image = image # keeps a referencce so that garbage collection does not occur
    img_label.grid(row=0, column=0, columnspan=2, pady=(0, 10)) # spans across 2 columns

    tk.Label(inner_frame, text=name, font=("Arial", 14, "bold"), fg="white", bg="black").grid(row=1, column=0, columnspan=2, pady=5) # shows pizza name in bold white text

    price = prices.get(name, 0.0) # gets the price from the dictionary
    tk.Label(inner_frame, text=f"Price: £{price:.2f}", font=("Arial", 12), fg="white", bg="black").grid(row=2, column=0, columnspan=2, pady=5) # shows the price in white text

    tk.Label(inner_frame, text="Quantity:", fg="white", bg="black").grid(row=3, column=0, sticky="e", pady=5) # shows the quantity label in white text and aligned to the right
    
    quantity = tk.Spinbox(inner_frame, from_=1, to=10, width=5) # spinbox allows user to select quantity from 1 to 10
    quantity.grid(row=3, column=1, sticky="w", pady=5)

    def add_to_cart():
       
        qty = int(quantity.get()) # retrieves the value form spinbox where the user selects how much pizzaa they want
        cart[name] = { # adds or updates the cart dictonary using pizza name as key
            "image": image, # stores image for displaying in cart
            "quantity": qty, # stores how many the user wants
            "price": price # stores the price of the pizza
        }

        for widget in details_frame.winfo_children():
            widget.destroy()
        
        update_order_details_frame(order_frame, cart, total_price_label)

    def cancel_selection(): # defines the cancel button
        for widget in details_frame.winfo_children():
            widget.destroy() # removes all widgets from the frame 

    ttk.Button(inner_frame, text="Add to Cart", command=add_to_cart).grid(row=4, column=0, pady=10, padx=5) # adds selected pizza to cart

    ttk.Button(inner_frame, text="Cancel", command=cancel_selection).grid(row=4, column=1, pady=10, padx=5) # clears the selection and returns to pizza selection

def update_order_details_frame(frame, cart, total_price_label):
    for widget in frame.winfo_children():
        widget.destroy()

    row, total = 1, 0.0
    for name, item in cart.items():
        tk.Label(frame, image=item["image"]).grid(row=row, column=0, padx=5, pady=5)
        tk.Label(frame, text=name).grid(row=row, column=1, sticky="w")
        tk.Label(frame, text=f"£{item['price']:.2f}").grid(row=row, column=2, sticky="e")
        tk.Label(frame, text=f"Qty: {item['quantity']}").grid(row=row+1, column=1, sticky="w")
        line_total = item["price"] * item["quantity"]
        tk.Label(frame, text=f"£{line_total:.2f}").grid(row=row+1, column=2, sticky="e")
        total += line_total
        row += 2

    if not cart: # if the cart is empty, shows a message
        tk.Label(frame, text="Your cart is empty").pack()
        total_price_label.config(text="Total: £0.00")
        return # exits the function 

    # adds a header to the order details frame
    tk.Label(frame, text="Your Order:", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

    # update the total price label 
    total_price_label.config(text=f"Total: £{total:.2f}")

    # creates a sub frame to hold tje cancel and confirm buttons 
    button_frame = tk.Frame(frame)
    button_frame.grid(row=row+1, column=0, columnspan=3, pady=10)

    # defines the buttons and their action to clear the cart 
    def on_clear_cart():
        clear_cart(frame, cart, total_price_label)

    # defines the buttons and their action to confirm the order 
    def on_confirm_order():
        confirm_order(frame, cart, total_price_label)

    ttk.Button(button_frame, text="Cancel", command=on_clear_cart).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Confirm", command=on_confirm_order).pack(side=tk.LEFT, padx=10)

def clear_all_frames(show_btn, clear_btn, pizza_frame, details_frame, order_frame, cart):
   
    for frame in [pizza_frame, details_frame, order_frame]: # loops through the main content frames and clears their widgets 
        for widget in frame.winfo_children():
            widget.destroy()# clears the widgets in the frame

    show_btn.config(state=tk.NORMAL) # re enables the show button
    clear_btn.config(state=tk.DISABLED) # disables the clear button 
    cart.clear() # empties the cart

def clear_cart(frame, cart, total_price_label):
    cart.clear() # clears the cart
    for widget in frame.winfo_children(): # clears the widgets in the frame 
        widget.destroy()
    tk.Label(frame, text="Your cart is empty").pack()# displays a message to the user 
    total_price_label.config(text="Total: £0.00") # resets the total price label to 0.00 

def confirm_order(frame, cart, total_price_label):
    cart.clear() # clears the cart 
    for widget in frame.winfo_children(): # removes all widgets from the frame 
        widget.destroy()
    tk.Label(frame, text="Order successfully placed!").pack() # displays a message to the user 
    total_price_label.config(text="Total: £0.00") # resets the total price label to 0.00 

def add_pizza(): 
    def save_new_pizza(): # gets users input and strips it of any whitespace 
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        image_path = image_entry.get().strip()

        if not name or not price or not image_path: # validate that no field is empty 
            messagebox.showerror("Error", "All fields must be filled!")
            return

        try: # valdiate that the price is a number 
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number!")
            return

        # Copy image to pizza image folder
        try:
            from shutil import copyfile
            image_ext = os.path.splitext(image_path)[1].lower()
            valid_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
            if image_ext not in valid_exts:
                raise ValueError("Invalid image file type.")
            
            dest_path = os.path.join("allPizza", name + image_ext) # sets the destination path for the image
            copyfile(image_path, dest_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")
            return

        try: # appends the new pizza to the csv file 
            with open("pizza_prices.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, f"{price:.2f}"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save price to CSV: {e}")
            return

        messagebox.showinfo("Success", f"Pizza '{name}' added successfully.") # shows a success message and closes the window 
        top.destroy()

    top = tk.Toplevel() # creates a new window for adding a pizza 
    top.title("Add New Pizza")

    tk.Label(top, text="Pizza Name:").grid(row=0, column=0, padx=10, pady=5) #entry for pizza name 
    name_entry = tk.Entry(top)
    name_entry.grid(row=0, column=1)

    tk.Label(top, text="Price (£):").grid(row=1, column=0, padx=10, pady=5) # entry for pizza price 
    price_entry = tk.Entry(top)
    price_entry.grid(row=1, column=1)

    tk.Label(top, text="Image Path:").grid(row=2, column=0, padx=10, pady=5) # entry for image path 
    image_entry = tk.Entry(top, width=40)
    image_entry.grid(row=2, column=1)

    ttk.Button(top, text="Save Pizza", command=save_new_pizza).grid(row=3, column=0, columnspan=2, pady=10) # button to trigger sve function 

def del_pizza():
    print("Delete button activated") 

def on_quit(app):
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"): # shows a message box to confirm if the user wants to quit
        app.destroy() # closes the app 

def configure_style():
    style = ttk.Style() 
    style.configure("TButton", padding=5) # modifies the style of the app, adds padding and font and makes buttons look better 
    style.configure("big.TButton", font=("Arial", 10, "bold")) # defines a custom button style and sets font to arial, size 10 with bold weight

def update_scrollregion(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_configure_scrollable_order(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def create_frames(app):
    menu_frame = tk.Frame(app, bg="lightgray", height=50)  # top menu frame
    menu_frame.pack(side=tk.TOP, fill=tk.X)

    center_frame = tk.Frame(app)  # main center area
    center_frame.pack(expand=True, fill=tk.BOTH)

    pizza_frame = tk.Frame(center_frame, bg="red", width=800)  # left pizza options
    pizza_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    details_frame = tk.Frame(center_frame, bg="black", width=400, height=400)  # right pizza details
    details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    details_frame.configure(width=400, bg="black")
    details_frame.grid_propagate(False)

    cart_frame = tk.Frame(app, bg="green", height=250)  # bottom cart frame
    cart_frame.pack(side=tk.BOTTOM, fill=tk.X)
    cart_frame.pack_propagate(False)

    canvas = tk.Canvas(cart_frame, bg="green", height=200, highlightthickness=0)  # scrollable cart area
    scrollbar = ttk.Scrollbar(cart_frame, orient="vertical", command=canvas.yview)
    scrollable_order = tk.Frame(canvas, bg="green")  # frame inside canvas

    # Bind with named function 
    scrollable_order.bind("<Configure>", partial(on_configure_scrollable_order, canvas=canvas))

    canvas.create_window((0, 0), window=scrollable_order, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return {
        "menu": menu_frame,
        "pizza": pizza_frame,
        "details": details_frame,
        "cart": cart_frame,
        "scrollable_order": scrollable_order,
    }


def create_buttons(menu_frame, app, images, pizza_frame, details_frame, order_frame, cart, prices, total_price_label):
    def show_pizza_action(): # action to show the pizza images 
        pizza_images_as_buttons(images, pizza_frame, details_frame, order_frame, cart, prices, total_price_label) # laod pizza images as buttons 
        show_btn.config(state=tk.DISABLED) # disables the show button so that it cannot be clicked again
        clear_btn.config(state=tk.NORMAL) # enables the clear button so that it can be clicked 

    def clear_pizza_action(): # action to clear the pizza images
        clear_all_frames(show_btn, clear_btn, pizza_frame, details_frame, order_frame, cart)

    def quit_action(): # action to quit the app
        quit(app)  # closes the app

    show_btn = ttk.Button(menu_frame, text="Show Pizzas", command=show_pizza_action)# button to show the pizza images
    show_btn.pack(side=tk.LEFT, padx=5) # adds some padding to the button 

    clear_btn = ttk.Button(menu_frame, text="Clear All Pizzas", command=clear_pizza_action) # button to clear the pizza images
    clear_btn.pack(side=tk.LEFT, padx=5) # adds some padding to the button 

    ttk.Button(menu_frame, text="Add New", command=add_pizza).pack(side=tk.LEFT, padx=5) # button to add a new pizza 
    ttk.Button(menu_frame, text="Delete", command=del_pizza).pack(side=tk.LEFT, padx=5) # button to delete a pizza
    ttk.Button(menu_frame, text="Quit", command=quit_action).pack(side=tk.RIGHT, padx=5) # button to quit the app

def main():
    app = tk.Tk()
    app.title("Online Pizza Store by Student")
    app.geometry("1200x800")
    app.configure(bg="white")

    configure_style()
    frames = create_frames(app)

    pizza_images = {} # dictionary to hold the images 
    save_images("allPizza/", pizza_images) # loads the images from the directory 
    pizza_prices = load_pizza_prices("pizza_prices.csv")# loads the prices from the csv file
    pizza_cart = {} # initialises the cart as an empty dictionary 

    total_price_label = tk.Label(frames["cart"], text="Total: £0.00", font=("Arial", 14, "bold"), bg="green", fg="white") # creates a label to show the total price of the order 
    total_price_label.pack(side=tk.RIGHT, padx=20, pady=10)

    create_buttons(frames["menu"], app, pizza_images, frames["pizza"], frames["details"], frames["scrollable_order"], 
               pizza_cart, pizza_prices, total_price_label) # creates the buttons in the menu frame, also passes the frames to the function so that they can be used in the button actions

    app.mainloop()

main()