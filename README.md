# 🔴 Projeto de Web Scraping  (TASK 1)

## Descrição
Este projeto é uma aplicação Java Spring Boot que realiza web scraping no site do governo brasileiro para baixar documentos PDF específicos (anexos) relacionados à atualização do rol de procedimentos da ANS (Agência Nacional de Saúde Suplementar). A aplicação baixa os arquivos, armazena-os localmente e os compacta em um arquivo ZIP.

## Funcionalidades
- Web scraping na página da ANS para identificar links de documentos PDF
- Download automático dos dois primeiros anexos encontrados
- Armazenamento dos arquivos em diretório local
- Compactação dos arquivos baixados em um único arquivo ZIP
- API REST para acionar o processo de scraping e download

## Estrutura do Projeto
- **Controller**: Gerencia as requisições HTTP e direciona para os serviços apropriados
- **Service**: Contém a lógica de negócio para scraping e download dos anexos
- **Utils**: Classes utilitárias para download de arquivos e manipulação de arquivos/diretórios

## Tecnologias Utilizadas
- Java
- [Spring Boot](https://spring.io/projects/spring-boot)
- [JSoup](https://jsoup.org/) (para web scraping)
- [SLF4J](https://www.baeldung.com/slf4j-with-log4j2-logback) (para logging)

## Pré-requisitos
- JDK 8 ou superior
- Maven

## Como Executar
### 1. Clone o repositório
```bash
git clone https://github.com/DanielDeAzevedoCordeiro1/extracao_dados_operadoras.git
cd task1
```
2. Navegue até o diretório do projeto
3. Execute o comando: `mvn spring-boot:run`
4. Acesse a API em: `http://localhost:8080/api/scraping/download-attachments`

## Estrutura de Diretórios
- `downloads/`: Diretório onde os arquivos baixados são armazenados temporariamente
- `output/`: Diretório onde o arquivo ZIP final é salvo

## Endpoints da API
- **GET** `/api/scraping/download-attachments`: Inicia o processo de scraping, download e compactação dos anexos

## Classes Principais

### ScrapingController
Controlador REST que expõe o endpoint para acionar o download dos anexos.

### ScrapingService
Serviço responsável por conectar ao site da ANS, identificar os links de PDF, baixar os arquivos e compactá-los.

### DownloadUtils
Utilitário para download de arquivos da web para o sistema de arquivos local.

### FileUtils
Utilitário para operações com arquivos, incluindo a compactação de diretórios em arquivos ZIP.

## Configurações
- **BASE_URL**: URL base para o scraping (`https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos`)
- **DOWNLOAD_DIR**: Diretório para armazenamento temporário dos arquivos baixados (`downloads`)
- **OUTPUT_DIR**: Diretório para o arquivo ZIP final (`output`)

## Observações
- A aplicação está configurada para baixar apenas os dois primeiros arquivos PDF encontrados na página
- Certifique-se de que a aplicação tem permissão para criar diretórios e arquivos no sistema
- Verifique se o site alvo permite web scraping antes de utilizar esta aplicação



# 🔴 Extração e Transformação de Dados do Rol de Procedimentos ANS  (TASK 2)

## Descrição
Este projeto consiste em um script Python que extrai tabelas de procedimentos e eventos em saúde de arquivos PDF da ANS (Agência Nacional de Saúde Suplementar), processa os dados extraídos substituindo abreviações por suas descrições completas, e exporta os resultados em formato CSV compactado.

## Funcionalidades
- Extração de tabelas de procedimentos de arquivos PDF
- Identificação automática de arquivos de anexo no diretório especificado
- Extração de legendas para substituição de abreviações (OD e AMB)
- Processamento e limpeza dos dados extraídos
- Exportação para formato CSV
- Compactação do resultado em arquivo ZIP

## Pré-requisitos
- Python 3.x
- Bibliotecas Python listadas em `requirements.txt`
- Java Runtime Environment (JRE) - necessário para a biblioteca Tabula

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/DanielDeAzevedoCordeiro1/extracao_dados_operadoras.git
cd task2
```

2. Crie e ative um ambiente virtual Python:
```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Estrutura do Projeto
- `main.py`: Script principal que orquestra todo o processo
- `extractor.py`: Funções para extração de tabelas e legendas do PDF
- `processor.py`: Funções para processamento e limpeza dos dados
- `file_utils.py`: Funções utilitárias para manipulação de arquivos
- `requirements.txt`: Lista de dependências do projeto

## Como Usar

1. Configure o diretório de downloads no arquivo `main.py`:
```python
downloads_dir = "/caminho/para/seu/diretorio/"
```

2. Execute o script principal:
```bash
python main.py
```

3. Os resultados serão salvos em:
   - CSV: `./output/tabela_rol_procedimentos.csv`
   - ZIP: `./output/Teste_Daniel.zip` (Altere o nome do zip para o que desejar )

![Captura de tela de 2025-03-30 17-19-02](https://github.com/user-attachments/assets/fa11bd66-52ea-487a-887c-fdd97ea89fd9)


## Fluxo de Execução

1. Criação dos diretórios necessários
2. Localização do arquivo de anexo no diretório especificado
3. Extração das tabelas do PDF
4. Extração das legendas para substituição das abreviações
5. Processamento e limpeza dos dados
6. Exportação para CSV
7. Compactação do CSV em arquivo ZIP

## Detalhes Técnicos

### Extração de Tabelas
Utiliza a biblioteca Tabula para extrair tabelas do PDF. O processo identifica tabelas que contêm a coluna "PROCEDIMENTO".

### Extração de Legendas
Utiliza expressões regulares para encontrar as descrições completas das abreviações OD e AMB no texto do PDF.

### Processamento de Dados
Substitui as abreviações encontradas nas colunas pelos seus valores completos e remove linhas vazias.

## Bibliotecas Utilizadas
- `pandas`: Manipulação de dados tabulares
- `tabula-py`: Extração de tabelas de PDFs
- `PyPDF2`: Leitura e extração de texto de PDFs
- `re`: Processamento de expressões regulares
- `os`: Interação com o sistema de arquivos
- `zipfile`: Criação de arquivos ZIP

## Solução do Teste
Este projeto cumpre os requisitos do Teste de Transformação de Dados:
1. Extrai os dados da tabela Rol de Procedimentos do PDF do Anexo I
2. Salva os dados em formato CSV estruturado
3. Compacta o CSV em um arquivo denominado "Teste_{seu_nome}.zip"
4. Substitui as abreviações nas colunas OD e AMB pelas descrições completas

## Troubleshooting

Se você encontrar problemas com a biblioteca Tabula, verifique se:
- Java está instalado e configurado corretamente
- A versão do Java é compatível (recomendado JRE 8+)
- As permissões de acesso ao arquivo PDF estão corretas



# 🔴 Projeto de Importação de Dados ANS  (TASK 3)

## Descrição
Este projeto fornece uma solução para importação e processamento de dados da Agência Nacional de Saúde Suplementar (ANS) para um banco de dados MySQL rodando em um contaier Docker. O sistema processa dois tipos principais de dados:

1. **Demonstrativos Contábeis** - Dados financeiros das operadoras de saúde
2. **Cadastro de Operadoras** - Informações cadastrais das operadoras de planos de saúde

## Funcionalidades
- Importação de múltiplos arquivos CSV de demonstrativos contábeis
- Processamento paralelo para maior eficiência
- Importação de dados de operadoras de saúde
- Validação e limpeza de dados durante o processo de importação
- Contêinerização com Docker para fácil implantação

## Pré-requisitos
- Python 3.8+
- Docker e Docker Compose
- Conexão com a internet para download das imagens Docker

## Estrutura do Projeto
- `dms.py` - Script para importação dos demonstrativos contábeis
- `operadoras.py` - Script para importação dos dados de operadoras
- `docker-compose.yml` - Configuração do ambiente Docker
- `init.sql` - Script SQL para inicialização do banco de dados
- `requirements.txt` - Dependências Python do projeto

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/DanielDeAzevedoCordeiro1/extracao_dados_operadoras.git
cd task3
```

### 2. Crie e ative um ambiente virtual Python ((venv)[https://docs.python.org/pt-br/3/library/venv.html]))
```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Inicie o banco de dados MySQL com Docker
```bash
docker-compose up -d
```

## Configuração

### Configuração dos diretórios de dados
Antes de executar os scripts, certifique-se de ajustar os caminhos para os arquivos CSV nos scripts:

No arquivo `dms.py`:
```python
CSV_DIRECTORY = "/caminho/para/seus/arquivos/csv/"
```

No arquivo `operadoras.py`:
```python
CSV_PATH_OPERADORAS = "./relatorio/Relatorio_cadop.csv"
```
![Captura de tela de 2025-03-30 18-03-25](https://github.com/user-attachments/assets/9981d9cd-9e28-46e1-8f0c-979ab1027ecb)

### Configuração do banco de dados
As configurações de conexão ao banco de dados estão definidas em ambos os scripts:

```python
DB_CONFIG = {
    "username": "root",
    "password": "123",
    "hostname": "localhost",
    "database": "ans_db",
    "port": 3306
}
```

Ajuste conforme necessário se você modificar as configurações do Docker.

## Uso

### Importar dados de operadoras rode primeiro o operadoras.py !
```bash
python operadoras.py
```

### Importar demonstrativos contábeis
```bash
python dms.py
```

## Parâmetros Configuráveis

### No script `dms.py`:
- `CHUNKSIZE`: Tamanho dos chunks para processamento em lote (padrão: 10.000)
- `MAX_WORKERS`: Número máximo de workers para processamento paralelo (padrão: 4)

## Estrutura do Banco de Dados

### Tabela `dems_contabeis`
- `id`: Identificador único (chave primária)
- `DATA`: Data do demonstrativo
- `REG_ANS`: Registro da operadora na ANS
- `CD_CONTA_CONTABIL`: Código da conta contábil
- `DESCRICAO`: Descrição da conta
- `VL_SALDO_INICIAL`: Valor do saldo inicial
- `VL_SALDO_FINAL`: Valor do saldo final

### Tabela `operadoras`
- `Registro_ANS`: Registro da operadora (chave primária)
- `CNPJ`: CNPJ da operadora
- `Razao_Social`: Razão social
- `Nome_Fantasia`: Nome fantasia
- E outros campos cadastrais...

## Processamento de Dados
O projeto implementa várias otimizações para melhorar o desempenho:

1. **Processamento em chunks**: Os dados são processados em lotes para reduzir o uso de memória
2. **Multithreading**: Utiliza ThreadPoolExecutor para processamento paralelo
3. **Connection pooling**: Mantém um pool de conexões com o banco de dados para reduzir overhead

## Troubleshooting

### Problemas com a conexão MySQL
Verifique se o contêiner Docker está rodando:
```bash
docker ps
```

Reinicie o contêiner se necessário:
```bash
docker-compose restart
```

### Erros de importação de dados
- Verifique se os arquivos CSV estão no formato correto (separados por `;`)
- Verifique se os caminhos dos arquivos estão configurados corretamente
- Consulte os logs para mensagens de erro detalhadas




# 🔴 Projeto de Visualização de Operadoras de Saúde ANS  (TASK 4)

## Descrição
Aplicação web para visualização dos dados financeiros das principais operadoras de saúde registradas na ANS (Agência Nacional de Saúde Suplementar), permitindo filtrar e exibir as 10 maiores operadoras por despesas Trimestral e Anual.

## Funcionalidades

- Visualização das 10 maiores operadoras por despesas: Ultimo Trimestre e Anual 

## Tecnologias Utilizadas

- **Frontend**: [Vue.js 3](https://vuejs.org/), [Axios](https://axios-http.com/ptbr/docs/intro)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/pt/), MySQL Connector Python
- **Banco de Dados**: [MySQL](https://www.mysql.com/) (em container Docker)

## Estrutura do Projeto

```
projeto-ans/
├── frontend/consultar-dados
│   └── App.vue                   
│
├── backend/
│   ├── main.py                 
│   ├── database.py               
│   └── requirements.txt       
```

## Configuração e Execução

### Banco de Dados
O banco de dados MySQL já está rodando em um container Docker. A conexão está configurada no arquivo `database.py` e aponta para o container criado na task-3, recomendo rodar a aplicacao que sobe o container com os dados ja tratados e inseridos no banco MySql, para esta aplicacao funcionar
### Backend (FastAPI)

### 1. Clone o repositório
```bash
git clone https://github.com/DanielDeAzevedoCordeiro1/extracao_dados_operadoras.git
cd task4
```
### 2. Crie e ative um ambiente virtual Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

### 3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Inicie o servidor FastAPI:
   ```bash
   uvicorn main:app --reload 
   ```

### Frontend (Vue.js)

1. Navegue para a pasta do frontend
2. Instale as dependências:
   ```bash
   npm install
   npm install axios  
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

## Uso da Aplicação

1. Selecione o tipo de despesa no dropdown
2. Clique em "Carregar Dados"
3. Visualize as informações das 10 maiores operadoras de saúde

![Captura de tela de 2025-03-31 09-47-01](https://github.com/user-attachments/assets/91d35e67-f04e-4bf7-9f6d-5297af8b82fc)


## API

- **GET /api/data?tipo=anual** - 10 operadoras com maiores despesas anuais
- **GET /api/data?tipo=trimestre** - 10 operadoras com maiores despesas no último trimestre

## Solução de Problemas

- Verifique se o container Docker do banco de dados está rodando
- Confirme as credenciais em `database.py`
- Verifique os logs do console para erros


# Collection Postman

### Link de acesso:
https://daniel-9778286.postman.co/workspace/Daniel's-Workspace~1a74fb26-fb18-4bfb-83e8-7d1cc40eb2e3/collection/43596788-fe87afac-6458-4adc-a5f8-9c5030a27418?action=share&creator=43596788

### Como utilizar :

### 1. Abra o postman e va na aba superior esquerda e clique em import

![Captura de tela de 2025-03-31 10-19-54](https://github.com/user-attachments/assets/392aacdd-1419-409d-8c5b-c3c1d0b1620d)

### 2. Adicione o link acima

![Captura de tela de 2025-03-31 10-24-59](https://github.com/user-attachments/assets/250d52f7-680f-4d91-97e5-02ff14f7dd98)

