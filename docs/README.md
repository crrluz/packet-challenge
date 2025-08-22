# Packet Capture and Storage Application

## Descrição

Este projeto captura pacotes de rede em uma interface especificada, armazena informações relevantes em um banco de dados PostgreSQL e exibe estatísticas resumidas sobre o tráfego capturado. É útil para análise de tráfego, monitoramento e aprendizado sobre redes.

## Funcionalidades

- Captura pacotes TCP e UDP em tempo real.
- Extrai informações como IP de origem, IP de destino, protocolo e tamanho do pacote.
- Armazena os dados capturados em uma tabela PostgreSQL.
- Exibe estatísticas em tempo real: total de pacotes, contagem por protocolo e os 5 IPs mais frequentes de origem e destino.

## Requisitos

- Python 3.7 ou superior
- PostgreSQL
- Bibliotecas Python:
  - scapy
  - psycopg2-binary
- Permissões de root/administrador para capturar pacotes na interface de rede.

## Configuração

1. **Banco de Dados**

Configure um banco PostgreSQL com os seguintes dados padrão (pode ser configurado via variáveis de ambiente):

DB_HOST=localhost
DB_PORT=5432
DB_NAME=packetdb
DB_USER=packetuser
DB_PASSWORD=packetpass


2. **Interface de Captura**

Ao rodar o programa, será solicitado que você informe a interface de rede para captura (exemplo: `en0`, `eth0`). Se a interface informada não existir no sistema, o programa exibirá uma mensagem clara de erro e encerrará a execução.

**Importante:** Informe corretamente o nome da interface de rede que deseja monitorar. Exemplos comuns:

- macOS: `en0`
- Linux: `eth0`, `wlan0`

3. **Instalação das Dependências**

Use o pip para instalar as bibliotecas necessárias:

```bash
pip install scapy psycopg2-binary
```

## Como Rodar

Execute o script principal com permissões de administrador (root/sudo):

```bash
sudo python3 capture.py
```
A captura inicia na interface configurada, e os pacotes capturados serão armazenados no banco. Quando você interromper a execução (Ctrl+C), o programa insere os dados restantes no banco e exibe as estatísticas.

## O que esperar

- Mensagens de log informando a conexão ao banco e a criação da tabela.
- Logs periódicos informando a inserção de pacotes no banco.
- Estatísticas resumidas de tráfego exibidas após o encerramento da captura.

## Considerações

Rodar sem permissões de root/administrador resultará em erro ao tentar abrir a interface de captura.
Assegure que o banco PostgreSQL esteja ativo e que o usuário exista.
A tabela packets será criada automaticamente se não existir.

## Estrutura do Banco

Tabela packets com colunas:
- id: Identificador sequencial
- src_ip: IP de origem
- dst_ip: IP de destino
- protocol: Protocolo (TCP, UDP ou número)
- packet_size: Tamanho do pacote em bytes
- capture_time: Timestamp da captura (padrão: momento da inserção)