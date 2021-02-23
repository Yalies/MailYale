const MAX_EMAILS_PER_DAY = 2000;

let p = {
    body: document.body,
    checkboxes: document.querySelectorAll('input[type="checkbox"]'),
    allCheckboxes: document.querySelectorAll('input[type="checkbox"][name$="-all"]'),
    output: document.getElementById('output'),
    query: document.getElementById('query'),
    submit: document.getElementById('submit'),
    filters: document.getElementsByClassName('filter'),
    clearFilters: document.getElementById('clear_filters'),
    list: document.getElementById('list'),
    loading: document.getElementById('loading'),
    empty: document.getElementById('empty'),
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

let submit = document.getElementById('submit'),
    sections = document.getElementsByTagName('section'),
    warning = document.getElementById('warning');

submit.onclick = function() {
    let filters = {};
    for (let filter of p.filters) {
        let category = filter.id;
        let otherCheckboxes = Array.from(filter.getElementsByTagName('input'));
        let allCheckbox = otherCheckboxes.shift();
        if (!allCheckbox.checked) {
            filters[category] = []
            for (let checkbox of otherCheckboxes) {
                if (checkbox.checked) {
                    if (category === 'leave') {
                        filters[category].push(checkbox.name === 'Yes');
                    } else {
                        filters[category].push(checkbox.name);
                    }
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
                warning.textContent = 'Warning: Gmail will only allow sending emails to a maximum of ' + MAX_EMAILS_PER_DAY + ' recipients per day. Consider sending your email in batches to smaller groups.';
            }
            setTimeout(function() {
                submit.textContent = 'Generate email list';
            }, 1500);
        });
}
