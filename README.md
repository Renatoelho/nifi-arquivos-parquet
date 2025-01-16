# Otimizando o Processamento de Dados no Apache NiFi com Arquivos Parquet

Este vídeo demonstra como otimizar o processamento de dados no **Apache NiFi**, com exemplos que convertem dados originados de diferentes fontes, incluindo **MySQL**, **MinIO** e o sistema de arquivos local, para o formato Parquet. O objetivo é evidenciar as vantagens do **Parquet** em termos de redução significativa do tamanho dos arquivos e maior eficiência no processamento. Além disso, o projeto explora as diferenças entre os métodos de compressão disponíveis para Parquet, como **GZIP** e **Snappy**, destacando seus impactos no desempenho e na compactação dos dados.

## Apresentação em Vídeo

<!-- https://www.youtube.com/@renato-coelho -->

<p align="center">
  <a href="https://www.youtube.com/@renato-coelho" target="_blank"><img src="imagens/thumbnail/thumbnail-nifi-arquivos-parquet-github.png" alt="Vídeo de apresentação"></a>
</p>

## Requisitos

+ ![Docker](https://img.shields.io/badge/Docker-27.4.1-green)

+ ![Docker-compose](https://img.shields.io/badge/Docker--compose-1.25.0-green)

+ ![Git](https://img.shields.io/badge/Git-2.25.1%2B-green)

+ ![Python](https://img.shields.io/badge/Python-3.8+-green)

+ ![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04-green)

## Setup do Projeto

### Deploy das Aplicações Via Docker Compose

```bash
docker compose -p nifi-otimizacao -f docker-compose.yaml up -d
```

### Geração do Arquivo `clientes.csv`

1. Acesse o diretório `nifi/mock`.

2. Crie o ambiente virtual:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate && pip install -U pip setuptools wheel faker
   ```

3. Execute o script para gerar o arquivo:
   ```bash
   python3 ./cria_mock_clientes.py
   ```

### Configurações no MinIO

#### Acesso MinIO

- **URL**: [http://localhost:9001/login](http://localhost:9001/login)
- **Usuário**: admin
- **Senha**: eO3RNPcKgWInlzPJuI08

### Ações no MinIO

- **Crie as credências**: Em ***Access Keys*** >> ***Create Access Key***
- **Crie um Bucket**: Em ***Bucket*** >> ***Create Bucket*** (Crie o bucket `exemplo` e o path `caminho_exemplo` e faça o upload do arquivo: `clientes.csv`)

### Instalação dos NARs para Parquet no Apache NiFi

Baixe os arquivos necessários:

- [nifi-parquet-nar](https://repo1.maven.org/maven2/org/apache/nifi/nifi-parquet-nar/2.0.0/nifi-parquet-nar-2.0.0.nar)
- [nifi-hadoop-libraries-nar](https://repo1.maven.org/maven2/org/apache/nifi/nifi-hadoop-libraries-nar/2.0.0/nifi-hadoop-libraries-nar-2.0.0.nar)

Adicione os NARs ao contêiner do NiFi:
```bash
docker cp ./nifi-parquet-nar-2.0.0.nar apache-nifi:/opt/nifi/nifi-current/nar_extensions
docker cp ./nifi-hadoop-libraries-nar-2.0.0.nar apache-nifi:/opt/nifi/nifi-current/nar_extensions
```

### Upload dos Templates no Apache NiFi

Faça o upload dos seguintes templates:

- Flow_Carga_Clientes_MySQL.json
- Otimizando_com_Arquivos_Parquet.json

### Configurações no Apache NiFi

#### Acesso Apache Nifi

- **URL**: [https://localhost:8443/nifi/](https://localhost:8443/nifi/)
- **Usuário**: nifi
- **Senha**: HGd15bvfv8744ghbdhgdv7895agqERAo

#### Crie 3 Controller Services ParquetRecordSetWriter

Configurações:

- Sem Compressão
- Compressão **GZIP**
- Compressão **Snappy**

#### Crie Controller Services CSVReader

Configurações:

- Value Separator: `;`
- Treat First Line as Header: `true`

#### Crie Controller Services DBCPConnectionPool (MySQL)

Configurações:

- Database Connection URL: `jdbc:mysql://mysql:3306/exemplo_db`
- Database Driver Class Name: `com.mysql.cj.jdbc.Driver`
- Database Driver Location(s): `/home/nifi/jdbc/mysql-connector-j-8.0.31.jar`
- Database User: `root`
- Password: `W45uE75hQ15Oa`

#### Crie Controller Services AWSCredentialsProviderControllerService

Configurações:

- Access Key ID: `<Gerado no MinIO>`
- Secret Access Key: `<Gerado no MinIO>`

#### Crie Controller Services JSON Configurations

Configurações:

- JsonRecordSetWriter
- JsonTreeReader

### Testes e Execução

Configure e execute os templates:

- Flow_Carga_Clientes_MySQL
- Otimizando_com_Arquivos_Parquet

***OBS.:*** Depois de importados os flows os controller Services devem ser ativados. 

## Referências

Overview, **Apache Parquet**. Disponível em: <https://parquet.apache.org/docs/overview/l>. Acesso em: 15 Jan. 2025.

Documentation, **MinIO Docs**. Disponível em: <https://min.io/docs/minio/linux/index.html>. Acesso em: 15 Jan. 2025.

Apache NiFi User Guide, **Apache Nifi**. Disponível em: <https://nifi.apache.org/nifi-docs/user-guide.html>. Acesso em: 15 Jan. 2025.

possible bug missing parquetreader version 2.0.0-M1, **community.cloudera.com**. Disponível em: <https://community.cloudera.com/t5/Support-Questions/possible-bug-missing-parquetreader-version-2-0-0-M1/m-p/381669>. Acesso em: 15 Jan. 2025.
