#!/usr/bin/env python3
import ipaddress
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import Zebra, BGP, OSPF6, RouterConfig, AF_INET6,set_rr, ebgp_session, SHARE, CLIENT_PROVIDER, iBGPFullMesh, AF_INET, OSPF, STATIC, StaticRoute
from ipmininet.router.config.ospf import OSPFRedistributedRoute
from ipmininet.router.config.zebra import RouteMap
from ipmininet.router.config.zebra import RouteMap, CommunityList, AccessList, AccessListEntry

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
    
    #curr_routerid=0
    
    def setup_routers(self, routers):
        for r in routers:
            r.addDaemon(OSPF, debug=('event',), redistribute=(OSPFRedistributedRoute('connected'),))#, routerid=self.curr_routerid)
            #self.curr_routerid+=1
            r.addDaemon(OSPF6, debug=('event',), redistribute=(OSPFRedistributedRoute('connected'),))
            r.addDaemon(BGP, debug=('event',),address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected'])))
    def setup_servers(self, servers):
        for s in servers:
            #s.addDaemon(OSPF, debug=('event',), redistribute=(OSPFRedistributedRoute('connected'),))
            #s.addDaemon(OSPF6, debug=('event',), redistribute=(OSPFRedistributedRoute('connected'),))
            s.addDaemon(BGP, debug=('event',),address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected'])))
    

    def build(self, *args, **kwargs):
        LOCAL_PREF_HIGH=['16276:7200',200]
        LOCAL_PREF_LOW=['16276:7100',50]
        LOCAL_PREFS=[LOCAL_PREF_HIGH,LOCAL_PREF_LOW]

        lon_thw_sbb1_nc5 = self.addRouter("lon_1", config=RouterConfig, lo_addresses=["2001:41D0:0000:0280::/128", "192.148.3.0/32"])
        lon_drch_sbb1_nc5 = self.addRouter("lon_2", config=RouterConfig,lo_addresses=["2001:41D0:0000:0281::/128", "192.148.3.1/32"])
        self.addSubnet(nodes=[lon_thw_sbb1_nc5, lon_drch_sbb1_nc5], subnets=["192.148.2.0/30","2001:41D0:0:0200::/64"])

        gra_g1_nc5 = self.addRouter("gra_1", config=RouterConfig,lo_addresses=["2001:41D0:0000:0080::/128", "192.148.3.2/32"])
        gra_g2_nc5 = self.addRouter("gra_2", config=RouterConfig,lo_addresses=["2001:41D0:0000:0081::/128", "192.148.3.3/32"])
        self.addSubnet(nodes=[gra_g1_nc5, gra_g2_nc5], subnets=["192.148.2.4/30","2001:41D0:0:0000::/64"])
        self.addSubnet(nodes=[gra_g1_nc5, lon_thw_sbb1_nc5], subnets=["192.148.2.8/30","2001:41D0:0:1F00::/64"])
        self.addSubnet(nodes=[gra_g2_nc5, lon_drch_sbb1_nc5], subnets=["192.148.2.12/30","2001:41D0:0:1F01::/64"])

        fra_fr5_sbb1_nc5 = self.addRouter("fra_1", config=RouterConfig, lo_addresses=["2001:41D0:0000:0180::/128", "192.148.3.4/32"])
        fra_fr5_sbb2_nc5 = self.addRouter("fra_2", config=RouterConfig, lo_addresses=["2001:41D0:0000:0181::/128", "192.148.3.5/32"])
        fra_1_n7 = self.addRouter("fra_3", config=RouterConfig, lo_addresses=["2001:41D0:0000:0182::/128", "192.148.3.6/32"])
        fra_5_n7 = self.addRouter("fra_4", config=RouterConfig, lo_addresses=["2001:41D0:0000:0183::/128", "192.148.3.7/32"])
        self.addSubnet(nodes=[fra_fr5_sbb1_nc5, fra_fr5_sbb2_nc5], subnets=["192.148.2.16/30","2001:41D0:0:0100::/64"])
        self.addSubnet(nodes=[fra_1_n7, fra_5_n7], subnets=["192.148.2.20/30","2001:41D0:0:0101::/64"])
        self.addSubnet(nodes=[fra_1_n7, fra_fr5_sbb1_nc5], subnets=["192.148.2.24/30","2001:41D0:0:0102::/64"])
        self.addSubnet(nodes=[fra_1_n7, fra_fr5_sbb2_nc5], subnets=["192.148.2.28/30","2001:41D0:0:0103::/64"])
        self.addSubnet(nodes=[fra_5_n7, fra_fr5_sbb1_nc5], subnets=["192.148.2.32/30","2001:41D0:0:0104::/64"])
        self.addSubnet(nodes=[fra_5_n7, fra_fr5_sbb2_nc5], subnets=["192.148.2.36/30","2001:41D0:0:0105::/64"])
        self.addSubnet(nodes=[gra_g1_nc5, fra_fr5_sbb1_nc5], subnets=["192.148.2.40/30","2001:41D0:0:1F02::/64"])
        self.addSubnet(nodes=[gra_g2_nc5, fra_fr5_sbb2_nc5], subnets=["192.148.2.44/30","2001:41D0:0:1F03::/64"])

        rbx_g1_nc5 = self.addRouter("rbx_1", config=RouterConfig, lo_addresses=["2001:41D0:0000:0082::/128", "192.148.3.8/32"])
        rbx_g2_nc5 = self.addRouter("rbx_2", config=RouterConfig, lo_addresses=["2001:41D0:0000:0083::/128", "192.148.3.9/32"])
        self.addSubnet(nodes=[rbx_g1_nc5, rbx_g2_nc5], subnets=["192.148.2.48/30","2001:41D0:0:0001::/64"])
        self.addSubnet(nodes=[rbx_g1_nc5, fra_fr5_sbb1_nc5], subnets=["192.148.2.52/30","2001:41D0:0:1F04::/64"])
        self.addSubnet(nodes=[rbx_g1_nc5, lon_thw_sbb1_nc5], subnets=["192.148.2.56/30","2001:41D0:0:1F05::/64"])
        self.addSubnet(nodes=[rbx_g2_nc5, fra_fr5_sbb2_nc5], subnets=["192.148.2.60/30","2001:41D0:0:1F06::/64"])
        self.addSubnet(nodes=[rbx_g2_nc5, lon_drch_sbb1_nc5], subnets=["192.148.2.64/30","2001:41D0:0:1F07::/64"])

        par_gsw_sbb1_nc5 = self.addRouter("par_1", config=RouterConfig, lo_addresses=["2001:41D0:0000:0084::/128", "192.148.3.10/32"])
        par_th2_sbb1_nc5 = self.addRouter("par_2", config=RouterConfig, lo_addresses=["2001:41D0:0000:0085::/128", "192.148.3.11/32"])
        self.addSubnet(nodes=[par_gsw_sbb1_nc5, par_th2_sbb1_nc5], subnets=["192.148.2.68/30","2001:41D0:0:0002::/64"])
        self.addSubnet(nodes=[par_gsw_sbb1_nc5, rbx_g2_nc5], subnets=["192.148.2.72/30","2001:41D0:0:0003::/64"])
        self.addSubnet(nodes=[par_gsw_sbb1_nc5, gra_g1_nc5], subnets=["192.148.2.76/30","2001:41D0:0:0004::/64"])
        self.addSubnet(nodes=[par_th2_sbb1_nc5, gra_g2_nc5], subnets=["192.148.2.80/30","2001:41D0:0:0005::/64"])
        self.addSubnet(nodes=[par_th2_sbb1_nc5, rbx_g1_nc5], subnets=["192.148.2.84/30","2001:41D0:0:0006::/64"])

        routers = [lon_thw_sbb1_nc5,lon_drch_sbb1_nc5,
                gra_g1_nc5, gra_g2_nc5,
                fra_fr5_sbb1_nc5,fra_fr5_sbb2_nc5,fra_1_n7,fra_5_n7,
                rbx_g1_nc5,rbx_g2_nc5,
                par_gsw_sbb1_nc5,par_th2_sbb1_nc5]

        self.setup_routers(routers)


        # adding BGP and OSPF as IGP

        routers = [lon_thw_sbb1_nc5,lon_drch_sbb1_nc5,
                gra_g1_nc5, gra_g2_nc5,
                fra_fr5_sbb1_nc5,fra_fr5_sbb2_nc5,fra_1_n7,fra_5_n7,
                rbx_g1_nc5,rbx_g2_nc5,
                par_gsw_sbb1_nc5,par_th2_sbb1_nc5]
                
        MyServer1 = self.addRouter("ServOne", config=RouterConfig, lo_addresses=["2001:41D0:0000:00C0::/128", "192.148.1.0/32","192.148.3.12/32"])       
        MyServer2 = self.addRouter("ServTwo", config=RouterConfig, lo_addresses=["2001:41D0:0000:00C0::/128", "192.148.1.0/32","192.148.3.13/32"])
        MyServer3 = self.addRouter("ServThree", config=RouterConfig, lo_addresses=["2001:41D0:0000:00C0::/128", "192.148.1.0/32","192.148.3.14/32"])
        
        self.addSubnet(nodes=[MyServer1, rbx_g1_nc5], subnets=["192.148.0.0/30","2001:41D0:0:0007::/64"])
        MyServer1.addDaemon(STATIC, static_routes=[StaticRoute("::/0", "2001:41D0:0:0007::2"),StaticRoute("0.0.0.0/0", "192.148.3.8")])
        #self.addSubnet(nodes=[MyServer1, rbx_g2_nc5], subnets=["192.148.0.4/30","2001:41D0:0:0008::/64"])

        #self.addSubnet(nodes=[MyServer2, rbx_g1_nc5], subnets=["192.148.0.8/30","2001:41D0:0:0009::/64"])
        self.addSubnet(nodes=[MyServer2, rbx_g2_nc5], subnets=["192.148.0.12/30","2001:41D0:0:000A::/64"])
        MyServer2.addDaemon(STATIC, static_routes=[StaticRoute("::/0", "2001:41D0:0:000A::2"),StaticRoute("0.0.0.0/0", "192.148.3.9")])

        #self.addSubnet(nodes=[MyServer3, fra_fr5_sbb1_nc5], subnets=["192.148.0.16/30","2001:41D0:0:000B::/64"])
        self.addSubnet(nodes=[MyServer3, fra_fr5_sbb2_nc5], subnets=["192.148.0.20/30","2001:41D0:0:000C::/64"])
        MyServer3.addDaemon(STATIC, static_routes=[StaticRoute("::/0", "2001:41D0:0:000C::2"),StaticRoute("0.0.0.0/0", "192.148.3.5")])

        servers = [MyServer1, MyServer2, MyServer3]

        self.setup_servers(servers)
        self.addLinks((MyServer1, rbx_g1_nc5),# (MyServer1, rbx_g2_nc5),
                      (MyServer2, rbx_g2_nc5),# (MyServer2, rbx_g1_nc5),
                      (MyServer3, fra_fr5_sbb2_nc5))#, (MyServer3, fra_fr5_sbb1_nc5))#


        set_rr(self, rr=rbx_g2_nc5, peers=[par_gsw_sbb1_nc5, par_th2_sbb1_nc5,lon_thw_sbb1_nc5, lon_drch_sbb1_nc5, MyServer2])#, MyServer1])#
        set_rr(self, rr=rbx_g1_nc5, peers=[par_gsw_sbb1_nc5, par_th2_sbb1_nc5,lon_thw_sbb1_nc5, lon_drch_sbb1_nc5, MyServer1])#, MyServer2])#
        set_rr(self, rr=gra_g1_nc5, peers=[gra_g2_nc5, rbx_g1_nc5, rbx_g2_nc5,fra_fr5_sbb1_nc5,fra_fr5_sbb2_nc5])
        set_rr(self, rr=gra_g2_nc5, peers=[gra_g1_nc5, rbx_g1_nc5, rbx_g2_nc5,fra_fr5_sbb1_nc5,fra_fr5_sbb2_nc5])
        set_rr(self, rr=fra_fr5_sbb1_nc5, peers=[fra_1_n7, fra_5_n7])#, MyServer3])#
        set_rr(self, rr=fra_fr5_sbb2_nc5, peers=[fra_1_n7, fra_5_n7, MyServer3])#

        #self.addiBGPFullMesh(1, routers=routers+servers)
        self.addAS(16276, routers=routers+servers)


        '''********************   ADDING EXTERNAL AS     **********************************'''

        google_r1=self.addRouter("google_r1",config=RouterConfig,lo_addresses=["2001:4860:0:1::/64","8.8.4.1/32"])
        google_r2=self.addRouter("google_r2",config=RouterConfig,lo_addresses=["2001:4860:0:2::/64","8.8.4.2/32"])
        google_r3=self.addRouter("google_r3",config=RouterConfig,lo_addresses=["2001:4860:0:3::/64","8.8.4.3/32"])

        self.addLinks((par_gsw_sbb1_nc5,google_r1),(fra_5_n7,google_r3),(par_th2_sbb1_nc5,google_r2),
                        (google_r1,google_r2),(google_r1,google_r3),(google_r3,google_r2))

        self.addiBGPFullMesh(15169, routers=[google_r1,google_r2,google_r3])
        #self.addAS(15169,routers=[google_r1,google_r2,google_r3])

        self.addSubnet(nodes=[par_gsw_sbb1_nc5,google_r1], subnets=["2001:41D0:0:1F08::/64","192.148.2.88/30"])
        self.addSubnet(nodes=[fra_5_n7,google_r3], subnets=["2001:41D0:0:1F09::/64","192.148.2.92/30"])
        self.addSubnet(nodes=[par_th2_sbb1_nc5,google_r2], subnets=["2001:41D0:0:1F0A::/64", "192.148.2.96/30"])

        ebgp_session(self,par_gsw_sbb1_nc5,google_r1)
        ebgp_session(self,fra_5_n7,google_r3)
        ebgp_session(self,par_th2_sbb1_nc5,google_r2)

        self.setup_routers([google_r1,google_r2,google_r3])


        vodafone_r1=self.addRouter("voda_r1",config=RouterConfig,lo_addresses=["2001:5000:0:1::/64","2.16.35.1/32"])
        vodafone_r2=self.addRouter("voda_r2",config=RouterConfig,lo_addresses=["2001:5000:0:2::/64","2.16.35.2/32"])
        vodafone_r3=self.addRouter("voda_r3",config=RouterConfig,lo_addresses=["2001:5000:0:3::/64","2.16.35.3/32"])
        vodafone_r4=self.addRouter("voda_r4",config=RouterConfig,lo_addresses=["2001:5000:0:4::/64","2.16.35.4/32"])

        #self.addAS(1273,routers=[vodafone_r1,vodafone_r2,vodafone_r3,vodafone_r4])
        self.addLinks((par_th2_sbb1_nc5,vodafone_r2),(fra_5_n7,vodafone_r4),(fra_1_n7,vodafone_r3),(par_gsw_sbb1_nc5,vodafone_r1),
                        (vodafone_r1,vodafone_r2),(vodafone_r2,vodafone_r3),(vodafone_r3,vodafone_r4),(vodafone_r4,vodafone_r1),
                        (vodafone_r2,vodafone_r4))
        self.addiBGPFullMesh(1273,routers=[vodafone_r1,vodafone_r2,vodafone_r3,vodafone_r4])

        self.addSubnet(nodes=[par_gsw_sbb1_nc5,vodafone_r1], subnets=["192.148.2.112/30", "2001:41D0:0:1F0E::/64"])
        self.addSubnet(nodes=[fra_1_n7,vodafone_r3], subnets=["192.148.2.108/30", "2001:41D0:0:1F0D::/64"])
        self.addSubnet(nodes=[fra_5_n7,vodafone_r4], subnets=["192.148.2.104/30", "2001:41D0:0:1F0C::/64"])
        self.addSubnet(nodes=[par_th2_sbb1_nc5,vodafone_r2], subnets=["192.148.2.100/30", "2001:41D0:0:1F0B::/64"])
        ebgp_session(self,par_th2_sbb1_nc5,vodafone_r2)
        ebgp_session(self,fra_5_n7,vodafone_r4 )
        ebgp_session(self,fra_1_n7,vodafone_r3 )
        ebgp_session(self,par_gsw_sbb1_nc5,vodafone_r1 )

        self.setup_routers([vodafone_r1,vodafone_r2,vodafone_r3,vodafone_r4])



        cogent_r1=self.addRouter("cogent_r1",config=RouterConfig,lo_addresses=["2001:550:0:1::/64","2.58.4.1/32"])
        cogent_r2=self.addRouter("cogent_r2",config=RouterConfig,lo_addresses=["2001:550:0:2::/64","2.58.4.2/32"])
        cogent_r3=self.addRouter("cogent_r3",config=RouterConfig,lo_addresses=["2001:550:0:3::/64","2.58.4.3/32"])
        #self.addAS(174,routers=[cogent_r1,cogent_r2,cogent_r3])
        self.addLinks((par_gsw_sbb1_nc5,cogent_r1),(lon_thw_sbb1_nc5,cogent_r3),(par_th2_sbb1_nc5,cogent_r2),
                        (cogent_r1,cogent_r2),(cogent_r2,cogent_r3),(cogent_r3,cogent_r1))

        self.addiBGPFullMesh(174,routers=[cogent_r1,cogent_r2,cogent_r3])

        self.addSubnet(nodes=[par_th2_sbb1_nc5,cogent_r2], subnets=["192.148.2.124/30", "2001:41D0:0:1F11::/64"])
        self.addSubnet(nodes=[lon_thw_sbb1_nc5,cogent_r3], subnets=["192.148.2.120/30", "2001:41D0:0:1F10::/64"])
        self.addSubnet(nodes=[par_gsw_sbb1_nc5,cogent_r1], subnets=["192.148.2.116/30", "2001:41D0:0:1F0F::/64"])
        ebgp_session(self,par_gsw_sbb1_nc5,cogent_r1 )
        ebgp_session(self,lon_thw_sbb1_nc5,cogent_r3 )
        ebgp_session(self,par_th2_sbb1_nc5,cogent_r2 )

        self.setup_routers([cogent_r1,cogent_r2,cogent_r3])


        telia_r1=self.addRouter("telia_r1",config=RouterConfig,lo_addresses=["2001:2000:0:1::/64","2.255.248.1/32"])
        telia_r2=self.addRouter("telia_r2",config=RouterConfig,lo_addresses=["2001:2000:0:2::/64","2.255.248.2/32"])
        telia_r3=self.addRouter("telia_r3",config=RouterConfig,lo_addresses=["2001:2000:0:3::/64","2.255.248.3/32"])

        #self.addAS(1299,routers=[telia_r1,telia_r2,telia_r3])
        self.addLinks((fra_5_n7,telia_r2),(fra_1_n7,telia_r1),(lon_thw_sbb1_nc5,telia_r3),
                        (telia_r1,telia_r2),(telia_r2,telia_r3),(telia_r3,telia_r1))

        self.addiBGPFullMesh(1299,routers=[telia_r1,telia_r2,telia_r3])

        self.addSubnet(nodes=[fra_5_n7,telia_r2], subnets=["192.148.2.128/30", "2001:41D0:0:1F12::/64"])
        self.addSubnet(nodes=[fra_1_n7,telia_r1], subnets=["192.148.2.132/30", "2001:41D0:0:1F13::/64"])
        self.addSubnet(nodes=[lon_thw_sbb1_nc5,telia_r3], subnets=["192.148.2.136/30", "2001:41D0:0:1F14::/64"])
        ebgp_session(self,fra_5_n7,telia_r2 )
        ebgp_session(self,fra_1_n7,telia_r1 )
        ebgp_session(self,lon_thw_sbb1_nc5,telia_r3 )

        self.setup_routers([telia_r1,telia_r2,telia_r3])


        amazon_r1=self.addRouter("amazon_r1",config=RouterConfig,lo_addresses=["2001:4f8:b:0:1::/64","3.5.128.1/32"])
        amazon_r2=self.addRouter("amazon_r2",config=RouterConfig,lo_addresses=["2001:4f8:b:0:2::/64","3.5.128.2/32"])
        #self.addAS(16509,routers=[amazon_r1,amazon_r2])
        self.addLinks((lon_thw_sbb1_nc5,amazon_r2),(par_th2_sbb1_nc5,amazon_r1),
                        (amazon_r1,amazon_r2))

        self.addiBGPFullMesh(16509,routers=[amazon_r1,amazon_r2])


        self.addSubnet(nodes=[par_th2_sbb1_nc5,amazon_r1], subnets=["192.148.2.140/30", "2001:41D0:0:1F15::/64"])
        self.addSubnet(nodes=[lon_thw_sbb1_nc5,amazon_r2], subnets=["192.148.2.144/30", "2001:41D0:0:1F16::/64"])
        ebgp_session(self,par_th2_sbb1_nc5,amazon_r1 )
        ebgp_session(self,lon_thw_sbb1_nc5,amazon_r2 )

        self.setup_routers([amazon_r1,amazon_r2])#,vodafone,cogent,telia,amazon])

        '''********************   communities     **********************************'''
        #google_r1.get_config(BGP).set_community(community='16276:7100',to_peer=par_gsw_sbb1_nc5)
        '''********************   NOT ANNOUNCED TO     **********************************'''

        lon_thw_sbb1_nc5.get_config(BGP).set_community(community='16276:2010', from_peer=telia_r3)
        lon_thw_sbb1_nc5.get_config(BGP).set_community(community='16276:2020', from_peer=cogent_r3)
        lon_thw_sbb1_nc5.get_config(BGP).set_community(community='16276:2050', from_peer=amazon_r2)

        fra_1_n7.get_config(BGP).set_community(community='16276:2030', from_peer=vodafone_r3)
        fra_1_n7.get_config(BGP).set_community(community='16276:2010', from_peer=telia_r1)

        fra_5_n7.get_config(BGP).set_community(community='16276:2040', from_peer=google_r3)
        fra_5_n7.get_config(BGP).set_community(community='16276:2030', from_peer=vodafone_r4)
        fra_5_n7.get_config(BGP).set_community(community='16276:2010', from_peer=telia_r2)

        par_gsw_sbb1_nc5.get_config(BGP).set_community(community='16276:2020', from_peer=cogent_r1)
        par_gsw_sbb1_nc5.get_config(BGP).set_community(community='16276:2040', from_peer=google_r1)
        par_gsw_sbb1_nc5.get_config(BGP).set_community(community='16276:2010', from_peer=vodafone_r1)

        par_th2_sbb1_nc5.get_config(BGP).set_community(community='16276:2040', from_peer=google_r2)
        par_th2_sbb1_nc5.get_config(BGP).set_community(community='16276:2020', from_peer=cogent_r2)
        par_th2_sbb1_nc5.get_config(BGP).set_community(community='16276:2050', from_peer=amazon_r1)
        par_th2_sbb1_nc5.get_config(BGP).set_community(community='16276:2030', from_peer=vodafone_r2)


        '''********************   Learn from     **********************************'''

        lon_thw_sbb1_nc5.get_config(BGP).set_community(community='16276:100',from_peer=[telia_r3,cogent_r3,amazon_r2])
        fra_1_n7.get_config(BGP).set_community(community='16276:100',from_peer=[vodafone_r3,telia_r1])
        fra_1_n7.get_config(BGP).set_community(community='16276:100',from_peer=[google_r3,vodafone_r3,telia_r2])
        fra_1_n7.get_config(BGP).set_community(community='16276:100',from_peer=[cogent_r1,google_r1,vodafone_r1])
        fra_1_n7.get_config(BGP).set_community(community='16276:100',from_peer=[google_r2,cogent_r2,amazon_r1,vodafone_r2])


        '''********************   ROUTE POLICIES     **********************************'''

        lon_thw_sbb1_nc5.get_config(BGP).deny(to_peer=[telia_r3],matching=[CommunityList(community='16276:2010')])
        lon_thw_sbb1_nc5.get_config(BGP).deny(to_peer=[cogent_r3],matching=[CommunityList(community='16276:2020')])
        lon_thw_sbb1_nc5.get_config(BGP).deny(to_peer=[amazon_r2],matching=[CommunityList(community='16276:2050')])

        fra_1_n7.get_config(BGP).deny(to_peer=[vodafone_r3],matching=[CommunityList(community='16276:2030')])
        fra_1_n7.get_config(BGP).deny(to_peer=[telia_r1],matching=[CommunityList(community='16276:2010')])

        fra_5_n7.get_config(BGP).deny(to_peer=[google_r3],matching=[CommunityList(community='16276:2040')])
        fra_5_n7.get_config(BGP).deny(to_peer=[vodafone_r4],matching=[CommunityList(community='16276:2030')])
        fra_5_n7.get_config(BGP).deny(to_peer=[telia_r2],matching=[CommunityList(community='16276:2030')])

        par_gsw_sbb1_nc5.get_config(BGP).deny(to_peer=[cogent_r1],matching=[CommunityList(community='16276:2020')])
        par_gsw_sbb1_nc5.get_config(BGP).deny(to_peer=[google_r1],matching=[CommunityList(community='16276:2040')])
        par_gsw_sbb1_nc5.get_config(BGP).deny(to_peer=[vodafone_r1],matching=[CommunityList(community='16276:2030')])

        par_th2_sbb1_nc5.get_config(BGP).deny(to_peer=[google_r2],matching=[CommunityList(community='16276:2040')])
        par_th2_sbb1_nc5.get_config(BGP).deny(to_peer=[cogent_r2],matching=[CommunityList(community='16276:2020')])
        par_th2_sbb1_nc5.get_config(BGP).deny(to_peer=[amazon_r1],matching=[CommunityList(community='16276:2050')])
        par_th2_sbb1_nc5.get_config(BGP).deny(to_peer=[vodafone_r2],matching=[CommunityList(community='16276:2030')])


        '''********************   CUSTOM LOCAL-PREF     **********************************'''
        '''
        setlocalPrefs(lon_thw_sbb1_nc5,LOCAL_PREFS,fromPeer=telia_r3,ipv4='2.255.248.3/32',ipv6='2001:2000:0:3::')
        setlocalPrefs(lon_thw_sbb1_nc5,LOCAL_PREFS,fromPeer=amazon_r2,ipv4='3.5.128.2/32',ipv6='2001:4f8:b:0:2::')
        setlocalPrefs(lon_thw_sbb1_nc5,LOCAL_PREFS,fromPeer=cogent_r3,ipv4='2.58.4.3/32',ipv6='2001:550:0:3::')

        #setlocalPrefs(fra_1_n7,LOCAL_PREFS,fromPeer=vodafone_r3,ipv4='2.16.35.3/32',ipv6='2001:5000:0:3::')
        #setlocalPrefs(fra_1_n7,LOCAL_PREFS,fromPeer=telia_r1,ipv4='2.255.248.1/32',ipv6='2001:2000:0:1::')

        #setlocalPrefs(fra_5_n7,LOCAL_PREFS,fromPeer=google_r3,ipv4='8.8.4.3/32',ipv6='2001:4860:0:3::')
        #setlocalPrefs(fra_5_n7,LOCAL_PREFS,fromPeer=vodafone_r4,ipv4='2.16.35.4/32',ipv6='2001:5000:0:4::')
        #setlocalPrefs(fra_5_n7,LOCAL_PREFS,fromPeer=telia_r2,ipv4='2.255.248.2/32',ipv6='2001:2000:0:2::')

        #setlocalPrefs(par_gsw_sbb1_nc5,LOCAL_PREFS,fromPeer=cogent_r1,ipv4='2.58.4.1/32',ipv6='2001:550:0:1::/64')
        #setlocalPrefs(par_gsw_sbb1_nc5,LOCAL_PREFS,fromPeer=google_r1,ipv4='8.8.4.1/32',ipv6='2001:4860:0:1::/64')
        #setlocalPrefs(par_gsw_sbb1_nc5,LOCAL_PREFS,fromPeer=vodafone_r1,ipv4='2.16.35.1/32',ipv6='2001:5000:0:1::/64')

        setlocalPrefs(par_th2_sbb1_nc5,LOCAL_PREFS,fromPeer=google_r2,ipv6='2001:4860:0:1::',ipv4='8.8.4.2/32')
        setlocalPrefs(par_th2_sbb1_nc5,LOCAL_PREFS,fromPeer=cogent_r2,ipv4='2.58.4.2/32',ipv6='2001:550:0:2::')
        setlocalPrefs(par_th2_sbb1_nc5,LOCAL_PREFS,fromPeer=amazon_r1,ipv4='3.5.128.1/32',ipv6='2001:4f8:b:0:1::')
        setlocalPrefs(par_th2_sbb1_nc5,LOCAL_PREFS,fromPeer=vodafone_r2,ipv4='2.16.35.2/32',ipv6='2001:5000:0:2::')
        '''

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


        super().build(*args, **kwargs)
def setLocalPref(router,localPref,communityNbr,fromPeer,ipv4,ipv6):
    router.get_config(BGP).set_local_pref(local_pref=localPref,
        from_peer=fromPeer,
        matching=[
            CommunityList(community=communityNbr),
            AccessList(entries=[AccessListEntry(prefix=ipaddress.IPv4Network(ipv4)),AccessListEntry(prefix=ipaddress.IPv6Network(ipv6))])
        ])

def setlocalPrefs(router,localPrefCommList,fromPeer,ipv4,ipv6):
    for e in localPrefCommList:
        setLocalPref(router,localPref=e[1],communityNbr=e[0],fromPeer=fromPeer,ipv4=ipv4,ipv6=ipv6)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=MyTopology(), allocate_IPs=True)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
