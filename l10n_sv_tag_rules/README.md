# l10n_sv_tag_rules
Módulo MVP para reglas dinámicas de tax tags sobre account.move.line.

## Instalación
1. Copiar la carpeta `l10n_sv_tag_rules` a addons path.
2. Actualizar apps list e instalar el módulo.

## Uso
1. Ir a Configuración → Reglas etiquetas l10n_sv.
2. Crear regla: poner `filter_domain` usando el widget `domain` (modelo `account.move.line`).
   - Ejemplo: "[(\'move_id.move_type\',\'=\',\'out_invoice\'), (\'move_id.partner_id.country_id.code\',\'=\',\'SV\') ]"
3. Seleccionar `tag_ids` que se aplicarán.
4. Si se desea retroactividad: abrir la regla y usar "Aplicar a movimientos existentes...".

## Tests
Ejecutar tests de Odoo con `-i l10n_sv_tag_rules --test-enable` o usar la suite de tests del proyecto.
