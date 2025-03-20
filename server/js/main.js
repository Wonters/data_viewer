import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import { initChat } from "./modules/chat.js";
import { showNotification } from "./modules/notifications.js";
import { logMessage } from "./modules/utils.js";
import {createAlertButton} from "./modules/buttonAlerte"

// Initialisation du chat
document.addEventListener("DOMContentLoaded", () => {
    initChat();
    showNotification("Bienvenue dans le chat !");
    logMessage("Application démarrée.");
    document.body.appendChild(createAlertButton());
});