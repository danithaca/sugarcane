from multiprocessing import Process, Queue, Pool, cpu_count, managers#, Value, Array
from multiprocessing.managers import SyncManager
import csv, os, threading, time, re, urllib2, shutil
import datetime

def currentTime():
	return datetime.datetime.now()

### Parameters ###############################################################

class Parameters:
	def __init__( self, wave_size=100, time_inc=1, time_limit=10,
		save_states=False, save_files=False, save_edges=False,
		csv_header=[],
		prioritize_urls=False,
		process_url_function=None,
		decide_terminate_function=None,
		processing_params=None):

		self.wave_size = wave_size

		self.time_inc = time_inc
		self.time_limit = time_limit

		self.save_states = save_states
		self.save_files = save_files
		self.save_edges = save_edges

		self.csv_header = csv_header
		self.prioritize_urls = prioritize_urls

		self.process_url_function = process_url_function
		self.decide_terminate_function = decide_terminate_function

		if process_url_function == None:
			self.process_url_function = null_processor
		else: self.process_url_function = process_url_function

		if decide_terminate_function == None:
			self.decide_terminate_function = default_decider
		else: self.decide_terminate_function = decide_terminate_function

		self.processing_params = processing_params

	def __str__(self):
		return (
			'\twave_size\t' + str(self.wave_size) + '\n' +
			'\ttime_inc\t' + str(self.time_inc) + '\n' +
			'\ttime_limit\t' + str(self.time_limit) + '\n' +
			'\tsave_files\t' + str(self.save_states) + '\n' +
			'\tsave_files\t' + str(self.save_files) + '\n' +
			'\tsave_edges\t' + str(self.save_edges) + '\n'
			)

	def save(self, file_name ):
		F = file( file_name, 'w' )
		F.write( self.__str__() )
		F.close()

	def returnSelf(self):
		#This command is used to pass Parameter objects from server to client
		return self



### Crawlers #################################################################

class SoloCrawler:
	def __init__(self):
		print '='*79
		print '=== Launching SoloCrawler ... ====='

	def runUntilDone(self, path, parameters, master_list={}, seed_list=[], current_wave=None, overwrite_existing_files=False ):
		print '='*79
		self._initCrawlState( parameters, master_list=master_list, seed_list=seed_list, current_wave=current_wave )

		if not self._initOutputFiles( path, parameters, seed_list, overwrite_existing_files ):
			return None		#Output files already exist, and overwrite_existing_files is not set

		#Main loop
		while not (self.parameters.decide_terminate_function(self) or self._checkIfDone()):
			print
			print '='*79
			print 'Wave', self.current_wave, '...'
			print

			urls = self._chooseUrls()
			results = self._processUrls( urls )
			self._processResults( results )
			self._countCompletedUrls()
			self._saveOutput( path, results )
			self.current_wave += 1

		print '='*79
		print 'Crawl complete.'
		print '='*79

	def saveState(self, filename):
		master_file = file(filename, 'wb')
		master_writer = csv.writer( master_file )
		master_writer.writerow( [ 'site', 'links', 'visited' ] )
		for a in self._master_list:
