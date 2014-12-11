import smtplib

from weppy.extension import Extension

class MailServer:
    """
    Wrapper of SMTP server.
    """

    def __init__(self, debug, host, port):
        """
        debug -- bool that specifies wheter it is a development environment.
        host -- str that specifies the host of the Redis server.
        port -- int that specifies the port of the Redis server.
        """
        self.debug = debug
        self.smtp = smtplib.SMTP(host, port) if debug is False else None

    def send(self, from_addr, to_addrs, msg):
        """
        Sends an e-mail message to at least on address or raises an exception if
        it is not a development environment. Prints an email representation to
        the standard output if it is a development environment.

        from_addr -- str that specifies the sender of the message.
        to_addrs -- str or list that specifies the receivers of the message.
        msg -- str that specifies the message.
        """
        to_addrs = [to_addrs] if isinstance(to_addrs, str) else to_addrs
        if self.debug:
            print('From: %s\nTo: %s\n%s' % (from_addr, to_addrs, msg))
        else:
            self.smtp.sendmail(from_addr, to_addrs, msg)

class MailExtension(Extension):
    """
    Sets a connection to a SMTP server in the app object.
    """

    def __init__(self, debug, host, port, attr_name='mail_server'):
        """
        debug -- bool that specifies wheter it is a development environment.
        host -- str that specifies the host of the Redis server.
        port -- int that specifies the port of the Redis server.
        attr_name -- str that specifies the name of the attribute of the app
                     object in which the connection is set. 'mail_server'
                     by default.
        """
        self.attr_name = attr_name
        self.mail_server = MailServer(debug, host, port)

    def __call__(self, app):
        """
        Sets the connection in the app object.

        app -- WSGIApplication instance.
        """
        setattr(app, self.attr_name, self.mail_server)
