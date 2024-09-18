import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def calculate_hamming_code(data):
    m = len(data)
    r = 0
    while (2 ** r < m + r + 1):
        r += 1

    hamming_code = ['0'] * (m + r)
    j = 0
    for i in range(1, m + r + 1):
        if i == 2 ** j:
            j += 1
        else:
            hamming_code[-i] = data[-1]
            data = data[:-1]

    for i in range(r):
        position = 2 ** i
        parity = 0
        for j in range(1, len(hamming_code) + 1):
            if j & position:
                parity ^= int(hamming_code[-j])
        hamming_code[-position] = str(parity)

    parity_positions = [2 ** i for i in range(r)][::-1]  # Reversed list for right-to-left
    return ''.join(hamming_code), parity_positions

def detect_and_correct_error(hamming_code):
    n = len(hamming_code)
    r = 0
    while (2 ** r < n + 1):
        r += 1

    error_pos = 0
    for i in range(r):
        position = 2 ** i
        parity = 0
        for j in range(1, n + 1):
            if j & position:
                parity ^= int(hamming_code[-j])
        if parity != 0:
            error_pos += position

    if error_pos == 0:
        return hamming_code, None
    else:
        corrected_code = list(hamming_code)
        corrected_code[-error_pos] = '0' if hamming_code[-error_pos] == '1' else '1'
        return ''.join(corrected_code), error_pos

def generate_hamming_code():
    data = data_entry.get()
    if not set(data).issubset({'0', '1'}):
        messagebox.showerror("Invalid Input", "Please enter a binary string.")
        return
    hamming_code, parity_positions = calculate_hamming_code(data)
    hamming_code_display.delete(0, tk.END)
    hamming_code_display.insert(0, hamming_code)
    parity_positions_display.delete(0, tk.END)
    parity_positions_display.insert(0, ', '.join(map(str, parity_positions)))
    status_var.set("Hamming Code Generated Successfully")
    visualize_hamming_code(hamming_code, parity_positions)

def check_and_correct_error():
    received_data = received_data_entry.get()
    if not set(received_data).issubset({'0', '1'}):
        messagebox.showerror("Invalid Input", "Please enter a binary string.")
        return
    corrected_code, error_pos = detect_and_correct_error(received_data)
    if error_pos:
        error_position_display.delete(0, tk.END)
        error_position_display.insert(0, error_pos)
        corrected_data_display.delete(0, tk.END)
        corrected_data_display.insert(0, corrected_code)
        received_data_entry.config(foreground="red")
        messagebox.showinfo("Error Detected",
                            f"Error detected at position {error_pos}. Corrected data: {corrected_code}")
        status_var.set("Error Detected and Corrected")
    else:
        received_data_entry.config(foreground="black")
        messagebox.showinfo("No Error", "No error detected in the received data.")
        status_var.set("No Error Detected")
    visualize_hamming_code(corrected_code if error_pos else received_data, [])

def reset_fields():
    data_entry.delete(0, tk.END)
    hamming_code_display.delete(0, tk.END)
    parity_positions_display.delete(0, tk.END)
    received_data_entry.delete(0, tk.END)
    error_position_display.delete(0, tk.END)
    corrected_data_display.delete(0, tk.END)
    received_data_entry.config(foreground="black")
    status_var.set("Fields Reset")
    for widget in visual_frame.winfo_children():
        widget.destroy()


def visualize_hamming_code(hamming_code, parity_positions):
    for widget in visual_frame.winfo_children():
        widget.destroy()

    r = len(parity_positions)
    for i, bit in enumerate(hamming_code):
        lbl = ttk.Label(visual_frame, text=bit, font=("Helvetica", 10), relief="solid", width=2)

        # Determine if the current position is a parity bit position
        if (i + 1) in parity_positions:
            lbl.config(background="lightblue")  # Highlight parity bits in light blue
        else:
            lbl.config(background="lightgreen")  # Highlight data bits in light green

        # Grid positioning in reverse order (right to left)
        lbl.grid(row=0, column=len(hamming_code) - i - 1, padx=1, pady=1)

    status_var.set(f"{r} Parity bits highlighted in blue, Data bits highlighted in green")


