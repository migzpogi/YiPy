# YiPy

`Updated: Oct 20 2017`

This project gets the most recent movie uploads from YTS via RSS feed. Of course, you could just subscribe using that but where's the fun in that?

## Getting Started

### Prerequisites

* Python 2.7 or 3
* An internet connection to get the RSS feed
* A GMail account to send the email notification

### Configuration

1. Open the `settings.ini` file located in the config folder.
2. Specify your Gmail **username** and **password**. I highly recommend using [Google App Passwords](https://security.google.com/settings/security/apppasswords) to generate randomized passwords for your account.
3. Put your Gmail address in the **from** and **to** section. 
4. Change the email subject if you wish to.

Your `settings.ini` file should look something like:

```ini
[smtp]
username=john_star
password=ABC123def246

[email]
from=john_star@gmail.com
to=john_star@gmail.com
subject=YiPy Updates
```

### Running

Just run the `YiPyMain.py` file and you should be receiving an email notification about YTS's recently uploaded movies.

## About

I made this project just to practice my Python skills. From reading configurations files to sending emails via SMTP and performing unit tests. 

### Libraries Used

* feedparser - to read the RSS feed
* jinja2 - to format the email notification

```python
def printName(name):
  return name
```

```java
System.out.println("The quick brown fox");
```

