from datetime import datetime
import Levenshtein
import tkinter as tk


def age(birthdate):
    today = datetime.now()
    if isinstance(birthdate, str):
        birthdate = datetime.strptime(birthdate, "%d-%m-%Y")
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def str_to_date(str, format='%Y%m%d'):
    return datetime.strptime(str, format)

def previous_year(n=1, from_date=None):
    if from_date is None:
        date = datetime.now()
    else:
        date = from_date
    return date.year - n

def today():
    return datetime.now().year

def similarity(str1, str2):
    # set1 = set(str1)
    # set2 = set(str2)
    # intersection_size = len(set1.intersection(set2))
    # union_size = len(set1.union(set2))
    # return intersection_size / union_size
    return Levenshtein.ratio(str1.upper(), str2.upper())

def show_merge_choice(option1, option2):
    def on_radio_button_change():
        selection_label.config(text=f"Selected option: {var.get()}")
        selected_option = var.get()
        if selected_option == "custom":
            edit_entry.config(state=tk.NORMAL)
            edit_entry.insert(0, option2)
            edit_entry.focus()
        else:
            edit_entry.delete(0, tk.END)
            edit_entry.config(state=tk.DISABLED)

    def on_confirm_button_click():
        window.quit()

    # Create the main window
    window = tk.Tk()
    window.title("Choose an Option")
    window.geometry("300x300")  # Set the window size to 300x300

    # Create a variable to hold the selected option
    var = tk.StringVar(value=option2)

    # Create a frame to group the radio buttons
    frame = tk.Frame(window)

    # Create radio buttons for the options within the frame
    options = [option1, option2, 'custom']
    radio_buttons = []
    for option in options:
        radio_button = tk.Radiobutton(frame, text=option, variable=var, value=option, command=on_radio_button_change)
        radio_buttons.append(radio_button)

    # Place the radio buttons in the frame
    for radio_button in radio_buttons:
        radio_button.pack(anchor=tk.W)

    # Place the frame in the window
    frame.pack(pady=10)

    # Create an Entry widget for custom input
    edit_entry = tk.Entry(window, state=tk.DISABLED)
    edit_entry.pack(pady=10)

    # Create a label to display the selected option
    selection_label = tk.Label(window, text=f'Selected option: {option2}')
    selection_label.pack()

    # Create a confirm button
    confirm_button = tk.Button(window, text="Confirm", command=on_confirm_button_click)
    confirm_button.pack(pady=10)

    # Run the Tkinter event loop
    window.mainloop()
    selected_option = var.get()
    edit_text = edit_entry.get()
    window.destroy()

    # Once the user has confirmed, continue with the rest of your script
    if selected_option == "custom":
        return edit_text
    else:
        return selected_option

def show_update_name(name):
    def on_confirm_button_click():
        window.quit()

    # Create the main window
    window = tk.Tk()
    window.title("Update Name")
    window.geometry("400x300")  # Set the window size to 300x300

    # Show window in the center of the screen
    window.eval('tk::PlaceWindow . center')

    # Add label with original name
    original_name_label = tk.Label(window, text=f'Original name: {name}')
    original_name_label.pack()

    # Create an Entry widget for custom input
    edit_entry = tk.Entry(window)
    edit_entry.pack(fill=tk.X, pady=10)
    edit_entry.pack(pady=10)
    edit_entry.insert(0, name)
    edit_entry.focus()

    # Create a confirm button
    confirm_button = tk.Button(window, text="Confirm", command=on_confirm_button_click)
    confirm_button.pack(pady=10)

    # Run the Tkinter event loop
    window.mainloop()
    edit_text = edit_entry.get()
    window.destroy()

    # Once the user has confirmed, continue with the rest of your script
    return edit_text


if __name__ == '__main__':
    print(show_merge_choice('a', 'b'))