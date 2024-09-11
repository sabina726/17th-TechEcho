import Alpine from "alpinejs"
import Tagify from "@yaireo/tagify"
import programmingLanguages from "../../constants/choices.js"

Alpine.data("label_input", () => ({
    init() {
        new Tagify(this.$el, {
            whitelist: [
                "python",
                "javascript",
                "java",
                "c++",
                "c#",
                "ruby",
                "php",
                "go",
                "swift",
                "kotlin",
                "rust",
                "typescript",
                "dart",
                "scala",
                "perl",
                "haskell",
                "lua",
                "r",
                "matlab",
                "objective-c",
                "fortran",
                "cobol",
                "elixir",
                "clojure",
                "f#",
                "visual basic",
                "shell",
                "assembly",
                "erlang",
                "groovy",
                "vhdl",
                "ada",
                "tcl",
                "zig",
                "julia",
                "crystal",
                "ocaml",
                "nim",
                "scheme",
                "prolog",
                "smalltalk",
                "vala"
            ],
            enforceWhitelist: true,
        })
    },
}))
