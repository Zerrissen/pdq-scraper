const textarea = document.getElementById("results-area");
const eventSource = new EventSource("/stream");

eventSource.onmessage = function (event) {
    const textarea = document.getElementById("results-area");
    textarea.value += event.data + "\n";
};
