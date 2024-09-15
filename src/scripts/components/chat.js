import Alpine from "alpinejs"

Alpine.data("scroll", _ => ({

    init() {
        list = this.$el.closest('ul')
        list.scrollTop = list.scrollHeight;
    },
}))