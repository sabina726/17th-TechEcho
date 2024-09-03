var success = showSuccess;
var error = showError

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