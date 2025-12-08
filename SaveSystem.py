import json
import os

SAVE_FILE = "savegame.json"

class SaveSystem:

    @staticmethod
    def save_game(playerInfo, game_state):
        data = {
            "money": playerInfo.playerMoney,
            "owned_jokers": list(game_state.playerJokers),
            "completed_levels": getattr(game_state, "completedLevels", []),
            "hand_scores": getattr(game_state, "HAND_SCORES", {})
        }

        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print("[SAVE] Game saved successfully!")

    @staticmethod
    def load_game(playerInfo, game_state):
        if not os.path.exists(SAVE_FILE):
            print("[SAVE] No save file found.")
            return

        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        # Load money
        if "money" in data:
            playerInfo.playerMoney = data["money"]

        # Load jokers
        if "owned_jokers" in data:
            game_state.playerJokers = data["owned_jokers"]

        # Load completed levels
        if "completed_levels" in data:
            setattr(game_state, "completedLevels", data["completed_levels"])

        # Load hand scores (planet upgrades)
        if "hand_scores" in data and hasattr(game_state, "HAND_SCORES"):
            game_state.HAND_SCORES.update(data["hand_scores"])

        print("[SAVE] Game loaded successfully!")