#			print self._master_list[a], '\t', a
			(links, visited) = self._master_list[a]
			master_writer.writerow( [a] + [links, visited] )
		master_file.close()

		return

	def _initCrawlState(self, parameters, master_list={}, seed_list=[], current_wave=None ):
		self.parameters = parameters

		print 'Initializing state...\t\t', currentTime()
		if not master_list == {}:
			self._master_list = master_list
		elif not seed_list == []:
			self._master_list = {}
			for s in seed_list:
				self._master_list[s] = (0,0)
		else:
			print '\tWarning: You must specify either a master list or a seed list.'
			print '\tSnowcrawl can\'t start from nothing.'
			print '\tCreating an empty list and continuing...!'
			print
			self._master_list = {}

		if not current_wave:
			self.current_wave = 1
		else:
			self.current_wave = current_wave

		self._countCompletedUrls()

	def _initOutputFiles( self, path, parameters, seed_list, overwrite_existing_files=False ):
		print 'Validating file path ', path, '...\t\t', currentTime()
		if os.path.isdir( path ):
			print '\tThe path already exists!'
			if not overwrite_existing_files:
				print '\tSnowCrawl is quitting because the specified file path already exists.'
				print '\tChoose a different path, or allow runUntilDone to overwrite_existing_files.'
				return None
		else:
			os.mkdir( path )
		print

		print 'Creating subdirectories...\t', currentTime()
		if parameters.save_states and not os.path.isdir( path+'states' ):
			os.mkdir( path+'states' )
		if parameters.save_files and not os.path.isdir( path+'files' ):
			os.mkdir( path+'files' )
		if parameters.save_edges and not os.path.isdir( path+'edges' ):
			os.mkdir( path+'edges' )

		print 'Saving parameters...\t\t', currentTime()
		print parameters
		parameters.save( path+'snowcrawl_parameters.txt' )

		print 'Saving seed list...\t\t', currentTime()
		out_file = file( path+'snowcrawl_seed_list.txt', 'w' )
		for s in seed_list: out_file.write( s + '\n' )
		out_file.close()

		print 'Saving initial state...\t\t', currentTime()
		self.saveState( path+'snowcrawl_master_list.csv' )

		print 'Creating results file...\t', currentTime()
		results_file = file(path+'snowcrawl_results.csv', 'wb')
		results_writer = csv.writer( results_file )
		results_writer.writerow( [ 'wave', 'siteid', 'url', 'filename', 'timed_out', 'kept' ] + parameters.csv_header )
		results_file.close()

		print 'Creating progress file...\t', currentTime()
		progress_file = file(path+'snowcrawl_progress.csv', 'wb')
		progress_writer = csv.writer( progress_file )
		progress_writer.writerow( [ 'wave', 'total', 'completed', 'remaining', 'time'] )
		progress_file.close()

		print

		return 1

	def _checkIfDone(self):
		print '\tChecking if crawl is complete...\t', currentTime()
		for u in self._master_list:
			if not self._master_list[u][1] == 1: return 0
		return 1

	def _countCompletedUrls(self):
		print '\tChecking completed urls...\t\t', currentTime()

		#Figure out how many of the urls in the master list are unvisited.
		#(For a new list, this will be all of them.)

		completed = 0
		for u in self._master_list:
			if self._master_list[u][1] == 1:
				completed += 1

		self.urls_completed = completed
		self.urls_remaining = len(self._master_list) - self.urls_completed

		print '\t\t', self.urls_remaining, 'urls remaining.'
		print '\t\t', self.urls_completed, 'urls processed so far.'

	def _chooseUrls(self):
		print '\tChoosing urls for next wave...\t', currentTime()

		unvisited_list = []
		for u in self._master_list:
			if self._master_list[u][1] == 0:
				unvisited_list.append( u )

		if self.parameters.prioritize_urls:
			unvisited_list.sort( lambda x, y: self._master_list[x][0] - self._master_list[y][0] )

		chosen_urls = unvisited_list[:self.parameters.wave_size]

		print '\t\t', len(chosen_urls), 'urls chosen.'
		return chosen_urls


	def _processUrls(self, urls):
		# Note: This code makes no use of multithreading
		print '\tProcessing urls...\t\t', currentTime()
		results = []
		for u in urls:
			
			r = _processUrl( (self.parameters.time_limit, u, self.parameters.processing_params, self.parameters.process_url_function) )
			(url, timed_out, kept, text, eligible_urls, all_edges, statistics) = r
			print '\t', timed_out, '\t', kept, '\t', u
			results.append( r )

		return results

	def _processResults(self, results):
		print '\tProcessing results...\t\t', currentTime()

		old_urls = []	#Contains urls of sites visited in the last wave
		new_urls = {}	#Contains urls of sites linked from the last wave
		for (old_url, timed_out, kept, text, eligible_urls, edges, stats) in results:
			for u in eligible_urls:
				if u in new_urls: new_urls[u] += eligible_urls[u]
				else: new_urls[u] = eligible_urls[u]
			old_urls += [old_url]

		#Update master list
		print '\tUpdating master list...\t\t', currentTime()

		#Flag visited sites as visited
		for u in old_urls:
			self._master_list[u] = (self._master_list[u][0], 1)

		for u in new_urls:
			if not u in self._master_list:
				#Add new sites to the list
				self._master_list[u] = (new_urls[u], 0)
			else:
				#Increase the count for sites already in the list
				self._master_list[u] = (self._master_list[u][0]+new_urls[u], self._master_list[u][1])


	def _saveOutput(self, path, results ):
		print '\tSaving results...\t\t', currentTime()
		if self.parameters.save_files:
			wave_path = path+'files/wave'+str(self.current_wave)
			if os.path.isdir( wave_path ):
				shutil.rmtree( wave_path )
			os.mkdir( wave_path )
			

		if self.parameters.save_edges:
			edgelist_file = file(path+'edges/snowcrawl_edgelist'+str(self.current_wave)+'.txt', 'wb')

		results_file = file(path+'snowcrawl_results.csv', 'ab')
		results_writer = csv.writer( results_file )
		a = 1
		for (url, timed_out, kept, text, eligible_urls, edges, stats) in results:
			#Save files, if so instructed
			if self.parameters.save_files:
				escaped_url = url.replace("/", "-")
				filename = 'files/wave'+str(self.current_wave)+'/'+escaped_url
				try:
					out_file = file(path+filename,'w')
					out_file.write(text)	#...Save the text of the page.
					out_file.close()
				except:
					print '\tWARNING: Unable to save file', filename
					filename = '.'
			else: filename = '.'

			#Save results to results.csv
			results_writer.writerow( [self.current_wave, a, url, filename, timed_out, kept] + stats )

			if self.parameters.save_edges:
				for e in edges:
					edgelist_file.write( url + '\t' + e + '\t' + str(edges[e]) + '\n' )

			a += 1
		results_file.close()


		#Save progress file
		progress_file = file(path+'snowcrawl_progress.csv', 'ab')
		progress_writer = csv.writer( progress_file )
		progress_writer.writerow( [self.current_wave, len(self._master_list), self.urls_completed, self.urls_remaining, currentTime().ctime()] )
		progress_file.close()

		#Backup the state to the main directory
		print '\tSaving master list...\t\t', currentTime()
		self.saveState( path+'snowcrawl_master_list.csv' )

		#Save a permanent record of the current state, if so instructed
		if self.parameters.save_states:
			print '\tBacking up master list...\t', currentTime()
			self.saveState( filename=path+'states/snowcrawl_state'+str(self.current_wave)+'.csv' )

		print




