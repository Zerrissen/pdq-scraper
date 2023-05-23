function update() {
    let doc = document.getElementById("time");

    fetch("/scrape")
        .then((response) => response.json())
        .then(function (data) {
            console.log(data["now"]);
            doc.innerText = data["now"];
        });
}

// update all 10000 ms
(function () {
    update();
    setInterval(function () {
        update();
    }, 1000);
})();
