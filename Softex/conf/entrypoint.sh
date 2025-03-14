#!/bin/bash
set -e

echo "Iniciando o MariaDB..."
service mariadb start

echo "Aguardando 30 segundos para o MySQL iniciar..."
sleep 30

echo "Configurando o MySQL..."
mysql -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('root');"
mysql -e "FLUSH PRIVILEGES;"
mysql -e "CREATE DATABASE IF NOT EXISTS softex;"

echo "Iniciando o Apache..."
service apache2 start

echo "Executando o código Python de rateios (main.py)..."
python codigos/main.py

echo "Iniciando o Streamlit Dashboard..."
nohup streamlit run codigos/dashboard.py --server.enableCORS false --server.enableXsrfProtection false &

echo "Container rodando. Acesse o Adminer em http://localhost/adminer.php e o MySQL na porta 3306."
tail -f /dev/null
