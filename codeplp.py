from kivy.app import App
# ... demais imports do kivy ...

import mysql.connector  # <-- adiciona aqui

# ─── Conexão MySQL ────────────────────────────────────────────────────────────
conn = mysql.connector.connect(
    user='root',
    password='whyblu3',
    host='localhost',
    port='3306',
    database='estoque_discos'
)
cursor = conn.cursor()

# ─── Funções do banco (substitui os stubs) ────────────────────────────────────
def adicionar_produto(nome, artista, genero, quantidade, preco):
    cursor.execute("""
        INSERT INTO produtos (nome, artista, genero, quantidade, preco)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, artista, genero, quantidade, preco))
    conn.commit()

def vender_produto(nome, quantidade):
    cursor.execute("""
        UPDATE produtos
        SET quantidade = quantidade - %s
        WHERE nome = %s AND quantidade >= %s
    """, (quantidade, nome, quantidade))
    conn.commit()
    if cursor.rowcount == 0:
        raise ValueError("Estoque insuficiente ou produto não encontrado.")

def alterar_produto(id_produto, novo_nome, nova_quantidade, novo_preco):
    cursor.execute("""
        UPDATE produtos
        SET nome = %s, quantidade = %s, preco = %s
        WHERE id_produto = %s
    """, (novo_nome, nova_quantidade, novo_preco, id_produto))
    conn.commit()
    if cursor.rowcount == 0:
        raise ValueError("Produto não encontrado.")
        
# Interface gráfica

"""
Controle de Estoque - Galeria do Metal
Interface gráfica em Kivy
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.popup import Popup

# ─── Paleta ───────────────────────────────────────────────────────────────────
AZUL        = (0.012, 0.580, 0.988, 1)   # #0394fc
PRETO       = (0.05,  0.05,  0.05,  1)   # fundo escuro
CINZA_ESCURO= (0.13,  0.13,  0.13,  1)
CINZA_MEDIO = (0.22,  0.22,  0.22,  1)
BRANCO      = (1,     1,     1,     1)
VERMELHO    = (0.851, 0.137, 0.086, 1)   # #d92316
VERDE       = (0.188, 0.851, 0.153, 1)   # #30d927
AMARELO     = (1,     0.8,   0,     1)

Window.clearcolor = PRETO
Window.size = (1100, 660)
Window.minimum_width  = 900
Window.minimum_height = 580

# ─── Funções de negócio (conecte ao seu banco aqui) ───────────────────────────
def adicionar_produto(nome, artista, genero, quantidade, preco):
    print(f"[ADD] {nome} | {artista} | {genero} | {quantidade} | R${preco:.2f}")

def vender_produto(nome, quantidade):
    print(f"[SELL] {nome} x{quantidade}")

def alterar_produto(id_produto, nome, quantidade, preco):
    print(f"[UPD] ID={id_produto} | {nome} | x{quantidade} | R${preco:.2f}")

# ─── Widgets auxiliares ───────────────────────────────────────────────────────
class Separator(Widget):
    def __init__(self, color=AZUL, height=dp(2), **kw):
        super().__init__(size_hint_y=None, height=height, **kw)
        with self.canvas:
            Color(*color)
            self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *_):
        self._rect.pos  = self.pos
        self._rect.size = self.size


class StyledInput(TextInput):
    def __init__(self, **kw):
        super().__init__(
            multiline=False,
            size_hint_y=None,
            height=dp(38),
            background_color=CINZA_MEDIO,
            foreground_color=BRANCO,
            cursor_color=AZUL,
            hint_text_color=(0.5, 0.5, 0.5, 1),
            font_size=dp(14),
            padding=[dp(10), dp(8)],
            **kw,
        )


class StyledButton(Button):
    def __init__(self, bg=AZUL, **kw):
        super().__init__(
            size_hint_y=None,
            height=dp(42),
            font_size=dp(13),
            bold=True,
            background_normal="",
            background_color=bg,
            color=BRANCO,
            **kw,
        )


