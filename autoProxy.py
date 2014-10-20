#!/usr/bin/python
import urllib2,re,os,random,sys


def getNewProxyFromWeb(redown = False):
	proxy_file = 'proxy.txt';
	
	if (os.path.isfile(proxy_file) == False) or (redown):
		
		url = 'http://cn-proxy.com/';
		print 'fetching web proxy list....';

		data = urllib2.urlopen(url).read();
		pattern = re.compile("<tr>\n<td>([^<]+)</td>\n<td>([^<]+)</td>");
		ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}');
		data = pattern.findall(data);
		p = [];
		for i in data:
			if ip.match(i[0]):
				p.append((i[0],i[1]));
		p = '\n'.join("%s:%s"%(itm[0],itm[1]) for itm in p);
		
		f = open(proxy_file, 'w');
		f.write(p);
		f.close();
		p = p.split('\n');
	else:
		f = open(proxy_file,'r');
		data = f.read();
		f.close();
		p = data.split('\n');
	
	if p:
		print '%s proxy server found'%(len(p));
		proxy = random.choice(p);
		
		apply(proxy);
		
	else:
		print 'proxy list fetch error';

def apply(proxy):
	print 'trying to apply %s by randomize'%(proxy);
	proxy = proxy.split(':');
	
	current_active_driver_comannd = '''
SERVICE_GUID=`printf "open\nget State:/Network/Global/IPv4\nd.show" | \
scutil | grep "PrimaryService" | awk '{print $3}'`
 
SERVICE_NAME=`printf "open\nget Setup:/Network/Service/$SERVICE_GUID\nd.show" |\
scutil | grep "UserDefinedName" | awk -F': ' '{print $2}'`

echo $SERVICE_NAME
	'''

	current_active_dirver = os.popen(current_active_driver_comannd);
	current_active_dirver = current_active_dirver.read();
	current_active_dirver = current_active_dirver.replace('\n', '');
	print 'dirver %s is current active,so it will by applied this rule'%(current_active_dirver)
	
	apply_command = '''
networksetup -setwebproxy '%s' %s %s
	'''%(current_active_dirver, proxy[0], proxy[1]);
	os.system(apply_command);
	print 'apply success';

	pass;

getNewProxyFromWeb();
