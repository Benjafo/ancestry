
function openPopup(event) {
    tree_member = event.target.__data__.data
    popup(tree_member)
}

function popup(tree_member) {
    popupContainer = popupHTML(tree_member)
    document.body.appendChild(popupContainer);

    popupContainer.style.display = "block";

    popupContainer.addEventListener("click", () => {
        closePopup(popupContainer);
    });
}

function popupHTML(tree_member) {
    const popupContainer = document.createElement("div");
    popupContainer.className = "popup-container";

    const memberName = document.createElement("h2");
    memberName.textContent = tree_member.name;

    const memberGender = document.createElement("p");
    memberGender.textContent = "Gender: " + tree_member.gender;

    popupContainer.appendChild(memberName);
    popupContainer.appendChild(memberGender);

    return popupContainer;
}

function closePopup(popupContainer) {
    popupContainer.style.display = "none";
    popupContainer.remove();
}