function toggleVisibility() {
    let input = document.getElementById("shodan-api-key-input");
    let button = document.getElementById("show-hide-button");
    if (input.type === "password") {
        input.type = "text";
        button.innerText = "Hide Key";
        input.placeholder = "1234567890";
    } else {
        input.type = "password";
        button.innerText = "Show Key";
        input.placeholder = "**********";
    }
}

function clearKey() {
    let input = document.getElementById("shodan-api-key-input");
    input.value = "";
}
