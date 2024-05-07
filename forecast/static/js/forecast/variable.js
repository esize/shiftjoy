import { selectVisibilityToggle } from "/static/js/lib.js"
const hide_when_selected_mapping = {
    'VALUE': ['.field-calculated_default_value', '.field-offset_linked_variable', '.field-offset_days', '.field-offset_hours', '.field-behaviors'],
    'CALCULATED': ['.field-default_value', '.field-offset_linked_variable', '.field-offset_days', '.field-offset_hours'],
    'OFFSET': ['.field-calculated_default_value', '.field-default_value', '.field-behaviors']
}

selectVisibilityToggle(hide_when_selected_mapping, '#id_type')