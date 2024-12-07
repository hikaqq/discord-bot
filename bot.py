import disnake
from disnake.ext import commands
from disnake import TextInputStyle

intents = disnake.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

applications = {}

channel_id = 1312851925007470702 

@bot.slash_command()
async def apply(inter: disnake.AppCmdInter):
    """Создайте заявку на вступление/должность."""
    embed = disnake.Embed(
        title="Подача заявки",
        description="Выберите тип заявки или нажмите на кнопку ниже, чтобы начать!",
        color=0x000000,
    )
    embed.set_image(url="https://i.imgur.com/MFeieSI.png")

    await inter.response.send_message(
        embed=embed,
        components=[
            disnake.ui.Button(
                label="Подать заявку",
                style=disnake.ButtonStyle.grey,
                custom_id="open_application"
            )
        ]
    )

@bot.event
async def on_button_click(inter: disnake.MessageInteraction):
    if inter.component.custom_id == "open_application":
        await inter.response.send_modal(
            title="Подайте заявку",
            custom_id="application_form",
            components=[
                disnake.ui.TextInput(
                    label="Ваше имя OOC и возраст",
                    placeholder="Введите ваше имя OOC и возраст",
                    custom_id="name",
                    style=TextInputStyle.short,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Ваш NickName | Static:",
                    placeholder="Введите ваш NickName или Static",
                    custom_id="nickname",
                    style=TextInputStyle.short,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Ваш Discord и ID:",
                    placeholder="Укажите ваш Discord и ID",
                    custom_id="discord_id",
                    style=TextInputStyle.short,
                    max_length=100,
                ),
                disnake.ui.TextInput(
                    label="Откат с Сайги и Carabine MK2 (ссылка):",
                    placeholder="Приведите ссылку на откат",
                    custom_id="rollback",
                    style=TextInputStyle.short,
                    max_length=200,
                ),
                disnake.ui.TextInput(
                    label="Чего вы ждете от вступления в семью?",
                    placeholder="Опишите, что вы ожидаете от вступления в семью",
                    custom_id="expectations",
                    style=TextInputStyle.paragraph,
                ),
            ],
        )

@bot.event
async def on_modal_submit(inter: disnake.ModalInteraction):
    if inter.custom_id == "application_form":
        applications[inter.author.id] = inter.text_values

        try:
            channel = await bot.fetch_channel(channel_id)
        except disnake.NotFound:
            await inter.response.send_message("Канал для отправки заявки не найден.", ephemeral=True)
            return
        except disnake.Forbidden:
            await inter.response.send_message("У бота нет доступа к этому каналу.", ephemeral=True)
            return

        embed = disnake.Embed(
            title="Новая заявка",
            description=f"Новая заявка от {inter.author.mention}",
            color=0x000000
        )
        embed.add_field(name="Имя и возраст", value=inter.text_values["name"], inline=False)
        embed.add_field(name="NickName | Static", value=inter.text_values["nickname"], inline=False)
        embed.add_field(name="Discord и ID", value=inter.text_values["discord_id"], inline=False)
        embed.add_field(name="Откат", value=inter.text_values["rollback"], inline=False)
        embed.add_field(name="Ожидания", value=inter.text_values["expectations"], inline=False)
        embed.set_image(url="https://i.imgur.com/MFeieSI.png")

        await channel.send(embed=embed)
        await inter.response.send_message("Ваша заявка успешно отправлена!", ephemeral=True)


bot.run("MTMxNDkyNjA1MDE2NTM5MTM4MQ.Gpvlod.31p3qC4bbCsEgFEORBzBecdT4jt1Z5ot-4nEtw")
