#!/usr/bin/python

'''
Faraday Penetration Test IDE
Copyright (C) 2013  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

'''
from datetime import date

class CSVVulnStatusReport(object):
    """Class to build CSV Vulnerability Status Report
    Expected output from this object is a file with model objects flatten
    """
    def __init__(self, path, modelobjects):
        self.path = path
        self.modelobjects = modelobjects 

    #(self,ip,port,protocol,name,desc,severity,type):
    def getVulnCSVField(self, host, vuln, serv = None):
        vdate = str(date.fromtimestamp(vuln.getMetadata().create_time))
        status = 'vuln'
        level = str(vuln.severity)
        name = vuln.name
        vtype = '1'
        target = host.name + ( ':' + ','.join([ str(x) for x in serv.getPorts()]) if serv else '')
        if vuln.class_signature == "VulnerabilityWeb":
            vtype = '2'
        desc = vuln.desc.replace('\n', '<br/>')  if vuln.desc else ""
        desc = desc.replace(',', '&nbsp;')

        csv_fields = [ vdate , host.name ,' '.join([ str(x) for x in serv.getPorts()]) if serv else '', serv.getProtocol() if serv else "",  name, desc, level , vtype]
        
        
        try:
            encoded_csv_fields = map(lambda x: x.encode('utf-8'), csv_fields) 
        except Exception as e:  
            print e

        field = "|".join(encoded_csv_fields)
        return field

    def createCSVVulnStatusReport(self):
        hosts = self.modelobjects
        filename = self.path

        if filename and filename is not None:
            with open(self.path + ".csv","w") as f: 
                # Date, status, Level, Name, Target, Description
                vulns_list = [] 
                for host in hosts:
                    # Get al HostVulns
                    for v in host.getVulns(): 
                        vulns_list.append(self.getVulnCSVField(host, v))

                    # Service Vulns, we don't have Interface vulns
                    for i in host.getAllInterfaces():
                        for s in i.getAllServices():
                            for v in s.getVulns(): 
                                vulns_list.append(self.getVulnCSVField(host, v, s))
                f.writelines('\n'.join(vulns_list))
                f.write('\n')
