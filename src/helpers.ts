
export function changeThemeMode() {
   let current_mode = document.getElementById("footer-content");
   let github = document.getElementById("github-link");
   let about = document.getElementById("about-link");
   if (current_mode?.innerHTML == "Dark Mode") {
        document.body.style.backgroundColor = "#ffffff";
        current_mode.innerHTML = "Light Mode";
        if (github && about) {
            github.style.color = 'black';
            about.style.color = 'black';
        }
        return;
   }
   if (current_mode?.innerHTML == 'Light Mode') {
        document.body.style.backgroundColor =  "#3f3f3f";
        current_mode.innerHTML = "Dark Mode";
        if (github && about) {
            github.style.color = 'white';
            about.style.color = 'white'
        }
        return;
   }
}

