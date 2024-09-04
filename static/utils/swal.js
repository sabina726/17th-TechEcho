var success = showSuccess
var error = showError
var question = showQuestion

function showSuccess(title, text) {
    Swal.fire({
        title: title,
        text: text,
        icon: "success",
        timer: 3000
    });
}

function showError(title, text) {
    Swal.fire({
        title: title,
        text: text,
        icon: "error",
        timer: 3000
    });
}

function showQuestion(title, text) {
    Swal.fire({
        title: title,
        text: text,
        icon: "question",
        timer: 3000
    });
}