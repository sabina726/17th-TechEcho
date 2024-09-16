import Alpine from "alpinejs"

Alpine.data("scroll", _ => ({
    prevScrollHeight: 0,
    messageSender: false,

    init() {
        this.scrollBottom();
        this.prevScrollHeight = this.$refs.list.scrollHeight;

        this.$el.addEventListener("htmx:afterOnLoad", () => {
            this.$refs.list.scrollTop = this.prevScrollHeight;
            this.prevScrollHeight = this.$refs.list.scrollHeight
        });

        this.$el.addEventListener("htmx:wsAfterSend", () => {
            this.messageSender = true;
        });

        this.$el.addEventListener("htmx:wsAfterMessage", () => {
            if (this.messageSender) {
                this.scrollBottom()
                this.messageSender = false;
            }
        });
    },

    scrollBottom() {
        this.$refs.list.scrollTop = this.$refs.list.scrollHeight;
    },
}))
