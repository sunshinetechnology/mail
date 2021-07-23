"""
Mail adds support for sending emails.
Usage:

    >>> import pathlib
    >>> import mail
    >>> m = mail.Mail("alex@mail.com", "password1")
    >>> m.add_message("todd@mail.com", "Sales Report", "Find attached sales report.")
    >>> m.add_attachment(pathlib.Path("path/to/sales_report.csv"))
    >>> s = mail.SMTP("smtp@mail.com", 25)
    >>> m.send(s)
    >>> s.close()

See `help(mail.Mail)` and `help(mail.SMTP)` for more details.
"""
from mail.core import Mail, SMTP

__version__: str = "0.1.0"
