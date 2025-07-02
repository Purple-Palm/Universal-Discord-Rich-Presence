/*
 * Vencord, a Discord client mod
 * Copyright (c) 2025 Vendicated and contributors
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

import definePlugin from "@utils/types";
import { FluxDispatcher } from "@webpack/common";

// --- Configuration ---
const STATUS_URL = "http://localhost:8765/status";

let statusCheckInterval: number | null = null;
let lastKnownStatus: string | null = null;

// The main function to update the RPC status
function setRpc(activity: any) {
    FluxDispatcher.dispatch({
        type: "LOCAL_ACTIVITY_UPDATE",
        activity,
        socketId: "PythonHttpBridge", // A unique socket ID for our presence
    });
}

async function checkStatus() {
    try {
        const response = await fetch(STATUS_URL);
        if (!response.ok) {
            // This will happen if the python server is not running
            if (lastKnownStatus !== null) setRpc(null);
            lastKnownStatus = null;
            return;
        }

        const content = await response.text();

        // Only update if the content has actually changed
        if (content && content !== lastKnownStatus) {
            console.log("[PythonBridge] Fetched new status. Updating presence.");
            lastKnownStatus = content;
            const activity = JSON.parse(content);
            setRpc(activity);
        }
    } catch (error) {
        // This catches network errors when the server is down
        if (lastKnownStatus !== null) {
            console.log("[PythonBridge] Cannot connect to server. Clearing presence.");
            setRpc(null);
        }
        lastKnownStatus = null;
    }
}

export default definePlugin({
    name: "PythonBridge",
    description: "Receives Rich Presence data from a local Python HTTP server.",
    authors: [{ name: "You!", id: 1n }],

    start() {
        console.log("[PythonBridge] Starting HTTP status poller...");
        // Initial check
        checkStatus();
        // Start checking the server every 5 seconds
        statusCheckInterval = window.setInterval(checkStatus, 5000);
    },

    stop() {
        if (statusCheckInterval) {
            clearInterval(statusCheckInterval);
            statusCheckInterval = null;
        }
        setRpc(null); // Clear the Rich Presence
        console.log("[PythonBridge] Plugin stopped.");
    },
});
