#!/usr/bin/env python

from common.util.utilcommon import UtilCommon
import sal.clients.smtpspam as smtpspam
import common.util.connectioncache as connectioncache


# TODO: SmtpSpamMult yet to be implemented.

class SmtpSpam(UtilCommon):
    """
    Keywords for working with smtp_spam utility. If multiple smtp_spam utilities
    are running then all keywords from this library depends on the currently
    active instance of smtp_spam.
    """
    _cache = connectioncache.ConnectionCache(no_current_msg= \
                                                 "No started smtp_spam")

    def get_keyword_names(self):
        return [
            'smtp_spam_start',
            'smtp_spam_stop',
            'smtp_spam_wait',
            'smtp_spam_read',
            'smtp_spam_switch_smtp'
        ]

    def smtp_spam_start(self, *args):
        """
        Start SmtpSpam Utility.

        *Parameters*
        You can't provide positional parameters for this keyword.

        - `remote_host=`: Host on which smtp_spam should be run. Default is host
           on which test has been started.
        - `log_dir=`: Directory for smtp_spam logs. If not specified will write
          output to stdout. If specified will also write the logs into the file
          'smtpspam.log' under the specified directory.
        - `mail-from=`: Hostname to insert into the mail from field of each
          message.
        - `mail-from-in-list[=<suffix>]`: The address-list contains send address
          (sender,recipient). (mail-from and mail-from-in-list are mutually
          exclusive).If <suffix> is entered,all of the recipient email addresses
          in the list will have the suffix appended before transit.
        - `num-senders=N`: In order to cycle through many mail froms, a %d needs
          to be inserted into the mail-from option.
          If mail-from=user%d@domain.com and num-senders=5, smtp_spam will cycle
          through the addresses user0@domain.com to user4@domain.com.
        - `rcpt-host-list=`: List of hosts (comma separated) to address mail to.
        - `num-msgs=N`: Number of messages to send. This overrides any other
           option.(Setting this 0 will function like the option was not passed)
        - `msg-size=N`: Size of each message (Default 1024).
        - `msg-filename=N[,N...]`: Filename(s) of message bodies to use.
        - `mbox-filename=N[,N...]`: mbox-format mailbox to use for message
          bodies.
        - `mbox-header=<header_name>:<file_name>`: Use with mbox-filename:
          Replace the <header_name> header in each message with a line from the
          file <file_name>.If <file_name> runs out of lines, it is reopened and
          used again. This option can be used more than once for different
          headers.
        - `cache-mbox=N`:  0 if you don't want to cache mbox messages in memory
          (Default is 1).
        - `concurrency=N`: Number of connections (Default 10)
        - `duration=N`: Number of seconds to run the test (Default 30)
        - `address-list=<file_name>[:suffix]`:  File to get addresses from.
          Test runs until the addresses are exhausted. Append a suffix to all
          addresses by appending a string to the filename with a colon.
        - `delay=N`: Delay.
        - `bandwidth-cap=N`: Simulate limiting bandwith to N bytes per second
          aggregate.
        - `connection-bandwidth-cap=N`: Simulate limiting bandwith to N bytes
          per second per connection.
        - `addr-per-msg=N`: Number of recipients per message. (Default 1).
        - `dot=N`: Messages per dot.
          Messages per dot.
        - `repeat-address-list`: Run through the address list until duration.
        - `debug`:
        - `bind-ips=IP`: Bind to a local IP or IP range.
          (Ex. 1.2-3.4.5-6 yields 1.2.4.5, 1.2.4.6, 1.3.4.5, 1.3.4.6)
        - `port=`: Port to inject to. (Default 25)
        - `inject-host=`: Host to inject to.
        - `max-msgs-per-conn=N`: Maximum number of messages to send over each
          connection. (Default 0 - Infinite)
        - `timeout=N`: Number of seconds to wait for socket I/O. (Default 300).
        - `verbose`: Turn on verbose error output. (Default off)
        - `merge-xmrg`: Use XMRG mail merge protocol.
          Use XMRG mail merge protocol
        - `merge-parts`: Number of XPRT parts per message.
        - `merge-defs`: Number of XDFN keys/replacements per message.
        - `tls`: Send with TLS.
        - `auth-method=<type>`: Use SMTP Auth with method <type> where <type>
          can be PLAIN or LOGIN.
        - `user=<str>`: When using SMTP Auth,this is the user to be
          authenticated.
        - `passwd=<str>`: The password associated with the given user.
        - `smtpauth-file=<str>`: Location of file containing a list of SMTP Auth
          methods, users and passwords where each line looks like:
          <auth-method> <user> <password>.
          For each new connection made by smtp_spam, a new method/user/pass
          combo will be used from the list. smtp_spam will also repeat
          the list as needed.
        - `DUT=<hostname>`: The A/C60 in which to collect queue data from.
        - `queue-target=N,<queue_name>`: The target number of messages that
          smtp_spam should keep in the specified queue.
        - `queue-verbose`: Print out the current queue size (of the targeted
          queue) and the current message delay per connection into the C60.

        *Return*
            Number ID or alias of smtp_spam instance.
            This id is needed by other keywords of this library.

        *Exceptions*
        - `ConfigError`: if provided parameter `response-###=` because it
          haven't been implemented.
        - `KeyError`: if such parameter doesn't exist.
        - `ConfigError`: if keyword can't find location for smtp_spam command.
        - `RuntimeError`: if keyword can't create smtp_spam pidfile.

        *Example*
        | ${smtp1}= | Smtp Spam Start | inject-host=10.1.131.74 |
        | ... | rcpt-host-list=vmw025-bsd03.ibqa | num-msgs=1 |
        | Smtp Spam Start | inject-host=10.1.131.74 | num-msgs=1 |
        | ... | rcpt-host-list=vmw025-bsd03.ibqa | alias=${smtp3} |
        | ... | mbox-filename=${mbox} |
        """
        kwargs = self._parse_args(args)
        arg = {'alias': None, 'smtp_spam_port': None, 'remote_host': None,
               'log_dir': None, 'extra_opts': ''}

        for key in kwargs.keys():
            if key in arg.keys():
                arg[key] = kwargs[key]
                del kwargs[key]

        return self._cache.register(smtpspam.SmtpSpam(
            arg['smtp_spam_port'], arg['remote_host'], arg['log_dir'])
                                    .start(arg['extra_opts'], **kwargs), arg['alias'])

    def smtp_spam_stop(self):
        """
        Stop current smtp_spam by interrupting or force close.This is needed in
        case if user needs to terminate in between execution. This command
        changes curent smtp_spam instance to previous in list. It's strongly
        recomended to change instance of smtp_spam manualy after this keyword.

        *Parameters*
            None

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Smtp Spam Stop |
        """
        self._cache.current.stop()
        self._cache.delete(self._cache.current_index)
        return self._cache.current_index

    def smtp_spam_wait(self, *args):
        """
        Wait for smtp_spam command to finish.

        *Parameters*
        - `timeout`: wait() will for timeout seconds. Arg is ignored if 0.
        - `read_sz`: size of chunk of data to read (in bytes).

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Smtp Spam Wait |
        """
        kwargs = self._parse_args(args)
        arg = {'timeout': 0, 'read_sz': 1024}

        for key in kwargs.keys():
            if key in arg.keys():
                arg[key] = kwargs[key]

        self._cache.current.wait(int(arg['timeout']), int(arg['read_sz']))

    def smtp_spam_read(self, *args):
        """
        Read chunks of 512 bytes at a time

        *Parameters*
        - `timeout`: read data for timeout seconds.
        - `read_sz`: size of chunk of data to read (in bytes).

        *Return*
            Output of the smtp_command command executed

        *Exceptions*
            None.

        *Example*
        | Smtp Spam Read |
        """
        kwargs = self._parse_args(args)
        arg = {'timeout': 30, 'read_sz': 512}

        for key in kwargs.keys():
            if key in arg.keys():
                arg[key] = kwargs[key]

        data_output = self._cache.current.read(int(arg['timeout']),
                                               int(arg['read_sz']))
        return data_output

    def smtp_spam_switch_smtp(self, alias):
        """
        Switch to other smtp_spam instance. All next keywords connected to
        smtp_spam will make impact only to `alias` smtp_spam instance.

        *Parameters*
        - `alias`:  alias or ID of curently runing smtp_spam daemon.

        *Return*
           None.

        *Exceptions*
            None.

        *Example*
        | Smtp Spam Switch Smtp | ${smtp1} |
        """
        self._cache.switch(alias)
