import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class SimuladorMemoria(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simulador de Gerenciamento de Memória")
        self.geometry("1200x700")
        self.resizable(False, False)

        self.tabs = ctk.CTkTabview(self, width=1100, height=650, corner_radius=15)
        self.tabs.pack(pady=20)
        self.overlay_tab = self.tabs.add("Overlay")
        self.paginacao_tab = self.tabs.add("Paginação")
        self.segmentacao_tab = self.tabs.add("Segmentação")
        self.fragmentacao_tab = self.tabs.add("Fragmentação")

        self.init_overlay()
        self.init_paginacao()
        self.init_segmentacao()
        self.init_fragmentacao()

    # ------------- ABA OVERLAY ------------------
    def init_overlay(self):
        self.subrotinas_ativas = {}
        self.subrotinas_fila = []
        self.subrotinas_concluidas = []
        self.labels_tempo = {}

        self.memoria_frame = ctk.CTkFrame(self.overlay_tab, width=1000, height=150, fg_color="#4E4E4E", corner_radius=10)
        self.memoria_frame.pack(pady=20)

        botoes_frame = ctk.CTkFrame(self.overlay_tab, fg_color="transparent")
        botoes_frame.pack(pady=10)

        self.iniciar_btn = ctk.CTkButton(botoes_frame, text="Iniciar", command=self.iniciar_overlay)
        self.iniciar_btn.grid(row=0, column=0, padx=10)

        self.parar_btn = ctk.CTkButton(botoes_frame, text="Parar", command=self.parar_overlay)
        self.parar_btn.grid(row=0, column=1, padx=10)

        self.ativas_label = ctk.CTkLabel(self.overlay_tab, text="Ativas:\n", anchor="w")
        self.ativas_label.pack(pady=10)

        self.fila_label = ctk.CTkLabel(self.overlay_tab, text="Fila:\n", anchor="w")
        self.fila_label.pack(pady=10)

        self.concluidas_label = ctk.CTkLabel(self.overlay_tab, text="Concluídas:\n", anchor="w")
        self.concluidas_label.pack(pady=10)

        self.configurar_subrotinas_overlay()
        self.atualizar_labels_overlay()

    def configurar_subrotinas_overlay(self):
        self.fila_subrotinas = [f"Subrotina {i + 1}" for i in range(15)]
        self.tempo_execucao = {sub: random.randint(5000, 15000) for sub in self.fila_subrotinas}
        self.subrotinas_concluidas.clear()
        self.subrotinas_ativas.clear()
        self.labels_tempo.clear()

    def iniciar_overlay(self):
        self.parar_overlay()
        self.configurar_subrotinas_overlay()
        self.iniciar_subrotinas_overlay()

    def parar_overlay(self):
        for widget in self.memoria_frame.winfo_children():
            widget.destroy()
        self.subrotinas_concluidas.clear()
        self.subrotinas_ativas.clear()
        self.labels_tempo.clear()

    def iniciar_subrotinas_overlay(self):
        rotina_principal = ctk.CTkFrame(self.memoria_frame, fg_color="#A8DADC", width=150)
        rotina_principal.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        ctk.CTkLabel(rotina_principal, text="Rotina Principal").pack(expand=True)

        for i in range(5):
            if self.fila_subrotinas:
                self.executar_subrotina_overlay(self.fila_subrotinas.pop(0), i)

    def executar_subrotina_overlay(self, subrotina, index):
        cor = random.choice(["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF"])
        frame = ctk.CTkFrame(self.memoria_frame, fg_color=cor)
        frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(frame, text=subrotina, text_color="black").pack()
        tempo_restante = self.tempo_execucao[subrotina] / 1000.0
        tempo_label = ctk.CTkLabel(frame, text=f"{tempo_restante:.1f}s", text_color="black")
        tempo_label.pack()
        self.labels_tempo[subrotina] = tempo_label
        self.subrotinas_ativas[index] = subrotina

        def atualizar_tempo():
            nonlocal tempo_restante
            if tempo_restante > 0:
                tempo_restante -= 0.1
                self.labels_tempo[subrotina].configure(text=f"{tempo_restante:.1f}s")
                self.after(100, atualizar_tempo)
            else:
                frame.destroy()
                self.subrotinas_concluidas.append(subrotina)
                del self.subrotinas_ativas[index]
                if self.fila_subrotinas:
                    nova = self.fila_subrotinas.pop(0)
                    self.executar_subrotina_overlay(nova, index)
        self.after(100, atualizar_tempo)

    def atualizar_labels_overlay(self):
        self.ativas_label.configure(text=f"Ativas:\n" + "\n".join(self.subrotinas_ativas.values()))
        self.fila_label.configure(text=f"Fila:\n" + "\n".join(self.fila_subrotinas[:10]))
        self.concluidas_label.configure(text=f"Concluídas:\n" + "\n".join(self.subrotinas_concluidas))
        self.after(500, self.atualizar_labels_overlay)

    # ------------- ABA PAGINAÇÃO ------------------
    def init_paginacao(self):
        self.pagina_labels = []  # Inicializa a lista de labels

        self.label_titulo = ctk.CTkLabel(self.paginacao_tab, text="Simulação de Paginação", font=("Arial", 20))
        self.label_titulo.pack(pady=(20, 10))

        # Botão acima do frame de páginas
        self.botao_gerar_paginas = ctk.CTkButton(
            self.paginacao_tab,
            text="Gerar Paginação",
            command=self.criar_paginas,
            fg_color="#3498DB",
            corner_radius=10,
            width=220,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.botao_gerar_paginas.pack(pady=(10, 20))

        # Frame que vai receber os blocos de memória
        self.frame_paginas = ctk.CTkFrame(self.paginacao_tab, width=1000, height=500, fg_color="#5A5A5A", corner_radius=10)
        self.frame_paginas.pack()



    def criar_paginas(self):
        for widget in self.frame_paginas.winfo_children():
            widget.destroy()
        self.pagina_labels.clear()

        processos = [f"P{i}" for i in range(1, 11)]
        cores = {
            "P1": "#FFADAD", "P2": "#FFD6A5", "P3": "#FDFFB6", "P4": "#CAFFBF", "P5": "#9BF6FF",
            "P6": "#A0C4FF", "P7": "#BDB2FF", "P8": "#FFC6FF", "P9": "#FFFFFC", "P10": "#C8E6C9"
        }

        total_frames = 20
        rows = 4
        cols = 5

        for i in range(total_frames):
            frame_mem = ctk.CTkFrame(self.frame_paginas, width=130, height=90, fg_color="#D5D8DC", corner_radius=10)
            frame_mem.grid(row=i // cols, column=i % cols, padx=10, pady=10)

            if i < len(processos):
                processo = processos[i]
                pagina_num = random.randint(0, 5)
                cor = cores[processo]

                inner = ctk.CTkFrame(frame_mem, width=120, height=80, fg_color=cor, corner_radius=8)
                inner.pack(expand=True, fill="both", padx=5, pady=5)

                label = ctk.CTkLabel(inner, text=f"{processo}\nPag {pagina_num}", text_color="black", font=("Arial", 14))
                label.pack(expand=True)

                self.pagina_labels.append(label)
            else:
                label_vazio = ctk.CTkLabel(frame_mem, text="Livre", text_color="#7B7D7D", font=("Arial", 13))
                label_vazio.pack(expand=True)

    def init_segmentacao(self):
        self.label_segmentacao = ctk.CTkLabel(self.segmentacao_tab, text="Simulação de Segmentação", font=("Arial", 20))
        self.label_segmentacao.pack()

        self.botao_segmentar = ctk.CTkButton(
            self.segmentacao_tab,
            text="Gerar Segmentação",
            command=self.criar_segmentacao,
            fg_color="#27AE60",
            corner_radius=10,
            width=220,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.botao_segmentar.pack(pady=(10, 20))

        self.frame_segmentos = ctk.CTkFrame(self.segmentacao_tab, width=1400, height=350, fg_color="#5A5A5A", corner_radius=10)
        self.frame_segmentos.pack(pady=20)

    def criar_segmentacao(self):
        for widget in self.frame_segmentos.winfo_children():
            widget.destroy()

        segmentos = ["Código", "Dados", "Heap", "Pilha"]
        cores = ["#74b9ff", "#55efc4", "#ffeaa7", "#fab1a0"]
        usos = [random.randint(50, 400) for _ in segmentos]
        total = sum(usos)
        proporcoes = [int((uso / total) * 1300) for uso in usos]  # mais largura disponível

        for nome, cor, largura, uso in zip(segmentos, cores, proporcoes, usos):
            seg = ctk.CTkFrame(self.frame_segmentos, height=300, width=largura, fg_color=cor, corner_radius=15)
            seg.pack(side="left", padx=10, pady=15)
            ctk.CTkLabel(seg, text=f"{nome}\n{uso}MB", text_color="black", font=("Arial", 16)).pack(expand=True)


    def init_fragmentacao(self):
        self.frame_fragmentos = ctk.CTkFrame(self.fragmentacao_tab, width=1000, height=500, fg_color="#5A5A5A", corner_radius=10)
        self.frame_fragmentos.pack(pady=20)

        self.botao_fragmentar = ctk.CTkButton(
            self.fragmentacao_tab,
            text="Gerar Fragmentação",
            command=self.criar_fragmentacao,
            fg_color="#E67E22",
            width=220,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.botao_fragmentar.pack(pady=(10, 20))

    def criar_fragmentacao(self):
        for widget in self.frame_fragmentos.winfo_children():
            widget.destroy()

        memoria = []
        usado = 0
        for i in range(6):  # 6 processos ocupam memória
            tamanho = random.randint(80, 150)
            memoria.append(("Processo", tamanho))
            usado += tamanho
            if usado < 1000:
                fragmento = random.randint(10, 40)
                memoria.append(("Livre", fragmento))
                usado += fragmento

        for i, (tipo, tamanho) in enumerate(memoria):
            cor = "#85C1E9" if tipo == "Processo" else "#F1948A"
            frame = ctk.CTkFrame(self.frame_fragmentos, width=tamanho, height=60, fg_color=cor, corner_radius=6)
            frame.pack(side="left", padx=3, pady=10)

            texto = f"{tipo}\n{tamanho}KB"
            label = ctk.CTkLabel(frame, text=texto, text_color="black", font=("Arial", 11))
            label.pack(expand=True)


if __name__ == "__main__":
    app = SimuladorMemoria()
    app.mainloop()