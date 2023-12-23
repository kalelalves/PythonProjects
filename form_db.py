import pyodbc

# Parâmetros de conexão ao SQL Server
server = 'G15-5530\SQLEXPRESS'
database = 'Form'
driver = 'ODBC Driver 17 for SQL Server'
trusted_connection = 'yes'  # Usar autenticação do Windows

# String de conexão para autenticação do Windows
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'

# Conectar ao SQL Server
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Criação da tabela "users"
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='users')
    CREATE TABLE users (
        ID INT PRIMARY KEY IDENTITY(1,1),
        NOME NVARCHAR(100),
        IDADE NVARCHAR(50),
        RUA NVARCHAR(100),
        CIDADE NVARCHAR(100),
        NUMERO NVARCHAR(20),
        ESTADO NVARCHAR(50),
        EMAIL NVARCHAR(100)
    )
''')

# Confirmar e fechar a conexão
conn.commit()
conn.close()
