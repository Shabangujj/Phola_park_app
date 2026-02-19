function getToken() {
    return localStorage.getItem("token");
}

async function apiFetch(url, options = {}) {
    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    };

    const response = await fetch(url, {
        ...options,
        headers: headers
    });

    return response.json();
}
