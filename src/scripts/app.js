import "./fontawesome";
import Alpine from 'alpinejs';
import Tagify from '@yaireo/tagify';
import Swal from "sweetalert2";
import '@yaireo/tagify/dist/tagify.css';

// 暫時拔掉tagify

window.Swal = Swal;
Alpine.start();