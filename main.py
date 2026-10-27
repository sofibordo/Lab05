import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    alert = AlertManager(page)

    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")


    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    input_tipo = ft.TextField(label="Tipo", width=200)
    input_marca = ft.TextField(label="Marca", width=200)
    input_anno = ft.TextField(label="Anno d'acquisto", width=200)

    txt_valore = ft.TextField(value=0, disabled=True, text_align=ft.TextAlign.CENTER, width=100)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    STEP_VALORE = 10
    def incrementa_valore(e):
        txt_valore.value = txt_valore.value + STEP_VALORE
        txt_valore.update()

    def decrementa_valore(e):
        txt_valore.value = txt_valore.value - STEP_VALORE
        txt_valore.update()

    def aggiungi_strumento(e):
        tipo = input_tipo.value.strip() if input_tipo.value else ""
        marca = input_marca.value.strip() if input_marca.value else ""
        anno = input_anno.value.strip() if input_anno.value else ""

        if tipo == "" or marca == "":
            alert.show_alert("❌ Inserire tipo e marca dello strumento")
            return

        try:
            anno = int(anno)
        except ValueError:
            alert.show_alert("❌ Inserire valore numerico per l'anno")
            return

        valore = int(txt_valore.value)
        if valore < 0:
            alert.show_alert("❌ Inserire un valore positivo")
            return

        deposito.aggiungi_strumento(tipo, marca, anno, valore)

        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        txt_valore.value = 0

        aggiorna_lista_strumenti()
        page.update()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    btn_minus = ft.IconButton(icon = ft.Icons.REMOVE, icon_color="red", icon_size=24, on_click=decrementa_valore)
    btn_add = ft.IconButton(icon = ft.Icons.ADD, icon_color="green", icon_size=24, on_click=incrementa_valore)

    btn_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(
            controls=[input_tipo, input_marca, input_anno, btn_minus, txt_valore, btn_add],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        btn_aggiungi_strumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
