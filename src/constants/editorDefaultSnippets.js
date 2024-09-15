const default_message = "'Hello World'"
const default_javascript = `console.log(${default_message})`
const default_python = `print(${default_message})`
const default_cpp = `#include <iostream>
using namespace std;

int main() {
    cout << ${default_message} << endl;
    return 0;
}
`

const getDefaultSnippets = (language) => {
    if (language == "javascript") {
        return default_javascript;
    } else if (language == "python") {
        return default_python;
    } else if (language == "cpp") {
        return default_cpp
    }
    return ""
    // why can't this work ?? globalThis[`default_${language}`]
}


export default getDefaultSnippets
