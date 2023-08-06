import os
import sys
import argparse
import getpass
import shutil

import paramiko
import scp


def main():
    parser = argparse.ArgumentParser(description='csv2graph2web copy to the web server')

    parser.add_argument( '--server', '-s', default=None, type=str,
                        help='SSH server name' )
    parser.add_argument( '--port', '-p', default=22, type=int,
                        help='port (defulat: 22)' )
    parser.add_argument( '--login_name', '-l', default=None, type=str,
                        help='login name' )
    parser.add_argument( '--dir', '-d', default=None, type=str,
                        help='directory at the server' )
    args = parser.parse_args()

    absdir = os.path.dirname( os.path.abspath(__file__) )

    if( args.server is None ):
        shutil.copy( os.path.join( absdir, 'cgw.py' ), 'cgw.cgi' )
        os.chmod( 'cgw.cgi', 0o555 )
        os.mkdir( 'graphs' )
        os.chmod( 'graphs', 0o777 )

    else:
        if( args.login_name is None ):
            args.login_name = getpass.getuser()

        passphrase = getpass.getpass( 'Passphrase for {}@{} :'.format( args.login_name, args.server) )

        # https://qiita.com/int_main_void/items/1cdec761b745010629d5
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(hostname=args.server, port=args.port, username=args.login_name, password=passphrase)
            except Exception as e:
                    print( e )
                    sys.exit()

            with scp.SCPClient(ssh.get_transport()) as scpc:
                try:
                    scpc.put( os.path.join( absdir, 'cgw.py' ), os.path.join( args.dir, 'cgw.cgi' ) )
                except Exception as e:
                    print( e )
                    sys.exit()

            cmds = []
            cmds.append( 'chmod 555 {}'.format( os.path.join( args.dir, 'cgw.cgi' ) ) )
            cmds.append( 'mkdir {}'.format( os.path.join( args.dir, 'graphs' ) ) )
            cmds.append( 'chmod 777 {}'.format( os.path.join( args.dir, 'graphs' ) ) )

            for cmd in cmds:
                stdin, stdout, stderr = ssh.exec_command( cmd )
                for o in stdout:
                    print(o)
                for e in stderr:
                    print(e)


if( __name__ == '__main__' ):
    main()
