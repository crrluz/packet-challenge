import os
import sys
import logging
from scapy.all import sniff, IP, TCP, UDP
from collections import Counter
from database import create_table, insert_packets

# Configuração básica do logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BATCH_SIZE = 50

class PacketCapture:
    def __init__(self, iface, batch_size=50):
        self.iface = iface
        self.batch_size = batch_size
        self.packet_list = []   # Buffer para envio ao banco
        self.all_packets = []   # Acumula todos os pacotes para estatísticas

    def process_packet(self, packet):
        src_ip = dst_ip = protocol = None
        size = len(packet)

        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst

            if TCP in packet:
                protocol = "TCP"
            elif UDP in packet:
                protocol = "UDP"
            else:
                protocol = str(packet[IP].proto)
        else:
            return

        self.packet_list.append((src_ip, dst_ip, protocol, size))
        self.all_packets.append((src_ip, dst_ip, protocol, size))

        if len(self.packet_list) >= self.batch_size:
            self.flush_packets()

    def flush_packets(self):
        if not self.packet_list:
            return
        insert_packets(self.packet_list)
        logger.info(f"{len(self.packet_list)} pacotes inseridos no banco.")
        self.packet_list.clear()

    def show_statistics(self):
        if not self.all_packets:
            logger.info("Nenhum pacote capturado ainda.")
            return

        total_packets = len(self.all_packets)
        protocols = Counter(p[2] for p in self.all_packets)
        top_src = Counter(p[0] for p in self.all_packets).most_common(5)
        top_dst = Counter(p[1] for p in self.all_packets).most_common(5)

        logger.info("\n=== Estatísticas de Tráfego ===")
        logger.info(f"Total de pacotes: {total_packets}")
        logger.info("Pacotes por protocolo:")
        for proto, count in protocols.items():
            logger.info(f"  {proto}: {count}")
        logger.info("Top 5 IPs de origem:")
        for ip, count in top_src:
            logger.info(f"  {ip}: {count}")
        logger.info("Top 5 IPs de destino:")
        for ip, count in top_dst:
            logger.info(f"  {ip}: {count}")

def main():
    iface = input("Informe a interface para captura (exemplo: en0, eth0): ").strip()
    if not iface:
        logger.error("Interface não informada. Encerrando o programa.")
        sys.exit(1)

    logger.info(f"Iniciando captura na interface {iface}...")
    create_table()

    capture = PacketCapture(iface=iface, batch_size=BATCH_SIZE)

    try:
        sniff(iface=iface, prn=capture.process_packet, store=False)
    except PermissionError:
        logger.error("Erro: é necessário rodar com privilégios de administrador/root para capturar pacotes.")
        sys.exit(1)
    except ValueError as ve:
        logger.error(f"Erro: {ve}")
        logger.error("Interface informada não encontrada. Verifique o nome e tente novamente.")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Captura interrompida pelo usuário (Ctrl+C).")

    # Envia pacotes restantes que não foram inseridos ainda
    capture.flush_packets()

    # Mostra estatísticas ao final
    capture.show_statistics()

if __name__ == "__main__":
    main()
