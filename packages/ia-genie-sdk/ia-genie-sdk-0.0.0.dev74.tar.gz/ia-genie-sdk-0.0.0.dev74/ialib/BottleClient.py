import requests
import json
from time import sleep
from functools import wraps
from ialib.GenomeInfo import Genome

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.
    :param ExceptionToCheck: the exception to check. may be a tuple of
        excpetions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry

@retry(requests.exceptions.Timeout, tries=5, delay=3, backoff=1)
def primitiveClient(url, api_key, query, data=None):
    try:
        result = requests.post(url, json={'api_key': api_key, 'query': query, 'data': data})
        result.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(" Primitive Error returning! HTTP Error: %s" %(e))
    except requests.exceptions.ConnectionError as e:
        raise Exception(" Primitive Error returning! Connection Error: %s" %(e))
    except requests.exceptions.Timeout as e:
        raise Exception(" Primitive Error returning! Timeout Error: %s" %(e))
    except requests.exceptions.RequestException as e:
        raise Exception(" Primitive Error returning! RequestException Error: %s" %(e))
    
    if result.status_code in ['400', '401', '402', '403', '404', '405']: ##bad
        raise Exception(" Primitive Server Error!: %s" %(result.text))
    elif result.status_code in ['200']: ##good
        pass
    
    try:
        response = result.json()
    except:
        raise Exception(" Primitive Error returning! Error Code pC-20: %s status_code: %s" %(result.text, result.status_code))
    
    if 'error' in response:
        print(response)
        raise Exception(" Primitive Error returning! Error pC-57: %s status_code: %s" %(result.text, result.status_code))                
    if response['status'] == 'failed':
        if 'traceback' in response:
            print(response['traceback'])
        raise Exception(" Primitive Error returning! Error pC-58: %s status_code: %s" %(result.text, result.status_code))        
    message = response.pop("message")
    return message #not interested in the metadata


class BottleClient:
    def __init__(self, bottle_info, genome=None, ingress_nodes=[], query_nodes=[]):
        """
        Provide bottle information in a dictionary.

        ex:
        from ialib.BottleClient import BottleClient

        bottle_info = {'api_key': 'ABCD-1234',
                    'name': 'genie-bottle',
                    'domain': ':8181',
                    'secure': False}

        bottle = BottleClient(bottle_info)
        bottle.injectGenome(genome)
        bottle.setIngressNodes(['P1'])
        bottle.setQueryNodes(['P1'])


        Alternatively, you can connect to a bottle with an existing genie:

        ex:
        bottle = BottleClient(bottle_info)
        bottle.connect()
        """
        self.genome = genome
        self.bottle_info = bottle_info
        self.name = bottle_info['name']
        self.domain = bottle_info['domain']
        self.api_key = bottle_info['api_key']
        self.ingress_nodes = ingress_nodes
        self.query_nodes = query_nodes
        self.failures = []
        self.system_failures = []
        self._connected = False
        if self.genome == None:
            self.genie = None
        else:
            self.genie = self.genome.agent
        if 'secure' not in self.bottle_info or self.bottle_info['secure'] == True:
            self.secure = True
            self.controller_url = 'https://{name}.{domain}/genie-controller'.format(**self.bottle_info)
            self.url = 'https://{name}.{domain}/%s/jsonrpc'.format(**self.bottle_info)
        else:
            self.secure = False
            self.controller_url = 'http://{name}.{domain}/genie-controller'.format(**self.bottle_info)
            self.url = 'http://{name}.{domain}/%s/jsonrpc'.format(**self.bottle_info)
        return
    
    def __repr__(self):
        return '<{name}.{domain}| secure: %r, connected: %s, genie: %s, ingress_nodes: %i, query_nodes: %i, failures: %i>'.format(**self.bottle_info) %(self.secure, self._connected, self.genie, len(self.ingress_nodes), len(self.query_nodes), len(self.failures))

    def connect(self):
        r = requests.post(self.controller_url, json={'api_key': self.api_key, 'command': 'connect'}).json()
        self.genome = Genome(r['genome'])
        self.genie = r['genome']['agent']
        if r['connection'] == 'okay':
            self._connected = True
        else:
            self._connected = False
        return {'connection': r['connection'], 'genie': r['genie']}

    def primitiveCall(self, primitive_name, api_call, data=None):
        """
        There should not be a good reason to use this aside from experimentation.

        Provide the primitive name as 'name', the API call as 'call', and 'data' if any.
        """
        try:
            if data:
                r = primitiveClient(self.url %(self.genome.primitive_map[primitive_name]), self.api_key, api_call, data=data)
            else:
                r = primitiveClient(self.url %(self.genome.primitive_map[primitive_name]), self.api_key, api_call)
        except Exception as e:
                self.failures.append({primitive_name: e})
                raise Exception("primitiveCall Failure:", e)
        return r

    def observe(self, data=None):
        "Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."
        x = []
        for node in self.ingress_nodes:
            try:
                r = primitiveClient(self.url %(node['id']), self.api_key, 'observe', data=data)
                x.append({node['name']: r})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Observe Failure:", {node['name']: e})
        return x
    
    def query(self, query):
        x = []
        for node in self.query_nodes:
            try:
                r = primitiveClient(self.url %(node['id']), self.api_key, query)
                x.append({node['name']: r})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x
    
    def observeClassification(self, data=None):
        """
        Best practice is to send a classification to all ingress and query nodes as a singular symbol in the last event.
        This function does that for us.
        """
        x = []
        for node in self.query_nodes:
            try:
                r = primitiveClient(self.url %(node['id']), self.api_key, 'observe', data=data)
                x.append({node['name']: r})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Observe Failure:", {node['name']: e})
        return x

    def injectGenome(self, genome):
        self.genome = genome
        r1 = requests.post(self.controller_url, json={'api_key': self.api_key, 'command': 'clear-genome'}).json()
        sleep(2)
        r2 = requests.post(self.controller_url, json={'api_key': self.api_key, 'topology': self.genome.topology, 'command': 'inject-genome'}).json()
        ## TODO: Make code to check and wait until agent is started before returning
        sleep(4)
        self.genie = self.genome.agent
        self._connected = True
        return 'clear-genome: %s, inject-genome: %s' %(r1, r2)
        
    def setIngressNodes(self, nodes=[]):
        "Use list of primitive names."
        self.ingress_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return
    
    def setQueryNodes(self, nodes=[]):
        "Use list of primitive names."
        self.query_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return
    
    def changeGenes(self, gene_data):
        """
        Use primitive names.
        This will do live updates to an existing agent, rather than stopping an agent and starting a new one as per 'injectGenome'.
        gene_data of form: 
        
            {node-name: {gene: value}}
        
        where node-id is the ID of a primitive or manipulative.

        Only works on primitive nodes at this time.
        """
        self.genome.changeGenes(gene_data)
        x = []
        for node, updates in gene_data.keys(): ## only primitive nodes at this time.
            for gene, value in updates.items():
                r = requests.post(self.url %(self.genome.primitive_map[node]), json={'api_key': self.api_key, 'query': 'updateGene', 'data': {gene: value}}).json()
                if 'error' in r or r['message'] != 'updated-genes':
                    self.system_failures.append({node: r})
                    print("System Failure:", {node: r})
                x.append({node: r['message']})
        return x