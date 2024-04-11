import flet as ft
from flet import *
from functools import partial
import time
from abc import ABC, abstractmethod


class ModernNavBar(UserControl):
    def __init__(self):
        super().__init__()

    def HighLight(self, e):
        if e.data == "true":
            e.control.bgcolor = "white10"
            e.control.update()
        else:
            e.control.bgcolor = None
            e.control.update()

    def user_data(self, division, zvanie, name, surname) -> Container:
        """Информация о кабинете"""
        return Container(
            padding=padding.only(top=10, left=20, bottom=10),
            content=Row(
                adaptive=True,

                controls=[
                    Container(
                        width=42,
                        height=42,
                        adaptive=True,
                        bgcolor="bluegrey900",
                        border_radius=3,
                        alignment=alignment.center,
                        content=Text(value=division,
                                     size=10,
                                     color="grey"
                                     )
                    ), Column(spacing=1,
                              adaptive=True,
                              controls=[
                                  Text(
                                      value=zvanie,
                                      size=11,
                                      opacity=1,
                                      animate_opacity=200,

                                  ),
                                  Text(
                                      value=f"{surname} {name}",
                                      size=11,
                                      opacity=1,
                                      animate_opacity=200,

                                  )
                              ])
                ]
            )

        )

    def ConteinIcon(self, icon_name: str, text: str, click=None):
        return Container(
            width=280,
            height=50,
            border_radius=10,
            on_hover=None,
            padding=padding.only(left=10),
            content=Row(
                controls=[
                    TextButton(
                        on_click=click,
                        text=text,
                        height=60,
                        icon=icon_name,
                        icon_color="grey",
                        style=ButtonStyle(
                            color=ft.colors.BLUE_GREY,
                        )

                    ),
                    # Text(value=text,
                    #        size=11,
                    #        opacity=1,
                    #        animate_opacity=200)
                ]
            ),

        )

    def build(self):
        return Container(
            width=300,
            adaptive=True,
            height=900,
            padding=padding.only(top=10, left=10),
            border=ft.border.only(right=ft.border.BorderSide(1, ft.colors.GREY_300)),
            alignment=alignment.Alignment(-1, -1),
            content=Column(
                controls=[
                    self.user_data("ОБАиП", "ст.лейтенант", "Бузин Денис"),
                    self.ConteinIcon(icon_name=icons.SATELLITE_ALT, text="Космические аппараты"),
                    self.ConteinIcon(icon_name=icons.ROCKET_SHARP, text="Ракет-носители"),
                    self.ConteinIcon(icon_name=icons.TRANSFORM, text="Орбитальная механика"),
                    self.ConteinIcon(icon_name=cupertino_icons.ROCKET_FILL, text="Иностранные полигоны"),
                    self.ConteinIcon(icon_name=icons.STAR, text="Характеристики средств СККП"),
                    self.ConteinIcon(icon_name=icons.ROCKET_SHARP, text="Ракет-носители"),
                    self.ConteinIcon(icon_name=cupertino_icons.ROCKET_FILL, text="Ракет-носители"),
                    Divider(height=5, color="GREY_300"),
                    self.ConteinIcon(icon_name=ft.icons.LOGIN_ROUNDED, text="Выход")
                ]
            )

        )
