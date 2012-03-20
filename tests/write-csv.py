import csv, glob, random, string, re
from collections import defaultdict
#from lxml import etree

hashes = []

def gen_hash(N=20):
    h = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
    if h in hashes:
        h = gen_hash(N)
    return h


G = glob.glob("/scratch/scratch2/agong/blogspot-xml-batch-1/html/*.html")
print len(G)
random.shuffle(G)


C = csv.writer(file("/users/agong/Desktop/blogspot-s3-batch-1.csv", 'w'))
C.writerow( ['id', 'hash', 'blog_url', 'seq', 'filename', 'parser'] )

D = defaultdict(list)

for i in range(len(G)):
    filename = G[i].split('/')[-1]
    blog_url = '-'.join(filename.split('-')[:-1])
    seq = filename.split('-')[-1].split('.html')[0]
    
    row = [i, gen_hash(), blog_url, seq, filename, 'BlogspotParserA']
    C.writerow(row)

    D[blog_url].append(row)
    if not i%10000: print i
#    print '\t'.join([str(c) for c in row])

R = []
for b in D:
    post_list = D[b]
    random.shuffle(post_list)
    for post in post_list[:3]:
        R.append(post)

C = csv.writer(file("/users/agong/Desktop/blogspot-s3-batch-1-sample-1.csv", 'w'))
C.writerow( ['id', 'hash', 'blog_url', 'seq', 'filename', 'parser'] )

random.shuffle(R)        
for row in R:        
    C.writerow(row)
