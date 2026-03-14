# SRE AI-Ops Lab (Digital Twin Project)

Bem-vindo ao laboratório de SRE com Inteligência Artificial. Este repositório contém a documentação e os scripts de automação para provisionar um ambiente Kubernetes local (Kind) integrado com LLMs locais (LM Studio).

## 📂 Estrutura Organizada

- **`docs/`**: Contém toda a documentação técnica, manuais e planos de arquitetura.
    - [Arquitetura Visual](docs/architecture_diagram.md)
    - [Manual de Instruções Críticas](docs/Manual%20de%20Instruções%20Críticas%20para%20o%20Antigravity.md)
    - [Maturidade Técnica](docs/Maturidade%20Técnica.md)

- **`.agent/`**: Configurações e scripts do Assistente Antigravity.
    - `scripts/organize_lab.py`: Script de manutenção e geração de artefatos.

- **`/home/marcelo/lab-infra-repo/`** (Externo):
    - Diretório gerado automaticamente contendo o código fonte dos Agentes e Manifestos Kubernetes prontos para deploy.

## 🚀 Como Iniciar

A infraestrutura base já foi gerada em `lab-infra-repo`. Para subir o laboratório:

1.  Navegue até o diretório de infraestrutura:
    ```bash
    cd /home/marcelo/lab-infra-repo
    ```

2.  Siga as instruções de [Comandos de Build & Injeção](docs/Comandos%20de%20Build%20&%20Injeção.md) para construir a imagem do agente.

3.  Execute o script de provisionamento (quando disponível/gerado).

## 🛠️ Manutenção

Para reorganizar novos documentos ou regenerar os arquivos de infraestrutura, execute:

```bash
python3 .agent/scripts/organize_lab.py
```
