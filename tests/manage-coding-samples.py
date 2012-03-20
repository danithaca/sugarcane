import argh, sys, re, glob

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError


my_key = 'AKIAJIMVWPM2A3FHV25A'
secret_key = '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'
conn = S3Connection(my_key, secret_key)

batch_prefix = my_key.lower()+'-jcd-'

def list_batches(args):
    buckets = conn.get_all_buckets()

    for bucket in buckets:
        name = bucket.name
        if re.match(name, batch_prefix):
            print name

@argh.arg('batch_name', help='Name for the new batch')
@argh.arg('--path', default=None, help='A path to a directory of files to upload')
@argh.arg('--globstring', default=None, help='Glob syntax to be appended to path.  (Use quotes.)')
@argh.arg('--xml', default=None, help='An xml file containing posts, etc. to upload')
@argh.arg('--overwrite', default=False, help='Overwrite an existing batch of the same name?')
def upload_new_batch(args):

    if not args.path and not args.xml:
        print "You must specify EITHER a path OR an xml file"
#        return 0

    bucket_name = batch_prefix+args.batch_name

    try:
#    if 1:
        print 'Checking to see if bucket', bucket_name, 'already exists'
        bucket = conn.get_bucket(bucket_name)

        if not args.overwrite:
            print "Bucket already exists.  If you're SURE you want to overwrite, use the --overwrite flag.  This will delete all existing contents"
            return 0
        else:
            bucket.delete()
            print "Bucket deleted..."

    except S3ResponseError:
        print "Bucket does not exist yet..."

    bucket = conn.create_bucket(bucket_name)
    print 'Bucket created...'

    #!!Need to enable bucket website endpoint
    #!!Need to configure bucket permission policy
    bucket.set_acl('public-read')

    bucket.configure_website('index.html')

    policy_json = file('bucket_policy.json', 'r').read()
    policy_json = re.sub('BUCKET_NAME', bucket_name, policy_json)
    bucket.set_policy(policy_json)

    print 'http://'+bucket.get_website_endpoint()

    if args.globstring == None:
        args.globstring = '*'
    else:
        print '!'
        print args.globstring

    print args.path+args.globstring

    filename_list = glob.glob(args.path+args.globstring)
    print len(filename_list), 'files found in path', args.path

    aws_domain = bucket_name+'.s3-website-us-east-1.amazonaws.com/'
    outfile = file(args.batch_name+'-index.txt', 'w')

    k = Key(bucket)
    for f in filename_list[:10]:
        filename = f.split(args.path)[1]

        print '\tUploading file', filename, '...'
        k.key = filename
        k.set_contents_from_filename(f)
        #!!Add meta fields to key
        k.copy(bucket_name, k.key, metadata={'Content-Type': 'text/html', 'Cache-Control' : 'max-age=3601'}, preserve_acl=True)

        outfile.write(aws_domain+filename)

    outfile.close()

    #!Upload CSS file

    #Upload index file
    k.key = 'index.html'
    k.set_contents_from_filename(args.batch_name+'-index.txt')
    k.copy(bucket_name, k.key, metadata={'Content-Type': 'text/html', 'Cache-Control' : 'max-age=3601'}, preserve_acl=True)
    
    print 'http://'+bucket.get_website_endpoint()

@argh.arg('batch_name', help='The batch name')
def describe_batch(args):    
    bucket_name = batch_prefix+args.batch_name

    try:
        print 'Checking to see if bucket', bucket_name, 'already exists...'
        bucket = conn.get_bucket(bucket_name)

        keys = bucket.get_all_keys()
        for k in keys:
            print k.name

    except S3ResponseError:
        print 'Bucket', bucket_name, 'does not exist.'

def main(argv=None):
    p = argh.ArghParser()
    p.add_commands([list_batches, describe_batch, upload_new_batch])
    p.dispatch()

if __name__=='__main__':
    status = main(sys.argv)
    sys.exit(status)
    
