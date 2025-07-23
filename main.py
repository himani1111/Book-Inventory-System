import tkinter as tk
from tkinter import ttk
import utils
from tkinter import messagebox, filedialog


# Clear right frame before updating it
def clear_right_frame():
    for widget in right_frame.winfo_children():
        widget.destroy()


# Option functions
def check_book_status():
    clear_right_frame()

    # Entry and Label
    tk.Label(right_frame, text="🔍 Check Book Stock Status", font=("Arial", 16)).pack(pady=10)
    tk.Label(right_frame, text="Enter Book Name:").pack()

    book_entry = tk.Entry(right_frame, width=40)
    book_entry.pack(pady=5)

    def submit_check():
        keyword = book_entry.get().strip()
        result = utils.search_by_keyword(keyword)
        result_label.config(text=result)

    tk.Button(right_frame, text="Submit", command=submit_check).pack(pady=10)

    result_label = tk.Label(right_frame, text="", font=("Verdana", 8), fg="black", wraplength = 500)
    result_label.pack(pady=30, expand = True)


def search_book_author():
    clear_right_frame()

    # Entry and Label
    tk.Label(right_frame, text="🔍 Search Book by Author Name", font=("Arial", 16)).pack(pady=10)
    tk.Label(right_frame, text="Enter Author Name:").pack()

    book_entry = tk.Entry(right_frame, width=40)
    book_entry.pack(pady=5)

    def submit_check():
        author = book_entry.get().strip()
        result = utils.search_author(author)
        result_label.config(text=result)

    tk.Button(right_frame, text="Submit", command=submit_check).pack(pady=10)

    result_label = tk.Label(right_frame, text="", font=("Arial", 14), fg="blue")
    result_label.pack(pady=10)


def search_book_genre():
    clear_right_frame()

    # Entry and Label
    tk.Label(right_frame, text="🔍 Search Book By Genre", font=("Arial", 16)).pack(pady=10)
    tk.Label(right_frame, text="Enter Genre:").pack()

    book_entry = tk.Entry(right_frame, width=40)
    book_entry.pack(pady=5)

    def submit_check():
        genre = book_entry.get().strip()
        result = utils.search_genre(genre)
        result_label.config(text=result)

    tk.Button(right_frame, text="Submit", command=submit_check).pack(pady=10)

    result_label = tk.Label(right_frame, text="", font=("Arial", 14), fg="blue")
    result_label.pack(pady=10)


def top_selling():
    clear_right_frame()

    # Entry and Label
    tk.Label(right_frame, text="🔍 Top Selling Books", font=("Arial", 16)).pack(pady=10)
    output = utils.top_selling_books()
    tk.Label(right_frame, text=output, font=("Arial", 14), fg='green').pack(pady=20)


def browse_and_upload_inventory():
    clear_right_frame()

    def browse():
        filepath = filedialog.askopenfilename(
            title="Select New Inventory CSV",
            filetypes=[("CSV files", "*.csv")]
        )
        if filepath:
            result = utils.add_inventory(filepath)
            messagebox.showinfo("Upload Result", result)

    browse_btn = tk.Button(right_frame, text="Browse file", command=browse, width = 20, height = 2)
    browse_btn.pack(pady=10)


