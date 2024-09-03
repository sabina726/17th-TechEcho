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

window.show = showSuccess; 
