from datetime import datetime
from exceptions import CampoObrigatorioException
import PySimpleGUI as sg


class AdocaoView:
    def __init__(self):
        self.__window = None
        self.init_components()

    def telar_opcoes(self):
        self.init_components()
        button, values = self.__window.read()

        if button == "incluir":
            opcao = 1
        elif button == "alterar":
            opcao = 2
        elif button == "listar":
            opcao = 3
        elif button == "excluir":
            opcao = 4
        elif button == "animais_disponiveis":
            opcao = 5
        elif button == "adocoes_periodo":
            opcao = 6
        else:
            opcao = 0
        self.__window.close()
        return opcao

    def init_components(self):
        layout = [
            [
                sg.Column(
                    [
                        [
                            sg.Text(
                                "Adocoes",
                                font=["Inter", 30, "bold"],
                                size=[20, 2],
                                justification="center",
                                pad=((0, 0), (25, 0)),
                                background_color="#3F3F3F",
                            )
                        ],
                    ],
                    justification="center",
                    background_color="#3F3F3F",
                )
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Button(
                                "Incluir",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="incluir",
                            )
                        ],
                        [
                            sg.Button(
                                "Alterar",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="alterar",
                            )
                        ],
                        [
                            sg.Button(
                                "Listar",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="listar",
                            )
                        ],
                        [
                            sg.Button(
                                "Excluir",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="excluir",
                            )
                        ],
                        [
                            sg.Button(
                                "Animais disponiveis para adocao",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="animais_disponiveis",
                            )
                        ],
                        [
                            sg.Button(
                                "Adocoes por periodo",
                                size=(20, 2),
                                font=("Inter", 13),
                                button_color=("black", "#FEFEFE"),
                                key="adocoes_periodo",
                            )
                        ],
                        [
                            sg.Button(
                                "Retornar",
                                size=(20, 2),
                                button_color=("black", "#FAF000"),
                                font=("Inter", 13),
                                key="retornar",
                            )
                        ],
                    ],
                    justification="center",
                    background_color="#3F3F3F",
                )
            ],
        ]
        self.__window = sg.Window(
            "Window Layout", layout, size=(500, 650), background_color="#3F3F3F", font=("Inter", 12)
        )

    def pegar_dados_adocao(self, adocao):
        if adocao:
            layout = [
                [sg.Text("ALTERAR ADOCAO", font=("Inter", 25), justification="center",
                         background_color="#3F3F3F", pad=15)],
                [sg.Text("Data de adocao:", size=(17, 1), background_color="#3F3F3F"),
                 sg.Input(adocao.data.strftime('%d/%m/%Y'), size=(26, 1), key="data"),
                 sg.CalendarButton("Abrir calendario", target="data", format="%d/%m/%Y",
                                   button_color=("white", "#2B2B2B"))],
                [self.termo_assinado_padrao(adocao.termo_assinado)],
                [sg.Column(
                    [
                        [
                            sg.Button(
                                "Confirmar",
                                key="confirmar",
                                font=("Inter", 12),
                                button_color=("white", "green"),
                            ),
                            sg.Cancel("Cancelar", key="cancelar", button_color="red", font=("Inter", 12)),
                        ],
                    ],
                    justification="right", background_color="#3F3F3F", pad=20
                ),
                ]
            ]
        else:
            layout = [
                [sg.Text("CADASTRO ADOCAO", font=("Inter", 25), justification="center",
                         background_color="#3F3F3F", pad=15)],
                [sg.Text("Data de adocao:", size=(12, 1), background_color="#3F3F3F"),
                 sg.Input("", size=(26, 1), key="data"),
                 sg.CalendarButton("Abrir calendario", target="data", format="%d/%m/%Y",
                                   button_color=("white", "#2B2B2B"))],
                [sg.Text("Assinar termo:", size=(12, 1), background_color="#3F3F3F"),
                 sg.Radio("Sim", "RD1", key="assinar", background_color="#3F3F3F"),
                 sg.Radio("Nao", "RD1", key="nao_assinar", background_color="#3F3F3F")],
                [sg.Column(
                    [
                        [
                            sg.Button(
                                "Confirmar",
                                key="confirmar",
                                font=("Inter", 12),
                                button_color=("white", "green"),
                            ),
                            sg.Cancel("Cancelar", key="cancelar", button_color="red", font=("Inter", 12)),
                        ],
                    ],
                    justification="right", background_color="#3F3F3F", pad=20
                ),
                ]
            ]

        self.__window = sg.Window("Layout", layout, background_color="#3F3F3F", font=("Inter", 12))

        while True:
            try:
                button, values = self.__window.read()
                if (button == "confirmar" and self.input_valido()) or button == "cancelar":
                    break
            except CampoObrigatorioException as e:
                self.mostrar_mensagem(e)

        self.__window.close()

        if button == "cancelar":
            return

        data_adocao_convertida = datetime.strptime(
            values["data"], "%d/%m/%Y"
        ).date()

        return {
            "data": data_adocao_convertida,
            "termo_assinado": True if values["assinar"] else False
        }

    def termo_assinado_padrao(self, termo_assinado):
        if termo_assinado:
            return [
                sg.Text("Assinar termo:", background_color="#3F3F3F"),
                sg.Radio("Sim", "RD1", default=True, key="assinar", background_color="#3F3F3F"),
                sg.Radio("Nao", "RD1", key="nao_assinar", background_color="#3F3F3F")
            ],
        return [
            sg.Text("Assinar termo:", background_color="#3F3F3F"),
            sg.Radio("Sim", "RD1", key="assinar", background_color="#3F3F3F"),
            sg.Radio("Nao", "RD1", default=True, key="nao_assinar", background_color="#3F3F3F")
        ],

    def pegar_dados_periodo(self):
        layout = [
            [sg.Text("Data de inicio:", size=(20, 1), background_color="#3F3F3F"),
             sg.Input("", size=(26, 1), key="data_inicio"),
             sg.CalendarButton("Abrir calendario", target="data_inicio", format="%d/%m/%Y",
                               button_color=("white", "#2B2B2B"))],
            [sg.Text("Data de fim:", size=(20, 1), background_color="#3F3F3F"),
             sg.Input("", size=(26, 1), key="data_fim"),
             sg.CalendarButton("Abrir calendario", target="data_fim", format="%d/%m/%Y",
                               button_color=("white", "#2B2B2B"))],
            [sg.Column(
                [
                    [
                        sg.Button(
                            "Confirmar",
                            key="confirmar",
                            font=("Inter", 12),
                            button_color=("white", "green"),
                        ),
                        sg.Cancel("Cancelar", key="cancelar", button_color="red", font=("Inter", 12)),
                    ],
                ],
                justification="right", background_color="#3F3F3F", pad=20
            ),
            ],
        ]

        self.__window = sg.Window("Layout", layout, background_color="#3F3F3F", font=("Inter", 12))
        while True:
            try:
                button, values = self.__window.read()

                if button == "cancelar":
                    self.__window.close()
                    return

                data_inicio_convertida = datetime.strptime(values["data_inicio"], "%d/%m/%Y").date()
                data_fim_convertida = datetime.strptime(values["data_fim"], "%d/%m/%Y").date()
                self.__window.close()
                return {"data_inicio": data_inicio_convertida, "data_fim": data_fim_convertida}
            except ValueError:
                self.mostrar_mensagem("ERRO: Data em formato invalido")

    def mostrar_adocao(self, adocao):
        output_adotante = f"\t - Adotante: {adocao.adotante.cpf}\n"
        output_adotante += f"\t - Animal: {adocao.animal.numero_chip}\n"
        output_adotante += f"\t - Data de adocao: {adocao.data.strftime('%d/%m/%Y')}\n"
        output_adotante += f"\t - Termo assinado: {'Sim' if adocao.termo_assinado else 'Nao'}\n"

        self.mostrar_mensagem(output_adotante)

    def mostrar_adocoes(self, adocoes: list):
        dados_adocoes = [
            [
                "{}.{}.{}-{}".format(
                    adocao.adotante.cpf[:3],
                    adocao.adotante.cpf[3:6],
                    adocao.adotante.cpf[6:9],
                    adocao.adotante.cpf[9:]
                ),
                adocao.animal.numero_chip,
                str(adocao.data.strftime('%d/%m/%Y')),
                "Sim" if adocao.termo_assinado else "Nao",
            ]
            for adocao in adocoes
        ]

        layout = self.layout_tabela_mostrar_adocoes(dados_adocoes)
        layout.append([sg.Button("Fechar", key="fechar", button_color="red")],)

        self.__window = sg.Window("Layout", layout, background_color="#3F3F3F", font=("Inter", 12))
        self.__window.read()
        self.__window.close()

    def layout_tabela_mostrar_adocoes(self, dados_adocoes: list):
        toprow = [
            "Adotante",
            "Animal",
            "Data adocao",
            "Termo assinado",
        ]

        return [
            [
                sg.Table(
                    headings=toprow,
                    values=dados_adocoes,
                    auto_size_columns=True,
                    expand_y=True,
                    expand_x=True,
                    justification="center",
                    display_row_numbers=True,
                    key="table",
                    background_color="#FEFEFE",
                    text_color="#000",
                    alternating_row_color="#BDBDBD",
                    selected_row_colors=("#FFF", "#2B2B2B"),
                    font=("Inter", 12),
                    sbar_background_color="#2B2B2B",
                    num_rows=10,
                )
            ],
        ]

    def selecionar_adocao(self, adocoes: list):
        dados_adocoes = [
            [
                "{}.{}.{}-{}".format(
                    adocao.adotante.cpf[:3],
                    adocao.adotante.cpf[3:6],
                    adocao.adotante.cpf[6:9],
                    adocao.adotante.cpf[9:]
                ),
                adocao.animal.numero_chip,
                str(adocao.data.strftime('%d/%m/%Y')),
                "Sim" if adocao.termo_assinado else "Nao",
            ]
            for adocao in adocoes
        ]
        layout = self.layout_tabela_mostrar_adocoes(dados_adocoes)

        layout.append([
            [sg.Text("Adocao que deseja selecionar: ", background_color="#3F3F3F")],
            [sg.Combo(values=[i for i in range(len(adocoes))],
                      default_value=0,
                      size=(22, 10),
                      font=("Inter", 14),
                      button_background_color="#2B2B2B",
                      pad=((15, 0), (0, 0)),
                      key="row")],
            [sg.Column(
                [
                    [
                        sg.Button(
                            "Confirmar",
                            key="confirmar",
                            font=("Inter", 12),
                            button_color=("white", "green")
                        ),
                        sg.Cancel("Cancelar", key="cancelar", button_color="red", font=("Inter", 12)),
                    ],
                ],
                justification="right", background_color="#3F3F3F", pad=15
            ),
            ],
        ])
        self.__window = sg.Window("Layout", layout, background_color="#3F3F3F", font=("Inter", 12))
        button, values = self.__window.read()
        print(values["row"])
        adocao = dados_adocoes[int(values["row"])]
        numero_chip = adocao[1]
        self.__window.close()

        if button == "cancelar":
            return

        return int(numero_chip)

    def mostrar_mensagem(self, msg: str):
        sg.popup("",
                 msg,
                 background_color="#3F3F3F",
                 button_color=("white", "red"),
                 font=("Inter", 13),
                 custom_text="Fechar")

    def input_valido(self):
        data_formato_valido = True
        campos_nao_preenchidos = []

        termo_assinado = self.__window["assinar"] or self.__window["nao assinar"]

        try:
            data_adocao = self.__window["data"].get().strip()
            datetime.strptime(data_adocao, "%d/%m/%Y").date()
        except ValueError:
            self.mostrar_mensagem("Data em formato invalido! Tente novamente.")
            data_formato_valido = False

        if not termo_assinado:
            campos_nao_preenchidos.append("Assinar termo")

        if len(campos_nao_preenchidos) > 0:
            raise CampoObrigatorioException(campos_nao_preenchidos)

        return data_formato_valido

