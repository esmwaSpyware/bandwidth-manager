# network/snmp_utils.py
from pysnmp.hlapi import *

def get_snmp_data(ip, community, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            return varBind[1]

# Usage example:
# incoming_traffic = get_snmp_data('192.168.1.1', 'public', '1.3.6.1.2.1.2.2.1.10.1')
