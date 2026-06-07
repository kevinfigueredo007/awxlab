#!/usr/bin/python
# -*- coding: utf-8 -*-

# 1. DOCUMENTAÇÃO PRINCIPAL
DOCUMENTATION = r'''
---
module: mask_account
short_description: Mascara IDs de contas bancárias ou cloud para auditoria
description:
    - Este módulo recebe um ID de conta e aplica uma máscara de caracteres ocultos.
    - Útil para sanitização de logs e relatórios estruturados.
version_added: "1.0.0"
author:
    - Kevin (@kevin_enterprise)
options:
  account_id:
    description:
      - O ID da conta ou recurso que precisa ser mascarado.
    type: str
    required: true
  visible_chars:
    description:
      - Quantidade de caracteres que permanecerão visíveis no início da string.
    type: int
    default: 4
'''

# 2. EXEMPLOS DE USO NO PLAYBOOK
EXAMPLES = r'''
# Exemplo básico de uso
- name: Mascarar uma conta com configuração padrão
  kevin_enterprise.estudo.mask_account:
    account_id: "123456789012"
  register: resultado

# Exemplo customizando os caracteres visíveis
- name: Mascarar mantendo apenas os 2 primeiros dígitos
  kevin_enterprise.estudo.mask_account:
    account_id: "9876543210"
    visible_chars: 2
'''

# 3. DOCUMENTAÇÃO DO RETORNO (O que o seu módulo devolve no 'register')
RETURN = r'''
masked_value:
    description: A string original processada com a máscara aplicada.
    returned: always
    type: str
    sample: "1234********"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.api_rickandmorty import buscar_personagem


def run_module():

    module_args = dict(
        nome=dict(type='str', required=True),
        idade=dict(type='int', required=False, default=18),
        token=dict(type='str', no_log=True),
        account_id=dict(type='str', aliases=['aws_account']),
        accounts=dict(type='list', elements='str'),
        action=dict(type='str', choices=['start', 'stop', 'restart']),
        config=dict(
            type='dict',
            options=dict(
                host=dict(type='str', required=True),
                port=dict(type='int', default=8181)
            )
        )
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )



    api_name = buscar_personagem(id=1)


    result = dict(
            changed=False,
            msg="Policy validada",
            user=module.params['nome'],
            idade=module.params['idade'],
            token=module.params['token'],
            config=module.params['config'],
            account_id=module.params['account_id'],
            accounts=module.params['accounts'],
            action=module.params['action'],
            rick_and_morty_character=api_name
    )    

    nome = module.params['nome']

    if nome == 'joao':
        result['changed'] = True
        result['mensagem'] = f'Olá {nome}! (alterado)'
    
    if nome == 'maria':
        module.fail_json(
        msg="Usuário não encontrado"
    )

    result['mensagem'] = f'Olá {nome}!'

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
