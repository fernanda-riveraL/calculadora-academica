import customtkinter as ctk
import tkinter as tk
from tkinter import colorchooser
import json
import os

ctk.set_appearance_mode("light")

ARCHIVO_DATOS = "notas.json"

PALETA_SUGERIDA = [
    ("#f8bbd0", "Rosa / Pink"),
    ("#e1bee7", "Lavanda / Lavender"),
    ("#c8e6c9", "Menta / Mint"),
    ("#ffe0b2", "Melocotón / Peach"),
    ("#bbdefb", "Cielo / Sky"),
    ("#fff9c4", "Vainilla / Vanilla")
]

# Diccionario de localización bilingüe
TEXTOS = {
    "es": {
        "titulo_app": "🌸 Gestor Académico ✨",
        "estudiante": "Estudiante:",
        "semestre": "Semestre:",
        "semestres_opc": ["1er Semestre", "2do Semestre", "Semestre de Verano"],
        "btn_lupa": "🔍 ¿Qué significa?",
        "tus_ramos": "Tus Ramos",
        "holder_ramo": "Nombre de ramo...",
        "btn_add_ramo": "+ Agregar Ramo",
        "sin_ramo": "Selecciona o crea un ramo para comenzar ✨",
        "btn_renombrar": "✏️ Renombrar",
        "btn_color": "🎨 Color",
        "btn_eliminar_ramo": "Eliminar ramo",
        "holder_eval": "Ej: Certamen 1",
        "holder_nota": "Nota (ej: 4.5)",
        "holder_pct": "% (ej: 25)",
        "btn_add_eval": "Añadir",
        "evaluado_circulo": "Evaluado",
        "switch_examen": "Ramo con Examen Final (60% Semestre + 40% Examen)",
        "lbl_nota_examen": "Nota Examen:",
        "btn_calcular_examen": "Calcular",
        "evaluado_semestre": "Evaluado del Semestre:",
        "puntos_aportados": "Puntos aportados:",
        "aprobado_final": "🎉 ¡Ramo Aprobado! Promedio final:",
        "reprobado_final": "❌ Reprobado. Promedio final: {prom:.1f} (Bajo 4.0)",
        "aprobado_seguro": "✨ ¡Aprobado asegurado! Incluso con un 1.0 en el {pct:.0f}% restante pasas con 4.0.",
        "imposible_7": "⚠️ Necesitas un {nota:.1f} en el {pct:.0f}% restante para promediar 4.0 (Supera escala 7.0).",
        "necesitas_pct": "🎯 Necesitas promediar un {nota:.2f} en el {pct:.0f}% restante para aprobar con 4.0.",
        "prom_sem": "Promedio semestre:",
        "aporta_60": "Aporta {ap:.2f} al 60%",
        "aprobado_ex": "🎉 ¡Ramo Aprobado con Examen! Nota final:",
        "reprobado_ex": "❌ Reprobado con Examen. Nota final: {final:.2f} (Bajo 4.0)",
        "err_num": "Ingresa un número válido para la nota del examen.",
        "aprobado_ex_seguro": "✨ ¡Aprobado! Con tu semestre ({sem:.2f}), con un 1.0 en el examen apruebas.",
        "imposible_ex": "⚠️ Con tu semestre ({sem:.2f}), necesitas un {req:.2f} en el examen (Supera 7.0).",
        "necesitas_ex": "🎯 Con tu semestre ({sem:.2f}), necesitas un {req:.2f} en el examen (40%) para 4.0.",
        "tit_editar_ramo": "Editar Ramo",
        "msg_editar_ramo": "Ingresa el nuevo nombre del ramo:",
        "tit_editar_ev": "Editar Evaluación ✏️",
        "lbl_modificar_ev": "Modificar Evaluación",
        "btn_guardar_cambios": "Guardar Cambios",
        "tit_guia": "Guía de Uso & Significado de Campos 🔍",
        "lbl_guia": "🔍 Guía de la Calculadora",
        "btn_otro_color": "Elegir otro color libre...",
        "tit_color": "Elegir Color del Ramo 🎨"
    },
    "en": {
        "titulo_app": "🌸 Academic Manager ✨",
        "estudiante": "Student:",
        "semestre": "Semester:",
        "semestres_opc": ["1st Semester", "2nd Semester", "Summer Semester"],
        "btn_lupa": "🔍 What does it mean?",
        "tus_ramos": "Your Courses",
        "holder_ramo": "Course name...",
        "btn_add_ramo": "+ Add Course",
        "sin_ramo": "Select or create a course to get started ✨",
        "btn_renombrar": "✏️ Rename",
        "btn_color": "🎨 Color",
        "btn_eliminar_ramo": "Delete course",
        "holder_eval": "Ex: Midterm 1",
        "holder_nota": "Grade (ex: 4.5)",
        "holder_pct": "% (ex: 25)",
        "btn_add_eval": "Add",
        "evaluado_circulo": "Graded",
        "switch_examen": "Course with Final Exam (60% Coursework + 40% Exam)",
        "lbl_nota_examen": "Exam Grade:",
        "btn_calcular_examen": "Calculate",
        "evaluado_semestre": "Coursework Graded:",
        "puntos_aportados": "Contributed points:",
        "aprobado_final": "🎉 Course Passed! Final average:",
        "reprobado_final": "❌ Failed. Final average: {prom:.1f} (Below 4.0)",
        "aprobado_seguro": "✨ Guaranteed Pass! Even with a 1.0 in the remaining {pct:.0f}% you pass with 4.0.",
        "imposible_7": "⚠️ You need a {nota:.1f} in the remaining {pct:.0f}% to achieve 4.0 (Exceeds 7.0 scale).",
        "necesitas_pct": "🎯 You need an average of {nota:.2f} in the remaining {pct:.0f}% to pass with 4.0.",
        "prom_sem": "Coursework average:",
        "aporta_60": "Contributes {ap:.2f} to the 60%",
        "aprobado_ex": "🎉 Course Passed with Exam! Final grade:",
        "reprobado_ex": "❌ Failed with Exam. Final grade: {final:.2f} (Below 4.0)",
        "err_num": "Enter a valid number for the exam grade.",
        "aprobado_ex_seguro": "✨ Passed! With your coursework ({sem:.2f}), a 1.0 on the exam is enough to pass.",
        "imposible_ex": "⚠️ With your coursework ({sem:.2f}), you need a {req:.2f} on the exam (Exceeds 7.0).",
        "necesitas_ex": "🎯 With your coursework ({sem:.2f}), you need a {req:.2f} on the exam (40%) for 4.0.",
        "tit_editar_ramo": "Edit Course",
        "msg_editar_ramo": "Enter the new course name:",
        "tit_editar_ev": "Edit Assessment ✏️",
        "lbl_modificar_ev": "Modify Assessment",
        "btn_guardar_cambios": "Save Changes",
        "tit_guia": "User Guide & Field Descriptions 🔍",
        "lbl_guia": "🔍 Calculator Guide",
        "btn_otro_color": "Pick custom color...",
        "tit_color": "Choose Course Color 🎨"
    }
}

