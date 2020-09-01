let body = document.body,
    checkboxes = document.querySelectorAll('input[type="checkbox"]'),
    allCheckboxes = document.querySelectorAll('input[type="checkbox"][name$="-all"]');

for (let checkbox of checkboxes) {
    checkbox.checked = false;
}
for (let checkbox of allCheckboxes) {
    checkbox.checked = true;
}

onchange = function(e) {
    let input = e.target;
    if (input.type === 'checkbox') {
        let checked = input.checked;
        if (input.name.endsWith('-all')) {
            if (!checked) {

            } else {

            }
        } else {
            if (checked) {
                input.parentElement.parentElement.querySelector('input[type="checkbox"][name$="-all"]').checked = false;
            } else {
                let sectionCheckboxes = input.parentElement.parentElement.querySelectorAll('input[type="checkbox"]').slice(1);
                let anyChecked = false;
                for (let checkbox of sectionCheckboxes) {

                }
            }
        }
    }
};
