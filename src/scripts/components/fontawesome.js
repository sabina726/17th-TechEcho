import { library, dom } from "@fortawesome/fontawesome-svg-core"

import {
    faMagnifyingGlass,
    faArrowUp,
    faArrowDown,
    faBell,
    faGlasses,
    faUser
} from "@fortawesome/free-solid-svg-icons"
import Alpine from 'alpinejs';

library.add(
    faBell,
    faMagnifyingGlass,
    faArrowUp,
    faArrowDown,
    faGlasses,
    faUser,
)

dom.i2svg()

Alpine.data("convert_to_svg", () => ({
    init() {
        dom.i2svg();
    },
}))

