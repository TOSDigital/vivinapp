// Function to set the active class based on the current page URL
function setActiveTab() {
    const currentUrl = window.location.pathname;
    const navTabs = document.querySelectorAll('.nav-tab');

    // Loop through each nav-tab and check if its href matches the current URL
    navTabs.forEach(tab => {
        const tabUrl = tab.querySelector('a').getAttribute('href');
        if (currentUrl === tabUrl) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
}

// Call the setActiveTab function on page load
window.addEventListener('DOMContentLoaded', setActiveTab);
