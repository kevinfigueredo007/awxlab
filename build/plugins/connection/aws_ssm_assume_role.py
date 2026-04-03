# -*- coding: utf-8 -*-
from __future__ import annotations

import boto3
import botocore

from ansible.errors import AnsibleError
from ansible.utils.display import Display

# ---------------------------------------------------------------------------
# Import upstream plugin
# ---------------------------------------------------------------------------
try:
    from ansible_collections.amazon.aws.plugins.connection import aws_ssm as _upstream_module
    from ansible_collections.amazon.aws.plugins.connection.aws_ssm import (
        Connection as _UpstreamConnection,
    )
except ImportError as exc:
    raise AnsibleError(
        "aws_ssm_assume_role requer a collection 'amazon.aws'. "
        f"Instale com: ansible-galaxy collection install amazon.aws\n"
        f"Erro: {exc}"
    ) from exc

display = Display()

# ---------------------------------------------------------------------------
# Merge DOCUMENTATION (pai + custom)
# ---------------------------------------------------------------------------
_OUR_OPTIONS_YAML = r"""
  role_arn:
    description:
      - ARN da role para assumir
    type: str
    default: null
    vars:
      - name: ansible_aws_ssm_role_arn

  role_session_name:
    description:
      - Nome da sessão STS
    type: str
    default: ansible-ssm-session
    vars:
      - name: ansible_aws_ssm_role_session_name

  role_duration_seconds:
    description:
      - Duração das credenciais STS
    type: int
    default: 3600
    vars:
      - name: ansible_aws_ssm_role_duration_seconds
"""

try:
    import yaml

    parent_doc = yaml.safe_load(_upstream_module.DOCUMENTATION)
    our_opts = yaml.safe_load(_OUR_OPTIONS_YAML)

    parent_doc["name"] = "aws_ssm_assume_role"
    parent_doc["options"].update(our_opts)

    DOCUMENTATION = yaml.dump(parent_doc, allow_unicode=True)

except Exception:
    DOCUMENTATION = f"""
name: aws_ssm_assume_role
short_description: aws ssm com assume role
options:
{_OUR_OPTIONS_YAML}
"""

# ---------------------------------------------------------------------------
# Plugin
# ---------------------------------------------------------------------------

__all__ = ["Connection"]


class Connection(_UpstreamConnection):
    transport = "aws_ssm_assume_role"

    _assumed_role_credentials = None

    # ------------------------------------------------------------

    def _get_assume_role_options(self):
        return (
            self.get_option("role_arn"),
            self.get_option("role_session_name") or "ansible-ssm-session",
            int(self.get_option("role_duration_seconds") or 3600),
        )

    # ------------------------------------------------------------

    def _assume_role(self, role_arn, session_name, duration):

        region = self.get_option("region") or None

        display.vvv(
            f"Assumindo role {role_arn}",
            host=self._play_context.remote_addr,
        )

        try:
            # 🔥 CORRETO: usa o mesmo mecanismo do plugin oficial
            sts = self._get_boto_client("sts", region_name=region)

            resp = sts.assume_role(
                RoleArn=role_arn,
                RoleSessionName=session_name,
                DurationSeconds=duration,
            )

        except botocore.exceptions.ClientError as e:
            raise AnsibleError(f"Erro STS: {e}")

        creds = resp["Credentials"]

        display.vvv(
            "AssumeRole OK",
            host=self._play_context.remote_addr,
        )

        return creds

    # ------------------------------------------------------------

    def _inject_assumed_role_session(self, creds):

        region = self.get_option("region") or None

        def patched(service, region_name=None, config=None):

            effective_region = region_name or region

            kwargs = {}
            if effective_region:
                kwargs["region_name"] = effective_region
            if config:
                kwargs["config"] = config

            session = boto3.Session(
                aws_access_key_id=creds["AccessKeyId"],
                aws_secret_access_key=creds["SecretAccessKey"],
                aws_session_token=creds["SessionToken"],
                region_name=effective_region,
            )

            return session.client(service, **kwargs)

        import types
        self._get_boto_client = types.MethodType(
            lambda self_inner, svc, region_name=None, config=None:
            patched(svc, region_name, config),
            self,
        )

        # recria clientes se já existirem
        if hasattr(self, "_client") and self._client:
            self._client = patched("ssm", region)

        if hasattr(self, "_s3_client") and self._s3_client:
            from botocore.config import Config

            self._s3_client = patched(
                "s3",
                region,
                Config(signature_version="s3v4"),
            )

    # ------------------------------------------------------------

    def _connect(self):

        role_arn, session_name, duration = self._get_assume_role_options()

        if role_arn:
            if not self._assumed_role_credentials:
                creds = self._assume_role(role_arn, session_name, duration)
                self._assumed_role_credentials = creds
                self._inject_assumed_role_session(creds)
            else:
                display.vvv(
                    "Reutilizando credenciais STS",
                    host=self._play_context.remote_addr,
                )
        else:
            display.vvvv("Sem assume role")

        return super()._connect()