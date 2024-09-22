import { library, dom } from "@fortawesome/fontawesome-svg-core"
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
    faTimes
} from "@fortawesome/free-solid-svg-icons"

import {
    faCalendar
} from "@fortawesome/free-regular-svg-icons"

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
    faTimes
)

dom.i2svg()

Alpine.data("convert_to_svg", () => ({
    init() {
        dom.i2svg();
    },
}))