class MultiCrawler( SoloCrawler ):
	def __init__(self, pool_size=None ):
		print '='*79
		print '=== Launching MultiCrawler ... ====='

		if pool_size==None:	self.pool_size = cpu_count()
		else: self.pool_size = pool_size

	def _processUrls(self, urls):
		print '\tProcessing urls...\t\t', currentTime()
		start_time = currentTime()
		num_urls = len( urls )
		print '\t\tPct Complete\tEst. total time\tEst. Remaining'

		my_pool = Pool( self.pool_size )
		results = my_pool.map_async( _processUrl,
			[ (self.parameters.time_limit, u, self.parameters.processing_params, self.parameters.process_url_function) for u in urls ],
			chunksize=1
		)

		while not results.ready():
			results.wait(self.parameters.time_inc)

			percent_complete = 1 - (float(results._number_left)/(float(num_urls)/results._chunksize))
			if percent_complete > 0:
				completion_duration = (currentTime() - start_time)*10000/int(10000*percent_complete)
				remaining_time = completion_duration*int(10000*(1-percent_complete))/10000
				completion_time = (start_time+completion_duration).ctime()
			else:
				completion_duration = 'Estimate not available'
				remaining_time = 'Estimate not available'
				completion_time = 'Estimate not available'
			print '\t\t', round( percent_complete*100, 1 ), '%\t\t', completion_duration, '\t', remaining_time		results = results.get()

		return results




