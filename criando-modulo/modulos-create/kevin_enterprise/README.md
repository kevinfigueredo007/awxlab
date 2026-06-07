# kevin_enterprise.automation

# Exemplo de documentação!!!!

Collection Ansible para automações corporativas, compliance e integração com AWS, AAP e Open Policy Agent (OPA).

## Visão Geral

A collection `kevin_enterprise.automation` fornece módulos, roles, plugins e utilitários para padronizar automações executadas através do Ansible Automation Platform (AAP).

Principais objetivos:

* Reduzir código duplicado entre playbooks
* Centralizar integrações com AWS
* Centralizar integrações com OPA
* Fornecer componentes reutilizáveis para compliance
* Padronizar auditoria e observabilidade das execuções

---

## Estrutura

```text
kevin_enterprise.automation/
├── plugins/
│   ├── modules/
│   ├── module_utils/
│   ├── callback/
│   ├── inventory/
│   └── filter/
│
├── roles/
│
├── docs/
│
└── tests/
```

---

## Requisitos

* Ansible Core >= 2.16
* Python >= 3.11

Dependências opcionais:

* boto3
* requests
* pyjwt

---

## Instalação

### Collection local

```bash
ansible-galaxy collection install kevin_enterprise-automation-1.0.0.tar.gz
```

### Desenvolvimento

```bash
git clone https://git.example.com/kevin_enterprise/automation.git

cd automation

ansible-galaxy collection build
```

---

## Módulos Disponíveis

### opa_authorize

Executa validações de autorização utilizando Open Policy Agent.

Exemplo:

```yaml
- name: Validar autorização
  kevin_enterprise.automation.opa_authorize:
    user: kevin
    action: execute
    resource: inventory-prod
```

---

### compliance_check

Executa verificações de compliance em contas AWS.

Exemplo:

```yaml
- name: Executar compliance
  kevin_enterprise.automation.compliance_check:
    account_id: "123456789012"
```

---

### aws_account_info

Obtém informações de uma conta AWS.

Exemplo:

```yaml
- name: Buscar informações
  kevin_enterprise.automation.aws_account_info:
    account_id: "123456789012"
```

---

## Roles

### opa

Instala e configura Open Policy Agent.

```yaml
roles:
  - role: kevin_enterprise.automation.opa
```

---

## Inventory Plugins

### aws_organization

Gera inventário automaticamente a partir do AWS Organizations.

Exemplo:

```yaml
plugin: kevin_enterprise.automation.aws_organization

root_ou: r-xxxx
```

Resultado:

```text
production
sandbox
shared-services
```

---

## Callback Plugins

### audit

Registra eventos de execução para auditoria corporativa.

Configuração:

```ini
[defaults]
callbacks_enabled = audit
```

Eventos capturados:

* Início do Job
* Fim do Job
* Tasks executadas
* Falhas
* Mudanças realizadas

---

## Retorno Padronizado

Todos os módulos da collection seguem o padrão:

```yaml
changed: false
success: true
message: Operação concluída
```

Exemplo:

```yaml
changed: false
success: true
account_id: "123456789012"
compliant: true
```

---

## Integração com AAP

A collection foi projetada para execução dentro do Ansible Automation Platform.

Compatível com:

* Job Templates
* Workflow Templates
* Execution Environments
* Dynamic Inventories
* Credential Types

---

## Observabilidade

A collection suporta:

* Logs estruturados
* Callback Plugins
* Métricas customizadas
* Integração com sistemas de auditoria

---

## Testes

Executar testes unitários:

```bash
pytest tests/unit
```

Executar testes de integração:

```bash
pytest tests/integration
```

---

## Versionamento

Seguimos Semantic Versioning.

Exemplos:

* 1.0.0 → Primeira versão estável
* 1.1.0 → Nova funcionalidade
* 1.1.1 → Correção de bug

---

## Contribuição

1. Crie uma branch
2. Implemente a alteração
3. Adicione testes
4. Abra um Pull Request

---

## Licença

Uso interno kevin_enterprise.
