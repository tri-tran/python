import dns.resolver
import csv

domains = []
with open('domain.list') as f:
    domains = [x.strip() for x in f.readlines()]

def nslookup(domain, r_type):
    try:
        r_data = dns.resolver.query(domain, r_type)
    except:
        return '-'

    #print(domain, list(r_data))
    if len(r_data) > 3:
        return '-'

    return ';'.join([str(x).endswith('.') and str(x)[:-1] or str(x) for x in r_data])

with open('result.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for d in domains:
        cname = ''
        a_record = ''
        aaaa_record = ''

        if d.startswith('www'):
            cname = nslookup(d, 'CNAME')
            a_record = nslookup(d[4:], 'A')
            aaaa_record = nslookup(d[4:], 'AAAA')
        else:
            cname = nslookup('www.' + d, 'CNAME')
            a_record = nslookup(d, 'A')
            aaaa_record = nslookup(d, 'AAAA')
        
        to_print = [d, cname, a_record, aaaa_record]
        writer.writerow(to_print)