# Creating main window
root = tk.Tk()
root.title("Hamming Code Error Detection and Correction")
root.geometry("700x500")

# Applying a theme
style = ttk.Style(root)
style.theme_use('clam')

# Title Label
title_label = ttk.Label(root, text="Hamming Code Error Detection and Correction", font=("Helvetica", 18, "bold"),
                        foreground="navy")
title_label.pack(pady=10)

# Frame for Data Entry
data_frame = ttk.Frame(root, padding="10")
data_frame.pack(pady=10, padx=20)

ttk.Label(data_frame, text="Enter Binary Data:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5,
                                                                              sticky='w')
data_entry = ttk.Entry(data_frame, font=("Helvetica", 12))
data_entry.grid(row=0, column=1, padx=5, pady=5)
ttk.Button(data_frame, text="Generate Hamming Code", command=generate_hamming_code, style="Accent.TButton").grid(row=0,
                                                                                                                 column=2,
                                                                                                                 padx=10,
                                                                                                                 pady=5)

# Frame for Hamming Code Display
code_frame = ttk.Frame(root, padding="10")
code_frame.pack(pady=10, padx=20)

ttk.Label(code_frame, text="Generated Hamming Code:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5,
                                                                                   sticky='w')
hamming_code_display = ttk.Entry(code_frame, font=("Helvetica", 12))
hamming_code_display.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(code_frame, text="Parity Bit Positions (Right to Left):", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky='w')
parity_positions_display = ttk.Entry(code_frame, font=("Helvetica", 12))
parity_positions_display.grid(row=1, column=1, padx=5, pady=5)

# Frame for Received Data Entry
received_frame = ttk.Frame(root, padding="10")
received_frame.pack(pady=10, padx=20)

ttk.Label(received_frame, text="Enter Received Data:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5,
                                                                                    sticky='w')
received_data_entry = ttk.Entry(received_frame, font=("Helvetica", 12))
received_data_entry.grid(row=0, column=1, padx=5, pady=5)
check_button = ttk.Button(received_frame, text="Check and Correct Error", command=check_and_correct_error,
                          style="Accent.TButton")
check_button.grid(row=0, column=2, padx=10, pady=5)

# Frame for Error and Correction Display
error_frame = ttk.Frame(root, padding="10")
error_frame.pack(pady=10, padx=20)

ttk.Label(error_frame, text="Error Position:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky='w')
error_position_display = ttk.Entry(error_frame, font=("Helvetica", 12))
error_position_display.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(error_frame, text="Corrected Data:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky='w')
corrected_data_display = ttk.Entry(error_frame, font=("Helvetica", 12))
corrected_data_display.grid(row=1, column=1, padx=5, pady=5)

# Visual Frame for Hamming Code
visual_frame = ttk.Frame(root, padding="10", relief="ridge", borderwidth=2)
visual_frame.pack(pady=10, padx=20)

# Reset Button
reset_button = ttk.Button(root, text="Reset", command=reset_fields, style="Reset.TButton")
reset_button.pack(pady=10)

# Status Bar
status_var = tk.StringVar()
status_bar = ttk.Label(root, textvariable=status_var, relief="sunken", anchor="w", font=("Helvetica", 10))
status_bar.pack(side="bottom", fill="x", padx=10, pady=5)
status_var.set("Ready")

# Customizing styles
style.configure('Accent.TButton', foreground='white', background='#4CAF50', font=("Helvetica", 10, "bold"))
style.map('Accent.TButton', foreground=[('active', '!disabled', 'black')])
style.configure('Reset.TButton', foreground='white', background='#000000', font=("Helvetica", 10, "bold"))

# Running the main loop
root.mainloop()