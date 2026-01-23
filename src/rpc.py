from pypresence import Presence, ActivityType
import logging


class UniversalRPC:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.rpc = None
        self.connected = False
        self.last_activity_hash = None

    def connect(self):
        if not self.client_id:
            return
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            logging.info(f"✅ Connected to Discord RPC")
        except Exception as e:
            logging.error(f"❌ RPC Connection Error: {e}")
            self.connected = False

    def update(self, activity: dict):
        if not self.connected:
            self.connect()
            return

        # Simple deduplication
        act_hash = hash(frozenset(str(activity)))
        if act_hash == self.last_activity_hash:
            return

        try:

            payload = {
                "activity_type": ActivityType.WATCHING,
                "details": activity.get("header_text"),  # This will be the App Name
                "state": activity.get("description"),  # This will be what you are doing

                "large_image": activity.get("large_image"),
                "large_text": activity.get("header_text"),
                "small_image": activity.get("small_image"),
                "small_text": activity.get("small_text"),

                "start": activity.get("start"),
                "buttons": activity.get("buttons"),
                "instance": True
            }

            # Clean empty fields
            payload = {k: v for k, v in payload.items() if v}

            self.rpc.update(**payload)

            self.last_activity_hash = act_hash
            logging.info(f"📡 Updated: [Bold]{activity.get('header_text')}[/Bold] - {activity.get('description')}")

        except Exception as e:
            logging.error(f"Failed to update RPC: {e}")
            self.connected = False
            self.last_activity_hash = None

    def clear(self):
        if self.connected and self.last_activity_hash is not None:
            try:
                self.rpc.clear()
                self.last_activity_hash = None
            except:
                pass