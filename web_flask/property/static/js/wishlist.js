document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to all delete icons
    const deleteIcons = document.querySelectorAll('.delete-icon a');
    deleteIcons.forEach(function(icon) {
        icon.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default anchor behavior
            const propertyItem = this.closest('.property-item'); // Find the property card
            if (propertyItem) {
                propertyItem.remove(); // Remove the card
            }
        });
    });
});