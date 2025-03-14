# Projeto ETL – Softex

Este projeto implementa um pipeline ETL que extrai dados de uma planilha Google, realiza a limpeza e transformação dos dados e os carrega em um banco de dados MySQL. Além disso, há um dashboard interativo desenvolvido com Streamlit para visualizar métricas e gráficos dos dados processados.

## Estrutura do Projeto

- **codigos/**: Contém os scripts Python do pipeline ETL (extração, limpeza, transformação, carga) e o aplicativo Streamlit.
- **conf/**: Arquivos de configuração, incluindo credenciais e parâmetros de conexão.
- **Dockerfile**: Define o ambiente Docker para executar o projeto.
- **entrypoint.sh**: Script de entrada para inicializar o projeto dentro do container.

## Pré-requisitos

- Docker instalado na máquina.
- Acesso à internet para baixar as dependências e a imagem base.

## Instruções para Execução com Docker

1. **Clone o Repositório**  
   Se ainda não clonou o projeto, faça:
   ```bash
   git clone https://github.com/RobsonR07/Teste.git
   cd Softex

2. Verifique a Estrutura de Pastas  
   Certifique-se de que as pastas "codigos/" e "conf/" estão presentes na raiz do repositório, conforme esperado pelo Dockerfile.
   Adicione o arquivo adicione o "credenciais.json" que foi enviado por email dentro da pasta "conf/" pois por politicas do google a API Key não pode se exporta no GitHub
   E assim que exposta ela é desativada, fazendo assim o teste não ser executavel.

4. Build da Imagem Docker  
   No diretório raiz do projeto, execute:
   docker build -t projeto-etl-softex .
   Esse comando irá:
   - Usar a imagem base "python:3.8-slim".
   - Instalar pacotes do sistema (Apache, PHP, MariaDB, wget, tar).
   - Baixar o Adminer para gerenciamento do banco de dados.
   - Instalar as dependências Python listadas no "codigos/requirements.txt".
   - Configurar o entrypoint para iniciar o container.

5. Executar o Container  
   Após a build, execute o container:
   docker run -p 80:80 -p 3306:3306 -p 8501:8501 projeto-etl-softex
   Isso fará com que:
   - O Apache (e Adminer) estejam acessíveis pela porta 80.
   - O MySQL (MariaDB) esteja acessível pela porta 3306.
   - O dashboard do Streamlit esteja disponível pela porta 8501.

6. Acessar o Dashboard e Adminer  
   - Streamlit Dashboard: Abra o navegador e acesse http://localhost:8501 para visualizar o dashboard interativo.
   - Adminer: Acesse http://localhost/adminer.php para gerenciar o banco de dados.

## Detalhes do Dockerfile

O "Dockerfile" contém as seguintes etapas:
- Imagem Base: Utiliza "python:3.8-slim".
- Instalação de Dependências do Sistema: Instala Apache, PHP, PHP-MySQL, MariaDB Server, wget e tar.
- Download do Adminer: Baixa a versão mais recente do Adminer para acesso via navegador.
- Exposição de Portas: Expõe as portas 80 (Apache/Adminer), 3306 (MySQL) e 8501 (Streamlit).
- Configuração do Ambiente: Define o diretório de trabalho como "/app", copia os diretórios "codigos/" e "conf/" para o container e instala as dependências Python.
- Entrypoint: Torna o script "entrypoint.sh" executável e o utiliza para iniciar o container.

## Entrypoint

O arquivo "entrypoint.sh" é responsável por iniciar os serviços e o aplicativo. Certifique-se de que o script está configurado corretamente para:
- Iniciar o servidor web (Apache).
- Iniciar o servidor de banco de dados (MariaDB).
- Iniciar o aplicativo Streamlit.

Observação: Caso sejam necessárias configurações adicionais (por exemplo, inicialização do banco de dados ou migrações), ajuste o "entrypoint.sh" conforme as necessidades do projeto.

## Conclusão

Com estas instruções, você poderá construir e executar o projeto ETL utilizando Docker. O ambiente estará configurado para executar o pipeline ETL, carregar os dados no MySQL e disponibilizar um dashboard interativo para análise dos dados processados.

Para dúvidas ou sugestões, sinta-se à vontade para entrar em contato.