def popup_msg(titulo, msg, cor=AZUL):
    content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
    content.add_widget(Label(text=msg, color=BRANCO, font_size=dp(14), halign="center"))
    btn = Button(
        text="OK", size_hint_y=None, height=dp(40),
        background_normal="", background_color=cor,
    )
    content.add_widget(btn)
    pop = Popup(
        title=titulo, content=content,
        size_hint=(None, None), size=(dp(340), dp(180)),
        background_color=(*CINZA_ESCURO[:3], 1),
        title_color=BRANCO,
    )
    btn.bind(on_release=pop.dismiss)
    pop.open()

# ─── Painel esquerdo (formulário) ─────────────────────────────────────────────
class FormPanel(BoxLayout):
    def __init__(self, log_callback=None, **kw):
        super().__init__(
            orientation="vertical",
            size_hint=(None, 1),
            width=dp(310),
            padding=dp(16),
            spacing=dp(6),
            **kw,
        )
        self.log = log_callback or (lambda m, c=BRANCO: None)

        with self.canvas.before:
            Color(*CINZA_ESCURO)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd, size=self._upd)

        # ── Cabeçalho ──
        hdr = BoxLayout(size_hint_y=None, height=dp(56))
        with hdr.canvas.before:
            Color(*AZUL)
            self._hdr_bg = Rectangle(pos=hdr.pos, size=hdr.size)
        hdr.bind(pos=lambda *_: setattr(self._hdr_bg, "pos",  hdr.pos),
                 size=lambda *_: setattr(self._hdr_bg, "size", hdr.size))
        hdr.add_widget(Label(
            text="⬡  Controle de Estoque",
            color=BRANCO, bold=True, font_size=dp(15),
            halign="left", padding_x=dp(12),
        ))
        self.add_widget(hdr)
        self.add_widget(Separator())

        # ── Campos ──
        fields = [
            ("Nome do álbum",  "Digite o título",   "nome"),
            ("Artista",        "Ex: Metallica",      "artista"),
            ("Gênero",         "Ex: Thrash Metal",   "genero"),
            ("Quantidade",     "Ex: 10",             "quantidade"),
            ("Preço (R$)",     "Ex: 49.90",          "preco"),
            ("ID do Produto",  "Para alterar/vender","id"),
        ]
        self._entries = {}
        for label_txt, hint, key in fields:
            self.add_widget(Label(
                text=label_txt, color=(0.7, 0.85, 1, 1),
                font_size=dp(12), bold=True,
                size_hint_y=None, height=dp(22),
                halign="left", text_size=(dp(278), None),
            ))
            inp = StyledInput(hint_text=hint)
            self._entries[key] = inp
            self.add_widget(inp)

        self.add_widget(Separator(color=CINZA_MEDIO, height=dp(1)))
        self.add_widget(Widget(size_hint_y=None, height=dp(6)))

        # ── Botões ──
        btn_add = StyledButton(text="＋  Adicionar Produto", bg=VERDE)
        btn_add.bind(on_release=self._adicionar)
        self.add_widget(btn_add)

        btn_sell = StyledButton(text="✕  Vender Produto", bg=VERMELHO)
        btn_sell.bind(on_release=self._vender)
        self.add_widget(btn_sell)

        btn_upd = StyledButton(text="✎  Alterar Produto", bg=AMARELO)
        btn_upd.color = PRETO
        btn_upd.bind(on_release=self._alterar)
        self.add_widget(btn_upd)

        btn_clr = StyledButton(text="⌫  Limpar Campos", bg=CINZA_MEDIO)
        btn_clr.bind(on_release=self._limpar)
        self.add_widget(btn_clr)

        self.add_widget(Widget())  # spacer

    def _upd(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    # ── helpers ──
    def _get(self, key):
        return self._entries[key].text.strip()

    def _limpar(self, *_):
        for inp in self._entries.values():
            inp.text = ""

    # ── ações ──
    def _adicionar(self, *_):
        try:
            nome      = self._get("nome")
            artista   = self._get("artista")
            genero    = self._get("genero")
            quantidade= int(self._get("quantidade"))
            preco     = float(self._get("preco"))
            if not nome:
                raise ValueError("Nome obrigatório")
            adicionar_produto(nome, artista, genero, quantidade, preco)
            self.log(f"[ADD] '{nome}' adicionado — {quantidade} un. @ R${preco:.2f}", VERDE)
            popup_msg("Sucesso", f"'{nome}' adicionado ao estoque!", VERDE)
        except Exception as e:
            popup_msg("Erro", str(e), VERMELHO)
            self.log(f"[ERRO] {e}", VERMELHO)

    def _vender(self, *_):
        try:
            nome      = self._get("nome")
            quantidade= int(self._get("quantidade"))
            if not nome:
                raise ValueError("Nome obrigatório")
            vender_produto(nome, quantidade)
            self.log(f"[SELL] '{nome}' — {quantidade} un. vendidas", AMARELO)
            popup_msg("Venda registrada", f"{quantidade}x '{nome}' vendido(s).", AZUL)
        except Exception as e:
            popup_msg("Erro", str(e), VERMELHO)
            self.log(f"[ERRO] {e}", VERMELHO)

    def _alterar(self, *_):
        try:
            id_prod   = int(self._get("id"))
            nome      = self._get("nome")
            quantidade= int(self._get("quantidade"))
            preco     = float(self._get("preco"))
            alterar_produto(id_prod, nome, quantidade, preco)
            self.log(f"[UPD] ID={id_prod} '{nome}' atualizado", AZUL)
            popup_msg("Atualizado", f"Produto ID {id_prod} atualizado!", AZUL)
        except Exception as e:
            popup_msg("Erro", str(e), VERMELHO)
            self.log(f"[ERRO] {e}", VERMELHO)


# ─── Painel direito (log / tabela de produtos) ────────────────────────────────
class RightPanel(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", padding=dp(16), spacing=dp(10), **kw)

        with self.canvas.before:
            Color(*PRETO)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd, size=self._upd)

        # cabeçalho
        self.add_widget(Label(
            text="◈  LOG DE OPERAÇÕES",
            color=AZUL, bold=True, font_size=dp(16),
            size_hint_y=None, height=dp(36),
            halign="left", text_size=(None, None),
        ))
        self.add_widget(Separator())

        # scroll de log
        scroll = ScrollView()
        self._log_layout = GridLayout(
            cols=1, size_hint_y=None, spacing=dp(4),
            padding=[dp(4), dp(4)],
        )
        self._log_layout.bind(minimum_height=self._log_layout.setter("height"))
        scroll.add_widget(self._log_layout)
        self.add_widget(scroll)

        self._add_log_line("Sistema iniciado. Pronto para operações.", AZUL)

    def _upd(self, *_):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def _add_log_line(self, text, color=BRANCO):
        from kivy.clock import Clock
        import datetime
        ts  = datetime.datetime.now().strftime("%H:%M:%S")
        lbl = Label(
            text=f"[{ts}]  {text}",
            color=color,
            font_size=dp(13),
            size_hint_y=None, height=dp(28),
            halign="left",
            text_size=(None, None),
        )
        self._log_layout.add_widget(lbl)
        # scroll to bottom
        def _scroll(*_):
            from kivy.uix.scrollview import ScrollView as SV
            for child in self.children:
                if isinstance(child, SV):
                    child.scroll_y = 0
        Clock.schedule_once(_scroll, 0.05)

    def log(self, msg, color=BRANCO):
        self._add_log_line(msg, color)


# ─── Layout raiz ──────────────────────────────────────────────────────────────
class RootLayout(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="horizontal", **kw)
        right = RightPanel()
        form  = FormPanel(log_callback=right.log)
        self.add_widget(form)
        self.add_widget(right)


# ─── App ──────────────────────────────────────────────────────────────────────
class GaleriaDoMetalApp(App):
    def build(self):
        self.title = "Controle de Estoque — Galeria do Metal"
        return RootLayout()


if __name__ == "__main__":
    GaleriaDoMetalApp().run()
