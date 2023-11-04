function toggleNavigation() {
    const navigation = document.querySelector('.navigation');
    const displayboard = document.querySelector('.displayboard');

    if (navigation.classList.contains('hidden')) {
        // Show navigation
        navigation.classList.remove('hidden');
        displayboard.style.width = '80%'; // Reset displayboard width
    } else {
        // Hide navigation
        navigation.classList.add('hidden');
        displayboard.style.width = '100%'; // Expand displayboard to 100%
    }
}
