async function fetchContacts(platform) {
    try {
        const response = await fetch(`/api/contacts/${platform}`);
        const contacts = await response.json();
        displayContacts(contacts);
    } catch (error) {
        console.error('Error fetching contacts:', error);
        alert('Failed to fetch contacts. Please try again later.');
    }
}

function displayContacts(contacts) {
    const contactsContainer = document.querySelector('.contacts');
    contactsContainer.innerHTML = ''; // Clear previous contacts

    if (contacts.length === 0) {
        contactsContainer.innerHTML = '<p>No contacts found.</p>';
        return;
    }

    contacts.forEach(contact => {
        const contactItem = document.createElement('div');
        contactItem.className = 'contact-item';
        contactItem.innerHTML = `
            <img src="${contact.profilePic}" alt="${contact.name}" style="width:40px; height:40px;">
            <span>${contact.name}</span> - ${contact.recentActivity}
        `;
        contactsContainer.appendChild(contactItem);
    });
}

// Example function to simulate notifications
function addNotification(message) {
    const notificationList = document.querySelector('.notification-list');
    
    const notificationItem = document.createElement('div');
    notificationItem.textContent = message;

    notificationList.appendChild(notificationItem);
}

// Simulate real-time notifications
setInterval(() => {
   addNotification(`New post from John Doe at ${new Date().toLocaleTimeString()}`);
}, 5000); // Add a new notification every 5 seconds