// Remove the 'quotations' and 'sales orders' from portal view
document.addEventListener("DOMContentLoaded", () => {
    if (window.location.href.includes('/my/home')) {
        document.querySelector('[href="/my/quotes"]').remove();
        document.querySelector('[href="/my/orders"]').remove();
    }
});