"""test_mail_core

Unittests for the mail.core module.
"""
import pathlib

import pytest

from mail import core


@pytest.fixture
def mail() -> core.Mail:
    return core.Mail("alex", "password1")


@pytest.fixture
def attachment(tmp_path: pathlib.Path) -> pathlib.Path:
    attachment_path: pathlib.Path = tmp_path.joinpath("attachment.txt")
    with attachment_path.open("w") as writer:
        writer.write("Here's some attachment data")
    return attachment_path


@pytest.fixture
def smtp(mocker) -> core.SMTP:
    yield mocker.Mock(spec=core.SMTP)


def test_mail_init(mail) -> None:
    """Test mail initialises."""
    assert mail._sender == "alex"
    assert mail._password == "password1"


def test_mail_add_message(mail) -> None:
    mail.add_message("todd", "Sales Reports", "Here are the sales")
    assert mail._message.get("From") == "alex"
    assert mail._message.get("To") == "todd"
    assert mail._message.get("Subject") == "Sales Reports"
    assert mail._receiver == "todd"
    assert mail._message._payload[0]._payload == "Here are the sales"


def test_mail_add_attachment_headers(mail, attachment) -> None:
    mail.add_attachment(attachment)
    expect = [
        ("Content-Type", "application/octet-stream"),
        ("MIME-Version", "1.0"),
        ("Content-Transfer-Encoding", "base64"),
        ("Content-Disposition", "attachment; filename=attachment.txt"),
    ]
    actual = mail._message._payload[0]._headers
    assert actual == expect


def test_mail_add_attachment_payload(mail, attachment) -> None:
    mail.add_attachment(attachment)
    expect = "SGVyZSdzIHNvbWUgYXR0YWNobWVudCBkYXRh\n"
    actual = mail._message._payload[0]._payload
    assert actual == expect


def test_mail_send_invokes_commands(mocker, mail, smtp) -> None:
    mocked_message = mocker.Mock(spec=core.MIMEMultipart)
    mocked_message.as_string.return_value = "this is a message"

    mail._receiver = "todd"
    mail._message = mocked_message

    mail.send(smtp)

    smtp.ehlo.assert_any_call()
    smtp.starttls.assert_any_call()
    smtp.login.assert_any_call("alex", "password1")
    smtp.sendmail.assert_any_call("alex", "todd", "this is a message")
