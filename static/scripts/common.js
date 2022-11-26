// Returns the year via local timing
function getCurrentYear() {
    return new Date().getFullYear();
};
// Changing the inner html of the span with to the given year
document.querySelector('.year').innerHTML = getCurrentYear();
