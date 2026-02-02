class ComplexityAnalyzer {
    constructor() {
        this.timeComplexityPatterns = [
            // Exponential patterns
            { pattern: /fibonacci|fib.*\(.*n.*-.*1.*\).*\+.*fib.*\(.*n.*-.*2.*\)/gi, complexity: 'O(2^n)', weight: 10 },
            { pattern: /(\w+)\s*\([^)]*\)\s*{[^}]*\1\s*\([^)]*n\s*-\s*1[^)]*\)[^}]*\1\s*\([^)]*n\s*-\s*2[^)]*\)/g, complexity: 'O(2^n)', weight: 9 },
            
            // Factorial patterns
            { pattern: /factorial|fact.*\*.*\(.*n.*-.*1.*\)/gi, complexity: 'O(n!)', weight: 10 },
            
            // Cubic patterns
            { pattern: /for[^{]*{[^}]*for[^{]*{[^}]*for[^{]*{/g, complexity: 'O(n³)', weight: 8 },
            
            // Quadratic patterns
            { pattern: /for[^{]*{[^}]*for[^{]*{/g, complexity: 'O(n²)', weight: 7 },
            { pattern: /while[^{]*{[^}]*while[^{]*{/g, complexity: 'O(n²)', weight: 7 },
            { pattern: /nested.*loop|double.*loop/gi, complexity: 'O(n²)', weight: 6 },
            
            // N log N patterns
            { pattern: /(merge|quick|heap).*sort/gi, complexity: 'O(n log n)', weight: 8 },
            { pattern: /sort.*\(/g, complexity: 'O(n log n)', weight: 5 },
            
            // Linear patterns
            { pattern: /for[^{]*{(?![^}]*for)/g, complexity: 'O(n)', weight: 5 },
            { pattern: /while[^{]*{(?![^}]*while)/g, complexity: 'O(n)', weight: 5 },
            { pattern: /linear.*search|sequential.*search/gi, complexity: 'O(n)', weight: 6 },
            { pattern: /(\w+)\s*\([^)]*\)\s*{[^}]*\1\s*\([^)]*n\s*-\s*1[^)]*\)/g, complexity: 'O(n)', weight: 6 },
            
            // Logarithmic patterns
            { pattern: /binary.*search/gi, complexity: 'O(log n)', weight: 7 },
            { pattern: /\/\s*2|>>.*1|\*\s*2|<<.*1/g, complexity: 'O(log n)', weight: 4 },
            { pattern: /while.*n.*\/.*2|while.*n.*>>.*1/g, complexity: 'O(log n)', weight: 6 },
            
            // Constant patterns (default)
            { pattern: /.*/, complexity: 'O(1)', weight: 1 }
        ];

        this.spaceComplexityPatterns = [
            // Exponential space
            { pattern: /fibonacci.*recursive|fib.*recursive/gi, complexity: 'O(2^n)', weight: 9 },
            
            // Quadratic space
            { pattern: /\w+\s*\[\s*\w+\s*\]\s*\[\s*\w+\s*\]/g, complexity: 'O(n²)', weight: 8 },
            { pattern: /matrix|2d.*array|two.*dimensional/gi, complexity: 'O(n²)', weight: 7 },
            
            // Linear space
            { pattern: /\w+\s*\[\s*\w+\s*\]/g, complexity: 'O(n)', weight: 6 },
            { pattern: /(malloc|calloc|new|vector|list|array)\s*\(/g, complexity: 'O(n)', weight: 7 },
            { pattern: /(\w+)\s*\([^)]*\)\s*{[^}]*\1\s*\(/g, complexity: 'O(n)', weight: 5 }, // Recursion depth
            { pattern: /recursive|recursion/gi, complexity: 'O(n)', weight: 4 },
            
            // Logarithmic space
            { pattern: /binary.*tree|bst/gi, complexity: 'O(log n)', weight: 6 },
            { pattern: /tail.*recursive/gi, complexity: 'O(log n)', weight: 5 },
            
            // Constant space (default)
            { pattern: /.*/, complexity: 'O(1)', weight: 1 }
        ];
    }

    analyzeTimeComplexity(code) {
        if (!code || !code.trim()) return 'O(1)';
        
        let maxComplexity = 'O(1)';
        let maxWeight = 0;
        
        // Normalize code for better pattern matching
        const normalizedCode = code.toLowerCase().replace(/\s+/g, ' ');
        
        for (const pattern of this.timeComplexityPatterns) {
            const matches = code.match(pattern.pattern);
            if (matches && matches.length > 0) {
                const currentWeight = pattern.weight * matches.length;
                if (currentWeight > maxWeight) {
                    maxWeight = currentWeight;
                    maxComplexity = pattern.complexity;
                }
            }
        }
        
        // Special case analysis
        maxComplexity = this.refineComplexityAnalysis(code, maxComplexity);
        
        return maxComplexity;
    }

    analyzeSpaceComplexity(code) {
        if (!code || !code.trim()) return 'O(1)';
        
        let maxComplexity = 'O(1)';
        let maxWeight = 0;
        
        for (const pattern of this.spaceComplexityPatterns) {
            const matches = code.match(pattern.pattern);
            if (matches && matches.length > 0) {
                const currentWeight = pattern.weight * matches.length;
                if (currentWeight > maxWeight) {
                    maxWeight = currentWeight;
                    maxComplexity = pattern.complexity;
                }
            }
        }
        
        return maxComplexity;
    }

    refineComplexityAnalysis(code, initialComplexity) {
        // Count actual nested loop levels
        const nestedLoopDepth = this.countNestedLoops(code);
        
        if (nestedLoopDepth >= 3) return 'O(n³)';
        if (nestedLoopDepth === 2) return 'O(n²)';
        if (nestedLoopDepth === 1 && initialComplexity === 'O(1)') return 'O(n)';
        
        // Check for specific algorithms
        if (code.includes('quicksort') || code.includes('mergesort') || code.includes('heapsort')) {
            return 'O(n log n)';
        }
        
        // Check for exponential recursion patterns
        if (this.hasExponentialRecursion(code)) {
            return 'O(2^n)';
        }
        
        return initialComplexity;
    }

    countNestedLoops(code) {
        let maxDepth = 0;
        let currentDepth = 0;
        let inLoop = false;
        
        const tokens = code.split(/(\bfor\b|\bwhile\b|{|})/);
        
        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i];
            
            if (token === 'for' || token === 'while') {
                inLoop = true;
            } else if (token === '{' && inLoop) {
                currentDepth++;
                maxDepth = Math.max(maxDepth, currentDepth);
                inLoop = false;
            } else if (token === '}') {
                if (currentDepth > 0) currentDepth--;
            }
        }
        
        return maxDepth;
    }

    hasExponentialRecursion(code) {
        // Look for patterns like T(n) = T(n-1) + T(n-2)
        const funcCalls = code.match(/(\w+)\s*\([^)]*n[^)]*\)/g);
        if (!funcCalls) return false;
        
        const recursivePattern = /(\w+)\s*\([^)]*n\s*[-+]\s*\d+[^)]*\).*\1\s*\([^)]*n\s*[-+]\s*\d+[^)]*\)/;
        return recursivePattern.test(code);
    }

    getComplexityOrder(complexity) {
        const order = {
            'O(1)': 1,
            'O(log n)': 2,
            'O(n)': 3,
            'O(n log n)': 4,
            'O(n²)': 5,
            'O(n³)': 6,
            'O(2^n)': 7,
            'O(n!)': 8
        };
        return order[complexity] || 1;
    }

    compareComplexity(complexity1, complexity2) {
        const order1 = this.getComplexityOrder(complexity1);
        const order2 = this.getComplexityOrder(complexity2);
        
        if (order1 > order2) return 'Improved';
        if (order1 < order2) return 'Worse';
        return 'Same';
    }
}

// Make it globally available
window.ComplexityAnalyzer = ComplexityAnalyzer;