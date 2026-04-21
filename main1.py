import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os

class RestaurantManagementSystem:
    def __init__(self, root, menu_path, records_path, reservations_path):
        self.root = root
        self.root.title("Restaurant Management System")
        self.menu_path = menu_path
        self.records_path = records_path
        self.reservations_path = reservations_path

        self.customer_name = tk.StringVar()
        self.customer_contact = tk.StringVar()

        self.items = self.load_menu_from_csv()

        self.orders = {}

        self.gst_percentage = 18

        self.create_gui()

    def load_menu_from_csv(self):
        menu_items = {}
        try:
            with open(self.menu_path, "r") as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    item_name, item_price = row
                    menu_items[item_name] = float(item_price)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Menu file not found at {self.menu_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading menu: {e}")
        return menu_items

    def create_gui(self):
        details_frame = tk.LabelFrame(self.root, text="Customer Details")
        details_frame.pack(fill="x", padx=10, pady=10)

        name_label = tk.Label(details_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(details_frame, textvariable=self.customer_name)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        contact_label = tk.Label(details_frame, text="Contact:")
        contact_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(details_frame, textvariable=self.customer_contact)
        contact_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        contact_entry.configure(validate="key")
        contact_entry.configure(validatecommand=(contact_entry.register(self.validate_contact), "%P"))

        menu_frame = tk.LabelFrame(self.root, text="Menu")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        item_header = tk.Label(menu_frame, text="Items")
        item_header.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        quantity_header = tk.Label(menu_frame, text="Quantity")
        quantity_header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        row = 1
        for item, price in self.items.items():
            item_var = tk.IntVar()
            item_label = tk.Label(menu_frame, text=f"{item} - {self.convert_to_inr(price)}")
            item_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

            quantity_entry = tk.Entry(menu_frame, width=5)
            quantity_entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")

            self.orders[item] = {"var": item_var, "quantity": quantity_entry}

            row += 1

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        print_bill_button = tk.Button(buttons_frame, text="Print Bill", command=self.show_bill_popup)
        print_bill_button.pack(side="left", padx=5)

        reservations_button = tk.Button(buttons_frame, text="Reservations", command=self.show_reservations_popup)
        reservations_button.pack(side="left", padx=5)

        past_records_button = tk.Button(buttons_frame, text="Past Records", command=self.view_past_records)
        past_records_button.pack(side="left", padx=5)

        clear_selection_button = tk.Button(buttons_frame, text="Clear Selection", command=self.clear_selection)
        clear_selection_button.pack(side="left", padx=5)

        self.sample_bill_text = tk.Text(self.root, height=10)
        self.sample_bill_text.pack(fill="x", padx=10, pady=10)

        # Update sample bill when quantity or item is selected
        for item, info in self.orders.items():
            info["quantity"].bind("<FocusOut>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<Return>", lambda event, item=item: self.update_sample_bill(item))
            info["quantity"].bind("<KeyRelease>", lambda event, item=item: self.update_sample_bill(item))
            info["var"].trace("w", lambda *args, item=item: self.update_sample_bill(item))

    def show_bill_popup(self):
        # Check if customer name is provided
        if not self.customer_name.get().strip():
            messagebox.showwarning("Warning", "Please enter customer name.")
            return

        selected_items = []
        total_price = 0

        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)

        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one item.")
            return

        gst_amount = (total_price * self.gst_percentage) / 100

        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price + gst_amount)}"

        messagebox.showinfo("Bill", bill)
        # Record the order
        self.record_order()

    def show_reservations_popup(self):
        reservations_window = tk.Toplevel(self.root)
        reservations_window.title("Reservations")

        make_reservation_button = tk.Button(reservations_window, text="Make a Reservation", command=self.make_reservation)
        make_reservation_button.pack(pady=10)

        view_reservation_button = tk.Button(reservations_window, text="View Reservations", command=self.view_reservations)
        view_reservation_button.pack(pady=10)

    def make_reservation(self):
        reservation_window = tk.Toplevel(self.root)
        reservation_window.title("Make Reservation")

        # Label and Entry for Name
        name_label = tk.Label(reservation_window, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(reservation_window, textvariable=tk.StringVar())
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Label and Entry for Contact
        contact_label = tk.Label(reservation_window, text="Contact:")
        contact_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        contact_entry = tk.Entry(reservation_window, textvariable=tk.StringVar())
        contact_entry.grid(row=1, column=1, padx=5, pady=5)

        # Label and Entry for Date
        date_label = tk.Label(reservation_window, text="Date (YYYY-MM-DD):")
        date_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        date_entry = tk.Entry(reservation_window, textvariable=tk.StringVar())
        date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Label and Entry for Time
        time_label = tk.Label(reservation_window, text="Time (HH:MM AM/PM):")
        time_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        time_entry = tk.Entry(reservation_window, textvariable=tk.StringVar())
        time_entry.grid(row=3, column=1, padx=5, pady=5)

        # Label and Entry for Number of People
        num_people_label = tk.Label(reservation_window, text="Number of People:")
        num_people_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        num_people_entry = tk.Entry(reservation_window, textvariable=tk.StringVar())
        num_people_entry.grid(row=4, column=1, padx=5, pady=5)

        # Button to submit reservation
        submit_button = tk.Button(reservation_window, text="Submit Reservation", command=lambda: self.submit_reservation(name_entry.get(), contact_entry.get(), date_entry.get(), time_entry.get(), num_people_entry.get(), reservation_window))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_reservation(self, name, contact, date, time, num_people, reservation_window):
        try:
            with open(self.reservations_path, "a") as file:
                reservation_data = f"Name: {name}, Contact: {contact}, Date: {date}, Time: {time}, Number of People: {num_people}\n"
                file.write(reservation_data)
            messagebox.showinfo("Reservation", "Reservation made successfully.")
            reservation_window.destroy()  # Close the reservation window
        except Exception as e:
            messagebox.showerror("Error", f"Error making reservation: {e}")

    def view_reservations(self):
        try:
            with open(self.reservations_path, "r") as file:
                reservations = file.readlines()
                if reservations:
                    formatted_reservations = []
                    for i, reservation in enumerate(reservations, start=1):
                        formatted_reservations.append(f"Reservation {i}: {reservation}")
                    messagebox.showinfo("Reservations", "\n".join(formatted_reservations))
                else:
                    messagebox.showinfo("Reservations", "No reservations found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error accessing reservations: {e}")

    def view_past_records(self):
        try:
            with open(self.records_path, "r") as file:
                reader = csv.reader(file)
                records = list(reader)
                if records:
                    formatted_records = []
                    for i, record in enumerate(records, start=1):
                        record_data = {
                            "Order Time": record[0],
                            "Customer Name": record[1],
                            "Customer Contact": record[2],
                            "Selected Items": record[3],
                            "Total Price": record[4],
                            "GST": record[5],
                            "Grand Total": record[6]
                        }
                        formatted_record = f"Order Number: {i}\n"
                        for key, value in record_data.items():
                            if key == "Selected Items":
                                formatted_record += f"{key}:\n"
                                selected_items = value.split('|')
                                for item in selected_items:
                                    if ':' in item:
                                        item_name, quantity = item.split(':')
                                        formatted_record += f"{item_name}: {quantity}\n"
                                    else:
                                        formatted_record += f"{item}\n"
                            else:
                                formatted_record += f"{key}: {value}\n"
                        formatted_record += "\n"
                        formatted_records.append(formatted_record)
                    
                    messagebox.showinfo("Past Records", "Past Records:\n" + "\n".join(formatted_records))
                else:
                    messagebox.showinfo("Past Records", "No past records found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error accessing past records: {e}")

    def record_order(self):
        try:
            with open(self.records_path, "a", newline="") as file:
                writer = csv.writer(file)
                order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                customer_name = self.customer_name.get()
                customer_contact = self.customer_contact.get()
                selected_items = []
                total_price = 0
                for item, info in self.orders.items():
                    quantity = info["quantity"].get()
                    if quantity:
                        selected_items.append(f"{item}:{quantity}")
                        total_price += self.items[item] * int(quantity)
                gst_amount = (total_price * self.gst_percentage) / 100
                grand_total = total_price + gst_amount
                order_data = {"Order Time": order_time, "Customer Name": customer_name, "Customer Contact": customer_contact, "Selected Items": '|'.join(selected_items), "Total Price": total_price, "GST": gst_amount, "Grand Total": grand_total}
                writer.writerow(order_data.values())
        except Exception as e:
            messagebox.showerror("Error", f"Error recording order: {e}")

    def clear_selection(self):
        for item, info in self.orders.items():
            info["var"].set(0)
            info["quantity"].delete(0, tk.END)

    def update_sample_bill(self, item):
        selected_items = []
        total_price = 0

        for item, info in self.orders.items():
            quantity = info["quantity"].get()
            if quantity:
                selected_items.append((item, int(quantity)))
                total_price += self.items[item] * int(quantity)

        gst_amount = (total_price * self.gst_percentage) / 100

        bill = f"Customer Name: {self.customer_name.get()}\n"
        bill += f"Customer Contact: {self.customer_contact.get()}\n\n"
        bill += "Selected Items:\n"
        for item, quantity in selected_items:
            bill += f"{item} x {quantity} - {self.convert_to_inr(self.items[item] * quantity)}\n"
        bill += f"\nTotal Price: {self.convert_to_inr(total_price)}\n"
        bill += f"GST ({self.gst_percentage}%): {self.convert_to_inr(gst_amount)}\n"
        bill += f"Grand Total: {self.convert_to_inr(total_price + gst_amount)}"

        self.sample_bill_text.delete("1.0", tk.END)  # Clear previous contents
        self.sample_bill_text.insert(tk.END, bill)

    def validate_contact(self, value):
        return value.isdigit() or value == ""

    @staticmethod
    def convert_to_inr(amount):
        return "₹" + str(amount)

root = tk.Tk()
# Assuming menu.csv is in the same directory as the script
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_path = os.path.join(current_dir, "menu.csv")
records_path = os.path.join(current_dir, "records.csv")
reservations_path = os.path.join(current_dir, "reservations.txt")
restaurant_system = RestaurantManagementSystem(root, menu_path, records_path, reservations_path)
root.mainloop()

