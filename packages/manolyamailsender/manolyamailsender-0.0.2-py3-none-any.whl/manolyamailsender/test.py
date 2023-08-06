from manolyamailsender.MailMan import GmailMan, OtherServices

"""
This module provides identity or detailed mail address. You can use like this:
gm = GmailMan('ucok.umut', '****', 'ucok.umut')  

This instance targeted one email address.
If you want to send mail to multiple targets:
gm = GmailMan('ucok.umut', '****', 'ucok.ethem', 'ucok.serif')  # you can type like args

You can type detailed address:
gm = GmailMan('ucok.umut@gmail.com', '****', 'ucok.umut@gmail.com', 'ucok.ethem@gmail.com')
If you have duplicated e-mails in your target args, duplicate mail will be sent.


"""
if __name__ == '__main__':
    # gmail test
    # single
    # PASSED.

    # NOTE:
    # PLEASE EDIT BELOW variables:
    source_username = ''  # you can type 'ucok.umut' style or 'ucok.umut@gmail.com' or 'ucok.umut@companydomain.com'
    source_password = ''
    target_username = ''  # you can type 'ucok.umut' style or 'ucok.umut@gmail.com' or 'ucok.umut@companydomain.com'
    target_usernames = ('', '', '')

    gm = GmailMan(source_username, source_password, target_username)
    gm.test_email()

    # multiple
    # PASSED
    gm = GmailMan(source_username, source_password, *target_usernames)
    gm.test_email()

    # single open
    # PASSED
    gm = GmailMan(source_username, source_password, target_username)
    gm.test_email()

    # multiple open
    # PASSED
    gm = GmailMan('ucok.umut@gmail.com', source_password, 'ucok.umut@gmail.com', 'ucok.umut@gmail.com',
                  'eyyuptaskin@gmail.com')
    gm.test_email()

    # hybrid
    # PASSED
    gm = GmailMan('ucok.umut@gmail.com', source_password, 'ucok.umut@gmail.com', 'uucok@uni-yaz.com')
    gm.test_email()

    # different Services
    uni_other = OtherServices
    uni_other.smtp_addr = 'smtp.office365.com:587'
    uni_other_instance = uni_other('uucok@uni-yaz.com', source_password, 'etaskin@gmail.com', 'uucok@uni-yaz.com')
    uni_other_instance.test_email()