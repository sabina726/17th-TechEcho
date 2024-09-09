import Alpine from "alpinejs"

Alpine.data("notifications", _ => ({
    notificationOpen: false,
    notificationNumber: 0,

    init() {
        this.notificationNumber = parseInt(this.$refs.number_span.innerHTML) || 0;
        this.$el.addEventListener("htmx:wsAfterMessage", _ => {
            this.notificationNumber += 1;
            this.$refs.number_span.innerHTML = this.notificationNumber;
        })
    },

    toggleDropdown() {
        this.notificationOpen = !this.notificationOpen;
    },

    closeDropdown() {
        this.notificationOpen = false;
    },

    clear() {
        console.log('sssssss');
        this.notificationNumber -= 1;
        this.$el.closest("li").remove()
    },

    clearAll() {
        this.notificationNumber = 0;
        this.$refs.number_span.innerHTML = '';
        this.$refs.dropdown.querySelectorAll('li').forEach(notification => {
            notification.remove()
        });
    }
}))
