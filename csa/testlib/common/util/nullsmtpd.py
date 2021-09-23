#!/usr/bin/env python

# $Id: //prod/main/sarf_centos/testlib/common/util/nullsmtpd.py#2 $ $DataTime:$ $Author: saurgup5 $
from common.util.utilcommon import UtilCommon

import sal.servers.nullsmtpd as nullsmtpd
import common.util.connectioncache as connectioncache
import sys

DEFAULT_TIMEOUT = 15


class NullSmtpd(UtilCommon):
    """
    Keywords for working with null_smtpd deamon. All keywords from this library
    depends on currently active instance of null_smtpd, if multiple null_smtrd are
    running.
    """
    _cache = connectioncache.ConnectionCache(no_current_msg="No started drains")

    def get_keyword_names(self):
        return [
            'null_smtpd_start',
            'null_smtpd_stop',
            'null_smtpd_switch_drain',
            'null_smtpd_local_rollover',
            'null_smtpd_next_message',
            'null_smtpd_stop_all',
            'null_smtpd_read'
        ]

    def null_smtpd_start(self, *args):
        """
        Start NullSmtpd daemon.

        *Parameters*
        You can't provide positional parameters fro this keyword.
        All parameters for this keyword is parameter for 'null_smtpd' command.
        Double dash on start of parameter must be omittet. If parameter can
        contain a value then you have to provide it in format
        'parameter_name'='value'. If parameter can't contain value then you have
        to prodive it in format 'parameter'='parameter'.\n
        All parameters can be ommited.
        - `alias`: name or ID wich will be assigned to this instance. This alias
          you need to indiacte wich of null_smtpd proces you mean. String or
          number can be provided. Default value is ${None}.  If ${None}, number
          index will be assigned as alias.
        - `remote_host`: host on wich run null_smtpd. Default is host on which
          test has been started.
        - `port`: Port to bind to. Default 25.
        - `bind_ip`: IP address to bind to. Default is 'localhost'.
        - `log_dir`: directory for logs. Default is '/tmp'.
        - `mbox_log_idx`: file in which all emails will be logged. Log file will
          be created in directory `log_dir`+'/nullsmtpd/' and will be named
          'mbox`mbox_log_idx`.log'.
        - `do_mbox_delete`: delete mbox if it exists. Boolean. Default
          ${True}.
        - `nostats`: Don't collect statistics
        - `oldstats`: Collect memory-hungry timestamp-range stats
        - `grumpy`: Turn on major misbehaviour (4xx/5xx return codes,drop
        connections all over the place, etc.).
        - `zipf=`: Delay response to data command with zipf-distributed times.
        - `sleep=`: Floating point number of seconds to sleep after data
        received. (Default 0.0)
        - `helo-sleep=`: Floating point number of seconds to sleep before
        sending '220 yoyo.god SMTP'. (Default 0.0)
        - `connection-bandwidth-cap=`: Simulate limiting bandwidth to N bytes
        per second per connection
        - `bandwidth-cap=`: Simulate limiting bandwidth to N bytes per second
        aggregate
        - `collect=`: Append all email addresses to the given filename.
        - `drop=`: Drop N percent connections. (Default 0.0)
        - `sleep-domains=`: Use the domains in the given email list to
        compute 1/x^2 delay.
        - `max-message-size=`: Max bytes per message (Default 10485760)
        - `obs-real-world-file=`: Use the given file's per-domain delay data.
        - `chop=`: Comma-separated list of suffixes to remove from
        recipient domain names.
        - `soft_bounce=`: Percent (from 0 to 100) of messages to soft bounce.
        - `hard_bounce=`: Percent (from 0 to 100) of messages to hard bounce.
        - `soft_bounce_rcpt=`: Percent (from 0 to 100) of RCPT commands to soft
        bounce.
        - `hard_bounce_rcpt=`: Percent (from 0 to 100) of RCPT commands to hard
        bounce.
        - `helo=`: Numeric response to give to HELO command
        - `mail=`: Numeric response to give to MAIL command
        - `data=`: Numeric response to give to DATA command
        - `rcpt=`: Numeric response to give to RCPT command
        - `message=`: Numeric response to give for "message received"
        - `set=`: Numeric response to give to RSET command
        - `max-msgs-per-conn`: Close connection with 421 after this many msgs.
        - `tls`: advertise STARTTLS in response to EHLO (implies -e)
        - `tls-required`: STARTTLS must be used before any messages will be accepted
        - `tls-fail`: Cause TLS failure during second EHLO
        - `tls-fail2`: Cause TLS failure during first MAIL FROM
        - `monitor`: enable mail montor system and web interface
        - `offer-smtpauth`: Offer simulated SMTP Auth
        - `offer-plain-only`: With Auth, offer only PLAIN keyword/mechanism
        - `offer-login-only`: With Auth, offer only LOGIN keyword/mechanism
        - `smtpauth-sleep`: Time to delay the before returning the _first_ auth result.
        - `smtpauth-pct-succeed`: Percentage of successful AUTH return codes.
        - `no-ehlo-command`: Disallow the EHLO command
        - `debug`: Print all traffic to stderr\n
        Parameters which contain equal sign ('=') in names  have to be provided
        with values.\n
         --repsonse-### option is not supported.

        *Return*
            Number ID or alias of null_smtpd instance.
            This id is needed by other keywords of this library.

        *Exceptions*
        - `ConfigError`: if provided parameter `response-###=` because it
          haven't been implemented.
        - `KeyError`: if such parameter doesn't exist.
        - `ConfigError`: if keyword can't find location for null_smtpd command.
        - `RuntimeError`: if keyword can't create null_smtpd pidfile or can't
          check if null_smtpd is listened on port.

        *Examples*
        | ${id} | Null Smtpd Start |
        | ${id} | NUll Smtpd Start | port=110 | hard_bounce=100 |
        | ${id} | Null Smtpd Start | remote_host=10.4.0.116 | port=24 |
        | ... | mbox_log_idx=3 | helo=2 | debug=debug |
        """
        kwargs = self._parse_args(args)
        if sys.platform == "linux2" and 'max-msgs-per-conn' in kwargs:
            del kwargs['max-msgs-per-conn']
        arg = {'alias': None, 'port': None, 'bind_ip': None, 'remote_host': None,
               'log_dir': None, 'mbox_log_idx': len(self._cache.get_all_current()),
               'do_mbox_delete': True, 'extra_opts': ''}
        items = kwargs.keys()

        for key in items:
            if key in arg.keys():
                arg[key] = kwargs[key]
                del kwargs[key]

        return self._cache.register(nullsmtpd.NullSmtpd(
            arg['port'], arg['bind_ip'], arg['remote_host'], arg['log_dir'],
            int(arg['mbox_log_idx']),
            arg['do_mbox_delete']).start(arg['extra_opts'], **kwargs),
                                    arg['alias'])

    def null_smtpd_stop(self):
        """
        Stop current null_smtpd daemon.
        This command change curent null_smtpd instance to previous in list.
        It's strongly recomended to change instance of drain manualy after this
        keyword.

        *Parameters*
            None

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | NUll Smtpd Stop |
        """
        self._cache.current.stop()
        self._cache.delete(self._cache.current_index)
        return self._cache.current_index

    def null_smtpd_local_rollover(self):
        """
        Rollover logs of current instance of null_smtpd daemon.

        *Parameters*
            None.

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | NUll Smtpd Local Rollover |
        """
        self._cache.current.local_rollover()

    def null_smtpd_next_message(self, timeout=DEFAULT_TIMEOUT, string=False):
        """
         Read next message from mbox of curent null_smtpd daemon. Is implemented
         only for local host(host on which testcase is running). Message from
         null_smtpd daemons on remote hosts can't be read.

        *Parameters*
        - `timeout`: how long wait for next message. Seconds. Default value is 15
          seconds.
        - `string`: Set to ${True} if you want get message as string. boolean.
          By default ${False}.

        *Return*
          Full text of message with all header as it present in mbox. Or
          Dictionary keys of which represert header fields of email.

        *Exceptions*
        - `NotImplementedError`: if try to read email from remote host.

        *Examples*
        | NUll Smtpd Next Message | timeout=40 | string=${False} |
        | NUll Smtpd Next Message |
        """
        return self._cache.current.next_msg(timeout, string)

    def null_smtpd_switch_drain(self, alias):
        """
        Switch to other null_smtpd instance. All next keywords connected to
        null_smtpd will make impact only to `alias` null_smtpd instance.

        *Parameters*
        - `alias`:  alias or ID of curently runing null_smtpd daemon. You can
          get this value from null_smtpd_start keyword.

        *Return*
           None.

        *Exceptions*
            None.

        *Example*
        | Null Smtpd Switch Drain | my_drain |
        """
        self._cache.switch(alias)

    def null_smtpd_stop_all(self):
        """
         Stop all null_smtpd daemons.

        *Parameters*
            None.

        *Return*
            None.

        *Exceptions*
            None.

        *Example*
        | Null Smtpd Stop All |
        """
        return self._cache.close_all('stop')

    def null_smtpd_read(self, timeout=60):
        """
         Reads the null_smtpd output

        *Parameters*
       - `timeout`: time to wait for read. Default is 60 seconds.

        *Return*
         Returns complete output of null_smtpd command along with SMTP conversations.

        *Exceptions*
         TimeoutError

        *Example*
        | ${output}= | Null Smtpd Read |
        """
        return self._cache.current.read_all(timeout=timeout)
