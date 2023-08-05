**mailcomposer** aims to provide a simple, cross-platform interface for composing emails through an external application like Microsoft Outlook. Some reasons you might use it are:

* You're behind a corporate firewall, and are only able to send email using Outlook.
* You don't have an SMTP server, or don't want the hassle of using `smtplib`.
* You just prefer your desktop email client.

Here's how easy it is to use:

```python
# This automatically selects an appropriate email application
from mailcomposer import MailComposer
mc = MailComposer()

# Set some message headers
mc.to = "nobody@example.com"
mc.subject = "Testing mailcomposer"

# Set the message body
mc.body = "This is a demonstration of the mailcomposer package."

# Attach this README file
mc.attach_file("README.md")

# Display the message in your email application
mc.display()
```

The mailcomposer module can also be called as a script from the command line. When used this way, it provides an interface similar to the Unix `mail` utility. For more information, try `python -m mailcomposer --help`.


## Features

Notable features include:

* Straightforward API
* Cross-platform
* Runs on both Python 2 and 3
* Uses your desktop email client; no SMTP server required
* To, CC, and BCC fields accept single recipients or Python lists
* Messages can be composed in either plain-text or HTML format
* Attachments are easy -- just pass the filename


## Supported Email Applications

Supported email applications currently include:

* Microsoft Outlook (Windows only; requires [pywin32](https://pypi.org/project/pywin32/))
* Mozilla Thunderbird

On Unix systems, mailcomposer can also access other email applications via the `xdg-email` utility from [xdg-utils](https://freedesktop.org/wiki/Software/xdg-utils/). However, some features like setting the body format are not supported using `xdg-email`.
