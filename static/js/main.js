const body = document.querySelector("body"),
        sidebar = body.querySelector(".sidebar"),
        toggle = body.querySelector(".toggle"),
        modeSwitch = body.querySelector(".toggle-switch"),
        modeText = body.querySelector(".mode-text");

modeSwitch.addEventListener("click", () => {
    body.classList.toggle("light");

    if (body.classList.contains("light")) {
        modeText.innerText = "Dark Mode";
    }else{
        modeText.innerText = "Light Mode";
    }
});

// toggle.addEventListener("click", () => {
//     sidebar.classList.toggle("close");
// });

