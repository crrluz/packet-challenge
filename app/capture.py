
import os
from scapy.all import sniff, IP, TCP, UDP
from collections import Counter
from database import create_table, insert_packets
INTERFACE = os.getenv("INTERFACE", "eth0")
create_table()
packet_list = []
def process_packet(packet):
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
            protocol = packet[IP].proto
    else:
        return
    packet_list.append((src_ip, dst_ip, str(protocol), size))
def show_statistics():
    if not packet_list:
        print("Nenhum pacote capturado ainda.")
        return
    total_packets = len(packet_list)
    protocols = Counter(p[2] for p in packet_list)
    top_src = Counter(p[0] for p in packet_list).most_common(5)
    top_dst = Counter(p[1] for p in packet_list).most_common(5)
    print(f"\n=== Estatísticas de Tráfego ===")
    print(f"Total de pacotes: {total_packets}")
    print("Pacotes por protocolo:")
    for proto, count in protocols.items():
        print(f"  {proto}: {count}")
    print("Top 5 IPs de origem:")
    for ip, count in top_src:
        print(f"  {ip}: {count}")
    print("Top 5 IPs de destino:")
    for ip, count in top_dst:
        print(f"  {ip}: {count}")
def main():
    print(f"Iniciando captura na interface {INTERFACE}...")
    try:
        sniff(iface=INTERFACE, prn=process_packet, store=False)
    except PermissionError:
        print("Erro: é necessário rodar com privilégios de administrador/root para capturar pacotes.")
    insert_packets(packet_list)
    show_statistics()
if __name__ == "__main__":
    main()