def cargar_datos():
    estructura_base = {
        "estudiante": "",
        "semestre": "1er Semestre",
        "idioma": "es",
        "ramos": []
    }
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
                if isinstance(datos, list):
                    estructura_base["ramos"] = datos
                    return estructura_base
                elif isinstance(datos, dict):
                    if "estudiante" not in datos:
                        datos["estudiante"] = ""
                    if "semestre" not in datos:
                        datos["semestre"] = "1er Semestre"
                    if "idioma" not in datos:
                        datos["idioma"] = "es"
                    if "ramos" not in datos:
                        datos["ramos"] = []
                    return datos
            except json.JSONDecodeError:
                return estructura_base
    return estructura_base

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

class GestorAcademico(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora Académica y Gestor de Ramos ✨")
        self.geometry("1100x750")
        self.configure(fg_color="#fff0f5")

        self.data_global = cargar_datos()
        self.idioma_actual = self.data_global.get("idioma", "es")
        self.ramos = self.data_global["ramos"]
        self.ramo_activo_idx = 0 if self.ramos else None
        self.font_scale = 0

        # Barra superior con perfil, idioma y accesibilidad
        self.top_bar = ctk.CTkFrame(self, fg_color="#fce4ec", corner_radius=12)
        self.top_bar.pack(fill="x", padx=20, pady=(12, 6))

        # Título
        self.label_titulo = ctk.CTkLabel(
            self.top_bar,
            text=self.t("titulo_app"),
            font=ctk.CTkFont(size=self.fs(18), weight="bold"),
            text_color="#880e4f"
        )
        self.label_titulo.pack(side="left", padx=(15, 15), pady=10)

        # Estudiante
        self.lbl_estudiante = ctk.CTkLabel(
            self.top_bar,
            text=self.t("estudiante"),
            font=ctk.CTkFont(size=self.fs(12), weight="bold"),
            text_color="#5c1b3d"
        )
        self.lbl_estudiante.pack(side="left", padx=(5, 4))

        self.entry_estudiante = ctk.CTkEntry(
            self.top_bar,
            placeholder_text="Nombre / Name...",
            width=150,
            height=28,
            corner_radius=8,
            font=ctk.CTkFont(size=self.fs(12))
        )
        self.entry_estudiante.insert(0, self.data_global.get("estudiante", ""))
        self.entry_estudiante.pack(side="left", padx=(0, 10))
        self.entry_estudiante.bind("<FocusOut>", lambda e: self.guardar_perfil_estudiante())
        self.entry_estudiante.bind("<Return>", lambda e: self.guardar_perfil_estudiante())

        # Semestre
        self.lbl_semestre = ctk.CTkLabel(
            self.top_bar,
            text=self.t("semestre"),
            font=ctk.CTkFont(size=self.fs(12), weight="bold"),
            text_color="#5c1b3d"
        )
        self.lbl_semestre.pack(side="left", padx=(5, 4))

        self.combo_semestre = ctk.CTkComboBox(
            self.top_bar,
            values=self.t("semestres_opc"),
            width=140,
            height=28,
            corner_radius=8,
            font=ctk.CTkFont(size=self.fs(11)),
            command=self.cambiar_semestre
        )
        sem_actual = self.data_global.get("semestre", self.t("semestres_opc")[0])
        self.combo_semestre.set(sem_actual)
        self.combo_semestre.pack(side="left", padx=(0, 10))

        # Selector de Idioma (ES / EN)
        self.lbl_idioma = ctk.CTkLabel(
            self.top_bar,
            text="🌐",
            font=ctk.CTkFont(size=self.fs(13)),
            text_color="#5c1b3d"
        )
        self.lbl_idioma.pack(side="left", padx=(5, 2))

        self.combo_idioma = ctk.CTkComboBox(
            self.top_bar,
            values=["Español", "English"],
            width=100,
            height=28,
            corner_radius=8,
            font=ctk.CTkFont(size=self.fs(11)),
            command=self.cambiar_idioma
        )
        self.combo_idioma.set("Español" if self.idioma_actual == "es" else "English")
        self.combo_idioma.pack(side="left", padx=(0, 10))

        # Botón Guía Lupa
        self.btn_lupa = ctk.CTkButton(
            self.top_bar,
            text=self.t("btn_lupa"),
            width=135,
            height=28,
            fg_color="#f8bbd0",
            hover_color="#f48fb1",
            text_color="#880e4f",
            font=ctk.CTkFont(size=self.fs(11), weight="bold"),
            corner_radius=8,
            command=self.mostrar_guia_lupa
        )
        self.btn_lupa.pack(side="right", padx=(4, 12))

        # Controles de tamaño de letra
        self.btn_font_dec = ctk.CTkButton(
            self.top_bar, text="A-", width=34, height=28,
            fg_color="#ffffff", text_color="#880e4f", hover_color="#fce4ec",
            font=ctk.CTkFont(size=12, weight="bold"), corner_radius=8,
            command=self.disminuir_letra
        )
        self.btn_font_dec.pack(side="right", padx=2)

        self.btn_font_inc = ctk.CTkButton(
            self.top_bar, text="A+", width=34, height=28,
            fg_color="#ffffff", text_color="#880e4f", hover_color="#fce4ec",
            font=ctk.CTkFont(size=12, weight="bold"), corner_radius=8,
            command=self.aumentar_letra
        )
        self.btn_font_inc.pack(side="right", padx=2)

        # Contenedor principal
        self.contenedor_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_principal.pack(fill="both", expand=True, padx=20, pady=8)

        # Columna Izquierda: Ramos
        self.col_izquierda = ctk.CTkFrame(self.contenedor_principal, width=250, fg_color="#fce4ec", corner_radius=15)
        self.col_izquierda.pack(side="left", fill="y", padx=(0, 10), pady=5)

        self.lbl_ramos = ctk.CTkLabel(self.col_izquierda, text=self.t("tus_ramos"), font=ctk.CTkFont(size=self.fs(16), weight="bold"), text_color="#880e4f")
        self.lbl_ramos.pack(pady=10)

        self.entry_nuevo_ramo = ctk.CTkEntry(self.col_izquierda, placeholder_text=self.t("holder_ramo"), width=200, corner_radius=10, border_color="#f48fb1", font=ctk.CTkFont(size=self.fs(13)))
        self.entry_nuevo_ramo.pack(pady=5)

        self.btn_crear_ramo = ctk.CTkButton(self.col_izquierda, text=self.t("btn_add_ramo"), command=self.agregar_ramo, fg_color="#ec407a", hover_color="#d81b60", width=200, corner_radius=10, font=ctk.CTkFont(size=self.fs(13), weight="bold"))
        self.btn_crear_ramo.pack(pady=5)

        self.scroll_ramos = ctk.CTkScrollableFrame(self.col_izquierda, width=220, fg_color="#ffffff", corner_radius=10)
        self.scroll_ramos.pack(fill="both", expand=True, padx=10, pady=10)

        # Columna Derecha: Panel de Evaluaciones y Cálculos
        self.col_derecha = ctk.CTkFrame(self.contenedor_principal, fg_color="#ffffff", corner_radius=15)
        self.col_derecha.pack(side="right", fill="both", expand=True, pady=5)

        self.renderizar_lista_ramos()
        self.renderizar_panel_derecho()

    def t(self, clave):
        """Retorna el texto localizado según el idioma activo."""
        return TEXTOS.get(self.idioma_actual, TEXTOS["es"]).get(clave, "")

    def fs(self, base):
        return max(9, base + self.font_scale)

    def cambiar_idioma(self, seleccion):
        self.idioma_actual = "en" if seleccion == "English" else "es"
        self.data_global["idioma"] = self.idioma_actual
        guardar_datos(self.data_global)

        # Actualizar textos de la barra superior
        self.label_titulo.configure(text=self.t("titulo_app"))
        self.lbl_estudiante.configure(text=self.t("estudiante"))
        self.lbl_semestre.configure(text=self.t("semestre"))
        self.combo_semestre.configure(values=self.t("semestres_opc"))
        self.btn_lupa.configure(text=self.t("btn_lupa"))
        self.lbl_ramos.configure(text=self.t("tus_ramos"))
        self.entry_nuevo_ramo.configure(placeholder_text=self.t("holder_ramo"))
        self.btn_crear_ramo.configure(text=self.t("btn_add_ramo"))

        self.renderizar_panel_derecho()

    def guardar_perfil_estudiante(self):
        self.data_global["estudiante"] = self.entry_estudiante.get().strip()
        guardar_datos(self.data_global)

    def cambiar_semestre(self, opcion_seleccionada):
        self.data_global["semestre"] = opcion_seleccionada
        guardar_datos(self.data_global)

    def aumentar_letra(self):
        if self.font_scale < 5:
            self.font_scale += 1
            self.actualizar_interfaz_completa()

    def disminuir_letra(self):
        if self.font_scale > -3:
            self.font_scale -= 1
            self.actualizar_interfaz_completa()

    def actualizar_interfaz_completa(self):
        self.label_titulo.configure(font=ctk.CTkFont(size=self.fs(18), weight="bold"))
        self.lbl_estudiante.configure(font=ctk.CTkFont(size=self.fs(12), weight="bold"))
        self.lbl_semestre.configure(font=ctk.CTkFont(size=self.fs(12), weight="bold"))
        self.entry_estudiante.configure(font=ctk.CTkFont(size=self.fs(12)))
        self.combo_semestre.configure(font=ctk.CTkFont(size=self.fs(11)))
        self.combo_idioma.configure(font=ctk.CTkFont(size=self.fs(11)))
        self.lbl_ramos.configure(font=ctk.CTkFont(size=self.fs(16), weight="bold"))
        self.entry_nuevo_ramo.configure(font=ctk.CTkFont(size=self.fs(13)))
        self.btn_crear_ramo.configure(font=ctk.CTkFont(size=self.fs(13), weight="bold"))
        self.btn_lupa.configure(font=ctk.CTkFont(size=self.fs(11), weight="bold"))
        self.renderizar_lista_ramos()
        self.renderizar_panel_derecho()

    def renderizar_lista_ramos(self):
        for widget in self.scroll_ramos.winfo_children():
            widget.destroy()

        for idx, ramo in enumerate(self.ramos):
            color_asignado = ramo.get("color", "#f8bbd0")
            es_activo = (idx == self.ramo_activo_idx)

            btn_ramo = ctk.CTkButton(
                self.scroll_ramos,
                text=ramo["nombre"],
                fg_color=color_asignado,
                hover_color="#ffd1dc",
                border_color="#d81b60",
                border_width=2 if es_activo else 0,
                text_color="#4a148c" if es_activo else "#333333",
                font=ctk.CTkFont(size=self.fs(13), weight="bold" if es_activo else "normal"),
                corner_radius=8,
                command=lambda i=idx: self.seleccionar_ramo(i)
            )
            btn_ramo.pack(fill="x", pady=3)

    def seleccionar_ramo(self, indice):
        self.ramo_activo_idx = indice
        self.renderizar_lista_ramos()
        self.renderizar_panel_derecho()

    def renderizar_panel_derecho(self):
        for widget in self.col_derecha.winfo_children():
            widget.destroy()

        if self.ramo_activo_idx is None or self.ramo_activo_idx >= len(self.ramos):
            lbl_vacio = ctk.CTkLabel(self.col_derecha, text=self.t("sin_ramo"), text_color="#777777", font=ctk.CTkFont(size=self.fs(14)))
            lbl_vacio.pack(expand=True)
            return

        ramo = self.ramos[self.ramo_activo_idx]
        if "tiene_examen" not in ramo:
            ramo["tiene_examen"] = False
        if "nota_examen" not in ramo:
            ramo["nota_examen"] = ""
        if "color" not in ramo:
            ramo["color"] = "#f8bbd0"

        header_frame = ctk.CTkFrame(self.col_derecha, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))

        lbl_nombre_ramo = ctk.CTkLabel(
            header_frame,
            text=ramo["nombre"],
            font=ctk.CTkFont(size=self.fs(19), weight="bold"),
            text_color="#5c1b3d"
        )
        lbl_nombre_ramo.pack(side="left")

        btn_edit_ramo = ctk.CTkButton(
            header_frame,
            text=self.t("btn_renombrar"),
            width=90,
            height=26,
            fg_color="#ffe4ee",
            hover_color="#f8bbd0",
            text_color="#880e4f",
            corner_radius=8,
            font=ctk.CTkFont(size=self.fs(11)),
            command=self.editar_nombre_ramo_dialogo
        )
        btn_edit_ramo.pack(side="left", padx=8)

        btn_color_ramo = ctk.CTkButton(
            header_frame,
            text=self.t("btn_color"),
            width=70,
            height=26,
            fg_color=ramo.get("color", "#f8bbd0"),
            hover_color="#f48fb1",
            text_color="#333333",
            corner_radius=8,
            font=ctk.CTkFont(size=self.fs(11), weight="bold"),
            command=self.cambiar_color_ramo
        )
        btn_color_ramo.pack(side="left", padx=4)

        btn_borrar_ramo = ctk.CTkButton(
            header_frame,
            text=self.t("btn_eliminar_ramo"),
            fg_color="#ef5350",
            hover_color="#c62828",
            width=100,
            height=26,
            corner_radius=8,
            font=ctk.CTkFont(size=self.fs(11)),
            command=self.eliminar_ramo_actual
        )
        btn_borrar_ramo.pack(side="right")

        form_frame = ctk.CTkFrame(self.col_derecha, fg_color="#ffe4ee", corner_radius=10)
        form_frame.pack(fill="x", padx=15, pady=6)

        self.entry_eval = ctk.CTkEntry(form_frame, placeholder_text=self.t("holder_eval"), width=140, corner_radius=8, font=ctk.CTkFont(size=self.fs(12)))
        self.entry_eval.pack(side="left", padx=5, pady=6)

        self.entry_nota = ctk.CTkEntry(form_frame, placeholder_text=self.t("holder_nota"), width=95, corner_radius=8, font=ctk.CTkFont(size=self.fs(12)))
        self.entry_nota.pack(side="left", padx=5, pady=6)

        self.entry_pct = ctk.CTkEntry(form_frame, placeholder_text=self.t("holder_pct"), width=75, corner_radius=8, font=ctk.CTkFont(size=self.fs(12)))
        self.entry_pct.pack(side="left", padx=5, pady=6)

        btn_add_eval = ctk.CTkButton(form_frame, text=self.t("btn_add_eval"), width=75, fg_color="#ec407a", hover_color="#d81b60", corner_radius=8, font=ctk.CTkFont(size=self.fs(12), weight="bold"), command=self.agregar_evaluacion)
        btn_add_eval.pack(side="left", padx=5, pady=6)

        mid_frame = ctk.CTkFrame(self.col_derecha, fg_color="transparent")
        mid_frame.pack(fill="x", padx=15, pady=5)

        pct_acumulado = sum(e["porcentaje"] for e in ramo["evaluaciones"])
        suma_ponderada = sum(e["nota"] * (e["porcentaje"] / 100) for e in ramo["evaluaciones"])

        canvas_circulo = self.dibujar_circulo_progreso(mid_frame, pct_acumulado, ramo.get("color", "#d81b60"))
        canvas_circulo.pack(side="left", padx=(0, 10))

        card_diag = ctk.CTkFrame(mid_frame, fg_color="#fff3e0", corner_radius=10)
        card_diag.pack(side="left", fill="both", expand=True)

        self.actualizar_textos_diagnostico(card_diag, ramo, pct_acumulado, suma_ponderada)

        frame_examen = ctk.CTkFrame(self.col_derecha, fg_color="#fce4ec", corner_radius=10)
        frame_examen.pack(fill="x", padx=15, pady=6)

        self.switch_examen = ctk.CTkSwitch(
            frame_examen,
            text=self.t("switch_examen"),
            font=ctk.CTkFont(size=self.fs(12), weight="bold"),
            text_color="#880e4f",
            progress_color="#ec407a",
            command=self.toggle_examen
        )
        if ramo["tiene_examen"]:
            self.switch_examen.select()
        else:
            self.switch_examen.deselect()
        self.switch_examen.pack(side="left", padx=12, pady=8)

        if ramo["tiene_examen"]:
            lbl_examen_input = ctk.CTkLabel(frame_examen, text=self.t("lbl_nota_examen"), font=ctk.CTkFont(size=self.fs(11)), text_color="#5c1b3d")
            lbl_examen_input.pack(side="left", padx=(10, 2))

            self.entry_nota_examen = ctk.CTkEntry(frame_examen, width=65, height=26, font=ctk.CTkFont(size=self.fs(11)), corner_radius=6)
            self.entry_nota_examen.insert(0, str(ramo.get("nota_examen", "")))
            self.entry_nota_examen.pack(side="left", padx=4)

            btn_guardar_ex = ctk.CTkButton(frame_examen, text=self.t("btn_calcular_examen"), width=65, height=26, fg_color="#ec407a", hover_color="#d81b60", font=ctk.CTkFont(size=self.fs(11)), corner_radius=6, command=self.guardar_nota_examen)
            btn_guardar_ex.pack(side="left", padx=4)

        self.scroll_evals = ctk.CTkScrollableFrame(self.col_derecha, fg_color="#fafafa", corner_radius=10)
        self.scroll_evals.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        color_recuadro = ramo.get("color", "#f8bbd0")

        et_nota = "Nota" if self.idioma_actual == "es" else "Grade"
        et_pond = "Ponderación" if self.idioma_actual == "es" else "Weight"

        for i, ev in enumerate(ramo["evaluaciones"]):
            fila = ctk.CTkFrame(self.scroll_evals, fg_color="#ffffff", border_color=color_recuadro, border_width=1.5, corner_radius=8)
            fila.pack(fill="x", padx=5, pady=3)

            info_txt = f"📌 {ev['nombre']}   |   {et_nota}: {ev['nota']}   |   {et_pond}: {ev['porcentaje']}%"
            lbl_ev = ctk.CTkLabel(fila, text=info_txt, text_color="#333333", font=ctk.CTkFont(size=self.fs(12)))
            lbl_ev.pack(side="left", padx=10, pady=5)

            btn_quitar = ctk.CTkButton(
                fila, text="✕", width=26, height=22,
                fg_color="#f8bbd0", hover_color="#e91e63", text_color="#880e4f",
                font=ctk.CTkFont(size=self.fs(11)),
                command=lambda idx=i: self.eliminar_evaluacion(idx)
            )
            btn_quitar.pack(side="right", padx=(2, 8))

            btn_editar_eval = ctk.CTkButton(
                fila, text="✏️", width=26, height=22,
                fg_color="#e0e0e0", hover_color="#bdbdbd", text_color="#333333",
                font=ctk.CTkFont(size=self.fs(11)),
                command=lambda idx=i: self.editar_evaluacion_dialogo(idx)
            )
            btn_editar_eval.pack(side="right", padx=2)

    def cambiar_color_ramo(self):
        ramo = self.ramos[self.ramo_activo_idx]
        ventana_color = ctk.CTkToplevel(self)
        ventana_color.title(self.t("tit_color"))
        ventana_color.geometry("340x260")
        ventana_color.configure(fg_color="#fff0f5")
        ventana_color.grab_set()

        lbl = ctk.CTkLabel(ventana_color, text=f"Color: '{ramo['nombre']}'", font=ctk.CTkFont(size=14, weight="bold"), text_color="#880e4f")
        lbl.pack(pady=10)

        grid_colores = ctk.CTkFrame(ventana_color, fg_color="transparent")
        grid_colores.pack(pady=5)

        for i, (hex_code, nombre_color) in enumerate(PALETA_SUGERIDA):
            r = i // 3
            c = i % 3
            btn = ctk.CTkButton(
                grid_colores,
                text=nombre_color.split("/")[0].strip() if self.idioma_actual == "es" else nombre_color.split("/")[1].strip(),
                fg_color=hex_code,
                text_color="#333333",
                hover_color="#e0e0e0",
                width=90,
                height=32,
                corner_radius=8,
                command=lambda col=hex_code: self.aplicar_color(col, ventana_color)
            )
            btn.grid(row=r, column=c, padx=5, pady=5)

        btn_custom = ctk.CTkButton(
            ventana_color,
            text=self.t("btn_otro_color"),
            fg_color="#ec407a",
            hover_color="#d81b60",
            text_color="#ffffff",
            corner_radius=8,
            command=lambda: self.abrir_paleta_nativa(ventana_color)
        )
        btn_custom.pack(pady=12)

    def abrir_paleta_nativa(self, ventana_toplevel):
        color = colorchooser.askcolor(title=self.t("tit_color"))[1]
        if color:
            self.aplicar_color(color, ventana_toplevel)

    def aplicar_color(self, hex_color, ventana_toplevel):
        ramo = self.ramos[self.ramo_activo_idx]
        ramo["color"] = hex_color
        guardar_datos(self.data_global)
        ventana_toplevel.destroy()
        self.renderizar_lista_ramos()
        self.renderizar_panel_derecho()

    def editar_nombre_ramo_dialogo(self):
        ramo = self.ramos[self.ramo_activo_idx]
        dialogo = ctk.CTkInputDialog(text=self.t("msg_editar_ramo"), title=self.t("tit_editar_ramo"))
        nuevo_nom = dialogo.get_input()
        if nuevo_nom and nuevo_nom.strip():
            ramo["nombre"] = nuevo_nom.strip()
            guardar_datos(self.data_global)
            self.renderizar_lista_ramos()
            self.renderizar_panel_derecho()

    def editar_evaluacion_dialogo(self, indice):
        ramo = self.ramos[self.ramo_activo_idx]
        ev = ramo["evaluaciones"][indice]

        ventana_ed = ctk.CTkToplevel(self)
        ventana_ed.title(self.t("tit_editar_ev"))
        ventana_ed.geometry("320x250")
        ventana_ed.configure(fg_color="#fff0f5")
        ventana_ed.grab_set()

        lbl = ctk.CTkLabel(ventana_ed, text=self.t("lbl_modificar_ev"), font=ctk.CTkFont(size=14, weight="bold"), text_color="#880e4f")
        lbl.pack(pady=10)

        ent_nom = ctk.CTkEntry(ventana_ed, placeholder_text=self.t("holder_eval"), width=220)
        ent_nom.insert(0, ev["nombre"])
        ent_nom.pack(pady=4)

        ent_nota = ctk.CTkEntry(ventana_ed, placeholder_text=self.t("holder_nota"), width=220)
        ent_nota.insert(0, str(ev["nota"]))
        ent_nota.pack(pady=4)

        ent_pct = ctk.CTkEntry(ventana_ed, placeholder_text=self.t("holder_pct"), width=220)
        ent_pct.insert(0, str(ev["porcentaje"]))
        ent_pct.pack(pady=4)

        def guardar_cambios():
            nom = ent_nom.get().strip()
            nota_s = ent_nota.get().strip().replace(",", ".")
            pct_s = ent_pct.get().strip().replace("%", "")
            try:
                n = float(nota_s)
                p = float(pct_s)
                if 1.0 <= n <= 7.0 and 0 < p <= 100:
                    ev["nombre"] = nom if nom else ("Evaluación" if self.idioma_actual == "es" else "Assessment")
                    ev["nota"] = n
                    ev["porcentaje"] = p
                    guardar_datos(self.data_global)
                    ventana_ed.destroy()
                    self.renderizar_panel_derecho()
            except ValueError:
                pass

        btn_save = ctk.CTkButton(ventana_ed, text=self.t("btn_guardar_cambios"), fg_color="#ec407a", hover_color="#d81b60", command=guardar_cambios)
        btn_save.pack(pady=12)

    def dibujar_circulo_progreso(self, parent, porcentaje, color_hex):
        canvas = tk.Canvas(parent, width=105, height=105, bg="#ffffff", highlightthickness=0)
        angulo_progreso = min(360, (porcentaje / 100) * 360)

        canvas.create_oval(10, 10, 95, 95, outline="#f0f0f0", width=8)

        color_trazo = color_hex if color_hex != "#ffffff" else "#ec407a"
        if angulo_progreso > 0:
            canvas.create_arc(10, 10, 95, 95, start=90, extent=-angulo_progreso, outline=color_trazo, width=8, style="arc")

        canvas.create_text(52, 48, text=f"{porcentaje:.0f}%", font=("Helvetica", self.fs(13), "bold"), fill="#880e4f")
        canvas.create_text(52, 64, text=self.t("evaluado_circulo"), font=("Helvetica", self.fs(9)), fill="#777777")
        return canvas

    def actualizar_textos_diagnostico(self, contenedor, ramo, pct_acum, suma_pond):
        pct_restante = 100 - pct_acum
        resumen_txt = f"{self.t('evaluado_semestre')} {pct_acum:.1f}% / 100%   |   {self.t('puntos_aportados')} {suma_pond:.2f}"

        if not ramo.get("tiene_examen", False):
            if pct_restante <= 0:
                if suma_pond >= 3.95:
                    diag_txt = f"{self.t('aprobado_final')} {suma_pond:.1f}"
                    color = "#2e7d32"
                else:
                    diag_txt = self.t("reprobado_final").format(prom=suma_pond)
                    color = "#c62828"
            else:
                nota_necesaria = (4.0 - suma_pond) / (pct_restante / 100)
                if nota_necesaria <= 1.0:
                    diag_txt = self.t("aprobado_seguro").format(pct=pct_restante)
                    color = "#2e7d32"
                elif nota_necesaria > 7.0:
                    diag_txt = self.t("imposible_7").format(nota=nota_necesaria, pct=pct_restante)
                    color = "#c62828"
                else:
                    diag_txt = self.t("necesitas_pct").format(nota=nota_necesaria, pct=pct_restante)
                    color = "#e65100"
        else:
            nota_semestre = (suma_pond / (pct_acum / 100)) if pct_acum > 0 else 0.0
            aporte_semestre = nota_semestre * 0.60
            ap_txt = self.t("aporta_60").format(ap=aporte_semestre)
            resumen_txt += f"\n{self.t('prom_sem')} {nota_semestre:.2f} ({ap_txt})"

            nota_ex_str = ramo.get("nota_examen", "")
            if nota_ex_str != "":
                try:
                    nota_ex = float(nota_ex_str)
                    nota_final = aporte_semestre + (nota_ex * 0.40)
                    if nota_final >= 3.95:
                        diag_txt = f"{self.t('aprobado_ex')} {nota_final:.2f}"
                        color = "#2e7d32"
                    else:
                        diag_txt = self.t("reprobado_ex").format(final=nota_final)
                        color = "#c62828"
                except ValueError:
                    diag_txt = self.t("err_num")
                    color = "#777777"
            else:
                req_examen = (4.0 - aporte_semestre) / 0.40
                if req_examen <= 1.0:
                    diag_txt = self.t("aprobado_ex_seguro").format(sem=nota_semestre)
                    color = "#2e7d32"
                elif req_examen > 7.0:
                    diag_txt = self.t("imposible_ex").format(sem=nota_semestre, req=req_examen)
                    color = "#c62828"
                else:
                    diag_txt = self.t("necesitas_ex").format(sem=nota_semestre, req=req_examen)
                    color = "#e65100"

        lbl_res = ctk.CTkLabel(contenedor, text=resumen_txt, font=ctk.CTkFont(size=self.fs(11), weight="bold"), text_color="#333333", justify="left")
        lbl_res.pack(pady=(6, 2), padx=10, anchor="w")

        lbl_diag = ctk.CTkLabel(contenedor, text=diag_txt, font=ctk.CTkFont(size=self.fs(12), weight="bold"), text_color=color, justify="left")
        lbl_diag.pack(pady=(2, 6), padx=10, anchor="w")

    def toggle_examen(self):
        ramo = self.ramos[self.ramo_activo_idx]
        ramo["tiene_examen"] = bool(self.switch_examen.get())
        guardar_datos(self.data_global)
        self.renderizar_panel_derecho()

    def guardar_nota_examen(self):
        val = self.entry_nota_examen.get().strip().replace(",", ".")
        ramo = self.ramos[self.ramo_activo_idx]
        ramo["nota_examen"] = val
        guardar_datos(self.data_global)
        self.renderizar_panel_derecho()

    def mostrar_guia_lupa(self):
        guia = ctk.CTkToplevel(self)
        guia.title(self.t("tit_guia"))
        guia.geometry("520x490")
        guia.configure(fg_color="#fff0f5")
        guia.grab_set()

        lbl_t = ctk.CTkLabel(guia, text=self.t("lbl_guia"), font=ctk.CTkFont(size=16, weight="bold"), text_color="#880e4f")
        lbl_t.pack(pady=12)

        scroll = ctk.CTkScrollableFrame(guia, width=460, height=390, fg_color="#ffffff", corner_radius=12)
        scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        if self.idioma_actual == "es":
            explicaciones = [
                ("🌐 Selector de Idioma", "Cambia instantáneamente la interfaz entre Español e Inglés sin reiniciar."),
                ("Estudiante y Semestre", "Permite registrar tu nombre y periodo académico activo, guardándose automáticamente."),
                ("Color permanente en lista", "Cada ramo conserva siempre su color asignado en el panel izquierdo para distinguirlos de un vistazo."),
                ("✏️ Renombrar y Editar", "Permite corregir el nombre del ramo o cambiar la nota/porcentaje de una prueba sin borrarla."),
                ("🎨 Selector de Color", "Personaliza el color distintivo de cada asignatura para identificarla al instante."),
                ("Círculo de progreso", "Dibuja el avance con el color temático del ramo hasta alcanzar el 100% evaluado."),
                ("Predicción de 4.0", "Calcula qué nota necesitas promediar en el porcentaje restante para aprobar."),
                ("Ramo con Examen (60%/40%)", "Calcula si te alcanza para pasar con la nota de presentación (60%) o qué nota requieres en el examen final (40%).")
            ]
        else:
            explicaciones = [
                ("🌐 Language Switcher", "Instantly toggles the interface between Spanish and English without restarting."),
                ("Student & Semester", "Register your name and current academic term; saves automatically."),
                ("Permanent Course Color", "Each course maintains its custom color tag on the left panel for quick visual identification."),
                ("✏️ Rename & Edit", "Modify course names or edit assessment grades/weights without having to delete them."),
                ("🎨 Color Palette", "Pick custom pastel tones for each course."),
                ("Progress Ring", "Draws current graded completion percentage towards the full 100% term total."),
                ("Passing Grade Forecast (4.0)", "Calculates the exact average needed across remaining coursework to pass."),
                ("Final Exam Mode (60%/40%)", "Projects whether coursework (60%) guarantees a pass or what score is required on the final exam (40%).")
            ]

        for titulo, desc in explicaciones:
            f = ctk.CTkFrame(scroll, fg_color="#fce4ec", corner_radius=8)
            f.pack(fill="x", pady=4, padx=5)

            t = ctk.CTkLabel(f, text=f"📌 {titulo}", font=ctk.CTkFont(size=12, weight="bold"), text_color="#880e4f", anchor="w")
            t.pack(fill="x", padx=8, pady=(4, 1))

            d = ctk.CTkLabel(f, text=desc, font=ctk.CTkFont(size=11), text_color="#333333", justify="left", wraplength=420, anchor="w")
            d.pack(fill="x", padx=8, pady=(0, 6))

    def agregar_ramo(self):
        nombre = self.entry_nuevo_ramo.get().strip()
        if nombre:
            idx_color = len(self.ramos) % len(PALETA_SUGERIDA)
            color_default = PALETA_SUGERIDA[idx_color][0]

            self.ramos.append({
                "nombre": nombre,
                "evaluaciones": [],
                "tiene_examen": False,
                "nota_examen": "",
                "color": color_default
            })
            guardar_datos(self.data_global)
            self.ramo_activo_idx = len(self.ramos) - 1
            self.entry_nuevo_ramo.delete(0, "end")
            self.renderizar_lista_ramos()
            self.renderizar_panel_derecho()

    def eliminar_ramo_actual(self):
        if self.ramo_activo_idx is not None:
            self.ramos.pop(self.ramo_activo_idx)
            guardar_datos(self.data_global)
            self.ramo_activo_idx = 0 if self.ramos else None
            self.renderizar_lista_ramos()
            self.renderizar_panel_derecho()

    def agregar_evaluacion(self):
        nom = self.entry_eval.get().strip()
        nota_str = self.entry_nota.get().strip().replace(",", ".")
        pct_str = self.entry_pct.get().strip().replace("%", "")

        try:
            nota = float(nota_str)
            pct = float(pct_str)
        except ValueError:
            return

        if 1.0 <= nota <= 7.0 and 0 < pct <= 100:
            ramo = self.ramos[self.ramo_activo_idx]
            def_nom = "Evaluación" if self.idioma_actual == "es" else "Assessment"
            ramo["evaluaciones"].append({"nombre": nom if nom else def_nom, "nota": nota, "porcentaje": pct})
            guardar_datos(self.data_global)
            self.renderizar_panel_derecho()

    def eliminar_evaluacion(self, indice):
        ramo = self.ramos[self.ramo_activo_idx]
        ramo["evaluaciones"].pop(indice)
        guardar_datos(self.data_global)
        self.renderizar_panel_derecho()

if __name__ == "__main__":
    app = GestorAcademico()
    app.mainloop()


                  
