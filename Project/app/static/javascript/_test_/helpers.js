// attach the .equals method to Array's prototype to call it on any array
Array.prototype.equals = function(array) {
    // if the other array is a falsy value, return
    if (!array || this.length !== array.length) {
        return false;
    }

    for (var i = 0, l = this.length; i < l; i++) {
        if (this[i] !== array[i]) {
            return false;
        }
    }
    return true;
};

// Hide method from for-in loops
Object.defineProperty(Array.prototype, "equals", { enumerable: false });

// function arrayContainsAnotherArray(needle, haystack) {
//     for (var i = 0; i < needle.length; i++) {
//         if (haystack.indexOf(needle[i]) === -1)
//             return false;
//     }
//     return true;
// }
