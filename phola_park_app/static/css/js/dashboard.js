async function loadNotifications() {
    const token = localStorage.getItem("access_token");

    const response = await fetch("/api/v1/notifications", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (!response.ok) {
        console.log("Failed to load notifications");
        return;
    }

    const notifications = await response.json();

    const list = document.getElementById("notification-list");
    const count = document.getElementById("notification-count");

    list.innerHTML = "";
    let unread = 0;

    notifications.forEach(n => {
        const item = document.createElement("li");
        item.textContent = n.message;

        if (!n.is_read) {
            item.style.fontWeight = "bold";
            unread++;
        }

        item.onclick = () => markAsRead(n.id);

        list.appendChild(item);
    });

    count.textContent = unread;
}
async function markAsRead(id) {
    const token = localStorage.getItem("access_token");

    await fetch(`/api/v1/notifications/${id}/read`, {
        method: "PUT",
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    loadNotifications();
}
document.addEventListener("DOMContentLoaded", loadNotifications);
