export function createAlertButton() {
    const button = document.createElement("button");
    button.textContent = "Clique-moi !";
    button.className = "btn btn-primary";

    button.addEventListener("click", () => {
        const alertDiv = document.createElement("div");
        alertDiv.className = "alert alert-success";
        alertDiv.textContent = "🎉 Bravo, tu as cliqué sur le bouton !";
        document.body.appendChild(alertDiv);
    });

    return button;
}