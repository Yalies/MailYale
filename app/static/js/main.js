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
        let otherCheckboxes = Array.from(input.parentElement.parentElement.getElementsByTagName('input'));
        let allCheckbox = otherCheckboxes.shift();
        if (input == allCheckbox) {
            for (let checkbox of otherCheckboxes) {
                checkbox.checked = !checked;
            }
        } else {
            if (checked) {
                allCheckbox.checked = false;
            } else {
                let anyChecked = false;
                for (let checkbox of otherCheckboxes) {
                    anyChecked = anyChecked || checkbox.checked;
                }
                allCheckbox.checked = !anyChecked;
            }
        }
    }
};

let submit = document.getElementById('submit');
    sections = document.getElementsByTagName('section');

submit.onclick = function() {
    let payload = {};
    for (let section of sections) {
        let category = section.id;
        let otherCheckboxes = Array.from(section.getElementsByTagName('input'));
        let allCheckbox = otherCheckboxes.shift();
        if (!allCheckbox.checked) {
            payload[category] = []
            for (let checkbox of otherCheckboxes) {
                if (checkbox.checked) {
                    payload[category].push(checkbox.name);
                }
            }
        }
    }
    console.log(payload);
}
