import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ialib.GenomeInfo import Genome

class BottleClient:
    def __init__(self, bottle_info, genome=None, ingress_nodes=[], query_nodes=[]):
        """
        Provide bottle information in a dictionary.

        ex:
        from ialib.BottleClient import BottleClient

        bottle_info = {'api_key': 'ABCD-1234',
                    'name': 'genie-bottle',
                    'domain': 'intelligent-artifacts.com',
                    'secure': False}

        bottle = BottleClient(bottle_info)
        bottle.connect()

        bottle.setIngressNodes(['P1'])
        bottle.setQueryNodes(['P1'])

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

        self.session = requests.Session()
        self.retry = Retry(connect=3, backoff_factor=0.5)
        self.adapter = HTTPAdapter(max_retries=self.retry)
        self.session.mount('http://', self.adapter)
        self.session.mount('https://', self.adapter)

        
        r = requests.post(self.controller_url, json={'api_key': self.api_key, 'command': 'connect'}).json()
        self.genome = Genome(r['genome'])
        self.genie = r['genome']['agent']
        if r['connection'] == 'okay':
            self._connected = True
        else:
            self._connected = False
        return {'connection': r['connection'], 'genie': r['genie']}

    def primitiveCall(self, url, api_key, query, data=[]):
        """
        There should not be a good reason to use this aside from experimentation.

        Provide the primitive name as 'name', the API call as 'call', and 'data' if any.
        """
        r = self.session.post(url, json={'api_key': api_key, 'query': query, 'data': data})
        return r

    def observe(self, data=None):
        "Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."
        x = []
        for node in self.ingress_nodes:
            try:
                r = self.primitiveCall(self.url %(node['id']), self.api_key, 'observe', data=data).json()
                x.append({node['name']: r})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Observe Failure:", {node['name']: e})
        return x
    
    def query(self, query):
        x = []
        for node in self.query_nodes:
            try:
                r = self.primitiveCall(self.url %(node['id']), self.api_key, query).json()
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
                r = self.primitiveCall(self.url %(node['id']), self.api_key, 'observe', data=data).json()
                x.append({node['name']: r})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Observe Failure:", {node['name']: e})
        return x
        
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