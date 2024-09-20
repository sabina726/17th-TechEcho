const default_message = "'Hello World'"
const default_snippets = {
    javascript: `console.log(${default_message})`,
    python: `print(${default_message})`,
    cpp: `#include <iostream>
    using namespace std;

    int main() {
        cout << ${default_message} << endl;
        return 0;
    }`,
}

const getDefaultSnippets = (language) => {
    if (language in default_snippets) {
        return default_snippets[language]
    }
    return ""
}


export default getDefaultSnippets
