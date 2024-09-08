import Alpine from "alpinejs"

Alpine.data("notifications", _ => ({
    notificationOpen: false,
    notifications_number:0,

    init() {
        this.notifications_number = this.$refs.number_span.innerHTML ? parseInt(this.$refs.number_span.innerHTML) : 0

        this.$el.addEventListener("htmx:wsAfterMessage", _ => {
            this.notifications_number += 1
            this.$refs.number_span.innerHTML = this.notifications_number
        })
    },

    toggleDropdown() {
        this.notificationOpen = !this.notificationOpen
    },

    closeDropdown() {
        this.notificationOpen = false
    },

    clearAll() {
        this.$refs.number_span.innerHTML = ''
        this.$refs.dropdown.querySelectorAll('li').forEach(notification => {
            notification.remove()
        })
    }
}))
