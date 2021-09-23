# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/failover_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
from common.cli.clicommon import CliKeywordBase, DEFAULT

class FailoverConfig(CliKeywordBase):
    """
    """
    def get_keyword_names(self):
        keywords = [
            'failover_config_add',
            'failover_config_delete',
            'failover_config_edit',
            'failover_config_preemptive_enable',
            'failover_config_preemptive_disable',
            'failover_config_test',
            'failover_config_batch_add',
            'failover_config_batch_delete',
            'failover_config_batch_edit',
            'failover_config_batch_preemptive',
            'failover_config_batch_test',
        ]
        return keywords

    def failover_config_add(self,
        groupid,
        hostname,
        ip,
        interface=DEFAULT,
        priority=DEFAULT,
        interval=DEFAULT,
        enable=DEFAULT,
        passphrase=DEFAULT,
        passphrase_confirm=DEFAULT,
        description=DEFAULT,
        ):
        """Add failover entry

        Parameters:
        - `groupid': Failover group ID
        - `hostname': Hostname
        - `ip': Virtual IPv4 or IPv6 address and netmask(Ex: 192.168.1.2/24)
        - `interface': Name or number of interface
        - `priority': Priority
        - `interval': Advertisement interval
        - `enable': Enable this failover group? Y or N
        - `passphrase': Passphrase for message authentication
        - `passphrase_confirm': Re-enter Passphrase for message authentication
        - `description': Failover group description

        Examples:
        | Failover Config Add |
        | ... | 123 |
        | ... | a.host |
        | ... | 192.168.1.2/24 |
        | ... | interface=Autoselect |
        | ... | priority=3 |
        | ... | interval=12 |
        | ... | enable = Y |
        | ... | passphrase=HelloWorld |
        | ... | passphrase_confirm=HelloWorld |
        | ... | description=some description |
        """
        fc = self._cli.failoverconfig()
        return fc.new(groupid=groupid,
            hostname=hostname,
            ip=ip,
            interface=interface,
            priority=priority,
            interval=interval,
            enable=enable,
            passphrase=passphrase,
            passphrase_confirm=passphrase_confirm,
            description=description,
        )

    def failover_config_edit(self,
        groupid,
        new_groupid=DEFAULT,
        hostname=DEFAULT,
        ip=DEFAULT,
        interface=DEFAULT,
        priority=DEFAULT,
        interval=DEFAULT,
        enable=DEFAULT,
        passphrase=DEFAULT,
        passphrase_confirm=DEFAULT,
        description=DEFAULT,
        ):
        """Edit failover entry

        Parameters:
        - `groupid': Failover group ID
        - `new_groupid': Failover group ID if changed
        - `hostname': Hostname
        - `ip': Virtual IPv4 or IPv6 address and netmask(Ex: 192.168.1.2/24)
        - `interface': Name or number of interface
        - `priority': Priority
        - `interval': Advertisement interval
        - `enable': Enable this failover group? Y or N
        - `passphrase': Passphrase for message authentication
        - `passphrase_confirm': Re-enter Passphrase for message authentication
        - `description': Failover group description

        Examples:
        | Failover Config Edit |
        | ... | 123 |
        | ... | hostname=another.host |
        | ... | ip=192.168.1.2/24 |
        | ... | interface=Autoselect |
        | ... | priority=3 |
        | ... | interval=12 |
        | ... | enable = Y |
        | ... | passphrase=HelloWorld |
        | ... | passphrase_confirm=HelloWorld |
        | ... | description=some description |
        """
        fc = self._cli.failoverconfig()
        return fc.edit(groupid=groupid,
            new_groupid=new_groupid,
            hostname=hostname,
            ip=ip,
            interface=interface,
            priority=priority,
            interval=interval,
            enable=enable,
            passphrase=passphrase,
            passphrase_confirm=passphrase_confirm,
            description=description,
        )

    def failover_config_delete(self, groupid):
        """Delete failover entry

        Parameters:
        - `groupid': Failover group ID
        Examples:
        | Failover Config Delete |
        | ... | 123 |
        """
        return self._cli.failoverconfig().delete(groupid)

    def failover_config_preemptive_enable(self):
        """Enable preemptive for failover config

        Examples:
        | Failover Config Preemptive Enable|
        """
        return self._cli.failoverconfig().preemptive(True)

    def failover_config_preemptive_disable(self):
        """Disable preemptive for failover config

        Examples:
        | Failover Config Preemptive Disable|
        """
        return self._cli.failoverconfig().preemptive(False)

    def failover_config_test(self, groupid=-1, elapse_seconds=10):
        """Test failover group(s)

        Parameters:
        - `groupid': Failover group ID to test. If -1, test all groups
        - `elapse_seconds`: time of testing before clicking ^C
        Examples:
        | Failover Config Test |
        | Failover Config Test | groupid=2 |
        """
        result = self._cli.failoverconfig().test(groupid, elapse_seconds)
        self.restart_cli_session()
        return result

    # BATCH cmds
    def failover_config_batch_add(self,
        groupid,
        hostname,
        ip,
        interface='Autoselect',
        priority='3',
        interval='100',
        enable='1',
        passphrase='ironport',
        description='Empty',
        ):
        """Add failover entry in batch mode

        Parameters:
        - `groupid': Failover group ID
        - `hostname': Hostname
        - `ip': Virtual IPv4 or IPv6 address and netmask(Ex: 192.168.1.2/24)
        - `interface': Name or number of interface
        - `priority': Priority
        - `interval': Advertisement interval
        - `enable': Enable this failover group? 1 or 0
        - `passphrase': Passphrase for message authentication
        - `description': Failover group description

        Examples:
        | Failover Config Add |
        | ... | 123 |
        | ... | a.host |
        | ... | 192.168.1.2/24 |
        | ... | interface=Autoselect |
        | ... | priority=3 |
        | ... | interval=12 |
        | ... | enable = Y |
        | ... | passphrase=HelloWorld |
        | ... | description=some description |
        """
        params = [
            'failoverconfig',
            'new',
            _parameter(groupid),
            _parameter(hostname),
            _parameter(ip),
            _parameter(interface),
            _parameter(description),
            _parameter(enable),
            _parameter(priority),
            _parameter(passphrase),
            _parameter(interval),
        ]
        return self._cli.failoverconfig_batch().execute(' '.join(params))

    def failover_config_batch_edit(self,
        old_groupid,
        new_groupid,
        hostname,
        ip,
        interface='Autoselect',
        priority='3',
        interval='100',
        enable='1',
        passphrase='ironport',
        description='Empty',
        ):
        """Add failover entry in batch mode

        Parameters:
        - `old_groupid': Old failover group ID
        - `new_groupid': New failover group ID
        - `hostname': Hostname
        - `ip': Virtual IPv4 or IPv6 address and netmask(Ex: 192.168.1.2/24)
        - `interface': Name or number of interface
        - `priority': Priority
        - `interval': Advertisement interval
        - `enable': Enable this failover group? 1 or 0
        - `passphrase': Passphrase for message authentication
        - `description': Failover group description

        Examples:
        | Failover Config Batch Edit |
        | ... | 123 |
        | ... | 213 |
        | ... | a.host |
        | ... | 192.168.1.2/24 |
        | ... | interface=Autoselect |
        | ... | priority=3 |
        | ... | interval=12 |
        | ... | enable = Y |
        | ... | passphrase=HelloWorld |
        | ... | description=some description |
        """
        params = [
            'failoverconfig',
            'edit',
            _parameter(old_groupid),
            _parameter(new_groupid),
            _parameter(hostname),
            _parameter(ip),
            _parameter(interface),
            _parameter(description),
            _parameter(enable),
            _parameter(priority),
            _parameter(passphrase),
            _parameter(interval),
        ]
        return self._cli.failoverconfig_batch().execute(' '.join(params))

    def failover_config_batch_delete(self, groupid):
        """Delete failover entry in batch mode

        Parameters:
        - `groupid': Failover group ID
        Examples:
        | Failover Config Batch Delete |
        | ... | 123 |
        """
        params = [
            'failoverconfig',
            'delete',
            _parameter(groupid),
        ]
        return self._cli.failoverconfig_batch().execute(' '.join(params))

    def failover_config_batch_preemptive(self):
        """Switch preemptive for failover config in batch mode

        Examples:
        | Failover Config Batch Preemptive |
        """
        params = [
            'failoverconfig',
            'preemptive',
        ]
        return self._cli.failoverconfig_batch().execute(' '.join(params))

    def failover_config_batch_test(self, groupid=-1, elapse_seconds=10):
        """Test failover group(s) in batch mode

        Parameters:
        - `groupid': Failover group ID to test. If -1, test all groups
        - `elapse_seconds`: time of testing before clicking ^C
        Examples:
        | Failover Config Batch Test |
        | Failover Config Batch Test | groupid=2 |
        """
        result = self._cli.failoverconfig_batch().test(_parameter(groupid), elapse_seconds)
        self.restart_cli_session()
        return result

def _parameter(field):
    """
    Returns field in a "parameter-view":
       stripped from leading and failing spaces
       surrounded with double quotes
    Double quotes in values are not allowed
    """
    result = str(field).strip()
    if result.find('"') > -1:
        raise ValueError('Detected double quote in ' + result)
    if result.find(' ') > -1:
        result = '"' + result + '"'
    return result
