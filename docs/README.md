
# Packet Challenge
Aplicação para análise de tráfego de rede, captura de pacotes e exibição de estatísticas básicas.
## Estrutura do Projeto
packet-challenge/
├── docker-compose.yml
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── capture.py
│   └── database.py
└── docs/
    ├── README.md
    └── DECISIONS.md
## Pré-requisitos
- Docker e Docker Compose instalados
- Permissão de administrador/root para capturar pacotes
- Interface de rede disponível para captura (ex: eth0, wlan0)
## Configuração
1. Defina a interface de rede a ser monitorada através da variável de ambiente INTERFACE:
export INTERFACE=eth0
2. Configure a conexão com o banco de dados via Docker Compose (já definido nos serviços app e db).
## Execução
docker-compose up --build
## Estatísticas exibidas
- Total de pacotes capturados
- Número de pacotes por protocolo (TCP, UDP, outros)
- Top 5 endereços IP de origem com mais tráfego
- Top 5 endereços IP de destino com mais tráfego
