let body = document.body,
    checkboxes = document.querySelectorAll('input[type="checkbox"]'),
    allCheckboxes = document.querySelectorAll('input[type="checkbox"][name$="-all"]'),
    output = document.getElementById('output');

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
    let filters = {};
    for (let section of sections) {
        let category = section.id;
        let otherCheckboxes = Array.from(section.getElementsByTagName('input'));
        let allCheckbox = otherCheckboxes.shift();
        if (!allCheckbox.checked) {
            filters[category] = []
            for (let checkbox of otherCheckboxes) {
                if (checkbox.checked) {
                    filters[category].push(checkbox.name);
                }
            }
        }
    }
    console.log(filters);
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters),
    })
        .then(response => response.json())
        .then(emails => {
            console.log(emails);
            output.value = emails.join(', ');
            output.style.display = 'block';
        });
}