class ServerCrawler( SoloCrawler ):
	def __init__(self, port, pw, batch_size=20 ):
		print '='*79
		print '=== Launching ServerCrawler ... ====='

		self.batch_size = batch_size
		self.port = port
		self.pw = pw

	def _initCrawlState(self, parameters, master_list={}, seed_list=[], current_wave=None ):
		SoloCrawler._initCrawlState( self, parameters, master_list=master_list, seed_list=seed_list, current_wave=current_wave )

		#Define queues
		self._process_queue = Queue()		#Queue of sites to be processed
		self._results_queue = Queue()		#Queue of processed sites to be stored

		self._clients_queue = Queue()		#Queue to track how many clients are connected
		self._activity_queue = Queue()		#Queue to track how many batches are being processed
		self._terminate_queue = Queue()
		self._terminate_queue.put(0)		#Place a single value in terminateQ.  When this is removed, all processes will end

		#Set up IS_Manager class and register server functions
		class IS_Manager(managers.BaseManager): pass
		IS_Manager.register('get_clientsQ', callable=self.get_clients_queue)
		IS_Manager.register('get_processQ', callable=self.get_process_queue)
		IS_Manager.register('get_resultsQ', callable=self.get_results_queue)
		IS_Manager.register('get_activityQ', callable=self.get_activity_queue)
		IS_Manager.register('get_terminateQ', callable=self.get_terminate_queue)
		IS_Manager.register('get_parameters', callable=self.get_parameters)

		#Initialize manager, server, and workers
		self.manager = IS_Manager(address=('', self.port), authkey=self.pw)
		self.server = self.manager.get_server()

		self.server_process = Process( target=self.server.serve_forever )
		self.server_process.start()

	def get_clients_queue(self): return self._clients_queue
	def get_process_queue(self): return self._process_queue
	def get_results_queue(self): return self._results_queue
	def get_activity_queue(self): return self._activity_queue
	def get_terminate_queue(self): return self._terminate_queue
	def get_parameters(self): return self.parameters

	def runUntilDone(self, path, parameters, master_list={}, seed_list=[], current_wave=None, overwrite_existing_files=False ):
		print '='*79
		self._initCrawlState( parameters, master_list=master_list, current_wave=current_wave, seed_list=seed_list )
		if not self._initOutputFiles( path, parameters, seed_list, overwrite_existing_files ):
			return None

		#Fill the initial queue
		self._chooseUrls()

		#Main loop
		count = 0
		done = 0
		while not self.parameters.decide_terminate_function(self) and not done:
			time.sleep(.1)

			#If the _results_queue is high, process it
			if self._results_queue.qsize() > self.parameters.wave_size/self.batch_size:
				print
				print '\tResults queue is full enough: Processing...'
				results = self._getResults()
				self._processResults( results )
				self._saveOutput( path, results )

			#If the _process_queue is low (less than the number of active clients),
			#	force reprocessing and refill it
			if self._process_queue.qsize() < self._clients_queue.qsize():
				print '\tProcess queue is almost empty: Refilling...'
				if len(self._master_list) - self.urls_completed - self.urls_remaining == 0:
					if self._checkIfDone(2): #check and double check if everything is done
						print '\tIt looks like we\'re all out of work to do.'
						done = 1
					else:
						print '\tMaster list is empty: Waiting for batches to process...'
						while self._results_queue.empty(): pass
						results = self._getResults()
						self._processResults( results )
						self._saveOutput( path, results )
						self.current_wave += 1

				self._chooseUrls()
				self._print_queue_status(header=True)

			if count > float(self.parameters.time_inc)/.1:
				self._print_queue_status()
				count = 0
			count += 1

		self._shutDown()

	def _checkIfDone(self, depth):
		print '\tChecking if crawl is complete (depth', depth,')...\t', currentTime()
		if not self._process_queue.empty(): return 0
		if not self._results_queue.empty(): return 0
		if not self._activity_queue.empty(): return 0
		if self.urls_remaining > 0: return 0

		if depth==0: return 1
		else:
			time.sleep(.5)
			return self._checkIfDone(depth-1)

	def _print_queue_status(self, header=False):
		if not header:
			print '\t\t', self._process_queue.qsize(), '\t', self._activity_queue.qsize(), '\t', self._results_queue.qsize(), '\t', currentTime().ctime()
		else:
			print
			print '\tBatches...'
			print '\t\tQueued\tActive\tDone\t'


	def _shutDown(self):
		#Signal for clients to disconnect
		self._terminate_queue.get()
		print '='*79
		print 'Crawl complete.'
		print '='*79

		#Wait for all clients to disconnect
		print 'Signaling for clients to disconnect.'
		while not self._clients_queue.empty():
			print '\t', self._clients_queue.qsize(), 'client(s) still connected...'
			time.sleep(.5)

		print 'All clients disconnected.  Shutting down the server.'
		time.sleep(1)	#Give all the clients a moment to fully disconnect
		self.server_process.terminate()

	def _chooseUrls(self):
		print
		print '='*79
		print 'Wave', self.current_wave, '...'
		print

		urls = SoloCrawler._chooseUrls( self )

		#Flag visited sites as in process
		for u in urls:
			self._master_list[u] = (self._master_list[u][0], -1)

		batches = []
		a = 0
		while a < min(len(urls), self.parameters.wave_size):
			batches.append( urls[a:a+self.batch_size] )
			a += self.batch_size
		
		for b in batches:
			self._process_queue.put( b )

		self._countCompletedUrls()




	def _getResults(self):
		max_val = min( self._results_queue.qsize(), self.parameters.wave_size )
		results = []
		for a in range(max_val):
			results += self._results_queue.get() 

		return results



