
export function changeThemeMode() {
    let current_mode = document.getElementById("footer-content");
    let github = document.getElementById("github-link");
    let about = document.getElementById("about-link");

    if (current_mode?.innerHTML === "Dark Mode") {
        const lightColor = localStorage.getItem('lightColor');
        if (lightColor) {
            document.body.style.backgroundColor = lightColor;
        }
        current_mode.innerHTML = "Light Mode";
        localStorage.setItem('currentTheme', 'lightMode'); // Persist the current mode
        if (github && about) {
            github.style.color = 'black';
            about.style.color = 'black';
        }
        return;
    }

    if (current_mode?.innerHTML === "Light Mode") {
        document.body.style.backgroundColor = "#3f3f3f";
        current_mode.innerHTML = "Dark Mode";
        localStorage.setItem('currentTheme', 'darkMode'); // Persist the current mode
        if (github && about) {
            github.style.color = 'white';
            about.style.color = 'white';
        }
        return;
    }
}

export async function fetch_query_results() {
    let search_input = document.getElementById("search-bar") as HTMLInputElement;
    const response = await fetch("http://localhost:1410/process-query", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(search_input.value)
    });
    if (response.ok) {
        let results = []
        let responseResult = await response.json()
        results.push(responseResult, search_input.value)
        return results
    }
}

export async function handleLuckyButton() {
    const response = await fetch("http://localhost:1410/random-query", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }) 
    if (response.ok) {
        return await response.json()
    }          
}

export function applyHomePageTheme() {
    const currentTheme = localStorage.getItem('currentTheme');
    const current_mode = document.getElementById("footer-content");
    const github = document.getElementById("github-link");
    const about = document.getElementById("about-link");
    if (currentTheme === 'darkMode') {
        if (github && about) {
            github.style.color = 'white';
            about.style.color = 'white';
          }
        if (current_mode) {
            current_mode.innerHTML = "Dark Mode";
        }
    } 
    else {
        if (github && about) {
            github.style.color = 'black';
            about.style.color = 'black';
          }
        if (current_mode) {
            current_mode.innerHTML = "Light Mode";
        }
    }
}

export function changeSearchPageTheme() {
    const footerTheme = document.getElementById("footer-content-searchpage");
    if (footerTheme?.innerHTML == "Dark Mode") {
        const lightColor = localStorage.getItem('lightColor');
        footerTheme.innerHTML = "Light Mode";
        if (lightColor) {
        document.body.style.backgroundColor = lightColor }
        localStorage.setItem('currentTheme', 'lightMode');
    }
    else if (footerTheme?.innerHTML == "Light Mode") {
        const darkColor = localStorage.getItem('darkColor');
        footerTheme.innerHTML = "Light Mode";
        if (darkColor) {
        document.body.style.backgroundColor = darkColor }
        localStorage.setItem('currentTheme', 'darkMode');
    }   
    return applyTfidfColor()
}
    

export function applyTfidfColor() {
    const tfidfScore = document.getElementsByClassName("tf-idf-score");
    const currentTheme = localStorage.getItem('currentTheme');
    const theme = document.getElementById("footer-content-searchpage")
    if (currentTheme == 'lightMode') {
        if (theme) {
            theme.innerHTML = 'Light Mode'
        }
        Array.from(tfidfScore).forEach((score) => {
            (score as HTMLElement).style.color = "black"; // Cast Element to HTMLElement
        });
        return;
    }
    else {
        if (theme) {
            theme.innerHTML = 'Dark Mode'
        }
        Array.from(tfidfScore).forEach((score) => {
            (score as HTMLElement).style.color = "white"; // Cast Element to HTMLElement
        });
        return;
    }
}