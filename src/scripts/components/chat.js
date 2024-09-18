import Alpine from "alpinejs"

Alpine.data("scroll", _ => ({
    prevScrollHeight: 0,

    init() {
        this.scrollBottom();
        this.prevScrollHeight = this.$refs.list.scrollHeight;

        this.$el.addEventListener("htmx:afterOnLoad", () => {
            this.$refs.list.scrollTop = this.prevScrollHeight;
            this.prevScrollHeight = this.$refs.list.scrollHeight
        });

        this.$el.addEventListener("htmx:wsAfterMessage", () => {
            this.scrollBottom()
        });
    },

    scrollBottom() {
        this.$refs.list.scrollTop = this.$refs.list.scrollHeight;
    },
}))
