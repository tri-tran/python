import dns.resolver
import csv

EMPTY = '-'
GOOGLE_IPV4 = "35.201.83.130"
GOOGLE_IPV6 = "2600:1901:0:8a57::"

domains = []
with open('domain.list') as f:
    domains = [x.strip() for x in f.readlines()]

def nslookup(domain, r_type):
    try:
        r_data = dns.resolver.query(domain, r_type)
    except Exception as e:
        print('> %s' % domain)
        print(e)
        return EMPTY

    #print(domain, list(r_data))
    if len(r_data) > 3:
        return EMPTY

    return ';'.join(set([str(x).endswith('.') and str(x)[:-1] or str(x) for x in r_data]))

with open('result.csv', 'w', newline='') as csvfile:
    result_writer = csv.writer(csvfile)
    for d in domains:
        cname = ''
        a_record = ''
        aaaa_record = ''

        cname = nslookup(d, 'CNAME')
        
        if d.startswith('www.'):
            a_record = nslookup(d[4:], 'A')
            aaaa_record = nslookup(d[4:], 'AAAA')
        else:
            a_record = nslookup(d, 'A')
            aaaa_record = nslookup(d, 'AAAA')
            
            if (cname == EMPTY):
                cname = nslookup('www.' + d, 'CNAME')
            else:
                cname_a = nslookup(cname, 'A')
                cname_aaaa = nslookup(cname, 'AAAA')
                if cname_a == a_record:
                    a_record = EMPTY
                if cname_aaaa == aaaa_record:
                    aaaa_record = EMPTY

        fix_ips = 'FALSE'        
        if not (a_record == EMPTY or a_record == GOOGLE_IPV4):
            fix_ips = 'TRUE'
        if not (aaaa_record == GOOGLE_IPV6 or aaaa_record == EMPTY):
            fix_ips = 'TRUE'

        to_print = [d, cname, a_record, aaaa_record, fix_ips]
        result_writer.writerow(to_print)

