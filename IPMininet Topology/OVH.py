#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import Zebra, BGP, OSPF6, RouterConfig, AF_INET6,set_rr, ebgp_session, SHARE, CLIENT_PROVIDER, iBGPFullMesh, AF_INET, OSPF
from ipmininet.router.config.zebra import RouteMap

class MyTopology(IPTopo):
    """
    Please read me before digging in the code of this script.
    This simple network topology tries to connect two hosts separated
    by multiple routers and ASes.
    Running this network should be straightforward:
     i./ The script must be run as root since mininet will create routers inside your own machine
         $ chmod +x main.py
         $ sudo ./main.py
    ii./ The network should be started. The "mininet" CLI should appear on screen
    '''
    mininet>
    '''
    To access to one of the network, execute this command "xterm <your node name>". A new
    xterm terminal will be spawned. This new terminal will run bash. This means that you
    can execute any linux command. Be careful as the terminal is run as root!!
    '''
    mininet> xterm as1_rr1
    '''
    To access to the configuration of FRRouting, you have to use telnet to connect to
    FRRouting daemons.
    A different port is used to access to every routing daemon. This small table shows
    the port associated to its default daemon:
    PORT     STATE SERVICE
    2601/tcp open  zebra   --> controls the RIB of each daemon
    2605/tcp open  bgpd    --> show information related to the configuration of BGP
    2606/tcp open  ospf6d  --> same but for OSPFv3 (OSPF for IPv6)
    For example, if you want to look for all prefixes contained in the RIB, you must execute
    this command :
    <in the xterm of your node>$ telnet localhost 2601
    A new cli interface will be shown:
    '''
    Trying ::1...
    Connected to localhost
    Escape character is '^]'.
    Hello, this is FRRouting (version v7.4).
    Copyright 1996-2005 Kunihiro Ishiguro, et al.
    User Access Verification
    Password:
    '''
    At this time, you will be prompted for a password. In ipmininet the default password is "zebra".
    Simply type it and the FRRouting CLI will be shown:
    '''
    as1_rr1>
    '''
    Type "show ipv6 route" to show all the routes contained in the RIB. You can find an example of output below
    ''''
    as1_rr1> c
    Codes: K - kernel route, C - connected, S - static, R - RIPng,
           O - OSPFv3, I - IS-IS, B - BGP, N - NHRP, T - Table,
           v - VNC, V - VNC-Direct, A - Babel, D - SHARP, F - PBR,
           f - OpenFabric,
           > - selected route, * - FIB route, q - queued route, r - rejected route
    B>* c1a4:4ad:c0ff:ee::/64 [20/0] via fe80::f802:bbff:fe6d:4da0, as1_rr1-eth2, weight 1, 00:50:34
    O>* cafe:babe:dead:beaf::/64 [110/2] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:30
    O   fc00:0:3::/48 [110/1] is directly connected, as1_rr1-eth0, weight 1, 00:50:35
    C>* fc00:0:3::/48 is directly connected, as1_rr1-eth0, 00:50:38
    O   fc00:0:4::/48 [110/1] is directly connected, as1_rr1-eth1, weight 1, 00:50:35
    C>* fc00:0:4::/48 is directly connected, as1_rr1-eth1, 00:50:38
    B   fc00:0:5::/48 [20/0] via fe80::f802:bbff:fe6d:4da0, as1_rr1-eth2, weight 1, 00:50:34
    O   fc00:0:5::/48 [110/1] is directly connected, as1_rr1-eth2, weight 1, 00:50:38
    C>* fc00:0:5::/48 is directly connected, as1_rr1-eth2, 00:50:38
    O>* fc00:0:6::/48 [110/2] via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1,  00:50:30
    O>* fc00:0:7::/48 [110/2] via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1, 00:50:30
    B   fc00:0:7::/48 [200/0] via fc00:0:3::1, as1_rr1-eth0, weight 1, 00:50:34
    O>* fc00:0:8::/48 [110/2] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:30
    O   fc00:0:9::/48 [110/1] is directly connected, lo, weight 1, 00:50:38
    C>* fc00:0:9::/48 is directly connected, lo, 00:50:39
    O>* fc00:0:a::/48 [110/2] via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1, 00:50:30
    O>* fc00:0:b::/48 [110/3] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:25
      *                       via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1, 00:50:25
    O>* fc00:0:c::/48 [110/2] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:30
    B>* fc00:0:d::/48 [20/0] via fe80::f802:bbff:fe6d:4da0, as1_rr1-eth2, weight 1, 00:50:34
    B>* fc00:0:e::/48 [200/0] via fc00:0:3::1, as1_rr1-eth0, weight 1, 00:50:34
    C * fe80::/64 is directly connected, as1_rr1-eth0, 00:50:38
    C * fe80::/64 is directly connected, as1_rr1-eth2, 00:50:38
    C>* fe80::/64 is directly connected, as1_rr1-eth1, 00:50:38
    '''
    Press CTRL + D to exit the session. And again to exit the xterm session.
    You can find more information on how to use the CLI of FRRouting daemons in the FRRouting DOCS:
    http://docs.frrouting.org/en/latest/
    Remember that xterm launches a root bash. You can run any executable (in ROOT!).
    If wireshark is installed on your computer, you can execute it to capture packets
    reaching interfaces of your mininet node.
    The same applies if you want to check the Linux FIB (ip addr) or the addresses attached to the node
    interfaces (ip route)
    Finally, you can find other details on how to build an ipmininet script here:
    https://ipmininet.readthedocs.io/en/latest/
    """

    # 1. Can you picture the topology described in this python script ?
    #    Draw this topology by hand before running it in ipmininet.
    # 2. This small network is faulty. Can you find the problem ?
    # 3. Propose a fix to make this network operational again
    # 4. How can you do to check the LSDB of OSPF ?
    # 5. Again use it to show details about the BGP sessions.
    # 6. Add a new AS (AS3) on top of this topology which will contain 4 routers, each running
    #    OSPFv3 and BGP. Add also a new host as3_h3 in a new lan 7ac0:d0d0:15:dead::/64 in one of the 4 routers.
    #    h1, h2 and h3 must reach each other. The iBGP sessions, this time, must be in
    #    full mesh configuration. AS3 will have only one eBGP peering with AS1 on the as1_s1 router.

    def build(self, *args, **kwargs):

        lon_thw_sbb1_nc5 = self.addRouter("lon_1", config=RouterConfig, lo_addresses=["2001:41D0:0000:0280::/128", "192.148.2.0/32"])
        lon_drch_sbb1_nc5 = self.addRouter("lon_2", config=RouterConfig,lo_addresses=["2001:41D0:0000:0281::/128", "192.148.2.1/32"])
        self.addSubnet(nodes=[lon_thw_sbb1_nc5, lon_drch_sbb1_nc5], subnets=["192.148.0.0/30","2001:41D0:0:0200::/64"])

        gra_g1_nc5 = self.addRouter("gra_1", config=RouterConfig,lo_addresses=["2001:41D0:0000:0080::/128", "192.148.2.2/32"])
        gra_g2_nc5 = self.addRouter("gra_2", config=RouterConfig,lo_addresses=["2001:41D0:0000:0081::/128", "192.148.2.3/32"])
        self.addSubnet(nodes=[gra_g1_nc5, gra_g2_nc5], subnets=["192.148.0.4/30","2001:41D0:0:0000::/64"])
        self.addSubnet(nodes=[gra_g1_nc5, lon_thw_sbb1_nc5], subnets=["192.148.0.8/30","2001:41D0:0:1F00::/64"])
        self.addSubnet(nodes=[gra_g2_nc5, lon_drch_sbb1_nc5], subnets=["192.148.0.12/30","2001:41D0:0:1F01::/64"])

        fra_fr5_sbb1_nc5 = self.addRouter("fra_1", config=RouterConfig, lo_addresses=["2001:41D0:0000:0180::/128", "192.148.2.4/32"])
        fra_fr5_sbb2_nc5 = self.addRouter("fra_2", config=RouterConfig, lo_addresses=["2001:41D0:0000:0181::/128", "192.148.2.5/32"])
        fra_1_n7 = self.addRouter("fra_3", config=RouterConfig, lo_addresses=["2001:41D0:0000:0182::/128", "192.148.2.6/32"])
        fra_5_n7 = self.addRouter("fra_4", config=RouterConfig, lo_addresses=["2001:41D0:0000:0183::/128", "192.148.2.7/32"])
        self.addSubnet(nodes=[fra_fr5_sbb1_nc5, fra_fr5_sbb2_nc5], subnets=["192.148.0.16/30","2001:41D0:0:0100::/64"])
        self.addSubnet(nodes=[fra_1_n7, fra_5_n7], subnets=["192.148.0.20/30","2001:41D0:0:0101::/64"])
        self.addSubnet(nodes=[fra_1_n7, fra_fr5_sbb1_nc5], subnets=["192.148.0.24/30","2001:41D0:0:0102::/64"])
        self.addSubnet(nodes=[fra_1_n7, fra_fr5_sbb2_nc5], subnets=["192.148.0.28/30","2001:41D0:0:0103::/64"])
        self.addSubnet(nodes=[fra_5_n7, fra_fr5_sbb1_nc5], subnets=["192.148.0.32/30","2001:41D0:0:0104::/64"])
        self.addSubnet(nodes=[fra_5_n7, fra_fr5_sbb2_nc5], subnets=["192.148.0.36/30","2001:41D0:0:0105::/64"])
        self.addSubnet(nodes=[gra_g1_nc5, fra_fr5_sbb1_nc5], subnets=["192.148.0.40/30","2001:41D0:0:1F02::/64"])
        self.addSubnet(nodes=[gra_g2_nc5, fra_fr5_sbb2_nc5], subnets=["192.148.0.44/30","2001:41D0:0:1F03::/64"])

        rbx_g1_nc5 = self.addRouter("rbx_1", config=RouterConfig, lo_addresses=["2001:41D0:0000:0082::/128", "192.148.2.8/32"])
        rbx_g2_nc5 = self.addRouter("rbx_2", config=RouterConfig, lo_addresses=["2001:41D0:0000:0083::/128", "192.148.2.9/32"])
        self.addSubnet(nodes=[rbx_g1_nc5, rbx_g2_nc5], subnets=["192.148.0.48/30","2001:41D0:0:0001::/64"])
        self.addSubnet(nodes=[rbx_g1_nc5, fra_fr5_sbb1_nc5], subnets=["192.148.0.52/30","2001:41D0:0:1F04::/64"])
        self.addSubnet(nodes=[rbx_g1_nc5, lon_thw_sbb1_nc5], subnets=["192.148.0.56/30","2001:41D0:0:1F05::/64"])
        self.addSubnet(nodes=[rbx_g2_nc5, fra_fr5_sbb2_nc5], subnets=["192.148.0.60/30","2001:41D0:0:1F06::/64"])
        self.addSubnet(nodes=[rbx_g2_nc5, lon_drch_sbb1_nc5], subnets=["192.148.0.64/30","2001:41D0:0:1F07::/64"])

        par_gsw_sbb1_nc5 = self.addRouter("par_1", config=RouterConfig, lo_addresses=["2001:41D0:0000:0084::/128", "192.148.2.10/32"])
        par_th2_sbb1_nc5 = self.addRouter("par_2", config=RouterConfig, lo_addresses=["2001:41D0:0000:0085::/128", "192.148.2.11/32"])
        self.addSubnet(nodes=[par_gsw_sbb1_nc5, par_th2_sbb1_nc5], subnets=["192.148.0.68/30","2001:41D0:0:0002::/64"])
        self.addSubnet(nodes=[par_gsw_sbb1_nc5, rbx_g2_nc5], subnets=["192.148.0.72/30","2001:41D0:0:0003::/64"])
        self.addSubnet(nodes=[par_gsw_sbb1_nc5, gra_g1_nc5], subnets=["192.148.0.76/30","2001:41D0:0:0004::/64"])
        self.addSubnet(nodes=[par_th2_sbb1_nc5, gra_g2_nc5], subnets=["192.148.0.80/30","2001:41D0:0:0005::/64"])
        self.addSubnet(nodes=[par_th2_sbb1_nc5, rbx_g1_nc5], subnets=["192.148.0.84/30","2001:41D0:0:0006::/64"])

        routers = [lon_thw_sbb1_nc5,lon_drch_sbb1_nc5,
                gra_g1_nc5, gra_g2_nc5,
                fra_fr5_sbb1_nc5,fra_fr5_sbb2_nc5,fra_1_n7,fra_5_n7,
                rbx_g1_nc5,rbx_g2_nc5,
                par_gsw_sbb1_nc5,par_th2_sbb1_nc5]

        setup_routers(routers)


        # adding BGP and OSPF as IGP

        routers = [lon_thw_sbb1_nc5,lon_drch_sbb1_nc5,
                gra_g1_nc5, gra_g2_nc5,
                fra_fr5_sbb1_nc5,fra_fr5_sbb2_nc5,fra_1_n7,fra_5_n7,
                rbx_g1_nc5,rbx_g2_nc5,
                par_gsw_sbb1_nc5,par_th2_sbb1_nc5]
                
        MyServer1 = self.addRouter("ServOne", config=RouterConfig, lo_addresses=["2001:41D0:0000:00C0::/128","192.148.1.32/32"])
        MyServer2 = self.addRouter("ServTwo", config=RouterConfig, lo_addresses=["2001:41D0:0000:00C0::/128","192.148.1.32/32"])
        MyServer3 = self.addRouter("ServThree", config=RouterConfig, lo_addresses=["2001:41D0:0000:00C0::/128","192.148.1.32/32"])
        setup_routers([MyServer1, MyServer2, MyServer3])
        self.addLinks((MyServer1, rbx_g1_nc5),
        	       (MyServer2, lon_drch_sbb1_nc5),
        	       (MyServer3, fra_fr5_sbb2_nc5))

        set_rr(self, rr=rbx_g2_nc5, peers=[par_gsw_sbb1_nc5, par_th2_sbb1_nc5,lon_thw_sbb1_nc5, lon_drch_sbb1_nc5])#, MyServer2])
        set_rr(self, rr=rbx_g1_nc5, peers=[par_gsw_sbb1_nc5, par_th2_sbb1_nc5,lon_thw_sbb1_nc5, lon_drch_sbb1_nc5])#, MyServer1])
        set_rr(self, rr=gra_g1_nc5, peers=[gra_g2_nc5, rbx_g1_nc5, rbx_g2_nc5,fra_fr5_sbb1_nc5,fra_fr5_sbb2_nc5])
        set_rr(self, rr=gra_g2_nc5, peers=[gra_g1_nc5, rbx_g1_nc5, rbx_g2_nc5,fra_fr5_sbb1_nc5,fra_fr5_sbb2_nc5])
        set_rr(self, rr=fra_fr5_sbb1_nc5, peers=[fra_1_n7, fra_5_n7])
        set_rr(self, rr=fra_fr5_sbb2_nc5, peers=[fra_1_n7, fra_5_n7])#, MyServer3])

        #self.addiBGPFullMesh(1, routers=routers)
        self.addAS(16276, routers=routers)


        '''********************   ADDING EXTERNAL AS     **********************************'''

        google_r1=self.addRouter("google_r1",config=RouterConfig,lo_addresses=["2001:4860::1/64","8.8.4.1/32"])
        google_r2=self.addRouter("google_r2",config=RouterConfig,lo_addresses=["2001:4860::2/64","8.8.4.2/32"])
        google_r3=self.addRouter("google_r3",config=RouterConfig,lo_addresses=["2001:4860::3/64","8.8.4.3/32"])
        self.addAS(15169,routers=[google_r1,google_r2,google_r3])
        self.addLinks((par_gsw_sbb1_nc5,google_r1),(fra_5_n7,google_r3),(par_th2_sbb1_nc5,google_r2))

        self.addSubnet(nodes=[par_gsw_sbb1_nc5,google_r1], subnets=["2001:41D0:0:1F08::/64","192.148.0.88/30"])
        self.addSubnet(nodes=[fra_5_n7,google_r3], subnets=["2001:41D0:0:1F09::/64","192.148.0.92/30"])
        self.addSubnet(nodes=[par_th2_sbb1_nc5,google_r2], subnets=["2001:41D0:0:1F0A::/64", "192.148.0.96/30"])

        ebgp_session(self,par_gsw_sbb1_nc5,google_r1,link_type=CLIENT_PROVIDER)
        ebgp_session(self,fra_5_n7,google_r3,link_type=CLIENT_PROVIDER)
        ebgp_session(self,par_th2_sbb1_nc5,google_r2,link_type=CLIENT_PROVIDER)

        setup_routers([google_r1,google_r2,google_r3])


        vodafone_r1=self.addRouter("voda_r1",config=RouterConfig,lo_addresses=["2001:5000::1/64","2.16.35.1/32"])
        vodafone_r2=self.addRouter("voda_r2",config=RouterConfig,lo_addresses=["2001:5000::2/64","2.16.35.2/32"])
        vodafone_r3=self.addRouter("voda_r3",config=RouterConfig,lo_addresses=["2001:5000::3/64","2.16.35.3/32"])
        vodafone_r4=self.addRouter("voda_r4",config=RouterConfig,lo_addresses=["2001:5000::4/64","2.16.35.4/32"])

        self.addAS(1273,routers=[vodafone_r1,vodafone_r2,vodafone_r3,vodafone_r4])
        self.addLinks((par_th2_sbb1_nc5,vodafone_r2),(fra_5_n7,vodafone_r4),(fra_1_n7,vodafone_r3),(par_gsw_sbb1_nc5,vodafone_r1))

        self.addSubnet(nodes=[par_th2_sbb1_nc5,vodafone_r2], subnets=["192.148.0.100/30", "2001:41D0:0:1F0B::/64"])
        self.addSubnet(nodes=[fra_5_n7,vodafone_r4], subnets=["192.148.0.104/30", "2001:41D0:0:1F0C::/64"])
        self.addSubnet(nodes=[fra_1_n7,vodafone_r3], subnets=["192.148.0.108/30", "2001:41D0:0:1F0D::/64"])
        self.addSubnet(nodes=[par_gsw_sbb1_nc5,vodafone_r1], subnets=["192.148.0.112/30", "2001:41D0:0:1F0E::/64"])
        ebgp_session(self,par_th2_sbb1_nc5,vodafone_r2,link_type=CLIENT_PROVIDER)
        ebgp_session(self,fra_5_n7,vodafone_r4,link_type=CLIENT_PROVIDER)
        ebgp_session(self,fra_1_n7,vodafone_r3,link_type=CLIENT_PROVIDER)
        ebgp_session(self,par_gsw_sbb1_nc5,vodafone_r1,link_type=CLIENT_PROVIDER)

        setup_routers([vodafone_r1,vodafone_r2,vodafone_r3,vodafone_r4])



        cogent_r1=self.addRouter("cogent_r1",config=RouterConfig,lo_addresses=["2001:550::1/64","2.58.4.1/32"])
        cogent_r2=self.addRouter("cogent_r2",config=RouterConfig,lo_addresses=["2001:550::2/64","2.58.4.2/32"])
        cogent_r3=self.addRouter("cogent_r3",config=RouterConfig,lo_addresses=["2001:550::3/64","2.58.4.3/32"])
        self.addAS(174,routers=[cogent_r1,cogent_r2,cogent_r3])
        self.addLinks((par_gsw_sbb1_nc5,cogent_r1),(lon_thw_sbb1_nc5,cogent_r3),(par_th2_sbb1_nc5,cogent_r2))

        self.addSubnet(nodes=[par_gsw_sbb1_nc5,cogent_r1], subnets=["192.148.0.116/30", "2001:41D0:0:1F0F::/64"])
        self.addSubnet(nodes=[lon_thw_sbb1_nc5,cogent_r3], subnets=["192.148.0.120/30", "2001:41D0:0:1F10::/64"])
        self.addSubnet(nodes=[par_th2_sbb1_nc5,cogent_r2], subnets=["192.148.0.124/30", "2001:41D0:0:1F11::/64"])
        ebgp_session(self,par_gsw_sbb1_nc5,cogent_r1,link_type=CLIENT_PROVIDER)
        ebgp_session(self,lon_thw_sbb1_nc5,cogent_r3,link_type=CLIENT_PROVIDER)
        ebgp_session(self,par_th2_sbb1_nc5,cogent_r2,link_type=CLIENT_PROVIDER)

        setup_routers([cogent_r1,cogent_r2,cogent_r3])


        telia_r1=self.addRouter("telia_r1",config=RouterConfig,lo_addresses=["2001:2000::1/64","2.255.248.1/32"])
        telia_r2=self.addRouter("telia_r2",config=RouterConfig,lo_addresses=["2001:2000::2/64","2.255.248.2/32"])
        telia_r3=self.addRouter("telia_r3",config=RouterConfig,lo_addresses=["2001:2000::3/64","2.255.248.3/32"])

        self.addAS(1299,routers=[telia_r1,telia_r2,telia_r3])
        self.addLinks((fra_5_n7,telia_r2),(fra_1_n7,telia_r1),(lon_thw_sbb1_nc5,telia_r3))

        self.addSubnet(nodes=[fra_5_n7,telia_r2], subnets=["192.148.0.128/30", "2001:41D0:0:1F12::/64"])
        self.addSubnet(nodes=[fra_1_n7,telia_r1], subnets=["192.148.0.132/30", "2001:41D0:0:1F13::/64"])
        self.addSubnet(nodes=[lon_thw_sbb1_nc5,telia_r3], subnets=["192.148.0.136/30", "2001:41D0:0:1F14::/64"])
        ebgp_session(self,fra_5_n7,telia_r2,link_type=CLIENT_PROVIDER)
        ebgp_session(self,fra_1_n7,telia_r1,link_type=CLIENT_PROVIDER)
        ebgp_session(self,lon_thw_sbb1_nc5,telia_r3,link_type=CLIENT_PROVIDER)

        setup_routers([telia_r1,telia_r2,telia_r3])


        amazon_r1=self.addRouter("amazon_r1",config=RouterConfig,lo_addresses=["2001:4f8:b::1/64","3.5.128.1/32"])
        amazon_r2=self.addRouter("amazon_r2",config=RouterConfig,lo_addresses=["2001:4f8:b::2/64","3.5.128.2/32"])
        self.addAS(16509,routers=[amazon_r1,amazon_r2])
        self.addLinks((lon_thw_sbb1_nc5,amazon_r2),(par_th2_sbb1_nc5,amazon_r1))

        self.addSubnet(nodes=[par_th2_sbb1_nc5,amazon_r1], subnets=["192.148.0.140/30", "2001:41D0:0:1F15::/64"])
        self.addSubnet(nodes=[lon_thw_sbb1_nc5,amazon_r2], subnets=["192.148.0.144/30", "2001:41D0:0:1F16::/64"])
        ebgp_session(self,par_th2_sbb1_nc5,amazon_r1,link_type=CLIENT_PROVIDER)
        ebgp_session(self,lon_thw_sbb1_nc5,amazon_r2,link_type=CLIENT_PROVIDER)

        setup_routers([amazon_r1,amazon_r2])#,vodafone,cogent,telia,amazon])

        # adding BGP to establish iBGP sessions
        #as1_rr1.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_as1_h1,),),))
        #as1_rr2.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_as1_h1,),),))
        #as1_s1.addDaemon(BGP, address_families=(family,))
        #as1_s2.addDaemon(BGP, address_families=(family,))

        # set the ASN for routers belonging to AS1
        # self.addAS(1, (lon_thw_sbb1_nc5, lon_drch_sbb1_nc5, gra_g1_nc5, gra_g2_nc5, fra_fr5_sbb1_nc5, fra_fr5_sbb2_nc5, fra_1_n7, fra_5_n7, rbx_g2_nc5, rbx_g1_nc5, par_gsw_sbb1_nc5, par_th2_sbb1_nc5,))

        # configure as1_rr{1,2} as route reflectors
        #set_rr(self, rr=as1_rr1, peers=[as1_s2, as1_rr2])
        #set_rr(self, rr=as1_rr2, peers=[as1_s1, as1_rr1])

        # routers of as2
        #as2_cl1 = self.addRouter("as2_cl1", config=RouterConfig)
        #as2_cl2 = self.addRouter("as2_cl2", config=RouterConfig)

        # adding a BGP daemon for AS2 routers
        #as2_cl1.addDaemon(BGP, address_families=(AF_INET6(redistribute=['connected']),))
        #as2_cl2.addDaemon(BGP, address_families=(AF_INET6(redistribute=['connected']),))

        # AS3
        #lan_as3_h3 = '7ac0:d0d0:15:dead::/64'

        #as3_r1 = self.addRouter("as3_r1", config=RouterConfig)
        #as3_r2 = self.addRouter("as3_r2", config=RouterConfig)
        #as3_r3 = self.addRouter("as3_r3", config=RouterConfig)
        #as3_r4 = self.addRouter("as3_r4", config=RouterConfig)

        #as3_r1.addDaemon(OSPF6)
        #as3_r2.addDaemon(OSPF6)
        #as3_r3.addDaemon(OSPF6)
        #as3_r4.addDaemon(OSPF6)

        #as3_r1.addDaemon(BGP, address_families=(family,))
        #as3_r2.addDaemon(BGP, address_families=(family,))
        #as3_r3.addDaemon(BGP, address_families=(family,))
        #as3_r4.addDaemon(BGP, address_families=(family,))

        #self.addAS(3, (as3_r1, as3_r2, as3_r3, as3_r4))

        #iBGPFullMesh(3, routers=(as3_r1,as3_r2,as3_r3,as3_r4))

        #as3_h3 = self.addHost("as3_h3")

        #self.addLinks((as3_r1, as3_r2), (as3_r1, as3_r4),
                      #(as3_r2, as3_r3),
                      #(as3_r3, as3_r4), (as3_r3, as1_s1),
                      #(as3_h3, as3_r2))

        #self.addSubnet((as3_h3, as3_r2), subnets=(lan_as3_h3,))
        #ebgp_session(self, as3_r3, as1_s1, link_type=SHARE)

        # set the ASN for routers belonging to AS2
        #self.addAS(2, (as2_cl1, as2_cl2))

        # we add a host in as1
        #as1_h1 = self.addHost("as1_h1")
        # and also in as2
        #as2_h2 = self.addHost("as2_h2")

        # The goal of this network is to establish a connection between h1 and h2

        # adding links between the routers (and hosts)
        # self.addLink(as1_rr1, as1_rr2, igp_metric=5)
        
        self.addLinks((lon_thw_sbb1_nc5, lon_drch_sbb1_nc5), (lon_thw_sbb1_nc5, gra_g1_nc5), (lon_thw_sbb1_nc5, rbx_g1_nc5),
                      (lon_drch_sbb1_nc5, gra_g2_nc5), (lon_drch_sbb1_nc5, rbx_g2_nc5),
                      (gra_g1_nc5, gra_g2_nc5), (gra_g1_nc5, par_gsw_sbb1_nc5), (gra_g1_nc5, fra_fr5_sbb1_nc5),
                      (gra_g2_nc5, par_th2_sbb1_nc5), (gra_g2_nc5, fra_fr5_sbb2_nc5),
                      (fra_fr5_sbb1_nc5, fra_fr5_sbb2_nc5), (fra_fr5_sbb1_nc5, fra_1_n7), (fra_fr5_sbb1_nc5, fra_5_n7), (fra_fr5_sbb1_nc5, rbx_g1_nc5),
                      (fra_fr5_sbb2_nc5, fra_1_n7), (fra_fr5_sbb2_nc5, fra_5_n7), (fra_fr5_sbb2_nc5, rbx_g2_nc5),
                      (fra_1_n7, fra_5_n7),
                      (rbx_g1_nc5, rbx_g2_nc5), (rbx_g1_nc5, par_th2_sbb1_nc5),
                      (rbx_g2_nc5, par_gsw_sbb1_nc5),
                      (par_gsw_sbb1_nc5, par_th2_sbb1_nc5))
        

        # adding eBGP sessions between the two ASes
        #ebgp_session(self, as2_cl1, as1_rr1, link_type=SHARE)
        #ebgp_session(self, as2_cl2, as1_rr2, link_type=SHARE)

        super().build(*args, **kwargs)

def setup_routers(routers):
    for r in routers:
        r.addDaemon(OSPF)
        r.addDaemon(OSPF6)
        r.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected'])))
# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=MyTopology(), allocate_IPs=True)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
