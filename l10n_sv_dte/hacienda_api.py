# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

DTE_VOUCHER_TYE_MAP = {
    "01": 1,
    "03": 3,
    "04": 3,
    "05": 3,
    "06": 3,
    "11": 1,
    "14": 1,
    "15": 1,
}
HACIENDA_ENV_MAP = {
    "00": "apitest",
    "01": "api",
}


class HaciendaApi:

    def __init__(self, company_id=None):
        self.company_id = company_id
        self.env = '00' if self.company_id.l10n_sv_dte_mh_test_env else '01'

    def generate_signature(self, dte_json):
        # endpoint = "https://firmadorprod.gruposolutecno.com/firmardocumento/"
        endpoint = self.company_id.l10n_sv_signer_route
        partner_id = self.company_id.partner_id
        headers = {
            'Content-type': 'application/json',
        }
        data = {
            "nit": partner_id.nit,
            "activo": True,
            "passwordPri": self.company_id.l10n_sv_mh_private_pass,
            "dteJson": dte_json,
        }
        try:
            response = requests.post(endpoint, headers=headers, json=data)
            response_json = response.json()
            if response.status_code == 200:
                status = response_json.get('status')
                _logger.info(status)
                # return response_json.get('body')
                return response_json
            else:
                error_message = 'token_hacienda failed.  Error: ' + str(response.content)
                _logger.error('token_hacienda failed.  Error: %s', response.content)
                _logger.error('Code: %s', response.status_code)
                raise UserError(str(error_message))

        except requests.exceptions.HTTPError as err:
            _logger.error(err.response.text)
            raise UserError('Error al firmar %s' % err)
            # return False
        except requests.exceptions.RequestException as e:
            _logger.error('Error Obteniendo el Token desde MH. Excepcion %s' % e)
            raise UserError('Error al firmar %s' % e)
            # return False

    def _get_auth1(self):
        """ Retorna un token de seguridad
            """

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
        }
        data = {
            'user': self.company_id.l10n_sv_mh_auth_user,
            'pwd': self.company_id.l10n_sv_mh_auth_pass,
        }
        env = self.env
        # env = '00' if self.company_id.l10n_sv_dte_mh_test_env else '01'
        environment = HACIENDA_ENV_MAP[env]
        endpoint = "https://{}.dtes.mh.gob.sv/seguridad/auth".format(environment)
        try:
            response = requests.post(endpoint, headers=headers, data=data)
            response_json = response.json()
            if response.status_code == 200:
                status = response_json.get('status')
                _logger.info(status)
                return response_json.get('body')
            else:
                error_message = 'token_hacienda failed.  Error: ' + str(response.content)
                _logger.error('token_hacienda failed.  Error: %s', response.content)
                _logger.error('Code: %s', response.status_code)
                raise UserError(str(error_message))

        except requests.exceptions.HTTPError as err:
            _logger.error(err.response.text)
            raise UserError('Error HTTP.')
            # return False
        except requests.exceptions.RequestException as e:
            _logger.error('Error Obteniendo el Token desde MH. Excepcion %s' % e)
            raise UserError('Error Obteniendo el Token desde MH.')
            # return False
        except Exception as e:
            return e

    def recepcion_dte(self, doc):
        kernel = self._get_auth1()
        if not isinstance(kernel, dict):
            return False

        env = self.env
        # env = '00' if self.company_id.l10n_sv_dte_mh_test_env else '01'
        headers = {'Authorization': kernel.get('token', ''), 'Content-type': 'application/json'}
        data = {'ambiente': env,
                'idEnvio': 1,
                'version': DTE_VOUCHER_TYE_MAP[doc.l10n_sv_voucher_type_id.code],
                'tipoDte': doc.l10n_sv_voucher_type_id.code,
                'documento': doc.json_signed,
                }

        environment = HACIENDA_ENV_MAP[env]
        endpoint = "https://{}.dtes.mh.gob.sv/fesv/recepciondte".format(environment)
        response = requests.post(endpoint, headers=headers, json=data)
        _logger.info(response.status_code)
        _logger.info(response)
        return response

    def consulta_dte(self, doc):
        kernel = self._get_auth1()
        if not isinstance(kernel, dict):
            return False

        env = self.env
        headers = {'Authorization': kernel.get('token', ''), 'Content-type': 'application/json'}
        data = {'nitEmisor': self.company_id.l10n_sv_mh_auth_user,
                'tdte': doc.l10n_sv_voucher_type_id.code,
                'codigoGeneracion': doc.l10n_sv_generation_code,
                }

        environment = HACIENDA_ENV_MAP[env]
        endpoint = "https://{}.dtes.mh.gob.sv/fesv/recepcion/consultadte/".format(environment)
        response = requests.post(endpoint, json=data, headers=headers)
        _logger.info(response.status_code)
        _logger.info(response.text)
        return response

    def anular_dte(self, doc):
        kernel = self._get_auth1()
        if not isinstance(kernel, dict):
            return False

        env = self.env
        headers = {'Authorization': kernel.get('token', ''), 'Content-type': 'application/json'}
        data = {'ambiente': env,
                'idEnvio': 1,
                'version': 2,
                'documento': doc.json_andte_signed,
                }
        _logger.info(data)
        environment = HACIENDA_ENV_MAP[env]
        endpoint = "https://{}.dtes.mh.gob.sv/fesv/anulardte".format(environment)
        response = requests.post(endpoint, json=data, headers=headers)
        _logger.info(response.status_code)
        _logger.info(response.text)
        return response
