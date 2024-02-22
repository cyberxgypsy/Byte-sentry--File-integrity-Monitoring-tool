import hashlib
import smtplib
from email.message import EmailMessage
from tkinter import Tk, messagebox, Frame, Listbox, Scrollbar
from tkinter.filedialog import askopenfilenames
from threading import Thread
import os
from tkinter import PhotoImage
from PIL import ImageTk, Image
import customtkinter
import tkinter

# Initialize custom tkinter settings
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

def selectFiles():
    Tk().withdraw()
    filePaths = askopenfilenames()
    if len(filePaths) == 0:
        messagebox.showinfo("Error", "No files selected.")
    else:
        fileLabel.configure(text="Files Selected:")  # Use 'configure' instead of 'config'
        fileList.delete(0, "end")
        for filePath in filePaths:
            fileList.insert("end", os.path.basename(filePath))
        startButton.configure(state="normal")  # Use 'configure' instead of 'config'
        global selectedFiles
        selectedFiles = filePaths

def startMonitoring():
    usrEmail = emailEntry.get()
    usrPasswd = passwordEntry.get()
    print("Make sure two-factor authentication is enabled.")

    def getHash(filePath):
        sha256 = hashlib.sha256()
        with open(filePath, 'rb') as file:
            data = file.read()
            sha256.update(data)
            return sha256.hexdigest()

    def sendEmail(modifiedFile, modification):
        message = EmailMessage()
        message.set_content(f"File '{modifiedFile}' has been {modification}")
        message['subject'] = "File Modification Detected"
        message['from'] = usrEmail
        message['to'] = usrEmail

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(usrEmail, usrPasswd)
        server.send_message(message)
        server.quit()

    # Initialize a dictionary to store the last modification time for each file
    last_modified_time = {}

    # Calculate the initial hashes of the files
    baseline = {}
    for filePath in selectedFiles:
        baseline[filePath] = getHash(filePath)
        last_modified_time[filePath] = os.path.getmtime(filePath)
        print(f"[+] Just calculated the baseline hash of file: {os.path.basename(filePath)}")

    print("[+] Monitoring...")

    while True:
        for filePath in selectedFiles:
            check = getHash(filePath)
            current_modified_time = os.path.getmtime(filePath)

            if check != baseline[filePath] and current_modified_time > last_modified_time[filePath]:
                modification = "modified"
                print("[+] File modification detected.")
                print(f"[+] Modified file: {os.path.basename(filePath)}")

                sendEmail(os.path.basename(filePath), modification)
                last_modified_time[filePath] = current_modified_time

# Rest of your code remains unchanged


def startMonitoringThread():
    thread = Thread(target=startMonitoring)
    thread.start()

def closeWindow():
    window.destroy()

# Create the GUI window
window = Tk()
window.title("Byte Sentry")
window.geometry("400x400")

# Load the background image
bg_image = ImageTk.PhotoImage(Image.open("pattern.png"))  # Load the image using ImageTk

# Create a label for the background image
bg_label = customtkinter.CTkLabel(master=window, image=bg_image)  # Use custom frame and label
bg_label.place(relwidth=1, relheight=1)  # Set label size to cover the entire window

# Frame for email and password (replace this with the login frame from code1)
frame = customtkinter.CTkFrame(master=window, width=520, height=560, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text="BYTE SENTRY", font=('Century Gothic', 20))
l2.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)


# Frame for email and password (replace this with the login frame from code1)
frame = customtkinter.CTkFrame(master=window, width=520, height=560, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Email label and entry (replace this with the code from code1)
emailLabel = customtkinter.CTkLabel(master=frame, text="Email:")
emailLabel.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

emailEntry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
emailEntry.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

# Password label and entry (replace this with the code from code1)
passwordLabel = customtkinter.CTkLabel(master=frame, text="App Password:")
passwordLabel.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

passwordEntry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='App Password', show="*")
passwordEntry.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

# File selection button
selectFilesButton = customtkinter.CTkButton(master=frame, text="Select Files", command=selectFiles, corner_radius=6)
selectFilesButton.place(relx=0.5, rely=0.33, anchor=tkinter.CENTER)

# Selected files label
fileLabel = customtkinter.CTkLabel(master=frame, text="")
fileLabel.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

# File list and scrollbar
fileList = Listbox(master=frame, height=5, width=40)
fileList.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

scrollbar = Scrollbar(master=frame)
scrollbar.place(relx=0.7, rely=0.45, anchor=tkinter.CENTER)

fileList.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=fileList.yview)


# Button frame (replace this with the code from code2)
buttonFrame = customtkinter.CTkFrame(master=frame, width=390, height=40, corner_radius=15)
buttonFrame.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

# Start monitoring button (replace this with the code from code2)
startButton = customtkinter.CTkButton(master=buttonFrame, text="Start Monitoring", command=startMonitoringThread, state="disabled", corner_radius=6)
startButton.place(relx=0.3, rely=0.5, anchor=tkinter.CENTER)

# Close button (replace this with the code from code2)
closeButton = customtkinter.CTkButton(master=buttonFrame, text="Close", command=closeWindow, corner_radius=6)
closeButton.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)


window.mainloop()
