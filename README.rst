Home server remote power management
===================================

This library handles rather specific remote power management scenario.

- Server can be woken up with wake-on-lan (WOL)
- There's SSH access to the server (for shutting it down)
- Server responds to ping (checking whether the server is running)


Installation:

::

  pip install manage_server_power

or clone the `repository <https://github.com/ojarva/python-manage-server-power>`_ and use

::

  python setup.py install

Configuration and notes
-----------------------

On the server side:

- Enable WOL (from BIOS/... settings).
- Take note of relevant MAC address.
- Add new user to server (say, powermanagement).
- Edit sudoers (visudo) and add "powermanagement ALL=NOPASSWD: /sbin/poweroff"

On the management computer:

- Generate ssh public key pair (ssh-keygen)
- Copy public key to powermanagement user on server (add it to .ssh/authorized_keys)
- Connect to server to check that public key works properly and to add server host key to known_hosts.

Notes:

- At least with some devices/networks, WOL won't work if broadcast_ip is not set to local network's broadcast, instead of 255.255.255.255.

Usage
-----

::

  import manage_server_power
  sp = manage_server_power.ServerPower(server_hostname="example.com",
                                       server_mac="61:a3:18:1c:84:4b",
                                       server_port=22, # optional, default is 22
                                       ssh_username="powermanagement",
                                       broadcast_ip="192.168.1.255", # optional, default is 255.255.255.255
                                       socket_timeout=0.5, # optional
                                       wol_port=9, # optional, default is 9
                                       )
  print sp.is_alive()
  # SERVER_DOWN, SERVER_UP or SERVER_UP_NOT_RESPONDING
  print sp.wake_up() # send WOL packet
  print sp.shutdown() # ssh in and run "sudo poweroff"
