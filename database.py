import mysql.connector
from mysql.connector import pooling

# Establish connection
# conn = {
#     "user":"u146352233_root",  # Replace with your MySQL username
#     "password":"?K+e1FXhC1",  # Replace with your MySQL password
#     "host":"153.92.8.251",      # Replace with your MySQL host
#     "database":"u146352233_databank",   # Replace with your database name
#     "port":3306
# }
conn = {
    "user":"culprit_lab",  # Replace with your MySQL username
    "password":"-6?j2+M63h??",  # Replace with your MySQL password
    "host":"147.79.70.44",      # Replace with your MySQL host
    "database":"databank",   # Replace with your database name
    "port":3306
}
# localhost
# conn = {
#     "user":"root",  # Replace with your MySQL username
#     "password":"",  # Replace with your MySQL password
#     "host":"127.0.0.1",      # Replace with your MySQL host
#     "database":"databank",   # Replace with your database name
#     "port":3306
# }
connection_pool = pooling.MySQLConnectionPool(pool_name="databank_pool", pool_size=20, **conn)
def select_test():
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM users")

  # Fetch data
  results = cursor.fetchall()
  for row in results:
      print(row)

  # Close connection
  cursor.close()
  conn.close()
def select_device(user_id):
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()

  cursor.execute(f"SELECT * FROM devices where user_id="+str(user_id))

  # Fetch data
  results = cursor.fetchall()
  # Close connection
  cursor.close()
  conn.close()
  return results
def select_device_data(id,user):
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()
  if(id!= 'all'):
    cursor.execute(f"SELECT * FROM device_datas where device_id={id}")
  else:
    cursor.execute(f"SELECT * FROM device_datas left join devices on devices.id = device_datas.device_id where devices.user_id={str(user)}")

  # Fetch data
  results = cursor.fetchall()

  # Close connection
  cursor.close()
  conn.close()
  return results
def select_action():
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()
  cursor.execute(f"SELECT * FROM actions order by type")

  # Fetch data
  results = cursor.fetchall()

  # Close connection
  cursor.close()
  conn.close()
  return results
def select_action_with_clond_category(id):
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()
  cursor.execute(f"SELECT cloud_category_action.*,cloud_categories.name as cloud_name FROM cloud_category_action join cloud_categories on cloud_category_action.cloud_category_id =cloud_categories.id where action_id="+str(id))

  # Fetch data
  results = cursor.fetchall()

  # Close connection
  cursor.close()
  conn.close()
  return results

def select_service(user_id):
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()
  cursor.execute(f"SELECT services.*,service_category_connect.service_category_id FROM services join service_category_connect on service_category_connect.service_id=services.id where services.user_id="+str(user_id)+" order by service_category_connect.service_category_id ")

  # Fetch data
  results = cursor.fetchall()

  # Close connection
  cursor.close()
  conn.close()
  return results

def select_service_category():
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()
  cursor.execute(f"SELECT * FROM service_categories")

  # Fetch data
  results = cursor.fetchall()

  # Close connection
  cursor.close()
  conn.close()
  return results
def select_service_action():
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()
  cursor.execute(f"SELECT service_actions.*,cloud_categories.name as cloud_name FROM service_actions join cloud_categories on cloud_categories.id = service_actions.cloud_category_id order by id")

  # Fetch data
  results = cursor.fetchall()

  # Close connection
  cursor.close()
  conn.close()
  return results
def select_service_category_by_service(id):
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()

  cursor.execute(f"SELECT service_category_connect.service_category_id FROM service_category_connect left join service_categories on service_categories.id=service_category_connect.service_category_id where service_category_connect.service_id="+str(id))

  # Fetch data
  results = cursor.fetchall()

  # Close connection
  cursor.close()
  conn.close()
  return results

def select_cloud_category():
  # Create a cursor object
  conn = connection_pool.get_connection()
  cursor = conn.cursor()

  cursor.execute(f"SELECT * FROM cloud_categories order by id desc")

  # Fetch data
  results = cursor.fetchall()

  # Close connection
  cursor.close()
  conn.close()
  return results