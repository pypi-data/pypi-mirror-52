# All module is based on SMTP
# Python 2 supported.
import smtplib


from email.mime.text import MIMEText


class _Base:
    smtp_addr = None

    def __init__(self, username, password, *target_addrs):
        self.identity = None

        self._username, self._password = username, password
        self._target_addrs = target_addrs

        self.__username_mail_difference()
        self._smtp_object = self._create_smtp_object()
        self.connect()

    def __username_mail_difference(self):
        if '@' in self._username:
            self.identity = False

        else:
            self.identity = True

    def _create_smtp_object(self):
        return smtplib.SMTP(self.get_smtp_addr())

    def connect(self):
        self._smtp_object.ehlo()
        self._smtp_object.starttls()
        con = self._smtp_object.login(self._username, self._password)
        if con[0] == 235:  # succeeded code
            print ("Connection succeeded !")

        else:
            print ("A problem may be raised while attempting connection ?")

    def send(self, msg_object, source, target):
        try:
            self._smtp_object.sendmail(source, [i for i in target.split(";")], msg_object.as_string())
        except Exception as err:
            raise Exception("An error raised while sending the mail. Error : \n"
                            "{}".format(err))

    def create_mime_object(self, text, subject=None):
        msg = MIMEText(text)
        msg['Subject'] = subject

        if self.identity:
            msg['From'] = self._username + "@gmail.com"
        else:
            msg['From'] = self._username

        return msg

    def prepare_email(self, text, subject=None):
        msg = self.create_mime_object(text, subject)
        smtp_brand = self.get_smtp_brand()

        if len(self._target_addrs) == 1:
            if self.identity:
                msg['To'] = "{}@{}.com".format(self._target_addrs[0], smtp_brand)
            else:
                msg['To'] = self._target_addrs[0]

        else:
            if self.identity:
                msg['To'] = ";".join("{}@{}.com".format(i, smtp_brand) for i in self._target_addrs)

            else:

                msg['To'] = ";".join("{}".format(i) for i in self._target_addrs)

        return msg

    def _quit_server(self):
        self._smtp_object.quit()

    @classmethod
    def get_smtp_addr(cls):
        if cls.smtp_addr is None:
            raise ValueError('Please provide smtp class property. Maybe you initialize this class before fill it. '
                             'If you use different named providers, please create class, fill smpt then initialize !')

        return cls.smtp_addr

    @classmethod
    def get_smtp_brand(cls):
        addr = cls.smtp_addr
        try:
            # this is base smtp address syntax
            return addr.split(".")[1]

        except Exception:
            raise Exception("An error raised while parsing SMTP address. Please check it !")

    @staticmethod
    def read_file(filepath):
        with open(filepath) as fp:
            try:
                msg = MIMEText(fp.read())
                return msg

            except IOError:
                raise IOError("{} file cannot be accessed".format(filepath))

            except Exception as err:
                raise Exception("Unknown error raised: {}".format(err))

            finally:
                fp.close()


class GmailMan(_Base):
    smtp_addr = 'smtp.gmail.com:587'

    def __init__(self, username, password, *target_addrs):
        self.tls_port = 587
        self.ssl_port = 465

        _Base.__init__(self, username, password, *target_addrs)

    def test_email(self):
        msg = self.prepare_email("test email !")
        source = msg._headers[4][-1]
        target = msg._headers[5][-1]

        try:
            self.send(msg, source, target)

        except Exception as err:
            print ("Test failed !. \n"
                   "Hata : {}", err)
        finally:
            self._quit_server()


class UniyazMan(_Base):
    smtp_addr = 'smtp.office365.com:587'

    def __init__(self, username, password, *target_addrs):
        _Base.__init__(self, username, password, *target_addrs)

    def test_email(self):
        msg = self.prepare_email("test email !")
        source = msg._headers[4][-1]
        target = msg._headers[5][-1]

        self.send(msg, source, target)
        self._quit_server()


class OtherServices(_Base):
    smtp_addr = None

    def __init__(self, username, password, *target_addrs):
        _Base.__init__(self, username, password, *target_addrs)

    def test_email(self):
        msg = self.prepare_email("test email !")
        source = msg._headers[4][-1]
        target = msg._headers[5][-1]

        self.send(msg, source, target)
        self._quit_server()
