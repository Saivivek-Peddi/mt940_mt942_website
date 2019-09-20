MT940 & MT942 Parser
====================

## Description
Dashboard for uploading MT940 or MT942 messages and convert them in Excel.

File Upload Script which built on Python Flask and [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/) with multiple file selection, drag&amp;drop support, progress bars.


## Setup
- Create virtual enviroment (use `virtualenv`) and activate it.

- Then install python packages:  
```
$ pip install -r requirements.txt
```

- Go to site-packages and replace mt940 folder with mt940 from the repository.


- Run it:

```
$ python app.py
```

- Go to http://localhost:5000

If the regex didn't work for your case. Change the reg-exp, pertaining to your case, in mt940/parser.py.
Here it's:
```
{1:[^<>]*?-}
```
Finds between splits each transaction between {1: and -}. In your case it can be between {1: and }{5:

Frontend-Credits: https://github.com/ngoduykhanh/flask-file-uploader

Lib-Credits: https://github.com/WoLpH/mt940
