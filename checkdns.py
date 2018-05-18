import dns.resolver

domains = []
with open('domain.list') as f:
    domains = [x.strip() for x in f.readlines()]

for d in domains:
    print(d)
    cname_data = dns.resolver.query(d, 'CNAME')
    cnames = [str(x) for x in cname_data]

    print(d, cnames)
    break