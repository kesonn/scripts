#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException


# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    parsed = None
    nmproc = NmapProcess(targets, options)
    nmproc.run_background()
    while nmproc.is_running():
        print("Nmap Scan running: ETC: {0} DONE: {1}%".format(nmproc.etc,nmproc.progress))
        time.sleep(2)

    rc = nmproc.rc
    if rc != 0:
        print("nmap scan failed: {0}".format(nmproc.stderr))
    print(type(nmproc.stdout))
    open('sasdsa','w').write(nmproc.stdout)

    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))

    return parsed


# print scan results from a nmap report
def print_scan(nmap_report):
    print("Starting Nmap {0} ( http://nmap.org ) at {1}".format(
        nmap_report.version,
        nmap_report.started))

    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        print("Nmap scan report for {0} ({1})".format(
            tmp_host,
            host.address))
        print("Host is {0}.".format(host.status))
        print("  PORT     STATE         SERVICE         script")

        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
            #if len(serv.banner):
            #    pserv += " ({0})".format(serv.scripts_results)
            if len(serv.scripts_results) > 0:
                pserv += serv.scripts_results[0]['output']
            print(pserv)
    print(nmap_report.summary)


if __name__ == "__main__":
    #options = '-sT -P0 -sV -O --script=banner'
    #report = do_scan("127.0.0.1", options)
    #if report:
    report = open('sasdsa','r').read()
    print_scan(NmapParser.parse(report))
    #else:
    #    print("No results returned")