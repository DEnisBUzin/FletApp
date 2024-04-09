import flet as ft
from connect_db import UseDB
import config
import time

auth_flag = False


def main(page: ft.Page):
    page.title = "Добро пожаловать "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = 'dark'

    connect = UseDB(user=config.USER, password=config.PASSWORD, name_db=config.NAME_DB)

    def theme_changed(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            dark_light_icon.icon = ft.icons.SUNNY
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            dark_light_icon.icon = ft.icons.BRIGHTNESS_2
        page.update()

    # Верхний бар
    dark_light_icon = ft.IconButton(
        icon=ft.icons.SUNNY,
        on_click=theme_changed
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Главный центр РКО"),
        actions=[
            dark_light_icon
        ],
        bgcolor=ft.colors.with_opacity(0.04, ft.cupertino_colors.SYSTEM_BACKGROUND)
    )

    def validate(e):
        """ Функция включения кнопок при наборе """
        if all([user_login.value, user_password.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True
        page.update()

    user_email = ft.TextField(label="Подразделение", width=200, on_change=validate)
    user_login = ft.TextField(label="Введите логин", width=200, on_change=validate)
    user_password = ft.TextField(label="Введите пароль", password=True, width=200, on_change=validate)
    admin_password = ft.TextField(label="Код администратора", password=True, width=200, on_change=validate)

    def register(e):
        """Функция регистрации"""
        connect.create_structure()
        if admin_password.value == config.ADMIN_PASSWORD:
            connect.add_new_user(user_login.value, user_password.value, user_email.value)
            user_login.value = ''
            user_password.value = ''
            user_email.value = ''
            btn_reg.text = 'Добавлено'
            page.update()
            time.sleep(2)
            btn_reg.text = 'Добавить'
            page.update()
        else:
            user_login.value = ''
            user_password.value = ''
            user_email.value = ''
            admin_password.value = ''
            page.snack_bar = ft.SnackBar(ft.Text("Код администратора не верный!"))
            page.snack_bar.open = True
            page.update()

    def auth_user(e):
        global auth_flag
        """Функция авторизации"""
        answer = connect.auth_user(login=user_login.value, password=user_password.value)
        if answer is not None:
            auth_flag = True
            page.navigation_bar.destinations[1] = ft.NavigationDestination(icon=ft.cupertino_icons.STAR,
                                                                           label="Личный кабинет",
                                                                           selected_icon=ft.icons.STAR_ROUNDED)
            user_login.value = ''
            user_password.value = ''
            page.appbar.title = ft.Text("Личный кабинет")
            page.clean()
            page.add(panel_cabinet)
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Аутентификация не пройдена!"))
            page.snack_bar.open = True
            page.update()

    # Кнопки
    btn_reg = ft.OutlinedButton(text="Добавить", width=200, height=50, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton(text="Авторизовать", width=200, height=50, on_click=auth_user, disabled=True)

    # Вкладка Регистрации
    panel_reg = ft.Row([
        ft.Column(
            [
                ft.Text("Регистрация"),
                user_email,
                user_login,
                user_password,
                admin_password,
                btn_reg
            ]
        ),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Вкладка Авторизации
    panel_auth = ft.Row([
        ft.Column(
            [
                ft.Text("Авторизация"),
                user_login,
                user_password,
                btn_auth
            ]
        ),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Вкладка Личный кабинет
    panel_cabinet = ft.Row([
        ft.Column(
            [
                ft.Text("Личный кабинет"),
                ft.Container()
            ]
        ),
    ], alignment=ft.MainAxisAlignment.CENTER)

    def cabinet(e):
        pass

    def navigate(e):
        global auth_flag
        """Функция для отображения нижнего бара"""
        index = page.navigation_bar.selected_index
        page.clean()
        if index == 0:
            page.add(panel_reg)
        elif index == 1:
            if auth_flag:
                page.add(panel_cabinet)
                auth_flag = True
            else:
                page.add(panel_auth)

    # Нижний бар
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.APP_REGISTRATION, label="Регистрация"),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label="Авторизация")
        ], on_change=navigate
    )

    page.add(panel_reg)


ft.app(main)
