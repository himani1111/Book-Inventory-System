import pandas as pd
import numpy as np
from tkinter import *
book_path = r'C:\Users\Partish Singla\Downloads\books_final1.csv'
def read_books():
    books = pd.read_csv(book_path)
    return books

books = read_books()
books1 = books


# Track total stock
def track_book_stock(bookname):
  if books[books['Book Title']==bookname]['Stock Status'].values[0] == 'In Stock':
    return books[books['Book Title']==bookname]['Copies Left'].values[0]
  else:
    return books[books['Book Title']==bookname]['Stock Status'].values[0]


def book_stock_status(bookname):
    match = books[books['Book Title'] == bookname]
    if match.empty:
        return bookname, '-> Book not Available'

    status = match['Stock Status'].values[0]
    if status == 'In Stock':
        stock = books[books['Book Title']==bookname]['Copies Left'].values[0]
        return bookname, '-> In Stock', stock
    elif status == 'Out stock':
        return bookname, '-> Out of Stock'
    else:
        return bookname, '-> Book status unknown'

def search_by_keyword(keyword):
    matches = books[books['Book Title'].str.contains(keyword, case=False)]['Book Title'].reset_index(drop=True)
    results = []
    for title in matches:
        results.append(book_stock_status(title))

    my_series = pd.Series(results)
    if my_series.empty:
        return "No match found"
    else:
        my_series = my_series.reset_index(drop=True)
    return my_series

# Search for a specific Genre
def search_genre(keyword):
    l = books[books['Category'].str.contains(keyword, case=False, na=False)]['Book Title'].reset_index(drop=True)
    if l.empty:
        return "No match found"
    else:
        output = '\n'.join(l)
    return output

def search_author(keyword):
  l = books[books['Author'].str.contains(keyword, case=False, na=False)]['Book Title'].reset_index(drop = True)
  if l.empty:
      return "No match found"
  else:
    output = '\n'.join(l)
  return output

def top_selling_books():
  l = books.sort_values(by='Copies sold', ascending=False).head(3)['Book Title'].reset_index(drop = True)
  output = '\n'.join(l)
  return output

def get_stock_summary():
    total = len(books)
    in_stock = books[books['Stock Status'].str.lower() == 'in stock'].shape[0]
    out_stock = books[books['Stock Status'].str.lower() == 'out stock'].shape[0]
    sold = books['Copies sold'].sum()
    return total, in_stock, out_stock, sold


from datetime import datetime

# Global dictionary to hold sold books data
sold_books = {}

def sell_book(book_title, books_path=book_path):

    books['Book Title'] = books['Book Title'].str.strip()

    if book_title not in books['Book Title'].values:
        return "Book not found in inventory."

    idx = books[books['Book Title'] == book_title].index[0]
    current_stock = books.at[idx, 'Copies Left']

    if current_stock <= 0:
        return "Book is out of stock."

    # Update stock
    books.at[idx, 'Copies Left'] -= 1

    # Update stock status
    books.at[idx, 'Stock Status'] = 'In Stock' if books.at[idx, 'Copies Left'] > 0 else 'Out stock'

    # Save updated inventory
    books.to_csv(books_path, index=False)

    # Track the sale
    month = datetime.now().strftime("%B")
    if month not in sold_books:
        sold_books[month] = {}
    if book_title in sold_books[month]:
        sold_books[month][book_title] += 1
    else:
        sold_books[month][book_title] = 1

    return f"✅ '{book_title}' sold successfully."

def add_inventory(new_inventory_path, books_path=book_path):
    # Load existing and new inventory
    books = books1
    #books = pd.read_csv(books_path)
    new_books = pd.read_csv(new_inventory_path)

    # Normalize Book Title column for comparison (optional cleanup)
    books['Book Title'] = books['Book Title'].str.strip()
    new_books['Book Title'] = new_books['Book Title'].str.strip()

    for _, new_row in new_books.iterrows():
        title = new_row['Book Title']
        if title in books['Book Title'].values:
            # Existing book: increase Copies left
            books.loc[books['Book Title'] == title, 'Copies Left'] += new_row['Copies']
        else:
            # New book: append the full row
            books = pd.concat([books, pd.DataFrame([new_row])], ignore_index=True)

    # Optionally update Stock Status
    books['Stock Status'] = books['Copies Left'].apply(lambda x: 'In Stock' if x > 0 else 'Out stock')

    # Save the updated books back to CSV
    books.to_csv(books_path, index=False)
    return "Inventory updated successfully."



def add_stock_by_title(title, copies_to_add, books_path=book_path):
    try:
        # Read the books CSV
        books = pd.read_csv(books_path)
        books['Book Title'] = books['Book Title'].str.strip()

        if title not in books['Book Title'].values:
            return "❌ Book not found in inventory."

        # Locate the book row
        idx = books[books['Book Title'] == title].index[0]

        # Add to existing stock
        books.at[idx, 'Copies Left'] += copies_to_add

        # Update Stock Status
        books.at[idx, 'Stock Status'] = 'In Stock' if books.at[idx, 'Copies Left'] > 0 else 'Out stock'

        # Save back to CSV
        books.to_csv(books_path, index=False)
        return f"✅ Added {copies_to_add} copies to '{title}'.",books.at[idx, 'Copies Left']

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def books_info():
    total_books = len(books)
    stocked_books = books[books["Stock Status"].str.contains("In Stock", na=False)]
    total_in_stock = stocked_books["Copies Left"].astype(int).sum()
    low_stock_items = books[books["Copies Left"] <= 2]['Book Title'].values  # Threshold for low stock.
    categories = books["Category"].nunique()
    top_selling = top_selling_books()

    return total_books, stocked_books, total_in_stock,low_stock_items, categories, top_selling

def low_stock():
    l = books[books['Copies Left'] <= 2]['Book Title'].reset_index(drop = True)
    output = '\n'.join(l)
    return output

def get_highest_revenue_book():
    books["Revenue"] = books["Copies sold"] * books["Price (TK)"]
    top_book = books.sort_values("Revenue", ascending=False).iloc[0]
    return {
        "title": top_book["Book Title"],
        "revenue": top_book["Revenue"]
    }

