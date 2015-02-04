from wakeonlan import wol
import base64
import paramiko
import socket
import sys

__all__ = ["SERVER_DOWN", "SERVER_UP", "SERVER_UP_NOT_RESPONDING", "ServerPower"]

SERVER_DOWN = 1
SERVER_UP = 2
SERVER_UP_NOT_RESPONDING = 3

class ServerPower(object):
    def __init__(self, **kwargs):
        self.server_hostname = kwargs["server_hostname"]
        self.server_mac = kwargs["server_mac"]
        self.ssh_username = kwargs["ssh_username"]

        self.server_port = kwargs.get("server_port", 22)
        self.broadcast_ip = kwargs.get("broadcast_ip", "255.255.255.255")
        self.socket_timeout = kwargs.get("socket_timeout", 0.1)
        self.wol_port = kwargs.get("wol_port", 9)

    def is_alive(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.socket_timeout)
        try:
            s.connect((self.server_hostname, self.server_port))
        except socket.error, e:
            if e.errno == 61: # connection refused
                return SERVER_UP_NOT_RESPONDING
            elif e.message == "timed out": # socket timeout
                return SERVER_DOWN
            elif e.errno == 8: # invalid hostname
                raise e
            elif e.errno == 51: # network is unreachable
                return SERVER_DOWN
            elif e.errno == 64: # host is down
                return SERVER_DOWN
            else:
                print "Message:", e.message
                print "Error:", e.errno, e.strerror
                raise e
        return SERVER_UP

    def wake_up(self):
        for _ in range(0,3):
            wol.send_magic_packet(self.server_mac, port=self.wol_port)

    def shutdown(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(self.server_hostname, username=self.ssh_username)
        _, stdout, stderr = client.exec_command("sudo shutdown")
        stdout = stdout.read()
        stderr = stderr.read()
        client.close()
        return (stdout, stderr)


def main():
    sp = ServerPower(server_hostname="192.168.1.3", server_mac="28:92:4a:2b:03:c9", ssh_username="powermanagement", broadcast_ip="192.168.1.255")
    print sp.is_alive()
    print sp.wake_up()
    return 0

if __name__ == '__main__':
    sys.exit(main())
