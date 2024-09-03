var success = showSuccess
var error = showError
var question = showQuestion

function showSuccess(title, text) {
    Swal.fire({
        title: title,
        text: text,
        icon: "success"
    });
}

function showError(title, text) {
    Swal.fire({
        title: title,
        text: text,
        icon: "error"
    });
}

function showQuestion(title, text) {
    Swal.fire({
        title: title,
        text: text,
        icon: "question"
    });
}