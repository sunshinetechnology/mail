# Mail
Mail adds support for sending emails.

```pycon
>>> import pathlib
>>> import mail
>>> m = mail.Mail("alex@mail.com", "password1")
>>> m.add_message("todd@mail.com", "Sales Report", "Find attached sales report.")
>>> m.add_attachment(pathlib.Path("path/to/sales_report.csv"))
>>> s = mail.SMTP("smtp@mail.com", 25)
>>> m.send(s)
>>> s.close()
```

## Installing Mail
Mail can be installed via pip
```
$ python -m pip install git+https://github.com/sunshinetechnology/mail.git#egg=mail
```
