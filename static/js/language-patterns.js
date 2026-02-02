// Language detection patterns
const languagePatterns = {
    python: {
        score: 0,
        patterns: [
            { regex: /\b(def|class|import|from|if|elif|else|try|except|finally)\b/g, weight: 2 },
            { regex: /\b(print|return|yield|with|as|in|is|not|and|or)\b/g, weight: 1.5 },
            { regex: /#.*$/gm, weight: 1.5 },
            { regex: /"""|'''/g, weight: 1 },
            { regex: /\bindent\b/g, weight: 1 },
            { regex: /\bself\b/g, weight: 1.5 },
            { regex: /\bTrue\b|\bFalse\b|\bNone\b/g, weight: 1 }
        ]
    },
    javascript: {
        score: 0,
        patterns: [
            { regex: /\b(function|const|let|var|if|else|try|catch|class|return|async|await)\b/g, weight: 2 },
            { regex: /\b(undefined|null|typeof|instanceof)\b/g, weight: 1.5 },
            { regex: /\/\/.*$/gm, weight: 1.5 },
            { regex: /\/\*[\s\S]*?\*\//g, weight: 1.5 },
            { regex: /console\.(log|error|warn|info)/g, weight: 2 },
            { regex: /=>/g, weight: 1.5 },
            { regex: /\${.*?}/g, weight: 1.5 },
            { regex: /\b(true|false)\b/g, weight: 1 },
            { regex: /\.(map|filter|reduce|forEach)\(/g, weight: 1.5 }
        ]
    },
    java: {
        score: 0,
        patterns: [
            { regex: /\b(public|private|protected|class|interface|extends|implements)\b/g, weight: 2 },
            { regex: /\b(String|Integer|Boolean|void|static|final)\b/g, weight: 1.5 },
            { regex: /System\.out\.println/g, weight: 2 },
            { regex: /public\s+static\s+void\s+main/g, weight: 3 },
            { regex: /@Override/g, weight: 2 },
            { regex: /import\s+java\./g, weight: 2 },
            { regex: /new\s+\w+\(/g, weight: 1.5 }
        ]
    },
    c: {
        score: 0,
        patterns: [
            { regex: /#include\s*<.*\.h>/g, weight: 3 },
            { regex: /\b(printf|scanf|malloc|free|sizeof)\b/g, weight: 2.5 },
            { regex: /\b(int|float|double|char|void|struct|typedef)\b/g, weight: 1.5 },
            { regex: /\bmain\s*\(\s*(void|int\s+argc)/g, weight: 3 },
            { regex: /\*\w+\s*=/g, weight: 1.5 },
            { regex: /\b(FILE|NULL)\b/g, weight: 2 }
        ]
    },
    cpp: {
        score: 0,
        patterns: [
            { regex: /#include\s*<.*>/g, weight: 3 },
            { regex: /\b(cout|cin|endl|printf|scanf)\b/g, weight: 2 },
            { regex: /\b(int|float|double|char|bool|void|unsigned|struct|template)\b/g, weight: 1.5 },
            { regex: /std::/g, weight: 2 },
            { regex: /\b(public|private|protected):/g, weight: 1.5 },
            { regex: /->|::/g, weight: 1.5 }
        ]
    },
    html: {
        score: 0,
        patterns: [
            { regex: /<!DOCTYPE\s+html>/i, weight: 3 },
            { regex: /<[^>]+>/g, weight: 2 },
            { regex: /<(html|head|body|script|link|meta|div|span|p|a|img|ul|li)/g, weight: 2 },
            { regex: /class=["'][^"']*["']/g, weight: 1.5 },
            { regex: /id=["'][^"']*["']/g, weight: 1.5 },
            { regex: /<!--[\s\S]*?-->/g, weight: 1.5 },
            { regex: /href=["'][^"']*["']/g, weight: 1.5 }
        ]
    },
    css: {
        score: 0,
        patterns: [
            { regex: /{[^}]*}/g, weight: 1.5 },
            { regex: /\b(margin|padding|border|color|background|font|width|height|display|position)\b/g, weight: 2 },
            { regex: /@media\b|@keyframes\b|@import\b/g, weight: 2 },
            { regex: /[.#][a-zA-Z-_]+\s*{/g, weight: 1.5 },
            { regex: /:\s*(hover|active|focus|before|after)\b/g, weight: 1.5 },
            { regex: /\d+\s*(px|em|rem|%|vh|vw)/g, weight: 1.5 },
            { regex: /!important/g, weight: 1 }
        ]
    }
};

// Make the patterns available globally
window.languagePatterns = languagePatterns; 