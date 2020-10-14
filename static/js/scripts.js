function appToggle(bool) {
    console.log("setting toggler");
    let displays = ['none', 'block'];
    let colors = ['darkcyan', 'dodgerblue']
    if (bool) {
        displays = ['block', 'none'];
        colors = ['dodgerblue', 'darkcyan']
    }
    return () => {
        console.log("toggling");
        document.querySelector('#word-search').style.display = displays[0];
        document.querySelector('#date-search').style.display = displays[1];
        document.querySelector('#word-tab').style.backgroundColor = colors[0];
        document.querySelector('#date-tab').style.backgroundColor = colors[1];
    }
}

function dateQuery() {
    let date = document.querySelector('#date').value.split("-");
    try {
        let url = `https://fun-holiday-api.herokuapp.com/api/date?month=${date[1]}&day=${date[2]}`
        console.log(url);
    } catch (error) {
        console.log('bad date');
        return false;
    }
    let url = `https://fun-holiday-api.herokuapp.com/api/date?month=${date[1]}&day=${date[2]}`
    fetch(url)
    .then(response => response.json())
    .then(data => data.holidays)
    .then(holidays => {
        let resultContainer = document.querySelector('#results');
        let resultPlaceholder = document.querySelector('#result-placeholder');
        if (holidays.length > 0) {
            resultPlaceholder.style.display = 'none';
        } else {
            resultPlaceholder.style.display = 'inline';
        }
        // remove all old results except the placeholder
        while (resultContainer.lastChild !== resultPlaceholder) {
            resultContainer.removeChild(resultContainer.lastChild);
        };
        // insert new results
        holidays.forEach(element => {
            let p = document.createElement("p");
            p.innerHTML = `${date[1]}/${date[2]}: ${element}`
            resultContainer.appendChild(p);
        });
        let h = document.createElement("h2");
        let rawDate = document.querySelector('#date').value;
        h.innerHTML = `Share these results <a href="https://fun-holiday-api.herokuapp.com/app?dt=${rawDate}">https://fun-holiday-api.herokuapp.com/app?dt=${rawDate}</a>`;
        resultContainer.appendChild(h);
    });
}

function wordQuery() {
    let word = document.querySelector('#keyword').value;
    let resultContainer = document.querySelector('#results');
    let resultPlaceholder = document.querySelector('#result-placeholder');
    if (word === '') {
        resultPlaceholder.style.display = 'inline';
        while (resultContainer.lastChild !== resultPlaceholder) {
            resultContainer.removeChild(resultContainer.lastChild);
        };
        return false;
    } else {
        resultPlaceholder.style.display = 'none';
    }
    let url = `https://fun-holiday-api.herokuapp.com/api/when?like=${word}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        // remove all old results except the placeholder
        while (resultContainer.lastChild !== resultPlaceholder) {
            resultContainer.removeChild(resultContainer.lastChild);
        };
        if (Object.keys(data).length === 0) {
            let failure = document.createElement("p");
            failure.innerHTML = `No results for "${word}"`;
            resultContainer.appendChild(failure);
        }
        Object.keys(data).forEach(month => {
            Object.keys(data[month]).forEach(day => {
                data[month][day].forEach(holiday => {
                    let p = document.createElement("p");
                    p.innerHTML = `${month}/${day}: ${holiday}`;
                    resultContainer.appendChild(p);
                })
            })
        });
        let h = document.createElement("h2");
        let linkWord = encodeURIComponent(word);
        h.innerHTML = `Share these results <a href="https://fun-holiday-api.herokuapp.com/app?kw=${linkWord}">https://fun-holiday-api.herokuapp.com/app?kw=${linkWord}</a>`;
        resultContainer.appendChild(h);
    });
}