import pathlib
from smtplib import SMTP
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    """The Mail class."""

    def __init__(self, sender: str, password: str):
        self._sender: str = sender
        self._password: str = password
        self._receiver: str = None
        self._message: MIMEMultipart = None

    def add_message(self, receiver: str, subject: str, body: str) -> None:
        """Add a message object to the payload."""
        self._receiver = receiver
        self._message = MIMEMultipart()
        self._message["From"] = self._sender
        self._message["To"] = self._receiver
        self._message["Subject"] = subject
        self._message.attach(MIMEText(body, "plain"))

    def add_attachment(self, attachment: pathlib.Path) -> None:
        """Add an attachment object to the payload."""
        if not isinstance(self._message, MIMEMultipart):
            self._message = MIMEMultipart()
        with attachment.open("rb") as reader:
            attach: MIMEBase = MIMEBase("application", "octet-stream")
            attach.set_payload(reader.read())
        encoders.encode_base64(attach)
        attach.add_header(
            "Content-Disposition", f"attachment; filename={attachment.name}"
        )
        self._message.attach(attach)

    def send(self, smtp: SMTP) -> None:
        """Send the payload(s)."""
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self._sender, self._password)
        smtp.sendmail(self._sender, self._receiver, self._message.as_string())
