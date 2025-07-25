🎮 Fantasy Adventure Game with AI Agents
🧠 What It Does
The Fantasy Adventure Game is a text-based interactive game powered by multiple AI agents. It creates an immersive adventure where the player can explore mysterious locations, battle monsters, and collect rewards. Each part of the game is handled by a specialized AI agent, making the experience modular and easy to extend.

When you play, you can type commands like story to explore the world, fight to engage in combat, or loot to collect treasures. Each action is routed to a different AI agent that responds with a unique outcome, creating a dynamic storytelling experience.

🔄 How It Works
The game uses a Router Agent to understand your input and forward it to the right specialized agent:

NarratorAgent → Generates a mysterious story scene using the generate_event() tool.

MonsterAgent → Triggers a combat encounter, announces a monster fight, and rolls a dice with roll_dice() to decide the battle outcome.

ItemAgent → Gives you rewards like a Magic Sword or gold coins to update your inventory.

The Router Agent ensures only one handoff per command, making the game flow smooth and controlled.

⚙️ Tech & Tools
This game is built using the OpenAI Agent SDK along with the Runner to manage agent interactions. It uses simple tools like a Dice Roller for combat outcomes and an Event Generator for creating story scenes. The modular design allows easy handoffs between the Narrator, Monster, and Item agents, showcasing how multiple agents can collaborate in a single game experience.