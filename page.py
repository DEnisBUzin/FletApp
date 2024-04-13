import flet as ft
from connect_db import UseDB
import config
import time
from cabinet import ModernNavBar, ContentCabinet

auth_flag = False


def main(page: ft.Page):
    global auth_flag
    page.title = "Добро пожаловать "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = 'dark'
    page.adaptive = True
    page.window_maximized = True

    connect = UseDB(user=config.USER, password=config.PASSWORD, name_db=config.NAME_DB)
    cab = ModernNavBar()
    content_cab = ContentCabinet()

    def theme_changed(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            dark_light_icon.icon = ft.icons.SUNNY
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            dark_light_icon.icon = ft.icons.BRIGHTNESS_2
        page.update()

    def out_auth(e):
        global auth_flag
        page.navigation_bar.destinations[1] = ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label="Авторизация")
        page.clean()
        close_drawer(e)
        page.appbar.title = ft.Text("Главный центр РКО")
        page.add(panel_auth)
        page.appbar.title=ft.Row(
            [
                ft.Image(src="logo.png", height=50, width=50),
                ft.Text("Добро пожаловать!"),
            ], alignment=ft.MainAxisAlignment.CENTER)
        page.navigation_bar.visible = True
        auth_flag = False
        page.update()

    def validate(e):
        """ Функция включения кнопок при наборе """
        if all([user_login.value, user_password.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True
        page.update()

    user_division = ft.TextField(label="Подразделение", width=200, on_change=validate)
    user_zvanie = ft.TextField(label="Звание", width=200, on_change=validate)
    user_surname = ft.TextField(label="Фамилия", width=200, on_change=validate)
    user_name = ft.TextField(label="Имя", width=200, on_change=validate)
    user_login = ft.TextField(label="Логин", width=200, on_change=validate)
    user_password = ft.TextField(label="Пароль", password=True, width=200, on_change=validate)
    admin_password = ft.TextField(label="Код администратора", password=True, width=200, on_change=validate)

    panel_cabinet = ft.Row([
            ft.Text("Раздел в разработке")
    ], alignment=ft.MainAxisAlignment.CENTER)

    def auth_user(e):
        global auth_flag
        """Функция авторизации"""
        answer = connect.auth_user(login=user_login.value, password=user_password.value)
        if answer is not None:
            auth_flag = True
            page.navigation_bar.visible = False
            open_drawer(e,
                        connect.auth_user(login=user_login.value, password=user_password.value)[3],
                        connect.auth_user(login=user_login.value, password=user_password.value)[6],
                        connect.auth_user(login=user_login.value, password=user_password.value)[4],
                        connect.auth_user(login=user_login.value, password=user_password.value)[5])
            user_login.value = ''
            user_password.value = ''
            page.appbar.title = ft.Row(
            [
                ft.Image(src="logo.png", height=50, width=50),
                ft.Text("Главный центр РКО")
            ], alignment=ft.MainAxisAlignment.CENTER)
            page.clean()
            page.add(panel_cabinet)
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Аутентификация не пройдена!"))
            page.snack_bar.open = True
            page.update()

    def navigate_drawer(e):
        index = e.control.selected_index
        page.clean()
        if index == 0:
            page.add(content_cab.satellite_pindosov())
        else:
            page.add(panel_cabinet)

    def open_drawer(e, division, zvanie, name, surname):
        drawer = ft.NavigationDrawer(
            indicator_shape=None,
            open=True,
            selected_index=0,
            on_change=navigate_drawer,
            visible=True,
            controls=[
                cab.user_data(division, zvanie, name, surname),
                ft.NavigationDrawerDestination(label="КСВН", icon=ft.icons.SATELLITE_ALT),
                ft.NavigationDrawerDestination(icon=ft.icons.ROCKET_SHARP, label="Ракет-носители"),
                ft.NavigationDrawerDestination(icon=ft.icons.TRANSFORM, label="Орбитальная механика"),
                ft.NavigationDrawerDestination(icon=ft.cupertino_icons.ROCKET_FILL, label="Иностранные полигоны"),
                ft.NavigationDrawerDestination(icon=ft.icons.STAR, label="Характеристики средств СККП"),
                ft.NavigationDrawerDestination(icon=ft.icons.WARNING, label="Обзор контролей"),
                ft.NavigationDrawerDestination(icon=ft.cupertino_icons.BOOK, label="Руководящие документы"),
                ft.Divider(height=5, color="GREY_300"),
                cab.ConteinIcon(icon_name=ft.icons.LOGIN_ROUNDED, text="Выход", click=out_auth)
            ],
        )
        page.drawer = drawer
        page.update()

    def close_drawer(e):
        page.drawer.visible = False
        page.update()

    # Верхний бар
    dark_light_icon = ft.IconButton(
        icon=ft.icons.SUNNY,
        on_click=theme_changed
    )

    page.appbar = ft.AppBar(
        title=ft.Row(
            [
                ft.Image(src="logo.png", height=50, width=50),
                ft.Text("Добро пожаловать!")
            ], alignment=ft.MainAxisAlignment.CENTER),
        actions=[
            dark_light_icon
        ],
        bgcolor=ft.colors.with_opacity(0.04, ft.cupertino_colors.SYSTEM_BACKGROUND)
    )

    def register(e):
        """Функция регистрации"""
        connect.create_structure()
        if admin_password.value == config.ADMIN_PASSWORD:
            connect.add_new_user(user_login.value,
                                 user_password.value,
                                 user_division.value,
                                 user_name.value,
                                 user_surname.value,
                                 user_zvanie.value)
            user_login.value = ''
            user_password.value = ''
            user_division.value = ''
            user_name.value = ''
            user_surname.value = ''
            user_zvanie.value = ''
            admin_password.value = ''
            btn_reg.text = 'Добавлено'
            page.update()
            time.sleep(1)
            btn_reg.text = 'Добавить'
            page.update()
        else:
            user_login.value = ''
            user_password.value = ''
            user_division.value = ''
            user_name.value = ''
            user_surname.value = ''
            user_zvanie.value = ''
            admin_password.value = ''
            page.snack_bar = ft.SnackBar(ft.Text("Код администратора не верный!"))
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
                user_division,
                user_zvanie,
                user_surname,
                user_name,
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

    page.add(panel_auth)


ft.app(main)
