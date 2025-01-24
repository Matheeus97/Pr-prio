import requests
import mysql.connector
import os
from mysql.connector import Error

# Função para carregar configurações externas
def load_config():
    return {
        'api_key': os.getenv('API_KEY', 'your_api_key_here'),
        'db_host': os.getenv('DB_HOST', 'localhost'),
        'db_user': os.getenv('DB_USER', 'root'),
        'db_password': os.getenv('DB_PASSWORD', 'Tfnabsq34.'),
        'db_name': os.getenv('DB_NAME', 'crypto_db')
    }

# Conexão com a API
def get_crypto_data():
    url = "https://api.coincap.io/v2/assets"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data']
        else:
            print("Erro ao acessar API:", response.status_code)
            return None
    except Exception as e:
        print(f"Erro ao conectar à API: {e}")
        return None

# Conexão com o banco de dados MySQL
def connect_to_db(config):
    try:
        conn = mysql.connector.connect(
            host=config['db_host'],
            user=config['db_user'],
            password=config['db_password'],
            database=config['db_name']
        )
        if conn.is_connected():
            print("Conectado ao banco de dados")
            return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Função para limpar as tabelas existentes
def clear_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM crypto_prices")
        cursor.execute("DELETE FROM cryptocurrencies")
        conn.commit()
        print("Tabelas limpas com sucesso")
    except Exception as e:
        print(f"Erro ao limpar tabelas: {e}")

# Criar as tabelas no banco de dados
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cryptocurrencies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            symbol VARCHAR(50),
            market_cap_usd BIGINT,
            supply BIGINT,
            max_supply BIGINT,
            change_24h DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cryptocurrency_id INT,
            price_usd DECIMAL(18, 6),
            volume_usd DECIMAL(18, 2),
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cryptocurrency_id) REFERENCES cryptocurrencies(id)
        )
    """)
    conn.commit()
    print("Tabelas criadas com sucesso")

# Inserir dados nas tabelas
def insert_data(conn, crypto_data):
    cursor = conn.cursor()
    
    for crypto in crypto_data:
        try:
            name = crypto['name']
            symbol = crypto['symbol']
            # Alterando para float, pois pode conter casas decimais
            market_cap_usd = float(crypto['marketCapUsd']) if crypto['marketCapUsd'] else 0.0
            supply = float(crypto['supply']) if crypto['supply'] else 0.0
            max_supply = float(crypto['maxSupply']) if crypto['maxSupply'] else 0.0
            change_24h = float(crypto['changePercent24Hr']) if crypto['changePercent24Hr'] else 0.0
            
            # Inserir na tabela cryptocurrencies
            cursor.execute("""
                INSERT INTO cryptocurrencies (name, symbol, market_cap_usd, supply, max_supply, change_24h)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, symbol, market_cap_usd, supply, max_supply, change_24h))
            crypto_id = cursor.lastrowid
            
            # Inserir na tabela crypto_prices
            price_usd = float(crypto['priceUsd']) if crypto['priceUsd'] else 0.0
            volume_usd = float(crypto['volumeUsd24Hr']) if crypto['volumeUsd24Hr'] else 0.0
            
            cursor.execute("""
                INSERT INTO crypto_prices (cryptocurrency_id, price_usd, volume_usd)
                VALUES (%s, %s, %s)
            """, (crypto_id, price_usd, volume_usd))
        
        except Exception as e:
            print(f"Erro ao inserir dados da criptomoeda {crypto['name']}: {e}")
    
    conn.commit()
    print("Dados inseridos com sucesso")

# Função principal
def main():
    config = load_config()
    
    # Conectar ao banco de dados
    conn = connect_to_db(config)
    if conn:
        try:
            # Coletar dados da API
            crypto_data = get_crypto_data()
            if crypto_data:
                # Verificar se a coleta foi bem-sucedida
                print("Dados da API verificados com sucesso")
                
                # Limpar as tabelas antes de criar e inserir os dados
                clear_tables(conn)
                
                # Criar as tabelas no banco
                create_tables(conn)
                
                # Inserir os dados nas tabelas
                insert_data(conn, crypto_data)
            else:
                print("Erro: não foi possível coletar os dados da API.")
        
        except Exception as e:
            print(f"Erro durante o processo: {e}")
        
        finally:
            # Fechar a conexão com o banco de dados
            conn.close()

if __name__ == "__main__":
    main()
