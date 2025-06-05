import os

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', ''),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'charset': os.getenv('MYSQL_CHARSET', 'utf8mb4'),
	'collation': os.getenv('MYSQL_COLLATION', 'utf8mb4_general_ci'),
} 