import discord
from discord.ext import tasks
from pycoingecko import CoinGeckoAPI
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
cg = CoinGeckoAPI()

# get crypto prices
def get_crypto_prices():
    prices = cg.get_price(ids=['solana', 'ethereum'], vs_currencies='usd')
    sol_price = prices['solana']['usd']
    eth_price = prices['ethereum']['usd']
    return f"SOL: ${sol_price:.2f} | ETH: ${eth_price:.2f}"


@client.event
async def on_ready():
    print(f'Bot connesso come {client.user}')
    update_status.start()

# update status every 5 minutes
@tasks.loop(minutes=5)
async def update_status():
    try:
        print("Aggiornamento prezzi...")  # debug log
        price_string = get_crypto_prices()
        print(f"Nuovi prezzi: {price_string}")  # debug log
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.CustomActivity(name=price_string)
        )
        print("Stato aggiornato!")  # debug log
    except Exception as e:
        print(f"Errore nell'aggiornamento dei prezzi: {e}")

TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)