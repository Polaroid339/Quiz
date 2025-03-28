import flet as ft
import time
from perguntas import perguntas_facil, perguntas_normal, perguntas_dificil


def main(page: ft.Page):
    page.title = "Quiz Game"

    page.window.width = 700
    page.window.height = 770
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE


    # Perguntas do quiz
    perguntas = perguntas_normal

    indice = 0
    score = 0
    dificuldade_texto = ft.Text(
        value="Dificuldade: Normal",
        size=25,
        color=ft.Colors.BLUE,
        weight=ft.FontWeight.BOLD
    )

    imagem = ft.Image(
        src=perguntas[indice]["imagem"],
        width=300,
        height=200
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
    
    imagem_final = ft.Image(
        src="https://www.cearasc.com/media/img/noticias/daronco_2.jpg",
        width=400,
        height=400,
        visible=False
    )

    indice_texto = ft.TextField(
        value=f"Pergunta {indice + 1}/{len(perguntas)}",
        read_only=True,
        width=150,
        height=50,
        text_size=18,
        text_align=ft.TextAlign.CENTER,
        border_width=2,
        border_color=ft.Colors.BLUE,
        border_radius=20,
        text_style={"color": ft.Colors.BLUE, "weight": ft.FontWeight.BOLD},
    )

    indice_score = ft.TextField(
        value=f"Score: {score}",
        read_only=True,
        width=150,
        height=50,
        text_size=18,
        text_align=ft.TextAlign.CENTER,
        border_width=2,
        border_color=ft.Colors.BLUE,
        border_radius=20,
        text_style={"color": ft.Colors.BLUE, "weight": ft.FontWeight.BOLD}
    )

    botoes = []

    def verificar_resposta(e):
        nonlocal indice, score

        for botao in botoes:
            botao.disabled = True

        if e.control.text == perguntas[indice]["resposta"]:
            score += 1
            e.control.style = ft.ButtonStyle(
                side=ft.BorderSide(6, ft.colors.LIGHT_GREEN))
            resultado_texto.value = "Resposta Certa!"
            resultado_texto.color = ft.Colors.GREEN
        else:
            e.control.style = ft.ButtonStyle(
                side=ft.BorderSide(6, ft.colors.RED_900))
            resultado_texto.value = "Resposta Errada!"
            resultado_texto.color = ft.Colors.RED_900

            for botao in botoes:
                if botao.text == perguntas[indice]["resposta"]:
                    botao.style = ft.ButtonStyle(
                        side=ft.BorderSide(6, ft.colors.LIGHT_GREEN))

        indice_score.value = f"Score: {score}"
        page.update()
        time.sleep(2)
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
        imagem_final.visible = False
        
        for botao in botoes:
            botao.disabled = False

        indice += 1
        if indice < len(perguntas):
            imagem.src = perguntas[indice]["imagem"]
            pergunta_texto.value = perguntas[indice]["pergunta"]
            indice_texto.value = f"Pergunta {indice + 1}/{len(perguntas)}"
            for i, botao in enumerate(botoes):
                botao.text = perguntas[indice]["alternativas"][i]
                botao.bgcolor = ft.Colors.WHITE
                botao.style = ft.ButtonStyle(
                    side=ft.BorderSide(2, ft.colors.LIGHT_BLUE))
        else:
            pergunta_texto.value = f"Fim do jogo! Pontuação: {score} certas de {len(perguntas)}"
            imagem.visible = False
            imagem_final.visible = True
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
                    dificuldade_texto,
                    indice_score
                ],
                ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Column(
                [
                    ft.Container(height=5),
                    imagem,
                    ft.Container(height=5),
                    pergunta_texto,
                    ft.Container(height=10),
                    imagem_final,
                    *botoes
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            
            ft.Container(height=15),
            ft.Row([
                ft.ElevatedButton(
                    text="Reiniciar",
                    on_click=reiniciar,
                    icon=ft.Icons.REFRESH,
                    height=50,
                    width=150,
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE,
                    elevation=4),

                resultado_texto,
                
                ft.ElevatedButton(
                    text="Voltar ao Menu",
                    on_click=voltar_ao_menu,
                    icon=ft.Icons.ARROW_BACK,
                    height=50,
                    width=150,
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE,
                    elevation=4)
            ],
                ft.MainAxisAlignment.SPACE_BETWEEN)
        )
        proxima_pergunta()

    def dificuldade_facil(e=None):
        nonlocal perguntas, indice, score
        indice = -1
        score = 0
        perguntas = perguntas_facil
        dificuldade_texto.value = "Dificuldade: Fácil"
        game(e)

    def dificuldade_normal(e=None):
        nonlocal perguntas, indice, score
        indice = -1
        score = 0
        perguntas = perguntas_normal
        dificuldade_texto.value = "Dificuldade: Normal"
        game(e)

    def dificuldade_dificil(e=None):
        nonlocal perguntas, indice, score
        indice = -1
        score = 0
        perguntas = perguntas_dificil
        dificuldade_texto.value = "Dificuldade: Diffícil"
        game(e)

    def tela_inicial(e=None):
        page.clean()
        page.update()
        page.add(
            ft.Column(
                [
                    ft.Container(height=20),
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
                    ft.Image(
                        src="https://www.spotsound.fr/120315-home_default/gigante-mascote-bola-de-futebol-preto-e-branco.jpg",
                        width=300,
                        height=300
                    ),

                    ft.Container(height=15),
                    ft.ElevatedButton(
                        text="Dificuldade Fácil",
                        on_click=dificuldade_facil,
                        height=50,
                        width=200,
                        bgcolor=ft.Colors.GREEN,
                        color=ft.Colors.WHITE,
                        elevation=4),

                    ft.ElevatedButton(
                        text="Dificuldade Normal",
                        on_click=dificuldade_normal,
                        height=50,
                        width=200,
                        bgcolor=ft.Colors.ORANGE,
                        color=ft.Colors.WHITE,
                        elevation=4),

                    ft.ElevatedButton(
                        text="Dificuldade Difícil",
                        on_click=dificuldade_dificil,
                        height=50,
                        width=200,
                        bgcolor=ft.Colors.RED,
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
