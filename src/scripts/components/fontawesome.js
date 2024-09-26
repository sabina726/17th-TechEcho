
import { library, dom } from "@fortawesome/fontawesome-svg-core";
import Alpine from 'alpinejs';

import {
    faMagnifyingGlass,
    faGraduationCap,
    faArrowUp,
    faArrowDown,
    faBell,
    faGlasses,
    faUser,
    faCalendarCheck,
    faClockRotateLeft,
    faPen,
    faCamera,
    faBars,
    faTimes,
    faThumbsUp,
} from "@fortawesome/free-solid-svg-icons";

import {
    faCalendar,
} from "@fortawesome/free-regular-svg-icons";

// Add icons to the library
library.add(
    faMagnifyingGlass,
    faGraduationCap,
    faArrowUp,
    faArrowDown,
    faBell,
    faGlasses,
    faUser,
    faCalendarCheck,
    faCalendar,
    faClockRotateLeft,
    faPen,
    faCamera,
    faBars,
    faTimes,
    faThumbsUp,
);


dom.watch();


window.Alpine = Alpine;
Alpine.start();
