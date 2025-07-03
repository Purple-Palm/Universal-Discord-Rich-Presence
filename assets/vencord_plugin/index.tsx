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
        const response = await fetch(STATUS_URL, { cache: "no-store" });
        if (!response.ok) {
            if (lastKnownStatus !== null) setRpc(null);
            lastKnownStatus = null;
            return;
        }

        const content = await response.text();

        if (content && content !== lastKnownStatus) {
            lastKnownStatus = content;
            const activity = JSON.parse(content);
            
            // --- NEW: Debug Logging ---
            // This will print the exact object to the Discord console.
            console.log("[PythonBridge] Received payload from server:", activity);
            
            setRpc(activity);
        }
    } catch (error) {
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
        checkStatus();
        statusCheckInterval = window.setInterval(checkStatus, 1000);
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
