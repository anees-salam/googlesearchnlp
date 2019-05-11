# googlesearchnlp
Name entity recognition of html scraped from google search.This project is divided into 5 modules.


#MODULE 1
Project uses multiple text file as input and writes the keywords present into a hbase table


In module 2 ,using google search api, first 3 url of google search of each keyword is also added into hbase table.
In module 3 each url of the keyword is scraped from internet using urllib and beautiful soup and saved as html file
In  module 4, html file is opened and all the text in the child tags are written as text file using pyspark
In module 5, text file with scraped text from html is passed into a stanford Name Entity Recognition algorithm and output is saved as text file

In the output nam,phone number and email contained in html is seperated


