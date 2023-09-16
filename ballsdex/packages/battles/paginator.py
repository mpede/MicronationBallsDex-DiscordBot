from ballsdex.packages.players.countryballs_paginator import CountryballsSelector

async def nothing(): # im evil himself
    pass

# TODO: add random button

class BallSelectSingular(CountryballsSelector):
    selectionfunc = nothing

    async def ball_selected(self, interaction: discord.Interaction, ball_instance: BallInstance):
        await self.selectionfunc(interaction, ball_instance)
    def on_select(self, func):
        self.selectionfunc = func

class BallSelectMultiple(CountryballsSelector):
    selectionfunc = nothing

    @discord.ui.select(min_values=5, max_values=5)
    async def select_ball_menu(self, interaction: discord.Interaction, item: discord.ui.Select):
        await interaction.response.defer(thinking=True)
        instances = [await BallInstance.get(id=x) for x in interaction.data.get("values")]
        await self.ball_selected(interaction, instances)

    async def ball_selected(self, interaction: discord.Interaction, instances):
        await self.selectionfunc(interaction, instances)

    def on_select(self, func):
        self.selectionfunc = func
