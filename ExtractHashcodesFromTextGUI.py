# Please note that you must first install PyQt5 and fake_useragent(pip install ...) in your Python environment before running this script.

# Import necessary modules
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from fake_useragent import UserAgent
import requests
import sys
import re

# Define the main application class
class App(QWidget):

   # Constructor to initialize the application window
   def __init__(self):
       super().__init__()

       # Set initial parameters for the application window
       self.title = 'GDN HET - Hashcode Extraction Tool'
       self.left = 0
       self.top = 0
       self.width = 300
       self.height = 200
       self.initUI()

   # Method to set up the UI components
   def initUI(self):
       self.setWindowTitle(self.title)
       self.setGeometry(self.left, self.top, self.width, self.height)

       # Create a vertical layout to organize UI elements
       self.layout = QVBoxLayout()

       # Input text section
       self.input_label = QLabel('Input text:')
       self.input_text = QTextEdit()
       self.layout.addWidget(self.input_label)
       self.layout.addWidget(self.input_text)

       # Submit button for input text
       self.submit_button = QPushButton('Submit')
       self.submit_button.clicked.connect(self.submit)
       self.layout.addWidget(self.submit_button)

       # Output section
       self.output_label = QLabel('Hashcodes:')
       self.output_text = QTextEdit()
       self.output_text.setReadOnly(True)
       self.layout.addWidget(self.output_label)
       self.layout.addWidget(self.output_text)

       # Copy to Clipboard button
       self.copy_button = QPushButton('Copy to Clipboard', self)
       self.copy_button.clicked.connect(self.copy_text)
       self.layout.addWidget(self.copy_button)

       # Set the layout for the application window
       self.setLayout(self.layout)

   # Method to handle input text and extract hashcodes
   def submit(self):
       input_text = self.input_text.toPlainText()

       # Define a function to extract hash values from text
       def extract_hash_values(text):
          # Use regular expression to find all occurrences of the pattern
          pattern = r'STRING TRANSLATE BEGIN HASH:([a-fA-F0-9]+)'
          hash_values = re.findall(pattern, text)
          return hash_values

        # Call the function to extract hash values from the input text
       hash_values = extract_hash_values(input_text)

      # Print the extracted hash values as a single string with commas
       hash_values_string = ','.join(hash_values)
       # hash_values_link = '&hashcodes='.join(hash_values)
       self.output(hash_values_string)
       # self.projectLink(hash_values_link)

   # Method to copy text to the clipboard
   def copy_text(self):
     # Get the text from the QTextEdit
     text_to_copy = self.output_text.toPlainText()

     # Set the text to the clipboard
     clipboard = QApplication.clipboard()
     clipboard.setText(text_to_copy)

   # Method to display output text in the QTextEdit
   def output(self, text):
     self.output_text.clear()
     self.output_text.append(text)

# Run the application if this script is the main entry point
if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   ex.show()
   sys.exit(app.exec_())
