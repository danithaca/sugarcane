#! /usr/bin/env python
import math, random, time, subprocess, datetime
import Queue
import multiprocessing as mp

### Global variables ##########################################################

pending_log = 'logs/pending.txt'
complete_log = 'logs/complete.txt'
num_workers = 100
logWorker_delay = 2

def genCommandString( blog_url, blog_mirror_path, log_file ):
#        command_string = 'wget -mk http://'+blog_url+' -w 5 -t 3 -T 30 -l 0 -P '+blog_mirror_path+' -o '+log_file
#        command_string = 'wget -mk http://'+blog_url+' -w 1 -t 2 -T 15 -l 0 -P '+blog_mirror_path+' -o '+log_file
#        command_string = 'wget -r -N -l 4 --no-remove-listing -R mpg,mpeg,au,mp3,gif,png,jpeg,jpg,zip,tar,gz,gzip -k http://'+blog_url+' -w 1 -t 2 -T 15 -l 0 -P '+blog_mirror_path+' -o '+log_file
    return 'wget -r -N -l 3 --no-remove-listing -R mpg,mpeg,au,mp3,gif,png,jpeg,jpg,zip,tar,gz,gzip -k http://'+blog_url+' -w 1 -t 2 -T 15 -l 0 -P '+blog_mirror_path+' -o '+log_file

###############################################################################

class BlogWorker(mp.Process):
    def __init__(self, work_queue, log_queue, active_workers):
        # base class initialization
        mp.Process.__init__(self)
 
        # job management stuff
        self.work_queue = work_queue
        self.log_queue = log_queue
        self.kill_received = False
        self.active_workers = active_workers

        #Count me as active!
        self.active_workers.value += 1
                   
    def getBlog(self, blog_url):
        scratch_disks = ["1","2","3","4","5"]
        blog_path = '/scratch/unmirrored'+scratch_disks[hash(blog_url)%len(scratch_disks)]+'/agong/blog_crawl_2012_01/'
        blog_mirror_path = blog_path+'mirrors/'
        blog_log_path = blog_path+'logs/'
        log_file = blog_log_path + blog_url + '.log'

        command_string = genCommandString( blog_url, blog_mirror_path, log_file )

#        time.sleep(float(random.uniform(.1,3)))
#        return( command_string, "" )
#        return ( "A", "Z" )
        
        p = subprocess.Popen( ["-c", command_string], shell=True )
        p.wait()
        return (blog_mirror_path+blog_url, log_file)

 
    def run(self):
        while not self.kill_received: 
            # get a task
            try:
                job = self.work_queue.get_nowait()
            except Queue.Empty:
                #I'm quitting -- remove me from the active count
                self.active_workers.value -= 1
                break
 
            #Punch in
            start_time = datetime.datetime.now()
            self.log_queue.put({"status":"Start","info":{
                "blog_url" : job,
                "start_time" : start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }})
            
            # the actual processing
            #(file_path, log_file) = self.shillyShally(job)
            (file_path, log_file) = self.getBlog(job)
 
            #Punch out
            end_time = datetime.datetime.now()
            self.log_queue.put({"status":"Done","info":{
                "blog_url" : job,
                "file_path" : file_path,
                "log_file" : log_file,
                "start_time" : start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time" : end_time.strftime("%Y-%m-%d %H:%M:%S"),
            }})

###############################################################################

class LogWorker(mp.Process):
    def __init__(self, log_queue, active_workers):
        # base class initialization
        mp.Process.__init__(self)
 
        # job management stuff
        self.log_queue = log_queue
        self.kill_received = False
        self.active_workers = active_workers
        
    def rewritePendingLog(self, pending):
        p_log = file(pending_log,'w')
        for p in pending:
            p_log.write( p + '\t' + pending[p] + '\n' )
        p_log.close()
 
    def run(self):
        pending = {}#'placeholder' : ''}
        time_to_quit = False
        
        while not self.kill_received:
            # get a task
            try:
                message = self.log_queue.get_nowait()
                time_to_quit = False

                #Store to log
                url = message["info"]["blog_url"]
                start_time = message["info"]["start_time"]

                if message["status"] == "Start":
                    pending[url] = start_time
                    self.rewritePendingLog( pending )
                
                elif message["status"] == "Done":
                    del pending[url]
                    self.rewritePendingLog( pending )
                    
                    fields = ["blog_url","start_time","end_time","file_path","log_file"]
                    out_log = file(complete_log,'a').write( '\t'.join( [ message["info"][f] for f in fields ] ) + '\n' )
            
            except Queue.Empty:
                if time_to_quit:
                    break

                time.sleep(logWorker_delay)
                if self.active_workers.value == 0:
                    time_to_quit = True
            
            except:
                print '=== Error! ============================================='
                print 'There was a bad error in log Worker.  Here\'s what I know about it:'
                print message
                print '========================================================'
                

##############################################################################


#generate jobs
jobs = file('blog_list.txt', 'r').read().split('\n')

# load up work queue
work_queue = mp.Queue()
for job in jobs:
    work_queue.put(job)

# create a queue to pass to workers to handling logging
log_queue = mp.Queue()


active_workers = mp.Value('d', 0)

# spawn blog workers
for i in range(num_workers):
    worker = BlogWorker(work_queue, log_queue, active_workers)
    worker.start()

# spawn log worker
log_worker = LogWorker(log_queue, active_workers)
log_worker.start()

