import os
from dotenv import load_dotenv
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,function_tool
from agents.run import RunConfig
import asyncio
import random

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
api_key=api_key,
base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
model="gemini-2.0-flash",
openai_client=external_client
)

config = RunConfig(
model=model,
model_provider=external_client,
tracing_disabled=True
)

@function_tool
async def roll_dice()->str:
    dice=random.randint(1,10)
    return f"""🧟 A monster jumps out! Its time to fight..
            Rolling the dice to see your attack result!!
            you got number {dice}"""

@function_tool
async def generate_event()->str:
    return """You enter into the dark forest where you are all alone.
            Nobody is there except you and the dark moon which light sparks into the forest.
            Suddenly you see a hidden cave covered with green grass.
            You remove the grass and enter your first step and...."""

async def main():

    Narratoragent=Agent(
        name="Narrator Agent",
        instructions="""You are a Narrator Agent..“Always call 'generate_event()'
        to narrate story, do NOT reason or create extra text
        DONT start reasoning on anything just use tool.""",
        tools=[generate_event]

    )
    Monsteragent=Agent(
        name="Combat phase Agent",
        instructions="""You are a combat phase agent.
            IMMEDIATELY call the 'roll_dice' tool to get a dice result.
            After you show the dice result, STOP""",
        tools=[roll_dice]
    )

    ItemAgent=Agent(
        name="Inventory Agent",
        instructions="""You are an inventory agent.Your task is to 
        say user '🎁You found a Magic Sword and 20 gold coins!
        Your inventory is updated.'
        Just say this and then stop. Do NOT hand off to any other agent."""
    )
    RouterAgent=Agent(
        name="Router Agent",
        instructions="""You are a Router Agent.Your task is to route between specific agent.
        You NEVER respond directly to the user.
        RULES:
        -If user ask about story,adventure or explore->Handoff to 'Narratoragent'.
        -If user ask about combat,fight,monster -> handoff to 'Monsteragent'.
        -If user tell about Inventory,loot or rewards-> handoff to 'Itemagent'.""",
        handoffs=[Narratoragent,Monsteragent,ItemAgent]

    )
    
    print(f"🎮 Welcome to Fantasy Adventure Game!")
    while True:
       print("Starts Your Adventure..")
       user=input("Enter your move....")
       if "quit" in user.lower():
           print("💀 Game Over! Thanks for playing! 🏰")
           break
           

       response=await Runner.run(
        RouterAgent,
        input=user,
        run_config=config,
        
        )
       if response and response.final_output:

        print(response.final_output)

if __name__=="__main__":
    asyncio.run(main())
