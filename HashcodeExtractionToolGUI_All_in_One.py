# Please note that you must first install PyQt5 and fake_useragent(pip install ...) in your Python environment before running this script.

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit
from fake_useragent import UserAgent
import requests
import json
import sys
import re

class App(QWidget):

   def __init__(self):
       super().__init__()
       self.title = 'GDN HET - Hashcode Extraction Tool'
       self.left = 0
       self.top = 0
       self.width = 300
       self.height = 200
       self.initUI()

   def initUI(self):
       self.setWindowTitle(self.title)
       self.setGeometry(self.left, self.top, self.width, self.height)

       self.layout = QVBoxLayout()

       self.url_label = QLabel('Which localized URL would you like to Extract Hashcodes from?')
       self.url_input = QLineEdit()
       self.layout.addWidget(self.url_label)
       self.layout.addWidget(self.url_input)

       self.submit_button1 = QPushButton('Submit')
       self.submit_button1.clicked.connect(self.submit1)
       self.layout.addWidget(self.submit_button1)

       self.input_label = QLabel('Alternatively, Input html source text from EM3:')
       self.input_text = QTextEdit()
       self.layout.addWidget(self.input_label)
       self.layout.addWidget(self.input_text)

       self.submit_button2 = QPushButton('Submit')
       self.submit_button2.clicked.connect(self.submit2)
       self.layout.addWidget(self.submit_button2)

       self.output_label = QLabel('Hashcodes:')
       self.output_text = QTextEdit()
       self.output_text.setReadOnly(True)
       self.layout.addWidget(self.output_label)
       self.layout.addWidget(self.output_text)
       
       # self.projectLink_label = QLabel('Link to Project Strings:')
       # self.projectLink_text = QTextEdit()
       # self.projectLink_text.setReadOnly(True)
       # self.layout.addWidget(self.projectLink_label)
       # self.layout.addWidget(self.projectLink_text)

       self.copy_button = QPushButton('Copy to Clipboard', self)
       self.copy_button.clicked.connect(self.copy_text)
       self.layout.addWidget(self.copy_button)

       self.setLayout(self.layout)

   def submit1(self):
       url = self.url_input.text()

       # Append Editmode 3 parameter to URL
       localizedUrl = url + '?smartling_editmode=3'

       def extract_hash_values_from_url(url):
           # Create a fake user-agent to mimic Chrome
           user_agent = UserAgent().chrome

           # Set headers with the fake user-agent
           headers = {'User-Agent': user_agent}

           # Fetch the HTML content of the webpage
           response = requests.get(url, headers=headers)
           html_content = response.text

           # Use regular expression to find all occurrences of the pattern
           pattern = r'STRING TRANSLATE BEGIN HASH:([a-fA-F0-9]+)'
           hash_values = re.findall(pattern, html_content)
           return hash_values

        # Call the function:
       hash_values = extract_hash_values_from_url(localizedUrl)

      # Print the extracted hash values as a single string with commas
       hash_values_string = ', '.join(hash_values)
       # hash_values_link = '&hashcodes='.join(hash_values)
       self.output(hash_values_string)
       # self.projectLink(hash_values_link)

   def submit2(self):
       input_text = self.input_text.toPlainText()

       def extract_hash_values(text):
          # Use regular expression to find all occurrences of the pattern
          pattern = r'STRING TRANSLATE BEGIN HASH:([a-fA-F0-9]+)'
          hash_values = re.findall(pattern, text)
          return hash_values

        # Call the function:
       hash_values = extract_hash_values(input_text)

      # Print the extracted hash values as a single string with commas
       hash_values_string = ','.join(hash_values)
       # hash_values_link = '&hashcodes='.join(hash_values)
       self.output(hash_values_string)
       # self.projectLink(hash_values_link)

   def copy_text(self):
     # Get the text from the QTextEdit
     text_to_copy = self.output_text.toPlainText()

     # Set the text to the clipboard
     clipboard = QApplication.clipboard()
     clipboard.setText(text_to_copy)

   def output(self, text):
     self.output_text.clear()
     self.output_text.append(text)

   # def projectLink(self, text):
     # self.projectLink_text.clear()
     # self.projectLink_text.append('https://dashboard.smartling.com/app/projects/5f88f80c9/strings/?' + text)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   ex.show()
   sys.exit(app.exec_())
