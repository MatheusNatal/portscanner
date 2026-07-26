# ⚡ PortScanner CLI

> Ferramenta de linha de comando (CLI) leve, de alto desempenho e multithread para escaneamento e diagnóstico de portas TCP.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Type](https://img.shields.io/badge/Interface-CLI-orange)

## 📌 Visão Geral

O **PortScanner CLI** é um utilitário desenvolvido em Python projetado para verificar a disponibilidade de portas TCP em redes locais ou remotas. A ferramenta utiliza um pool de threads gerenciado (`ThreadPoolExecutor`) para realizar varreduras paralelas rápidas e eficientes, fornecendo resolução de nomes de serviço e suporte a faixas de portas (*ranges*).

### ✨ Principais Recursos

- **Varredura Ultrarrápida (Multithreaded):** Utiliza `concurrent.futures.ThreadPoolExecutor` para executar requisições simultâneas sem congelar o sistema.
- **Resolução Automática de Serviços:** Identifica o protocolo associado a portas abertas conhecidas (ex: `80 -> http`, `22 -> ssh`).
- **Flexibilidade de Alvos:** Aceita endereços IP (`192.168.1.1`) ou nomes de domínio (`scanme.nmap.org`).
- **Suporte a Faixas de Portas:** Permite especificar portas individuais (ex: `80,443`) ou faixas completas (ex: `20-1000`).
- **Tratamento de Interrupções:** Encerramento limpo e seguro via `Ctrl+C` sem lançar exceções não tratadas no terminal.
- **Sem Dependências Externas:** Desenvolvido exclusivamente com a biblioteca padrão do Python (`socket`, `argparse`, `concurrent.futures`).

---

## 🚀 Instalação

### Pré-requisitos
Apenas o **Python 3.8+** instalado na sua máquina (Windows, Linux ou macOS).

```bash
# Clone o repositório
git clone https://github.com/MatheusNatal/portscanner.git

# Acesse o diretório do projeto
cd portscanner
``` 

## 💻 Como Usar
### Execute o script diretamente pelo terminal:

1. Escaneamento Padrão (Localhost)
Escaneia as portas principais (21, 22, 25, 80, 443, 8080, 8443) no host local:
```bash
python portscanner.py
```
2. Escanear um Alvo Específico
```bash
python portscanner.py -t scanme.nmap.org
```
3. Especificar Portas Personalizadas ou Faixas (Ranges)
```bash
# Portas específicas
python portscanner.py -t 192.168.1.1 -p 80,443,8080

# Faixa de portas (1 a 1024)
python portscanner.py -t 192.168.1.1 -p 1-1024
```
---
## ⚙️ Opções de Linha de Comando (CLI)

| Opção | Nome Longo | Descrição |
| :--- | :--- | :--- |
| `-h` | `--help` | Exibe a mensagem de ajuda e instruções de uso. |
| `-t` | `--target` | IP ou hostname alvo (padrão: localhost). |
| `-p` | `--ports` | Portas a escanear (ex: 80,443 ou 20-1000). |
| `-w` | `--workers` | Número de threads simultâneas (padrão: 100). |
| | `--timeout` | Tempo limite por conexão em segundos (padrão: 1.0s). |

---
## 📄 Licença
Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter mais detalhes.

Desenvolvido por Matheus Natal.
