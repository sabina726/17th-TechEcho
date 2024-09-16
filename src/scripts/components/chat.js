import Alpine from "alpinejs"

Alpine.data("scroll", _ => ({
    init() {
        this.scrollBottom();
        document.body.addEventListener("htmx:afterOnLoad", (event) => {
            console.log("hi")
            console.log(event)
            // if (event.detail.target.id === 'load-older-messages') {
            //     document.getElementById('chat-container').scrollTop = 1;
            // }
        });
    },

    scrollBottom() {
        this.$el.scrollTop = this.$el.scrollHeight;
    }
}))

Alpine.data("wsScroll", _ => ({
    init() {
        list = this.$el.closest('ul')
        list.scrollTop = list.scrollHeight
    },
}))