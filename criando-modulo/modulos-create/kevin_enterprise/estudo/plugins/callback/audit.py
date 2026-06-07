from ansible.plugins.callback import CallbackBase
import os, datetime
timezone = datetime.timezone(datetime.timedelta(hours=-3))  # Definir o fuso horário para GMT-3 (Horário de Brasília)


class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'audit'

    timestamp = datetime.datetime.now(timezone).isoformat()


    def v2_playbook_on_start(self, playbook):
        print("Playbook iniciado demo")

        timestamp = datetime.datetime.now(timezone).isoformat()

        dir_log = "/tmp/audit/logs/audit.log"
        os.makedirs(os.path.dirname(dir_log), exist_ok=True)
        with open(dir_log, "a") as f:
            f.write(f"Playbook iniciado demo - {timestamp}\n ")
            
    def v2_playbook_on_stats(self, stats):
        print("Playbook finalizado demo")

        timestamp = datetime.datetime.now(timezone).isoformat()

        dir_log = "/tmp/audit/logs/audit.log"
        os.makedirs(os.path.dirname(dir_log), exist_ok=True)
        with open(dir_log, "a") as f:
            f.write(f"Playbook finalizado demo - {timestamp}\n")