def show_add_stock():
    clear_right_frame()

    tk.Label(right_frame, text="Enter Book Title", font=("Arial", 12)).pack(pady=5)
    title_entry = tk.Entry(right_frame, width=40)
    title_entry.pack(pady=5)

    tk.Label(right_frame, text="Enter Copies to Add", font=("Arial", 12)).pack(pady=5)
    copies_entry = tk.Entry(right_frame, width=20)
    copies_entry.pack(pady=5)

    def submit_add_stock():
        title = title_entry.get().strip()
        try:
            copies = int(copies_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for copies.")
            return

        result = utils.add_stock_by_title(title, copies)
        messagebox.showinfo("Stock Update", result)

    tk.Button(right_frame, text="Add Stock", command=submit_add_stock).pack(pady=10)



def show_sell_form():
    clear_right_frame()  # Make sure to define a function that clears right_frame

    # Label
    lbl = tk.Label(right_frame, text="Enter Book Title to Sell", font=("Arial", 12))
    lbl.pack(pady=10)

    # Entry box
    book_entry = tk.Entry(right_frame, width=40)
    book_entry.pack(pady=5)

    # Sell button
    def submit_sell():
        title = book_entry.get().strip()
        result = utils.sell_book(title)
        tk.messagebox.showinfo("Sell Book", result)

    sell_btn = tk.Button(right_frame, text="Sell Book", command=submit_sell)
    sell_btn.pack(pady=10)

def sold_books():
    clear_right_frame()
    tk.Label(right_frame, text="🔍 Sold Books", font=("Arial", 16)).pack(pady=10)
    output = utils.sold_books
    tk.Label(right_frame, text=output, font=("Arial", 14), fg='green').pack(pady=20)


def show_dashboard():
    clear_right_frame()

    # Get data from helper
    total_books, stocked_books, total_in_stock, low_stock_items, categories, top_selling = utils.books_info()
    revenue_book = utils.get_highest_revenue_book()
    # ✅ Stats Cards at the top
    stats_row = tk.Frame(right_frame, bg="#F5F6FA")
    stats_row.pack(fill="x", pady=(20, 10), padx=20)

    stats = [
        ("Total Books", total_books),
        ("Unique Categories", categories),
        ("Books In Stock", total_in_stock),
        ("Low Stock Items", len(low_stock_items)),
    ]

    for stat, value in stats:
        card = tk.Frame(stats_row, bd=1, relief="ridge", bg="#fff", width=160, height=70)
        card.pack(side="left", padx=10)
        card.pack_propagate(False)

        tk.Label(card, text=stat, font=("Arial", 10), bg="#fff", fg="#595959").pack(anchor="w", padx=12, pady=(8, 0))
        tk.Label(card, text=value, font=("Arial", 18, "bold"), bg="#fff").pack(anchor="w", padx=12)

    # 🔝 Top Selling Books Section
    top_frame = tk.LabelFrame(right_frame, text="Top Selling Books (Last 3 Months)",
                              font=("Arial", 12, "bold"), bg="#F5F6FA", bd=1)
    top_frame.pack(fill="x", padx=20, pady=(10, 18))

    if isinstance(top_selling, str):
        top_selling = [title.strip() for title in top_selling.split(',')]

    for title in top_selling:
        tk.Label(top_frame, text=f"{title}", bg="#F5F6FA", font=("Arial", 11), anchor="w").pack(anchor="w", padx=10, pady=2)

    revenue_frame = tk.LabelFrame(right_frame, text=" Highest Revenue Generating Book",
                                  font=("Arial", 12, "bold"), bg="#F5F6FA", bd=1)
    revenue_frame.pack(fill="x", padx=20, pady=(10, 18))

    msg = f"• {revenue_book['title']} generated  {revenue_book['revenue']:.2f}"
    tk.Label(revenue_frame, text=msg, bg="#F5F6FA", font=("Arial", 11)).pack(anchor="w", padx=10, pady=5)

    # ⚠️ Stock Alerts Section
    alerts_frame = tk.Frame(right_frame, bg="#F5F6FA")
    alerts_frame.pack(fill="x", padx=20, pady=10)

    def low_stock_alerts():
        for widget in alerts_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        results = utils.low_stock()
        tk.Label(alerts_frame, text=results, font=("Arial", 11),
                         fg="black", bg="#F5F6FA").pack(anchor="w", padx=10)

    alert_btn = tk.Button(alerts_frame, text="Low Stock Alerts",
                          command=low_stock_alerts,
                          font=("Arial", 12), fg="red", bg="#fff", relief="raised",
                          width=20)
    alert_btn.pack(pady=8)



# Root window setup
root = tk.Tk()
root.title("Book Inventory System")
root.geometry("1100x700")
root.configure(bg="#F5F6FA")

# Layout frames
left_frame = tk.Frame(root, width=200, bg="#353940")
right_frame = tk.Frame(root, bg='white')

left_frame.pack(side="left", fill="y")
right_frame.pack(side="right", fill="both", expand=True)

# Buttons with linked functions
buttons = [
    ("Dashboard", show_dashboard),
    ("Sell Book", show_sell_form),
    ("View Book Status", check_book_status),
    ("Search Book by Genre", search_book_genre),
    ("Search Book by Author", search_book_author),
    ("Upload Inventory", browse_and_upload_inventory),
    ("Books Sold This Month", sold_books)
]

for label, command in buttons:
    btn = tk.Button(left_frame, text=label, width=20, pady=10, command=command)
    btn.pack(pady=10)

# Start the app
root.mainloop()
