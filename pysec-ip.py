import getpass
import sys
import telnetlib

#HOST_1 user & pass 
user1 = input(" [ HOST 1 ]>> Enter your telnet user name :")
password1 = getpass.getpass()

#HOST_2 user & pass
user2 = input("[ HOST 2 ]>> Enter your telnet user name :")
password2 = getpass.getpass()

HOST_1 = ("10.50.1.1", user1 ,password1)
HOST_2 = ("10.40.1.1", user2 ,password2) 
def pysec(HOST_1,HOST_2):
    print(HOST_1[0] +"  ########<tunnul>##########  " + HOST_2[0])
    print("Configuring >> ",HOST_1[0])
    tn = telnetlib.Telnet(HOST_1[0])

    tn.read_until(b"Username:")
    tn.write(HOST_1[1].encode('ascii')+ b"\n")
    tn.read_until(b"Password:")
    tn.write(HOST_1[2].encode('ascii')+b"\n")

    tn.write(b"conf t \n")

    prio = input("Chose Priority of protection suite <1-10000> :")
    tn.write(b"crypto isakmp policy  "+prio.encode('ascii')+b"\n")

    tn.write(b"encr 3des\n")
    print("[+] encr 3des")

    tn.write(b"hash md5\n")
    print("[+] hash md5")

    tn.write(b"authentication pre-share\n")
    pre_sh = input("pre-share key :")
    print("[+] authentication pre-share")

    tn.write(b"group 2\n")
    print("[+] group 2")

    tn.write(b"lifetime 3600\n")
    print("[+] lifetime 3600")

    tn.write(b"end\n")

    tn.write(b"conf t\n")
    tn.write(b"crypto isakmp key "+pre_sh.encode('ascii') +b" address " + HOST_2[0].encode('ascii') + b"\n")

    print("[-] ACCESS LISTE ")

    tn.write(b"ip access-list extended VPN-TRAFFIC \n")  
    tn.write(b"permit ip  any any \n")
    #tn.write(b"permit ip "+ HOST_1[0].encode('ascii')+ b" 0.0.0.255 " + HOST_2[0].encode('ascii')+ b" 0.0.0.255 " + b" \n")
    tn.write(b"exit \n")
    print("IKEv1 Phase [ 2 ] :")
    tn.write(b"crypto ipsec transform-set MY-SET esp-md5-hmac esp-3des \n")
    tn.write(b"crypto map MAP 10 ipsec-isakmp \n")
    tn.write(b"set peer " + HOST_2[0].encode('ascii') + b"\n")

    tn.write(b"set transform-set  MY-SET \n")
    tn.write(b"match address VPN-TRAFFIC\n")
    tn.write(b"exit \n")
    tn.write(b"interface FastEthernet1/0\n")
    tn.write(b"crypto map MAP\n")

    tn.write(b"end\n")
    tn.write(b"exit\n")
    a = tn.read_all()
    print (a.decode("utf-8"))

pysec(HOST_1,HOST_2)
pysec(HOST_2,HOST_1)