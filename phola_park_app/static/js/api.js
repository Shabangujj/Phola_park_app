// 🔗 BASE API HELPER
async function apiRequest(url, method = "GET", data = null) {
    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
        console.error("API Error:", response.status);
        return null;
    }

    return await response.json();
}

///////////////////////////////////////////////////////////
// 🔔 NOTIFICATIONS
///////////////////////////////////////////////////////////

// Get notifications
async function getNotifications() {
    return await apiRequest("/notifications/");
}

// Mark as read
async function markNotificationRead(id) {
    return await apiRequest(`/notifications/read/${id}`, "POST");
}

// Delete notification
async function deleteNotification(id) {
    return await apiRequest(`/notifications/delete/${id}`, "POST");
}

///////////////////////////////////////////////////////////
// 📊 REPORTS
///////////////////////////////////////////////////////////

// Get all reports (role-based)
async function getReports() {
    return await apiRequest("/api/reports");
}

// Update report status
async function updateReportStatus(reportId, status) {
    return await apiRequest(`/admin/update_report_status/${reportId}`, "POST", {
        status: status
    });
}

///////////////////////////////////////////////////////////
// 👤 USERS
///////////////////////////////////////////////////////////

// Assign role
async function assignRole(userId, role) {
    return await apiRequest(`/admin/assign_role/${userId}`, "POST", {
        role: role
    });
}

// Assign portfolio
async function assignPortfolio(userId, portfolio) {
    return await apiRequest(`/admin/assign_portfolio/${userId}`, "POST", {
        portfolio: portfolio
    });
}

///////////////////////////////////////////////////////////
// 📢 ANNOUNCEMENTS
///////////////////////////////////////////////////////////

// Get announcements
async function getAnnouncements() {
    return await apiRequest("/admin/announcements");
}

// Delete announcement
async function deleteAnnouncement(id) {
    return await apiRequest(`/admin/delete_announcement/${id}`, "POST");
}

///////////////////////////////////////////////////////////
// 🧠 HELPER (UI)
///////////////////////////////////////////////////////////

// Show alert
function showMessage(msg, type = "info") {
    alert(msg); // later upgrade to toast UI
}