class ClientCrawler():
	def __init__(self, ip, port, pw, pool_size=None):
		self.ip, self.port, self.pw = ip, port, pw
		self.pool_size = pool_size
		print '='*79
		print '=== Launching ClientCrawler ... ====='

		class IS_Manager(managers.BaseManager): pass
		
		IS_Manager.register('get_clientsQ')
		IS_Manager.register('get_processQ')
		IS_Manager.register('get_resultsQ')
		IS_Manager.register('get_activityQ')
		IS_Manager.register('get_terminateQ')
		IS_Manager.register('get_parameters')

		#Set up manager, pool
		print '\tConnecting to server...'
		manager = IS_Manager(address=(ip, port), authkey=pw)
		manager.connect()

		self._clients_queue = manager.get_clientsQ()
		self._clients_queue = manager.get_clientsQ()
		self._process_queue = manager.get_processQ()
		self._results_queue = manager.get_resultsQ()
		self._activity_queue = manager.get_activityQ()
		self._terminate_queue = manager.get_terminateQ()

		self.parameters = manager.get_parameters().returnSelf()

		self._clients_queue.put(1)
		print '\tConnected.'

		print self.parameters

	def runUntilDone(self):
		print 'Starting client main loop...'
#		self.parameters = parameters

		#Main loop
		while not self._terminate_queue.empty():
			if self._process_queue.empty():
				print '\tI\'m bored here!', currentTime()
				time.sleep(.5)
			else:
				urls = self._process_queue.get()

				self._activity_queue.put(1)
				results = self._processUrls( urls )
				self._results_queue.put( results )
				self._activity_queue.get()

		print 'Client process is quitting.  Bye!'
		self._clients_queue.get()

	def _processUrls(self, urls):
		#This code should be identical to MultiCrawler._processUrls
		start_time = currentTime()
		num_urls = len( urls )
		print '\tProcessing', num_urls, 'urls...\t\t', currentTime()
		print '\t\tPct Complete\tEst. total time\tEst. Remaining'

		if self.pool_size:
			my_pool = Pool( self.pool_size )
		else:
			my_pool = Pool()

		#(time_limit, url, params, func)
		results = my_pool.map_async( _processUrl,
			[ (self.parameters.time_limit, u, self.parameters.processing_params, self.parameters.process_url_function) for u in urls ],
			chunksize=1
		)

		while not results.ready():
			results.wait(self.parameters.time_inc)

			percent_complete = 1 - (float(results._number_left)/(float(num_urls)/results._chunksize))
			if percent_complete > 0:
				completion_duration = (currentTime() - start_time)*10000/int(10000*percent_complete)
				remaining_time = completion_duration*int(10000*(1-percent_complete))/10000
				completion_time = (start_time+completion_duration).ctime()
			else:
				completion_duration = 'Estimate not available'
				remaining_time = 'Estimate not available'
				completion_time = 'Estimate not available'
			print '\t\t', round( percent_complete*100, 1 ), '%\t\t', completion_duration, '\t', remaining_time		results = results.get()

		"""
		#This version, preserved for debugging, is exactly the same as SoloCrawler
		print '\tProcessing urls...\t\t', currentTime()
		results = []
		for u in urls:
			r = _processUrl( (self.parameters.time_limit, u, self.parameters.processing_params, self.parameters.process_url_function) )
			(url, timed_out, kept, text, eligible_urls, all_edges, statistics) = r
			print '\t', timed_out, '\t', kept, '\t', u
			results.append( r )

		"""
		return results


