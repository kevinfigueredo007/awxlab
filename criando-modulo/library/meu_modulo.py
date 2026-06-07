#!/usr/bin/python

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
            msg="Policy validada!",
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