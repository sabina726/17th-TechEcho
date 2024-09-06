import Alpine from "alpinejs"
import Tagify from "@yaireo/tagify"

Alpine.data("label_input", () => ({
    init() {
        new Tagify(this.$el, {
<<<<<<< HEAD
            whitelist: ['javascript','python','ruby']
=======
            whitelist: ['javascript','python', 'ruby']
>>>>>>> will
        })
    },
}))
