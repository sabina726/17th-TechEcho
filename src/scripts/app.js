import "./fontawesome";
import Alpine from 'alpinejs';
import Tagify from '@yaireo/tagify';
import Swal from "sweetalert2";

var input = document.querySelector('input[name=tags-outside]')

var tagify = new Tagify(input, {
    whitelist: ['Python', 'JavaScript', 'Ruby'],
    dropdown: {
        position: 'input',
        enabled: 0
    }
})

window.Swal = Swal;
Alpine.start();