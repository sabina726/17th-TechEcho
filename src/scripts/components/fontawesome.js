import { library, dom } from "@fortawesome/fontawesome-svg-core"
import Alpine from 'alpinejs';

import {
    faMagnifyingGlass,
    faArrowUp,
    faArrowDown,
    faBell,
    faGlasses
} from "@fortawesome/free-solid-svg-icons"

library.add(
    faMagnifyingGlass,
    faArrowUp,
    faArrowDown,
    faBell,
    faGlasses
)

dom.i2svg()

Alpine.data("convert_to_svg", () => ({
    init() {
        dom.i2svg();
    },
}))

