import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Cores para o terminal (ANSI Escape Codes)
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"
GRAY = "\033[90m"

MAIN_PORTS = [21, 22, 25, 80, 443, 8080, 8443]

def parse_portas(texto_portas: str) -> list[int]:
    """Converte entradas como '80,443' ou '20-100' em uma lista de inteiros sem duplicatas."""
    portas = set()
    for parte in texto_portas.split(','):
        parte = parte.strip()
        if '-' in parte:
            inicio, fim = parte.split('-')
            portas.update(range(int(inicio), int(fim) + 1))
        elif parte.isdigit():
            portas.add(int(parte))
    return sorted(list(portas))

def escanear_porta(target: str, porta: int, timeout: float) -> tuple[int, bool]:
    """Tenta conectar à porta TCP do alvo de forma rápida."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            resultado = sock.connect_ex((target, porta))
            return porta, resultado == 0
    except Exception:
        return porta, False

def main():
    parser = argparse.ArgumentParser(
        description="PortScanner CLI - Ferramenta multithread rápida para verificação de portas TCP."
    )
    parser.add_argument("-t", "--target", help="IP ou hostname alvo (padrão: localhost)")
    parser.add_argument("-p", "--ports", help="Portas a escanear (ex: 80,443 ou 20-100). Se omitido, escaneia as principais portas.")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Número de threads simultâneas (padrão: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout do socket em segundos (padrão: 1.0s)")

    args = parser.parse_args()

    # Define o alvo
    target = args.target if args.target else socket.gethostname()
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{RED}[!] Erro: Não foi possível resolver o host '{target}'.{RESET}")
        sys.exit(1)

    # Define as portas
    if args.ports:
        try:
            portas = parse_portas(args.ports)
        except ValueError:
            print(f"{RED}[!] Erro: Formato de portas inválido. Use ex: '80,443' ou '20-100'.{RESET}")
            sys.exit(1)
    else:
        portas = MAIN_PORTS

    print(f"{CYAN}==================================================")
    print(f" PortScanner CLI - por Matheus Natal")
    print(f"=================================================={RESET}")
    print(f"Alvo:    {target} ({target_ip})")
    print(f"Portas:  {len(portas)} porta(s) selecionada(s)")
    print(f"Threads: {args.workers}")
    print(f"{CYAN}--------------------------------------------------{RESET}\n")

    portas_abertas = 0

    try:
        # Gerenciamento moderno de threads
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(escanear_porta, target_ip, porta, args.timeout): porta 
                for porta in portas
            }

            for future in as_completed(futures):
                porta, aberta = future.result()
                if aberta:
                    portas_abertas += 1
                    try:
                        nome_servico = socket.getservbyport(porta, 'tcp')
                    except OSError:
                        nome_servico = "desconhecido"
                    print(f" {GREEN}[+] Porta {porta:<5} ABERTA  ({nome_servico}){RESET}")
                else:
                    # Exibe portas fechadas em cinza escuro de forma mais discreta
                    pass 

    except KeyboardInterrupt:
        print(f"\n{RED}[!] Escaneamento interrompido pelo usuário (Ctrl+C).{RESET}")
        sys.exit(0)

    print(f"\n{CYAN}--------------------------------------------------{RESET}")
    print(f"Escaneamento concluído. {portas_abertas} porta(s) aberta(s) encontrada(s).")

if __name__ == "__main__":
    main()
