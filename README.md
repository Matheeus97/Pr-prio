#README: Coleta e Armazenamento de 
Dados de Criptomoedas 

Descrição 
Este projeto coleta dados de criptomoedas utilizando a API CoinCap e os armazena em um banco de dados MySQL. O processo inclui criação de tabelas, inserção de dados e verificação de erros. 

################################

Requisitos 
Certifique-se de que os seguintes softwares estão instalados: 
Python 3.8+ 
MySQL Server 

################################

Bibliotecas Python necessárias 
Instale as dependências executando: 
pip install requests mysql-connector-python python-dotenv 

################################

Configuração 
Banco de Dados 
Crie um banco de dados chamado criptomoedas no MySQL. 
Configure as informações de conexão no arquivo .env: 
DB_HOST=localhost 
DB_USER=root 
DB_PASSWORD=Tfnabsq34. 
DB_NAME=criptomoedas 

################################

Execução 
Baixe o código fonte. 
Execute o script principal: 
python crypto_final.py 
O script realiza os seguintes passos: 
Verifica a conectividade com o banco de dados. 
Limpa as tabelas existentes (se não houver erros de verificação). 
Cria as tabelas necessárias. 
Insere os dados coletados da API CoinCap. 

################################

Observação 
Caso o script encontre um erro durante a verificação, ele interromperá o processo para 
evitar a perda de dados existentes. 
