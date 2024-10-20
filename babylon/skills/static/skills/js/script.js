// scripts.js
document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript is working!");
    const buttons = document.querySelectorAll('a');
    
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            console.log(`${button.textContent} clicked`);
        });
    });
});
