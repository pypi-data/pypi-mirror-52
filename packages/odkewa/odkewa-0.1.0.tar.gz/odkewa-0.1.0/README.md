#ODK FORMS

This project is an application that allows us to generate data-collection forms from an excel spreadsheet.

#How to use.

To start you need an xls file that complies with XLSForm specifications.

First we use xls2json.py to convert our .xls (or .xlsx) file to JSON.

Next we convert it from JSON to HTML using json2html.py.

Now we are ready to run __init__.py to run our Flask application.

#Restrictions 

* field names must comply with the following regular expression:  [a-zA-Z_][a-zA-Z0-9_]*
