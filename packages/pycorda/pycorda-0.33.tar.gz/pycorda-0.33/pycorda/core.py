import os
import pandas as pd
import jaydebeapi
import sys
import requests
import jks
import base64, textwrap
from jpype import JavaException
from xml.etree import ElementTree

class H2Tools(object):
	def get_latest_version(self):
		"""Returns the latest version string for the h2 database"""
		r = requests.get('http://central.maven.org/maven2/com/h2database/h2/maven-metadata.xml')
		tree = ElementTree.fromstring(r.content)
		return tree.find('versioning').find('latest').text

	def get_h2jar_url(self,version):
		url = "http://central.maven.org/maven2/com/h2database/h2/"
		url += version + "/h2-" + version + ".jar"
		return url

	def download_h2jar(self,filepath='./h2.jar', version=None):
		"""Downloads h2 jar and copies it to a file in filepath"""
		if version is None:
			version = self.get_latest_version()
		r = requests.get(self.get_h2jar_url(version))
		with open(filepath, 'wb') as jarfile:
			jarfile.write(r.content)

class Node(object):
	"""Node object for connecting to H2 database and getting table dataframes

	Use get_tbname methods to get dataframe for table TBNAME. For example,
	calling node.get_vault_states() will return the dataframe for VAULT_STATES.
	After using the node, call the close() method to close the connection.
	"""

	# --- Notes for future support of PostgreSQL clients ---
	# To support pg clients, url must be parsed into psycopg2.connect arguments
	# and the password must not be empty
	# After parsing, use "self._conn = psycopg2.connect(...)"

	# --- Notes regarding get methods ---
	# If table names will change often, it may be worth to
	# dynamically generate methods with some careful metaprogramming

	def __init__(self, url, username, password, path_to_jar='./h2.jar',node_root=None):
		"""
        Parameters
        ----------
        url : str
            JDBC url to be connected
        username : str
            username of database user
        passowrd : str
            password of database user
        path_to_jar : str
        	path to h2 jar file
        """

		self._conn = jaydebeapi.connect(
			"org.h2.Driver",
			url,
			[username, password],
			path_to_jar,
		)

		self._curs = self._conn.cursor()
		if  node_root != None:
			self.set_node_root(node_root)

	def set_node_root(self,node_root):
		self._node_root = node_root
		self._node_cert = node_root + '/certificates'
		self._node_cert_jks = self._node_cert + '/nodekeystore.jks'
		print(self._node_cert_jks)

	def display_keys_from_jks(self,password='cordacadevpass'):
		ks = jks.KeyStore.load(self._node_cert_jks,password)
		columns = ['ALIAS','PRIVATE_KEY']
		keys = pd.DataFrame([],columns=columns)
		for alias, pk in ks.private_keys.items():
			#keys = keys.append([[alias,pk.pkey_pkcs8,'PK']])
			df = pd.DataFrame([[alias,base64.b64encode(pk.pkey_pkcs8).decode('ascii')]],columns=columns)
			keys = keys.append(df,ignore_index=True)

			for c in pk.cert_chain:
				print_pem(c[1], "CERTIFICATE")
			print()

		for alias, c in ks.certs.items():
			print("Certificate: %s" % c.alias)
			print_pem(c.cert, "CERTIFICATE")
			print()

		for alias, sk in ks.secret_keys.items():
			print("Secret key: %s" % sk.alias)
			print("  Algorithm: %s" % sk.algorithm)
			print("  Key size: %d bits" % sk.key_size)
			print("  Key: %s" % "".join("{:02x}".format(b) for b in bytearray(sk.key)))
			print()
		return keys

	def _get_df(self, table_name):
		"""Gets pandas dataframe from a table

		Parameters
        ----------
        table_name : str
            name of table in database
		"""
		self._curs.execute("SELECT * FROM " + table_name)
		columns = [desc[0] for desc in self._curs.description] # column names
		return pd.DataFrame(self._curs.fetchall(), columns=columns)

	def get_node_attachments(self):
		return self._get_df("NODE_ATTACHMENTS")

	def get_node_attachments_contracts(self):
		return self._get_df("NODE_ATTACHMENTS_CONTRACTS")

	def get_node_checkpoints(self):
		return self._get_df("NODE_CHECKPOINTS")

	def get_node_contract_upgrades(self):
		return self._get_df("NODE_CONTRACT_UPGRADES")

	def get_node_indentities(self):
		return self._get_df("NODE_IDENTITIES")

	def get_node_infos(self):
		return self._get_df("NODE_INFOS")

	def get_node_info_hosts(self):
		return self._get_df("NODE_INFO_HOSTS")

	def get_node_info_party_cert(self):
		return self._get_df("NODE_INFO_PARTY_CERT")

	def get_node_link_nodeinfo_party(self):
		return self._get_df("NODE_LINK_NODEINFO_PARTY")

	def get_node_message_ids(self):
		return self._get_df("NODE_MESSAGE_IDS")

	def get_node_message_retry(self):
		return self._get_df("NODE_MESSAGE_RETRY")

	def get_node_named_identities(self):
		return self._get_df("NODE_NAMED_IDENTITIES")

	def get_node_our_key_pairs(self):
		return self._get_df("NODE_OUR_KEY_PAIRS")

	def get_node_properties(self):
		return self._get_df("NODE_PROPERTIES")

	def get_node_scheduled_states(self):
		return self._get_df("NODE_SCHEDULED_STATES")

	def get_node_transactions(self):
		return self._get_df("NODE_TRANSACTIONS")

	def get_node_transaction_mappings(self):
		return self._get_df("NODE_TRANSACTION_MAPPINGS")

	def get_vault_fungible_states(self):
		return self._get_df("VAULT_FUNGIBLE_STATES")

	def get_vault_fungible_states_parts(self):
		return self._get_df("VAULT_FUNGIBLE_STATES_PARTS")

	def get_vault_linear_states(self):
		return self._get_df("VAULT_LINEAR_STATES")

	def get_vault_linear_states_parts(self):
		return self._get_df("VAULT_LINEAR_STATES_PARTS")

	def get_vault_states(self):
		return self._get_df("VAULT_STATES")

	def get_vault_transaction_notes(self):
		return self._get_df("VAULT_TRANSACTION_NOTES")

	def close(self):
		"""Closes the connection to the database"""
		self._curs.close()
		self._conn.close()

def print_pem(der_bytes, type):
	print("-----BEGIN %s-----" % type)
	print("\r\n".join(textwrap.wrap(base64.b64encode(der_bytes).decode('ascii'), 64)))
	print("-----END %s-----" % type)