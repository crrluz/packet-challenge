
# Decisões Técnicas e Justificativas - Packet Challenge
## Linguagem de Programação
- Python: simplicidade e bibliotecas poderosas (Scapy, psycopg2).
## Captura de Pacotes
- Scapy: captura e análise de pacotes IP, TCP e UDP.
- Interface configurável via variável de ambiente INTERFACE.
## Armazenamento
- PostgreSQL 15: banco relacional confiável e compatível com Docker.
- Tabela packets: src_ip, dst_ip, protocol, packet_size, capture_time.
## Docker
- Docker Compose: orquestração de serviços app e db.
- Network mode host: necessário para capturar pacotes do host.
- Python 3.11-slim: leve e compatível.
## Estatísticas
- Counter do Python: total de pacotes, por protocolo, top 5 IPs origem/destino.
## Justificativa de decisões
- Separação de módulos para clareza e manutenção.
- Inserção em batch para reduzir overhead do banco.
- Interface configurável e Dockerizado para portabilidade.
- Documentação detalhada para uso e entendimento do projeto.
