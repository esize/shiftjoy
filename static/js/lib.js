export function getElementAfterLoad(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                observer.disconnect();
                resolve(document.querySelector(selector));
            }
        });
        
        // If you get "parameter 1 is not of type 'Node'" error, see https://stackoverflow.com/a/77855838/492336
        observer.observe(document.documentElement, {
            childList: true,
            subtree: true
        });
    });
}

export function removeItemOnce(arr, value) {
    var index = arr.indexOf(value);
    if (index > -1) {
        arr.splice(index, 1);
    }
    return arr;
}

export function removeItemAll(arr, value) {
    var i = 0;
    while (i < arr.length) {
        if (arr[i] === value) {
            arr.splice(i, 1);
        } else {
            ++i;
        }
    }
    return arr;
}

export function hiddenHelper(newHidden) {
    let difference = hidden.filter(x => !newHidden.includes(x));
    let toHide = [...newHidden.filter(x => !hidden.includes(x))];
    difference.forEach((e) => {showElement(e)})
    toHide.forEach((e) => {hideElement(e)})
}

export async function hideElement(selector) {
    const element = await getElementAfterLoad(selector)
    element.parentNode.style.display = 'none'
    hidden.push(selector)
}

export async function showElement(selector) {
    const element = await getElementAfterLoad(selector)
    element.parentNode.style.display = 'block'
    removeItemAll(hidden, selector)
}

export async function toggleElement(selector) {
    const element = await getElementAfterLoad(selector)

    if (element.parentNode.style.display == 'none') {
        element.parentNode.style.display = 'block'
    } else {
        element.parentNode.style.display = 'none'
    }
}

export async function setElementVisability(selector, state){
    const element = await getElementAfterLoad(selector)
    if (!state) {
        element.parentNode.style.display = 'none'
    } else {
        element.parentNode.style.display = 'block'
    }
}

export async function setVisibilityToCheckbox(stateSelector, hiddenSelector, inverse=False){
    const state_element = await getElementAfterLoad(stateSelector)
    const visible = inverse ? state_element.checked : !state_element.checked
    setElementVisability(hiddenSelector, visible)
}

export async function checkboxVisibilityToggle(stateSelector, hiddenSelector, inverse=False){
    const state_element = await getElementAfterLoad(stateSelector)
    setVisibilityToCheckbox(stateSelector, hiddenSelector, inverse)
    state_element.addEventListener('change', (e) => { 
        e.preventDefault();
        setVisibilityToCheckbox(stateSelector, hiddenSelector, inverse)})
}

export async function selectVisibilityToggle(mapping, stateSelector) {
    const state_element = await getElementAfterLoad(stateSelector)
    hiddenHelper(mapping[state_element.value])
    // state_element.onchange = hiddenHelper(mapping[state_element.value])
    state_element.addEventListener("change", (e) => {
        e.preventDefault();
        hiddenHelper(mapping[e.target.value])
    })
}

export let hidden = []