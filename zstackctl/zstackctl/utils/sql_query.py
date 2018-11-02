from shell import ShellCmd


class CtlError(Exception):
    pass


def shell(cmd, is_exception=True):
    return ShellCmd(cmd)(is_exception)

class MySqlCommandLineQuery(object):
    def __init__(self):
        self.user = None
        self.password = None
        self.host = 'localhost'
        self.port = 3306
        self.sql = None
        self.table = None

    def query(self):
        assert self.user, 'user cannot be None'
        assert self.sql, 'sql cannot be None'
        assert self.table, 'table cannot be None'

        sql = "%s\G" % self.sql
        if self.password:
            cmd = '''mysql -u %s -p%s --host %s --port %s -t %s -e "%s"''' % (self.user, self.password, self.host,
                                                                               self.port, self.table, sql)
        else:
            cmd = '''mysql -u %s --host %s --port %s -t %s -e "%s"''' % (self.user, self.host, self.port, self.table, sql)

        output = shell(cmd)
        output = output.strip(' \t\n\r')
        ret = []
        if not output:
            return ret

        current = None
        for l in output.split('\n'):
            if current is None and not l.startswith('*********'):
                raise CtlError('cannot parse mysql output generated by the sql "%s", output:\n%s' % (self.sql, output))

            if l.startswith('*********'):
                if current:
                    ret.append(current)
                current = {}
            else:
                l = l.strip()
                if ":" in l:
                    key, value = l.split(':', 1)
                    current[key.strip()] = value[1:]

        if current:
            ret.append(current)

        return ret