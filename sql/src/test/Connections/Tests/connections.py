import os, time, sys

def remote_server_start(x,s,dbinit):
    port = os.getenv('MAPIPORT')
    srvcmd = '%s --dbname "%s_test1" --dbinit="%s"' % (os.getenv('MSERVER'),os.getenv('TSTDB'),dbinit)
    srvcmd = srvcmd.replace(port,str(int(port)+1))
    sys.stdout.write('\nserver %d%d : "%s"\n' % (x,s, dbinit))
    sys.stderr.write('\nserver %d%d : "%s"\n' % (x,s, dbinit))
    sys.stderr.flush()
    sys.stderr.write('\nremote mserver: "%s"\n' % (srvcmd))
    sys.stdout.flush()
    sys.stderr.flush()
    srv = os.popen(srvcmd, 'w')
    time.sleep(5)                      # give server time to start
    return srv

def server_start(x,s,dbinit):
    port = int(os.getenv('MAPIPORT'))
    srvcmd = '%s --dbname "%s" --dbinit="%s"' % (os.getenv('MSERVER'),os.getenv('TSTDB'),dbinit)
    sys.stdout.write('\nserver %d%d : "%s"\n' % (x,s, dbinit))
    sys.stderr.write('\nserver %d%d : "%s"\n' % (x,s, dbinit))
    sys.stderr.flush()
    sys.stderr.write('\nmserver: "%s"\n' % (srvcmd))
    sys.stdout.flush()
    sys.stderr.flush()
    srv = os.popen(srvcmd, 'w')
    time.sleep(5)                      # give server time to start
    return srv

def server_stop(srv):
    srv.close()

def client_load_file(clt, port, file):
    f = open(file, 'r')
    for line in f:
	line = line.replace('port_num', str(port+1))
	line = line.replace('port_num_5', str(port+2))
	line = line.replace('port_num_6', str(port+3))
        sys.stdout.write('"%s"\n' % (line))
    	sys.stdout.flush()
	clt.write(line)
    


def client(x,s, c, dbinit, lang, file):
    cltcmd = '%s' % os.getenv('%s_CLIENT' % lang)
    sys.stdout.write('\nserver %d%d : "%s", client %d: %s\n' % (x,s,dbinit,c,lang))
    sys.stderr.write('\nserver %d%d : "%s", client %d: %s\n' % (x,s,dbinit,c,lang))
    sys.stderr.flush()
    sys.stderr.write('\nclient%d: "%s"\n' % (x,cltcmd))
    sys.stdout.flush()
    sys.stderr.flush()
    clt = os.popen(cltcmd, 'w')
    port = int(os.getenv('MAPIPORT'))
    client_load_file(clt, port, file)
    clt.close()
    return '%s ' % (lang)


def clients(x,dbinit):
    s = 0
    s += 1; srv = server_start(x,s,dbinit)
    s += 1; remote_srv = remote_server_start(x,s,dbinit)
    c = 0 ; h = ''
    c += 1; h = client(x,s,c,dbinit,'SQL' , '%s/../connections_syntax.sql' % os.getenv('RELSRCDIR'))
    c += 1; h = client(x,s,c,dbinit,'SQL' , '%s/../connections_semantic.sql' % os.getenv('RELSRCDIR'))
    c += 1; h = client(x,s,c,dbinit,'SQL', '%s/../connections_default_values.sql' % os.getenv('RELSRCDIR'))
    server_stop(srv)
    server_stop(remote_srv)

def main():
    x = 0
    x += 1; clients(x,'include sql;')

main()
