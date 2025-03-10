import os
import pyttsx3
from gtts import gTTS
import tkinter as tk
from tkinter import messagebox

# Function for gTTS (Online)
def text_to_speech_gtts(text):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        os.system("start output.mp3")  # For Windows
    except Exception as e:
        messagebox.showerror("Error", f"gTTS failed: {str(e)}")

# Function for pyttsx3 (Offline)
def text_to_speech_pyttsx3(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", f"pyttsx3 failed: {str(e)}")

# Function to speak a welcome message when the app starts
def welcome_message():
    try:
        engine = pyttsx3.init()
        engine.say("Welcome to the Text to Speech app. Please enter some text and choose a mode to proceed.")
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", f"pyttsx3 failed: {str(e)}")

# Function to simulate typing text into the text box
def type_welcome_message(text_box, message, index=0):
    if index < len(message):
        text_box.insert(tk.END, message[index])  # Insert one character at a time
        text_box.after(100, type_welcome_message, text_box, message, index + 1)  # 100 ms delay between each character
    else:
        text_box.after(2000, lambda: text_box.delete("1.0", tk.END))  # Clear after 2 seconds

# GUI Application
def create_gui_app():
    # Function triggered by button press
    def speak():
        text = text_box.get("1.0", tk.END).strip()  # Fetch text from Text widget
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return
        choice = engine_var.get()
        if choice == "Online (gTTS)":
            text_to_speech_gtts(text)
        elif choice == "Offline (pyttsx3)":
            text_to_speech_pyttsx3(text)

    # Function to change button style on hover
    def on_enter(e):
        button.config(bg="lightblue", fg="black")

    def on_leave(e):
        button.config(bg="blue", fg="white")

    # Create window
    root = tk.Tk()
    root.title("Text to Speech App")

    # Add widgets
    tk.Label(root, text="Text to Speech Converter", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(root, text="Enter Text Below:", font=("Arial", 12)).pack(pady=10)
    
    # Use Text widget for multi-line input and set font to Courier (monospaced/robotic)
    text_box = tk.Text(root, height=10, width=50, font=("Courier", 12))  # Robotic feel
    text_box.pack(pady=10)
    
    tk.Label(root, text="Choose Mode:", font=("Arial", 12)).pack(pady=10)
    
    engine_var = tk.StringVar(value="Online (gTTS)")
    gtts_radio = tk.Radiobutton(root, text="Speak (Online Mode)", font=("Arial", 10), variable=engine_var, value="Online (gTTS)")
    pyttsx_radio = tk.Radiobutton(root, text="Speak (Offline Mode)", font=("Arial", 10), variable=engine_var, value="Offline (pyttsx3)")
    
    gtts_radio.pack(pady=5)
    pyttsx_radio.pack(pady=5)
    
    button = tk.Button(root, text="Convert to Speech", font=("Arial", 12, "bold"), command=speak, bg="blue", fg="white")
    button.pack(pady=20)

    # Bind hover effects to the button
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    # Simulate typing the welcome message into the text box and clear it afterward
    welcome_text = "Welcome to the Text to Speech app. Please enter some text and choose a mode to proceed."
    type_welcome_message(text_box, welcome_text)

    # Schedule the welcome speech after the window is opened
    root.after(500, welcome_message)  # 500ms delay to allow the window to render

    # Start the GUI event loop
    root.mainloop()

# Driver code: Running the GUI version
create_gui_app()
