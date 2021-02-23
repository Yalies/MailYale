const MAX_EMAILS_PER_DAY = 2000;

let p = {
    body: document.body,

    submit: document.getElementById('submit'),
    output: document.getElementById('output'),
    warning: document.getElementById('warning'),

    filters: document.getElementsByClassName('filter'),
    clearFilters: document.getElementById('clear_filters'),
    allCheckboxes: document.querySelectorAll('input[type="checkbox"][name$="-all"]'),
    checkboxes: document.querySelectorAll('input[type="checkbox"]'),
};

function collapseAllFilters() {
    for (let filter of p.filters) {
        filter.classList.add('collapsed');
    }
}

function resetFilters() {
    for (let filter of p.filters) {
        filter.classList.add('collapsed');
        filter.classList.remove('active');
    }
    for (let checkbox of p.checkboxes) {
        checkbox.checked = false;
    }
    for (let checkbox of p.allCheckboxes) {
        checkbox.checked = true;
    }
}
resetFilters();

p.clearFilters.onclick = function() {
    resetFilters();
}

function isFilter(element) {
    return element.tagName === 'DIV' && element.classList.contains('filter');
}

onclick = function(e) {
    let filter = null;
    if (isFilter(e.target)) {
        filter = e.target;
    } else if (e.target.tagName === 'H4' && isFilter(e.target.parentElement)) {
        filter = e.target.parentElement;
    } else if (e.target.tagName === 'I' && isFilter(e.target.parentElement.parentElement)) {
        filter = e.target.parentElement.parentElement;
    }

    if (filter) {
        filter.classList.toggle('collapsed');
    }
};

onchange = function(e) {
    let input = e.target;
    if (input.type === 'checkbox') {
        let checked = input.checked;
        let otherCheckboxes = Array.from(input.parentElement.parentElement.getElementsByTagName('input'));
        let allCheckbox = otherCheckboxes.shift();
        let filter = input.parentElement.parentElement;
        if (input == allCheckbox) {
            filter.classList.toggle('active', !checked);
            for (let checkbox of otherCheckboxes) {
                checkbox.checked = !checked;
            }
        } else {
            if (checked) {
                filter.classList.add('active');
                allCheckbox.checked = false;
            } else {
                let anyChecked = false;
                for (let checkbox of otherCheckboxes) {
                    if (checkbox.checked) {
                        anyChecked = true;
                        break;
                    }
                }
                filter.classList.toggle('active', anyChecked);
                allCheckbox.checked = !anyChecked;
            }
        }
    }
};

p.submit.onclick = function() {
    let filters = {};
    for (let filter of p.filters) {
        let category = filter.id;
        let otherCheckboxes = Array.from(filter.getElementsByTagName('input'));
        let allCheckbox = otherCheckboxes.shift();
        if (!allCheckbox.checked) {
            filters[category] = []
            for (let checkbox of otherCheckboxes) {
                if (checkbox.checked) {
                    let option = checkbox.name;
                    if (option === 'True') option = true;
                    else if (option === 'False') option = false;

                    filters[category].push(option);
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
            output.select();
            document.execCommand('copy');
            submit.textContent = 'Copied ' + emails.length + ' emails to clipboard!';
            if (emails.length > MAX_EMAILS_PER_DAY) {
                p.warning.textContent = 'Warning: Gmail will only allow sending emails to a maximum of ' + MAX_EMAILS_PER_DAY + ' recipients per day. Consider sending your email in batches to smaller groups.';
            }
            setTimeout(function() {
                p.submit.textContent = 'Generate email list';
            }, 1500);
        });
}