### Processing functions #####################################################

def findEdges( url, text ):
	start_time = time.time()

	edges = {}
	E = re.findall("http://([a-zA-Z0-9\.\-]*?)/", text)
	for e in E:
		e = e.lower()
#		e = re.sub('http://','',e[:len(e)-1])
		if e in edges: edges[e] += 1
		else: edges[e] = 1

	self_loops = 0
	if url in edges: self_loops = edges[url]

	end_time = time.time()
	return ( edges, [ start_time, end_time, len(edges), self_loops ] )

def downloadUrl( url ):
	start_time = time.time()
	try:
		text = urllib2.urlopen( url ).read()
		download_succeeded = 1
	except:
		text = ''
		download_succeeded = 0
	length = len(text)
	end_time = time.time()
	return ( text, [start_time, end_time, length] )

def defaultProcessUrl( (url, params) ):
#	 time.sleep( .01/random.uniform(.01,1) )
	(text, download_stats) = downloadUrl( 'http://'+url )
#	(kept, classify_stats) = classifyText( text, params )
	(kept, classify_stats) = (1, [0])
	(edges, edge_stats) = findEdges( url, text )
#	return (kept, links, download_stats + classify_stats + link_stats)
	return (kept, text, edges, edges, download_stats + classify_stats + edge_stats)

def null_processor( (url, params) ):
	return (url, 0, "", [], [], [])

def default_decider(self):
	print '***'
	unvisited_list = []
	for u in self._master_list:
		if self._master_list[u][1] == 0:
			unvisited_list.append( u )
	return not len(unvisited_list)>0


# This code modified from source at http://code.activestate.com/recipes/473878/ (r1)
# It limits the length of time a given page can take to process

class InterruptableThread(threading.Thread):
	def __init__(self, url, params, func):
		threading.Thread.__init__(self)
		self.result = None
		self.url = url
		self.params = params
		self.func = func

	def run(self):
#		try:
			(kept, text, eligible_urls, all_edges, statistics) = self.func( (self.url, self.params) )
			self.result = (self.url, kept, text, eligible_urls, all_edges, statistics)
#		except:
#			self.result = (self.url, kept, "", [], [], [])

def _processUrl( (time_limit, url, params, func) ):
	it = InterruptableThread(url, params, func)
	it.start()
	it.join( time_limit )

	if it.isAlive():
		return (url, 1, 0, '', [], [], [])
	else:
		(url, kept, text, eligible_urls, all_edges, statistics) = it.result
		return (url, 0, kept, text, eligible_urls, all_edges, statistics)

## End of code from http://code.activestate.com/recipes/473878/
