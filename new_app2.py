import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests

# Replace with your NewsAPI key
API_KEY = "6a839a3f48ce4abca33c67871c5e42fe"
NEWS_URL = "https://newsapi.org/v2/top-headlines"

# Credentials
USERNAME = "rgit123"
PASSWORD = "rgit@mct"

def login():
    if username_entry.get() == USERNAME and password_entry.get() == PASSWORD:
        login_window.destroy()
        show_main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def fetch_news(country=None, category=None):
    """Fetch news strictly based on selected country and category."""
    params = {
        "apiKey": API_KEY,
        "language": "en"
    }
    
    if category and category.lower() != "none":
        params["category"] = category.lower()
    
    if country:
        params["country"] = country.lower()
    
    try:
        response = requests.get(NEWS_URL, params=params)
        data = response.json()

        if data["status"] == "ok" and data["articles"]:
            articles = data["articles"][:10]  # Strictly take first 10 articles
            news_display.config(state=tk.NORMAL)
            news_display.delete("1.0", tk.END)
            
            for idx, article in enumerate(articles, start=1):
                title = article["title"]
                description = article.get("description", "No summary available.")
                source = article["source"]["name"]
                news_display.insert(tk.INSERT, f"{idx}. {title}\nSource: {source}\nSummary: {description}\n\n")
            
            news_display.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("No News Found", "No articles found for the selected filters. Please try different options.")
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to fetch news. Check your internet connection.\n{e}")

def get_random_news():
    """Fetch general top headlines."""
    fetch_news(country="in")  # Default to India for better synchronization

def get_custom_news():
    """Fetch news based on user input."""
    country = country_var.get()
    category = category_var.get() if category_var.get() != "None" else None
    fetch_news(country, category)

def show_main_app():
    global news_display, country_var, category_var
    
    root = tk.Tk()
    root.title("Instant News Headlines")
    root.geometry("700x550")
    root.configure(bg="#f5f5f5")

    main_frame = tk.Frame(root, bg="#ffffff", padx=10, pady=10, relief=tk.RIDGE, bd=2)
    main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    title_label = tk.Label(main_frame, text="News Headline Fetcher", font=("Arial", 16, "bold"), bg="#007ACC", fg="white", padx=10, pady=5)
    title_label.pack(fill=tk.X)

    input_frame = tk.Frame(main_frame, bg="#f0f0f0", padx=10, pady=10)
    input_frame.pack(fill=tk.X, pady=5)

    tk.Label(input_frame, text="Country:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    country_var = tk.StringVar(value="in")
    countries = ["us", "in", "de", "ca", "ru", "au", "jp", "gb", "fr", "br"]
    country_menu = ttk.Combobox(input_frame, textvariable=country_var, values=countries, width=20)
    country_menu.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Category:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    category_var = tk.StringVar(value="None")
    categories = ["None", "business", "entertainment", "health", "science", "sports", "technology"]
    category_menu = ttk.Combobox(input_frame, textvariable=category_var, values=categories, width=20)
    category_menu.grid(row=0, column=3, padx=5, pady=5)

    button_frame = tk.Frame(main_frame, bg="#ffffff")
    button_frame.pack(fill=tk.X, pady=5)

    custom_news_btn = tk.Button(button_frame, text="Get Custom News", font=("Arial", 12, "bold"), bg="#007ACC", fg="white", relief=tk.RAISED, command=get_custom_news)
    custom_news_btn.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.X)

    random_news_btn = tk.Button(button_frame, text="Get Random Headlines", font=("Arial", 12, "bold"), bg="#28A745", fg="white", relief=tk.RAISED, command=get_random_news)
    random_news_btn.pack(side=tk.RIGHT, padx=10, pady=5, expand=True, fill=tk.X)

    news_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=15, font=("Arial", 12), bg="#fafafa", relief=tk.SUNKEN, borderwidth=2)
    news_display.pack(pady=10, fill=tk.BOTH, expand=True)
    news_display.config(state=tk.DISABLED)
    
    root.mainloop()

# Login Window
login_window = tk.Tk()
login_window.title("Login - Instant News Headline")
login_window.geometry("700x550")
login_window.configure(bg="#f5f5f5")

tk.Label(login_window, text="Instant News Headline", font=("Arial", 18, "bold"), bg="#007ACC", fg="white", pady=10).pack(fill=tk.X)

tk.Label(login_window, text="Username:", font=("Arial", 12), bg="#f5f5f5").pack(pady=5)
username_entry = tk.Entry(login_window, font=("Arial", 12))
username_entry.pack(pady=5)

tk.Label(login_window, text="Password:", font=("Arial", 12), bg="#f5f5f5").pack(pady=5)
password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
password_entry.pack(pady=5)

tk.Button(login_window, text="Login", font=("Arial", 12, "bold"), bg="#007ACC", fg="white", command=login).pack(pady=20)

login_window.mainloop()
