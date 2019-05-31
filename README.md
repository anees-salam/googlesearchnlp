BACKGROUND: This is a project that  I am currently working. My idea behind the project was to extract names of professors from different colleges using web scraping and Name Entity Recognition.

PROBLEM STATEMENT: I have a list of google search keywords stored in a text file in a directory. The program should read each keyword and get html page for top 3 google search url. Name,phone number and emails from html should be extracted and saved in a text file.


DATA:  Input data for module 1 in github code is a text file with few google search keywords specified line by line. 


APPROACH:I divide the problem into 5 modules.First the text file is read and saved as a table in hbase. Secondly 3 url for each keyword is downloaded using google search api and saved as  columns in hbase table. In 3rd module html files for corresponding urls are downloaded. In module 4 text from html is scraped and saved using pyspark . In module 5 NER is applied to text and name,phone number and email are saved.


SOLUTION:  Problem is solved using hbase,pyspark and NER. Hbase thrift server should be running for modules 1,2 and 3. Each python code should be executed sequentially to get the output. Output of module 1 and module 2 are stored in hbase. After execution of module 2, an hbase table is formed with keyword and url. In module 3 hbase table is read and corresponding html pages are downloaded using beautifulsoup and urllib. l

These html files are read in module 4 and all html child tags with text are saved into a text file using beautiful soup recursive child generator. Output is saved by parallelizing the array and saving as textfile in pyspark. 


In module 5 name entity is filtered from parsed text from html files and saved to another text file using Stanford Name Entity Recognition algorithm. 


Repo link : https://github.com/anees-salam/googlesearchnlp



RESULT: Faculty names, phone number and email address from html pages of different colleges are extracted. Sample output is given below. This method can be used to filter name entity from webpages for any google search keywords. Only change to make is add new keywords to the initial data text file


