import flet as ft
import time
from perguntas import perguntas_normais

def main(page: ft.Page):
    page.title = "Quiz Game"

    page.window.width = 1100
    page.window.height = 870
    page.window.maximizable = False
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.CYAN_ACCENT_200

    # Perguntas do quiz
    perguntas = perguntas_normais

    indice = 0
    score = 0

    imagem = ft.Image(
        src=perguntas[indice]["imagem"],
        width=350,
        height=250
    )

    pergunta_texto = ft.Text(
        perguntas[indice]["pergunta"],
        size=20
    )

    resultado_texto = ft.Text(
        "",
        size=18,
        color=ft.Colors.GREEN,
        weight=ft.FontWeight.BOLD
    )

    indice_texto = ft.TextField(
        value=f"Pergunta {indice + 1}/{len(perguntas)}",
        read_only=True,
        width=150,
        height=50,
        text_size=18,
        text_align=ft.TextAlign.CENTER,
        border_width=2,
        border_color=ft.Colors.WHITE,
        border_radius=20,
        text_style={"color": ft.Colors.WHITE, "weight": ft.FontWeight.BOLD},
    )

    indice_score = ft.TextField(
        value=f"Score: {score}",
        read_only=True,
        width=150,
        height=50,
        text_size=18,
        text_align=ft.TextAlign.CENTER,
        border_width=2,
        border_color=ft.Colors.WHITE,
        border_radius=20,
        text_style={"color": ft.Colors.WHITE, "weight": ft.FontWeight.BOLD}
    )

    botoes = []

    def verificar_resposta(e):
        nonlocal indice, score
        if e.control.text == perguntas[indice]["resposta"]:
            score += 1
            resultado_texto.value = "Resposta Certa!"
            resultado_texto.color = ft.Colors.YELLOW
        else:
            resultado_texto.value = "Resposta Errada!"
            resultado_texto.color = ft.Colors.RED_900

        indice_score.value = f"Score: {score}"
        page.update()
        time.sleep(1.5)
        proxima_pergunta()

    def reiniciar(e):
        nonlocal indice, score
        indice = -1
        score = 0
        imagem.visible = True
        for botao in botoes:
            botao.visible = True

        indice_score.value = f"Score: {score}"
        proxima_pergunta()
        page.update()

    def proxima_pergunta():
        nonlocal indice
        indice += 1
        if indice < len(perguntas):
            imagem.src = perguntas[indice]["imagem"]
            pergunta_texto.value = perguntas[indice]["pergunta"]
            indice_texto.value = f"Pergunta {indice + 1}/{len(perguntas)}"
            for i, botao in enumerate(botoes):
                botao.text = perguntas[indice]["alternativas"][i]
        else:
            pergunta_texto.value = f"Fim do jogo! Pontuação: {score} certas de {len(perguntas)}"
            imagem.visible = False
            for botao in botoes:
                botao.visible = False

        resultado_texto.value = ""
        page.update()

    for alternativa in perguntas[indice]["alternativas"]:
        botao = ft.ElevatedButton(
            text=alternativa, on_click=verificar_resposta,
            height=50,
            width=300,
            elevation=4)
        botoes.append(botao)

    def game(e):
        page.controls.clear()
        page.update()
        page.add(
            ft.Row(
                [
                    indice_texto,
                    indice_score
                ],
                ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Column(
                [
                    ft.Container(height=10),
                    imagem,
                    ft.Container(height=5),
                    pergunta_texto,
                    ft.Container(height=15),
                    *botoes,
                    ft.Container(height=4),
                    resultado_texto,
                    ft.Container(height=4)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Row([
                ft.ElevatedButton(
                    text="Reiniciar",
                    on_click=reiniciar,
                    height=50,
                    width=150,
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE,
                    elevation=4),

                ft.ElevatedButton(
                    text="Voltar ao Menu",
                    on_click=voltar_ao_menu,
                    height=50,
                    width=150,
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE,
                    elevation=4)
                ],
                ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )

    def tela_inicial(e=None):
        page.clean()
        page.update()
        page.add(
            ft.Column(
                [
                    ft.Container(height=50),
                    ft.Text(
                        "Bem-vindo ao Quiz Game!",
                        size=30,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(
                        "Responda as perguntas e veja quantas você acerta!",
                        size=20
                    ),
                    ft.Container(height=30),
                    ft.ElevatedButton(
                        text="Começar",
                        on_click=game,
                        height=50,
                        width=150,
                        bgcolor=ft.Colors.GREEN,
                        color=ft.Colors.WHITE,
                        elevation=4)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def voltar_ao_menu(e):
        nonlocal indice, score
        indice = 0
        score = 0
        imagem.src = perguntas[indice]["imagem"]
        pergunta_texto.value = perguntas[indice]["pergunta"]
        indice_texto.value = f"Pergunta {indice + 1}/{len(perguntas)}"
        indice_score.value = f"Score: {score}"
        for i, botao in enumerate(botoes):
            botao.text = perguntas[indice]["alternativas"][i]
            botao.visible = True
        imagem.visible = True
        resultado_texto.value = ""
        tela_inicial()

    tela_inicial()
    page.update()

ft.app(target=main)