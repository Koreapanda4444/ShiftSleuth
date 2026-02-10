import customtkinter as ctk


class ShiftSleuthApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ShiftSleuth — Caesar/ROT Analyzer")
        self.geometry("1060x680")
        self.minsize(900, 580)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)

        self._build_topbar()
        self._build_main()
        self._build_bottom()

    def _build_topbar(self):
        top = ctk.CTkFrame(self, corner_radius=12)
        top.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        top.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(top, text="Mode").grid(row=0, column=0, padx=(12, 6), pady=12, sticky="w")
        self.mode_seg = ctk.CTkSegmentedButton(top, values=["decrypt", "encrypt"])
        self.mode_seg.set("decrypt")
        self.mode_seg.grid(row=0, column=1, padx=6, pady=12, sticky="w")

        ctk.CTkLabel(top, text="Shift").grid(row=0, column=2, padx=(18, 6), pady=12, sticky="w")
        self.shift_slider = ctk.CTkSlider(top, from_=0, to=25, number_of_steps=25)
        self.shift_slider.set(3)
        self.shift_slider.grid(row=0, column=3, padx=6, pady=12, sticky="ew")

        self.shift_value = ctk.CTkLabel(top, text="3", width=36)
        self.shift_value.grid(row=0, column=4, padx=(6, 12), pady=12, sticky="e")

        self.btn_recommend = ctk.CTkButton(top, text="Recommend", width=120)
        self.btn_recommend.grid(row=0, column=5, padx=(6, 6), pady=12)

        self.btn_copy = ctk.CTkButton(top, text="Copy Output", width=120)
        self.btn_copy.grid(row=0, column=6, padx=6, pady=12)

        self.btn_clear = ctk.CTkButton(top, text="Clear", width=90)
        self.btn_clear.grid(row=0, column=7, padx=(6, 12), pady=12)

    def _build_main(self):
        main = ctk.CTkFrame(self, corner_radius=12)
        main.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=2)

        left = ctk.CTkFrame(main, corner_radius=12)
        left.grid(row=0, column=0, sticky="nsew", padx=(10, 6), pady=10)
        left.grid_rowconfigure(1, weight=1)
        left.grid_rowconfigure(3, weight=1)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Input (ciphertext / plaintext)").grid(
            row=0, column=0, sticky="w", padx=12, pady=(12, 6)
        )
        self.input_box = ctk.CTkTextbox(left, wrap="word")
        self.input_box.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))

        ctk.CTkLabel(left, text="Output (result)").grid(
            row=2, column=0, sticky="w", padx=12, pady=(4, 6)
        )
        self.output_box = ctk.CTkTextbox(left, wrap="word")
        self.output_box.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))

        right = ctk.CTkFrame(main, corner_radius=12)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 10), pady=10)
        right.grid_rowconfigure(4, weight=1)
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(right, text="Crib Filter (hint)").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.crib_entry = ctk.CTkEntry(right, placeholder_text="e.g. flag, http, dreamhack (later: AND/OR, Regex)")
        self.crib_entry.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))

        toggles = ctk.CTkFrame(right, fg_color="transparent")
        toggles.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 8))
        self.andor_seg = ctk.CTkSegmentedButton(toggles, values=["AND", "OR"], width=140)
        self.andor_seg.set("AND")
        self.andor_seg.pack(side="left", padx=(0, 8))

        self.regex_switch = ctk.CTkSwitch(toggles, text="Regex")
        self.regex_switch.pack(side="left", padx=(0, 8))

        self.case_switch = ctk.CTkSwitch(toggles, text="Ignore case")
        self.case_switch.pack(side="left")

        ctk.CTkLabel(right, text="Top Candidates").grid(row=3, column=0, sticky="w", padx=12, pady=(8, 6))

        self.cand_frame = ctk.CTkScrollableFrame(right, height=220)
        self.cand_frame.grid(row=4, column=0, sticky="nsew", padx=12, pady=(0, 12))

        for _ in range(5):
            row = ctk.CTkFrame(self.cand_frame, corner_radius=10)
            row.pack(fill="x", padx=6, pady=6)
            ctk.CTkLabel(row, text="Shift ? | Confidence ?% | Score ?").pack(anchor="w", padx=10, pady=(8, 2))
            ctk.CTkLabel(row, text="(candidate preview appears here)").pack(anchor="w", padx=10, pady=(0, 8))

    def _build_bottom(self):
        bottom = ctk.CTkFrame(self, corner_radius=12)
        bottom.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        bottom.grid_rowconfigure(0, weight=1)
        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=2)

        chart = ctk.CTkFrame(bottom, corner_radius=12)
        chart.grid(row=0, column=0, sticky="nsew", padx=(10, 6), pady=10)
        chart.grid_rowconfigure(1, weight=1)
        chart.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(chart, text="Frequency Chart (Input vs Selected vs English)").grid(
            row=0, column=0, sticky="w", padx=12, pady=(12, 6)
        )
        self.chart_placeholder = ctk.CTkLabel(
            chart,
            text="(Commit 10: matplotlib canvas will be embedded here)",
            text_color=("gray40", "gray70")
        )
        self.chart_placeholder.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        mapping = ctk.CTkFrame(bottom, corner_radius=12)
        mapping.grid(row=0, column=1, sticky="nsew", padx=(6, 10), pady=10)
        mapping.grid_rowconfigure(2, weight=1)
        mapping.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(mapping, text="Mapping Table (A→D …)").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.map_mode_seg = ctk.CTkSegmentedButton(mapping, values=["decrypt map", "encrypt map"], width=220)
        self.map_mode_seg.set("decrypt map")
        self.map_mode_seg.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))

        self.map_placeholder = ctk.CTkLabel(
            mapping,
            text="(Commit 11: scrollable mapping table goes here)",
            text_color=("gray40", "gray70")
        )
        self.map_placeholder.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))


def main():
    app = ShiftSleuthApp()
    app.mainloop()
