from ballsdex.packages.battles.cog import Battles

async def setup(bot: "BallsDexBot"):
	await bot.add_cog(Battles(bot))
