import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def browse_folder(folder_path="/"):
    global current_folder
    if folder_path not in history:  # Check if folder_path is not already in history
        history.append(folder_path)  # Append folder_path to history
    current_folder = folder_path
    tree.delete(*tree.get_children())  # Clear existing items
    folders = []
    files = []
    for item in os.listdir(current_folder):
        item_path = os.path.join(current_folder, item)
        if os.path.isdir(item_path):
            folders.append(item)  # Collect folders separately
        else:
            files.append(item)  # Collect files separately

    # Insert folders first
    for folder in folders:
        tree.insert("", "end", text=folder, tags=('folder',))

    # Insert files after folders
    for file in files:
        tree.insert("", "end", text=file)

    # Update the label to display the current folder path
    label_path.config(text=current_folder)

    # Configure tags to display folders with bold font and files with regular font
    style.configure('folder.Treeview', font=('Arial', 12, 'bold'), foreground='green')  # Set folder text color 
    style.configure('file.Treeview', font=('Arial', 12))
    tree.tag_configure('folder', font=('Arial', 12, 'bold'), foreground='green')  # Set folder text color 
    tree.tag_configure('file', font=('Arial', 12))

def open_file(event=None):  # Updated to accept an optional event argument
    selected_item = tree.selection()
    if selected_item:
        item = selected_item[0]  # Get the first selected item
        item_text = tree.item(item, "text")  # Retrieve the text of the selected item
        item_path = os.path.join(current_folder, item_text)
        if os.path.isdir(item_path):
            browse_folder(item_path)  # If it's a directory, browse it
        else:
            file_extension = os.path.splitext(item_path)[1]  # Get file extension
            default_program = get_default_program(file_extension)
            if default_program:
                try:
                    subprocess.run([default_program, item_path])
                except FileNotFoundError:
                    messagebox.showerror("Error", f"Unable to open file with {default_program}.")
            else:
                messagebox.showerror("Error", f"No default program found to open {file_extension} files.")


def get_default_program(file_extension):
    # Dictionary mapping file extensions to default programs
    default_programs = {
        ".txt": "subl", 
        ".go": "subl"  
        # Add more file extensions and their corresponding default programs as needed
    }
    return default_programs.get(file_extension.lower())

def go_back():
    global history
    if len(history) > 1:
        print("Previous History:", history)  # Print previous history
        history.pop()  # Remove the last directory from history
        # Remove duplicate entries from history
        history = list(dict.fromkeys(history))
        print("Current History:", history)  # Print current history
        browse_folder(history[-1])  # Browse to the previous directory
    else:
        print("Cannot go back further, history is empty.")

# Create main window
root = tk.Tk()
root.title("Simple File Explorer")

# Set transparency (optional)
root.attributes('-alpha', 0.7)

# Set background color to black and text color to white
root.configure(bg="#000000")  # Black background

# Label to display current directory path
label_path = tk.Label(root, text="", bg="#000000", fg="#ffffff", font=("Arial", 12,"bold"))
label_path.pack(pady=10)

# Initially browse user directory
current_folder = "/Users/nns"
history = [current_folder]

# Create custom style for the Treeview widget
style = ttk.Style()
style.theme_use("clam")  # Use the "clam" theme
style.configure("Treeview", background="black", foreground="white")  # Set background color to black and text color to white
style.map("Treeview", background=[('selected', '#0078d7')])  # Set selected item color to blue

# Create Treeview widget to display files and folders
tree = ttk.Treeview(root, columns=("fullpath", "type"), show="tree", selectmode="browse")
tree.pack(expand=True, fill="both")

# Bind double click event to treeview
tree.bind("<Double-1>", open_file)

# Initially browse root directory
browse_folder(current_folder)

# Create a back arrow icon
back_icon = tk.PhotoImage(file="back_arrow.png")  # Provide the path to your back arrow icon image

# Button to go back
back_button = tk.Button(root, image=back_icon, command=go_back, bg="#000000", bd=0)  # Black background, no border
back_button.pack(side=tk.TOP, padx=(0, 10))

# Run the main event loop
root.mainloop()
