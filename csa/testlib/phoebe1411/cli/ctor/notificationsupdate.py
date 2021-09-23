import clictorbase


class notificationsupdate(clictorbase.IafCliConfiguratorBase):
    def __call__(self, force=False):
        cmd = 'notificationsupdate'
        if force:
            cmd += ' force'
        self._sess.writeln(cmd)
        return self._read_until()