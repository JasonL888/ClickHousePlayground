from clickhouse_driver import Client
from CPE import CPE

class ClickHouseConnection:
	def __init__(self):
		self.client = Client('localhost')
		self.init_setup()
	def init_setup(self):
		result = self.execute('SET input_format_import_nested_json=1')
		print("RESULT: {0}: {1}".format(type(result),result))
		result = self.execute('SET flatten_nested = 1')
		print("RESULT: {0}: {1}".format(type(result),result))
		result = self.execute('CREATE DATABASE IF NOT EXISTS cpe')
		print("RESULT: {0}: {1}".format(type(result),result))
		sql_file = open("data_schema.sql")
		sql_as_string = sql_file.read()
		result = self.execute(sql_as_string)
	def execute(self, sql_query):
		result = self.client.execute(sql_query)
		return( result )
	def insert(self, table_name, json_str):
		query = 'INSERT INTO %s FORMAT JSONEachRow %s' % (table_name, json_str)
		result = self.client.execute(query)
		return(result)

def main():
	client = ClickHouseConnection()
	result = client.execute('SELECT * from cpe.kpi')
	print("RESULT: {0}: {1}".format(type(result),result))
	for t in result:
		print(" ROW: {0}: {1}".format(type(t), t))
		for v in t:
			print("  COLUMN: {0}: {1}".format(type(v), v))

if __name__ == "__main__":
	cpes = [
		CPE('VDLINNNE1808009701', 'Realtek', 'DL4480V1_2019', "RTL960x", "DL4480V1_2.0.8"),
		CPE('VDLINNNE1808001234', 'Realtek', 'DL4480V1_2019', "RTL960x", "DL4480V1_2.0.9e"),
		CPE('VDLINNNE1808009845', 'Realtek', 'DL4480V1_2019', "RTL960x", "DL4480V1_2.0.8"),
		CPE('VDLINNNE1808009320', 'Realtek', 'DL4480V1_2019', "RTL960x", "DL4480V1_2.0.9e"),
		CPE('VDLINNNE1808028885', 'Realtek', 'DL4480V1_2019', "RTL960x", "DL4480V1_2.0.9e"),
	]
	client = ClickHouseConnection()
	for i in range(0,1000):
		for cpe in cpes:
			client.insert( table_name="cpe.kpi", json_str=cpe.getJSON());
			cpe.nextPII();
