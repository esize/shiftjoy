import { checkboxVisibilityToggle, getElementAfterLoad } from "/static/js/lib.js"

const state_element = await getElementAfterLoad('#id_gender_specific')
state_element.addEventListener('click', () => {console.log("hi")})

checkboxVisibilityToggle('#id_gender_specific', '.field-required_gender', true)