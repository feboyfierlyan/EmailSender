import tkinter as tk 
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
import smtplib
import ssl
import email
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from email.message import EmailMessage
import time
import os
from pathlib import Path

class App(ttk.Frame):
	def __init__(self, parent):
		ttk.Frame.__init__(self)

		for index in [0, 1, 2]:
			self.columnconfigure(index=index, weight=1)
			self.rowconfigure(index=index, weight=1)

		self.radio_frame = ttk.LabelFrame(self, text="Email Pengirim", padding=(20, 10))
		self.radio_frame.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="nsew")

		self.radio_frame2 = ttk.LabelFrame(self, text="Email Penerima", padding=(20, 10))
		self.radio_frame2.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")

		self.radio_frame3 = ttk.LabelFrame(self, text="Subject Email", padding=(20, 10))
		self.radio_frame3.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew")

		self.radio_framepass = ttk.LabelFrame(self, text="Password Email", padding=(20, 10))
		self.radio_framepass.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="nsew")

		global emailpengirim
		global emailpenerima
		global subjectemail
		global passwordemail

		emailpengirim = tk.StringVar()
		emailpenerima = tk.StringVar()
		subjectemail = tk.StringVar()
		passwordemail = tk.StringVar()

		self.entry = ttk.Entry(self.radio_frame, textvariable=emailpengirim)
		self.entry.insert(0, "")
		self.entry.grid(row=0, column=0, padx=5, pady=(20, 10), sticky="ew")

		self.entry2 = ttk.Entry(self.radio_frame2, textvariable=emailpenerima)
		self.entry2.insert(0, "")
		self.entry2.grid(row=0, column=0, padx=5, pady=(20, 10), sticky="ew")

		self.entry3 = ttk.Entry(self.radio_frame3, textvariable=subjectemail)
		self.entry3.insert(0, "")
		self.entry3.grid(row=0, column=0, padx=5, pady=(20, 10), sticky="ew")

		self.entrypass = ttk.Entry(self.radio_framepass, show="*", textvariable=passwordemail)
		self.entrypass.insert(0, "")
		self.entrypass.grid(row=0, column=0, padx=5, pady=(20, 10), sticky="ew")

		self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
		self.widgets_frame.grid(
			row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
		)
		self.widgets_frame.columnconfigure(index=0, weight=1)

		filename = ""

		self.filelabel = ttk.Label(self.widgets_frame, text="File : " + filename)
		self.filelabel.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")

		def carifile():

			global filename

			self.f = fd.askopenfilename(filetypes=[('All files', '*.*')])

			print("[INFO] File Path : " + self.f)
			print("[INFO] File Name : " + os.path.basename(self.f))

			filename = os.path.basename(self.f)

			self.filelabel = ttk.Label(self.widgets_frame, text="‎‎‎‎‎‎                    ")
			self.filelabel.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")

			self.filelabel = ttk.Label(self.widgets_frame, text="File : " + filename)
			self.filelabel.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")

		def startbutton():

			print("[INFO] Email Pengirim : " + emailpengirim.get())
			print("[INFO] Email Penerima : " + emailpenerima.get())
			print("[INFO] Email Subject : " + subjectemail.get())
			print("[INFO] Email Password : " + passwordemail.get())
			print("[INFO] Sending Email...")

			msg = MIMEMultipart()
			msg['From'] = emailpengirim.get()
			msg['To'] = emailpenerima.get()
			msg['Subject'] = subjectemail.get()
			body = ' '
			msg.attach(MIMEText(body))

			normaldirect = self.f

			attachment = open(r'' + normaldirect, "r")

			files = [normaldirect]
			filename = os.path.basename(self.f)

			for file_name in files:
				attachment = open(r'' + normaldirect, "br")
				part = MIMEBase("application", "octet-stream")
				part.set_payload(attachment.read())
				encoders.encode_base64(part)
				part.add_header("Content-Disposition",
				f"attachment; filename= {filename}")
				msg.attach(part)

			msg = msg.as_string()

			mailserver = smtplib.SMTP('smtp.gmail.com',587)
			mailserver.ehlo()
			mailserver.starttls()
			mailserver.ehlo()
			mailserver.login(emailpengirim.get(), passwordemail.get())

			mailserver.sendmail(emailpengirim.get(), emailpenerima.get(), msg)

			mailserver.quit()
			print("[INFO] Done!")

		self.accentbutton = ttk.Button(self.widgets_frame, text="Kirim!", style="Accent.TButton", command=startbutton)
		self.accentbutton.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

		self.filebutton = ttk.Button(self.widgets_frame, text="Cari File", style="Accent.TButton", command=carifile)
		self.filebutton.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")

if __name__ == '__main__':
	root = tk.Tk()
	root.title("Email Sender")

	root.tk.call("source", "sun-valley.tcl")
	root.tk.call("set_theme", "light")

	app = App(root)
	app.pack(fill="both", expand=True)

	root.update()
	root.minsize(root.winfo_width(), root.winfo_height())
	x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
	y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
	root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

	root.mainloop()
