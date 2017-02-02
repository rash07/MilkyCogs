
import asyncio
import discord
from lxml.html import fromstring
from discord.ext import commands 
import requests
from aiohttp import get

class bnseu:

	"""BNS custom commands!"""
	def __init__(self, bot):
		self.bot = bot
		
	def eb(text,b,e):
		begin=text.find(b)
		end=text.find(e,begin)
		return text[begin+len(b):end].strip()
		
	@commands.command(pass_context=True)
	async def bnseu(self, ctx, *text):
		""" Parsing character data from accessing BNS web API
		"""
		# URLs
		
		
		BNS_REGION = 'na'

		id = None
		class_name = None
		server = None
		level = None
		hmlevel = None
		faction = None
		factionLevel = None
		guild = None
		weapon_durability = None
		stats = None
		equips = None
		error = False
		otherChars = None		

		# Preparing the Name
		stack = ctx.message.content.lower().split()
		if len(stack) < 2:
			await self.bot.say('Correct Syntax: *!bns Evangeline Arashel*')
			return
			
		if len(stack) < 3:
			name = stack[1]
			outputName = name 
		else:
			name = stack[1] + '%20' + stack[2]
			outputName = stack[1] + ' ' + stack[2]

		# Need to convert space to URL encoding character
		await self.bot.say('*Fetching...*')
		page = await get
		# page = await get(BNS_WEB_PROFILE.format(name=text, region=BNS_REGION))
		content = await page.read()
		content = fromstring(str(content))

		# Player ID
		playerID = content.xpath('//dl[@class="signature"]/dt/a/text()')
		if len(playerID) != 0:
			id = playerID[0]
			#await self.bot.say(id)
		else:
			await self.bot.say('Character not found...')
			return
		
		# Player HM Level
		playerHMLv = content.xpath('//span[@class="masteryLv"]/text()')
		if len(playerHMLv) != 0:
			hmlevel = playerHMLv[0]

		# Player Info
		playerInfo = content.xpath('//dd[@class="desc"]/ul/li/text()')

		if hmlevel == None:
			if len(playerInfo) == 3:
				# [CLASS NAME] [LEVEL] [SERVER]
				class_name, level, server = [x.replace('[', '').replace(']', '') for x in playerInfo]
			elif len(playerInfo) == 4:
				# [CLASS NAME] [LEVEL] [SERVER] [FACTION]
				class_name, level, server, faction = [x.replace('[', '').replace(']', '') for x in playerInfo]
			elif len(playerInfo) == 5:
				# [CLASS NAME] [LEVEL] [SERVER] [FACTION] [GUILD]
				class_name, level, server, faction, guild = [x.replace('[', '').replace(']', '') for x in playerInfo]			
		else:
			if len(playerInfo) == 4:
				# [CLASS NAME] [LEVEL] [] [SERVER]
				class_name, level, _, server = [x.replace('[', '').replace(']', '') for x in playerInfo]
			elif len(playerInfo) == 5:
				# [CLASS NAME] [LEVEL] [] [SERVER] [FACTION]
				class_name, level, _, server, faction = [x.replace('[', '').replace(']', '') for x in playerInfo]
			elif len(playerInfo) == 6:
				# [CLASS NAME] [LEVEL] [] [SERVER] [FACTION] [GUILD]
				class_name, level, _, server, faction, guild = [x.replace('[', '').replace(']', '') for x in playerInfo]


		# Faction and Faction Level
		if faction != None:
			faction_texts = faction.split('\xa0')
			faction = faction_texts[0]
			factionLevel = faction_texts[1]
	
	# Player Stats
		stats = content.xpath('//span[@class="stat-point"]/text()')

		# Player Equipments
		equips = content.xpath('//div[@class="name"]/span/text()')

		# Player Weapon Durability
		playerWeaponDurability = content.xpath('//div[@class="wrapWeapon"]/div/div[@class="quality"]/span[@class="text"]/text()')
		if len(playerWeaponDurability) != 0:
			weapon_durability = playerWeaponDurability[0]

		# Setting up the output
		result =  '```\n' \
			'☆ Profile ☆ \n' \
			'Name     : {name} [{ID}]\n' \
			'Guild    : {guild} [{server}]\n' \
			'Faction  : {faction} | {factionLevel}\n' \
			'Class    : {class_name}\n' \
			'Level    : {level} | {hmlevel}\n' \
			'☆ Stats ☆ \n' \
			'AP       : {attack_power}\n' \
			'Cri      : {critical} ({critical_rate})\n' \
			'CritDmg  : {critical_damage} ({critical_damage_rate})\n' \
			'Acc      : {accuracy} ({accuracy_rate})\n' \
			'Pierce   : {piercing} ({piercing_rate})\n' \
			'Health   : {hp}\n' \
			'Def      : {defense} ({defense_rate})\n' \
			'Block    : {block} ({block_rate})\n' \
			'Eva      : {evasion} ({evasion_rate})\n' \
			'☆ Equipments ☆\n' \
			'Weapon   : {weapon} ({weapon_dura})\n' \
			'Necklace : {necklace}\n' \
			'Earing   : {earing}\n' \
			'Ring     : {ring}\n' \
			'Bracelet : {bracelet}\n' \
			'Belt     : {belt}\n' \
			'Soul     : {soul}```'
		
		# Check for empty equipment
		weapon = equips[0]
		necklace = equips[1]
		earing = equips[2]
		ring = equips[3]
		bracelet = equips[4]
		belt = equips[5]
		soul = equips[6]

		if weapon == 'Weapon':
			weapon = 'No Weapon'
		if necklace == 'Necklace':
			necklace = 'No Necklace'
		if earing == 'Earring':
			earing = 'No Earing'
		if ring == 'Ring':
			ring = 'No Ring'
		if belt == 'Belt':
			belt = 'No Belt'
		if bracelet == 'Bracelet':
			bracelet = 'No Bracelet'
		if soul == 'Soul':
			soul = 'This person has no soul'
		
		# Displaying the output
		output = result.format(name=outputName,
			ID=id,
			server=server,
			class_name=class_name,
			level=level,
			hmlevel = hmlevel,
			faction=faction,
			factionLevel=factionLevel,
			guild=guild,
			attack_power= stats[0],
			critical = stats[21],
			critical_rate = stats[24],
			critical_damage = stats[25],
			critical_damage_rate = stats[28],
			accuracy = stats[12],
			accuracy_rate = stats[15],
			piercing = stats[7],
			piercing_rate = stats[10],
			hp = stats[44],
			defense = stats[48],
			defense_rate = stats[51],
			block = stats[65],
			block_rate = stats[70],
			evasion = stats[60],
			evasion_rate = stats[63],
			weapon = weapon,
			weapon_dura = weapon_durability,
			necklace = necklace,
			earing = earing,
			ring = ring,
			bracelet = bracelet,
			belt = belt,
			soul = soul)

		await self.bot.say(output)

			
def setup(bot):
	n = bnseu(bot)
	bot.add_cog(n)
