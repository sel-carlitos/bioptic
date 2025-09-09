# -*- coding: utf-8 -*-
{
    "name": "Facturas de proveedor - El Salvador",
    'countries': ['sv'],
    "version": "18.0.1.0.0",
    "author": "SEGU",
    "license": "LGPL-3",
    "category": "Localization",
    "summary": "Importa y Aceptar Facturas de Proveedor",
    "description": """Importa y Aceptar Facturas de Proveedor:
    Al importar un documento tome en consideración las siguientes pautas: \n
    • Solo los documentos XML (.xml) serán analizados, el resto se cargara sin análisis.
    • La moneda de la factura a cargar, debe estar activa, de lo contrario el sistema le indicara un error.
    • El tipo de documento XML admitido es de tipo FacturaElectronica (Codigo: 01), Nota de débito electrónica (02), NotaCreditoElectronica (03) . Si el documento no cumple esta condición sera cargado sin análisis.
    • Los tipos de impuestos deben estar configurados correctamente en el sistema.
    """,
    "depends": [
        "l10n_sv_dte",
        "product",
    ],
    "data": [
        # "views/account_move_views.xml",
        "views/res_config_settings_view.xml",
    ],
}
