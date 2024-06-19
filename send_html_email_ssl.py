# Simple script used to send an HTML file as an HTML formatted email,
# using Gmail's SMTP service. Used for testing HTML emails.
# The core message-sending code is taken from the docs:
# http://docs.python.org/2/library/email-examples.html
# The code for correctly authenticating against Gmail comes from:
# http://kutuma.blogspot.co.uk/2007/08/sending-emails-via-gmail-with-python.html
import smtplib, logging, os, mimetypes, base64
import argparse
from getpass import getpass
from os.path import basename
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from .proxy_smtp import ProxySMTP

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)


def parse_args():
    """
    Parse script input arguments.

    Returns the parsed args, having validated that the input
    file can be read, and that there is a valid Username.
    """
    parser = get_parser()
    args = parser.parse_args()

    # artificially adding this to args, so that
    # it can be passed around easily
    args.html = open(args.html_filename).read()

    # we have to have a valid Gmail account in order to access the SMTP service
    #if args.username is None:
    #    args.username = raw_input('Gmail username: ')
    print_args(args)
    return args


def get_parser():
    """ Return the parser used to interpret the script arguments."""
    usage = (
        "Script to send an HTML file as an HTML email."
        "\nExamples:"
        "\n1. Send the contents of test_file.html to fred"
        "\n$ send_html_email.py fred@example.com test_file.html"
        "\n"
        "\n2. Send the mail to both fred and bob"
        "\n$ send_html_email.py fred@example.com bob@example.com test_file.html"
        "\n"
        "\n3. Use fred123@gmail.com as the Gmail authenticating account"
        "\n$ send_html_email.py fred@example.com test_file.html -u fred123@gmail.com"
        "\n"
        "\n4. Override the default test mail subject line"
        "\n$ send_html_email.py fred@example.com test_file.html -t 'Test email'"
        "\n"
        "\n5. Turn on SMTP debugging"
        "\n$ send_html_email.py fred@example.com test_file.html -d"
        "\n6. Attache a file"
        "\n$ send_html_email.py fred@example.com test_file.html -f file_example.gz"
    )
    epilog = "This will send SMPT emails with no user name or password"

    parser = argparse.ArgumentParser(description=usage, epilog=epilog,
        # maintains raw formatting, instead of wrapping lines automatically
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('recipients', help='The recipient email addresses (space delimited)', nargs='+')
    parser.add_argument('html_filename', help='The HTML file to use as the email body content')
    parser.add_argument('-s', '--sender',
        help='The sender email address (defaults to <do-not-reply@example.com>)',
        default='do-not-reply@example.com'
    )
    parser.add_argument('-u', '--username',
        help=('A valid Gmail user account (used to authenticate against Google\'s SMTP service). '
            'If this argument is not supplied, the user will be prompted to type it in.')
    )
    parser.add_argument('-t', '--title',
        help='The test email subject line (defaults to "Test email")',
        default="Test email"
    )
    parser.add_argument('-p', '--plain',
        help=('The test email plain text content. This script is designed primarily for the '
            'testing of HTML emails, so this text is really just a placeholder, for completeness. '
            'The default is "This is a test email (plain text)."'),
        default="This is a test email (plain text)"
    )
    parser.add_argument('-d', '--debug', action='store_true',
        help=('Use this option to turn on DEBUG for the SMTP server interaction.')
    )
    parser.add_argument('-f', '--files',
        help=('Use this option to attach files to the email. Use a , to seperate files')
    )
    parser.add_argument('-x', '--password',
        help=('Use this option to attach files to the email. Use a , to seperate files')
    )
    parser.add_argument('-o', '--port',
        help=('Use this specifies the port to send the email on'),
        default="465"
    )
    parser.add_argument('-k', '--host',
        help=('Use this specifies the smtp host to use'),
        default="smtp.gmail.com"
    )
    return parser


def print_args(args):
    """Print out the input arguments."""
    print('Sending test email to: %s' % args.recipients)
    print('Sending test email from: %s' % args.sender)


def create_message(args):
    """ Create the email message container from the input args."""
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = args.title
    msg['From'] = args.sender
    msg['To'] = ','.join(args.recipients)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(args.plain, 'plain')
    part2 = MIMEText(args.html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # attach files to an existing msg object
    attach_files = []

    if (args.files != None):
        attach_files = args.files.split(',')

    for f in attach_files or []:
        logging.debug( "Adding %s to email.",f)
        try:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
        except IOError as e:
            logging.error("IO error on %s", e)

    return msg

def send_email(args,use_proxy,proxy_host,proxy_port):
    """ Args: recipients (space delimeted), html_filename, title, plain, debug, files, username, password, port, host
    """
    msg = create_message(args)

    try:
        logging.debug("sending email %s:%s",args.host,args.port)
        logging.debug("args = %s",args)
        logging.debug("debug = %s",args.debug)
        if use_proxy: 
            logging.debug("(proxy) proxy %s:%s",proxy_host,proxy_port)
            smtpserver = ProxySMTP(host=args.host, port=args.port,
                            p_address=proxy_host, p_port=proxy_port)
        else:
            smtpserver = smtplib.SMTP_SSL(args.host, int(args.port))
        logging.debug("debug = %s",args.debug)
        smtpserver.set_debuglevel(args.debug)
        smtpserver.ehlo()
        #smtpserver.starttls()
        #smtpserver.ehlo
        # getpass() prompts the user for their password (so it never appears in plain text)
        #logging.debug("user = %s, pass = %s",args.username, args.password)
        smtpserver.login(args.username, args.password)
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        logging.debug("sendmail, sender = %s, recipients = %s, msg = %s",args.sender, args.recipients, msg.as_string())
        smtpserver.sendmail(args.sender, args.recipients, msg.as_string())
        logging.info("Message sent to '%s'.",args.recipients)
        smtpserver.quit()
    except smtplib.SMTPAuthenticationError as e:
        logging.info("Unable to send message: %s",e)

def create_send_grid_message(args):
    """ Create the email message for send grid from the input args."""
    
    message = Mail(
        from_email=args.sender,
        to_emails=args.recipients,
        subject=args.title,
        html_content=args.html)

    # attach files to an existing msg object
    attach_files = []

    if (args.files != None):
        attach_files = args.files.split(',')


    for f in attach_files or []:
        logging.debug( "Adding %s to email.",f)
        try:
            with open(f, "rb") as fil:
                encoded_string = base64.b64encode(fil.read()).decode()
                fil.close()
            
            tmp = mimetypes.guess_type(f); mime_type = tmp[0] if tmp else ""

            message.attachment = Attachment(
                file_content=FileContent(encoded_string),
                file_name=FileName(basename(f)),
                file_type=FileType(mime_type),
                disposition=Disposition("attachment")
            )
        except IOError as e:
            logging.error("IO error on %s", e)

    return message

def send_email_sendgrid(args):
    logging.info("sending send grid email to: %s",args.recipients)
    logging.debug("debug = %s",args.debug)
    logging.debug("args = %s",args)

    message = create_send_grid_message(args)
    # logging.debug('sendgrid message: %s', message)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API'))
        response = sg.send(message)
        logging.debug(response.status_code)
        logging.debug(response.body)
        logging.debug(response.headers)
    except Exception as e:
        logging.info("Unable to send message: %s",e)

def send_email_gmail(args):
    logging.info("sending gmail email to: %s",args.recipients)
    logging.debug("debug = %s",args.debug)
    logging.debug("args = %s",args)

    CRED_LOCATION = '/home/genesys/.gmail/credentials.json'
    TOKEN_LOCATION = '/home/genesys/.gmail/token.json'

    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    message = create_gmail_message(args)

    if os.path.exists(TOKEN_LOCATION):
        creds = Credentials.from_authorized_user_file(TOKEN_LOCATION, SCOPES)
    # If there are no (valid) credentials available, try to refresh
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save the credentials for the next run
            with open(TOKEN_LOCATION, 'w') as token:
                token.write(creds.to_json())
        else:
            logging.error("Need to regenerate gmail token file.. see test_send_gmail.py")
        

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)
    
        send_message = (service.users().messages().send
                        (userId="me", body=message).execute())
        logging.info("gmail sent message id: %s", send_message["id"])
        logging.debug("gmail sent message: %s", send_message)
       
        
    except HttpError as error:
        logging.error('An error occurred sending email via gmail: %s',error)
        send_message = None
    return send_message

def create_gmail_message(args):
    """ Create the email message for gmail from the input args."""

    mime_message = EmailMessage()

    # headers
    mime_message['To'] = args.recipients
    mime_message['From'] = args.sender
    mime_message['Subject'] = args.title
    # text
    if args.html:
        mime_message.set_content(args.html, subtype='html')
    elif args.plain:
        mime_message.set_content(args.plain)

    # attach files to an existing msg object
    attach_files = []

    if (args.files != None):
        attach_files = args.files.split(',')

    for f in attach_files or []:
        logging.debug( "Adding %s to email.",f)
        try:
            type_subtype, _ = mimetypes.guess_type(f)
            maintype, subtype = type_subtype.split('/')
            filename=basename(f)
            with open(f, "rb") as fp:
                attachment_data = fp.read()
            
            tmp = mimetypes.guess_type(f); mime_type = tmp[0] if tmp else ""
            mime_message.add_attachment(attachment_data, maintype, subtype, filename=filename)
            
        except IOError as e:
            logging.error("IO error on %s", e)
    
    encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    message = {
        'raw': encoded_message
    }
    return message


def setup_console_logging():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)


def main():
    setup_console_logging()
    args = parse_args()
    send_email(args)
    

if __name__ == "__main__":
    main()
