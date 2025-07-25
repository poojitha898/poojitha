import tkinter as tk
from tkinter import messagebox, font

class FoodDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery App")
        self.root.geometry("720x480")
        self.root.resizable(False, False)

        # Canvas for colorful gradient background
        self.canvas = tk.Canvas(self.root, width=720, height=480, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_multicolor_gradient()

        # Main container frame with white background and subtle shadow effect
        self.container = tk.Frame(self.root, bg="white", bd=0, highlightthickness=0)
        # place with padding around and simulate shadow using canvas rectangles
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=680, height=440)

        # Draw shadow effect behind container on canvas
        shadow_offset = 8
        self.canvas.create_rectangle(
            (720 - 680)//2 + shadow_offset,
            (480 - 440)//2 + shadow_offset,
            (720 + 680)//2 + shadow_offset,
            (480 + 440)//2 + shadow_offset,
            fill="#c4d7ff", outline="", width=0, tags="shadow"
        )

        self.menu = {
            "Burger": 5.99,
            "Pizza": 8.99,
            "Sushi": 12.99,
            "Salad": 6.50,
            "Fries": 3.50
        }

        self.order = {}

        self.setup_fonts()
        self.create_widgets()

    def draw_multicolor_gradient(self):
        # Create a vertical multi-color gradient
        colors = ["#ff9a9e", "#fad0c4", "#fad0c4", "#a18cd1", "#fbc2eb"]
        height = 480
        segment_height = height // (len(colors) - 1)
        for i in range(len(colors) - 1):
            c1 = self.root.winfo_rgb(colors[i])
            c2 = self.root.winfo_rgb(colors[i + 1])
            for y in range(segment_height):
                ratio = y / segment_height
                r = int(c1[0] + (c2[0] - c1[0]) * ratio) >> 8
                g = int(c1[1] + (c2[1] - c1[1]) * ratio) >> 8
                b = int(c1[2] + (c2[2] - c1[2]) * ratio) >> 8
                color = f"#{r:02x}{g:02x}{b:02x}"
                self.canvas.create_line(0, i * segment_height + y, 720, i * segment_height + y, fill=color)

    def setup_fonts(self):
        self.title_font = ("Segoe UI", 24, "bold")
        self.menu_font = ("Segoe UI", 13)
        self.header_font = ("Segoe UI", 16, "bold")
        self.summary_font = ("Segoe UI", 12)
        self.button_font = ("Segoe UI", 15, "bold")

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.container, text="Food Delivery App", font=self.title_font, bg="white", fg="#4a148c")
        title_label.pack(pady=(20, 15))

        # Frames container
        frames_container = tk.Frame(self.container, bg="white")
        frames_container.pack(padx=20, pady=10, fill="both", expand=True)

        # Left Frame - Menu selection with rounded corners simulation
        menu_frame = tk.Frame(frames_container, bg="#ede7f6", bd=0)
        menu_frame.pack(side="left", fill="y", expand=False, padx=(0, 20), ipadx=10, ipady=10)

        menu_label = tk.Label(menu_frame, text="Menu", font=self.header_font, bg="#ede7f6", fg="#311b92")
        menu_label.pack(pady=12)

        self.quantity_vars = {}
        for item, price in self.menu.items():
            item_frame = tk.Frame(menu_frame, bg="#ede7f6")
            item_frame.pack(fill="x", padx=15, pady=6)

            label = tk.Label(item_frame, text=f"{item} - ${price:.2f}", font=self.menu_font, bg="#ede7f6")
            label.pack(side="left")

            qty_var = tk.IntVar(value=0)
            self.quantity_vars[item] = qty_var
            spinbox = tk.Spinbox(item_frame, from_=0, to=20, textvariable=qty_var, width=4, font=self.menu_font,
                                 command=self.update_order_summary, relief="flat", bg="white")
            spinbox.pack(side="right")

        # Right Frame - Bill summary with headers, also rounded corners simulation
        summary_frame = tk.Frame(frames_container, bg="#ede7f6", bd=0)
        summary_frame.pack(side="right", fill="both", expand=True, ipadx=10, ipady=10)

        summary_label = tk.Label(summary_frame, text="Order Bill", font=self.header_font, bg="#ede7f6", fg="#311b92")
        summary_label.pack(pady=12)

        # Bill Header
        header_frame = tk.Frame(summary_frame, bg="#d1c4e9")
        header_frame.pack(fill="x", padx=10)

        tk.Label(header_frame, text="Item", font=self.menu_font, width=15, anchor="w", bg="#d1c4e9").grid(row=0, column=0)
        tk.Label(header_frame, text="Qty", font=self.menu_font, width=5, anchor="center", bg="#d1c4e9").grid(row=0, column=1)
        tk.Label(header_frame, text="Price", font=self.menu_font, width=10, anchor="e", bg="#d1c4e9").grid(row=0, column=2)
        tk.Label(header_frame, text="Cost", font=self.menu_font, width=12, anchor="e", bg="#d1c4e9").grid(row=0, column=3)

        # Frame for bill items
        self.bill_items_frame = tk.Frame(summary_frame, bg="white")
        self.bill_items_frame.pack(fill="both", expand=True, padx=10, pady=8)

        # Total label
        self.total_label = tk.Label(summary_frame, text="Total: $0.00", font=self.header_font, bg="#ede7f6", fg="#4a148c")
        self.total_label.pack(pady=12)

        # Place Order button
        place_order_btn = tk.Button(self.container, text="Place Order", font=self.button_font, bg="#7e57c2", fg="white",
                                    activebackground="#5e35b1", padx=20, pady=10, command=self.place_order, bd=0, relief="raised",
                                    cursor="hand2")
        place_order_btn.pack(pady=(0, 25))

    def update_order_summary(self):
        for widget in self.bill_items_frame.winfo_children():
            widget.destroy()

        self.order.clear()
        total = 0
        row = 0

        for item, qty_var in self.quantity_vars.items():
            qty = qty_var.get()
            if qty > 0:
                price = self.menu[item]
                cost = price * qty
                self.order[item] = qty
                total += cost

                tk.Label(self.bill_items_frame, text=item, font=self.summary_font, anchor="w", width=15, bg="white").grid(row=row, column=0, sticky="w")
                tk.Label(self.bill_items_frame, text=str(qty), font=self.summary_font, width=5, bg="white").grid(row=row, column=1)
                tk.Label(self.bill_items_frame, text=f"${price:.2f}", font=self.summary_font, width=10, anchor="e", bg="white").grid(row=row, column=2)
                tk.Label(self.bill_items_frame, text=f"${cost:.2f}", font=self.summary_font, width=12, anchor="e", bg="white").grid(row=row, column=3)
                row += 1

        self.total_label.config(text=f"Total: ${total:.2f}" if total > 0 else "Total: $0.00")

    def place_order(self):
        if not self.order:
            messagebox.showwarning("No Items Selected", "Please select at least one item to place an order.")
            return

        order_details = "\n".join([f"{item} x{qty}" for item, qty in self.order.items()])
        total_cost = sum(self.menu[item] * qty for item, qty in self.order.items())
        messagebox.showinfo("Order Placed",
                            f"Thank you for your order!\n\n{order_details}\n\nTotal Cost: ${total_cost:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodDeliveryApp(root)
    root.mainloop()
