ip = '192.168.43.220'
name = 'localhost'

from .models import Client

def ClientExists (ipaddress, hostname):
    client = Client.query.filter_by(ip=ipaddress, hostname=hostname).first()
    if client:
        return True
    else:
        return False
    
# def VerifyClientVote ()