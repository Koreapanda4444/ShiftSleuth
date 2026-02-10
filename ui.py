import customtkinter as ctk

from cipher import encrypt, decrypt
from scoring import chi_square_score


class ShiftSleuthApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ShiftSleuth — Caesar/ROT Analyzer")
        self.geometry("1060x680")
        self.minsize(900, 580)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._debounce_job = None

        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)

        self._build_topbar()
        self._build_main()
        self._build_bottom()

        self._wire_events()
        self.update_all()

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

        ctk.CTkLabel(left, text="Input").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))
        self.input_box = ctk.CTkTextbox(left, wrap="word")
        self.input_box.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))

        ctk.CTkLabel(left, text="Output").grid(row=2, column=0, sticky="w", padx=12, pady=(4, 6))
        self.output_box = ctk.CTkTextbox(left, wrap="word")
        self.output_box.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.output_box.configure(state="disabled")

        right = ctk.CTkFrame(main, corner_radius=12)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 10), pady=10)
        right.grid_rowconfigure(4, weight=1)
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(right, text="Crib Filter").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))
        self.crib_entry = ctk.CTkEntry(right, placeholder_text="e.g. flag, http, dreamhack")
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
        ctk.CTkLabel(chart, text="Frequency Chart").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))
        self.chart_placeholder = ctk.CTkLabel(chart, text="(chart area)", text_color=("gray40", "gray70"))
        self.chart_placeholder.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        mapping = ctk.CTkFrame(bottom, corner_radius=12)
        mapping.grid(row=0, column=1, sticky="nsew", padx=(6, 10), pady=10)
        mapping.grid_rowconfigure(2, weight=1)
        mapping.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(mapping, text="Mapping Table").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))
        self.map_mode_seg = ctk.CTkSegmentedButton(mapping, values=["decrypt map", "encrypt map"], width=220)
        self.map_mode_seg.set("decrypt map")
        self.map_mode_seg.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))
        self.map_placeholder = ctk.CTkLabel(mapping, text="(mapping area)", text_color=("gray40", "gray70"))
        self.map_placeholder.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))

    def _wire_events(self):
        self.input_box.bind("<KeyRelease>", lambda _e: self.schedule_update())
        self.mode_seg.configure(command=lambda _v: self.schedule_update())
        self.shift_slider.configure(command=lambda _v: self.on_shift_change())

        self.btn_copy.configure(command=self.copy_output)
        self.btn_clear.configure(command=self.clear_all)
        self.btn_recommend.configure(command=self.recommend_best)

    def schedule_update(self):
        if self._debounce_job is not None:
            self.after_cancel(self._debounce_job)
        self._debounce_job = self.after(120, self.update_all)

    def on_shift_change(self):
        shift = int(round(self.shift_slider.get()))
        self.shift_value.configure(text=str(shift))
        self.schedule_update()

    def get_input_text(self) -> str:
        return self.input_box.get("1.0", "end-1c")

    def set_output_text(self, text: str):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.configure(state="disabled")

    def update_all(self):
        self._debounce_job = None
        self.update_output()
        self.update_candidates()

    def update_output(self):
        text = self.get_input_text()
        if not text.strip():
            self.set_output_text("")
            return

        shift = int(round(self.shift_slider.get()))
        mode = self.mode_seg.get()

        try:
            out = decrypt(text, shift) if mode == "decrypt" else encrypt(text, shift)
        except Exception as e:
            out = f"[Error] {e}"

        self.set_output_text(out)

    def _clear_candidates(self):
        for w in self.cand_frame.winfo_children():
            w.destroy()

    def _preview_line(self, s: str, limit: int = 140) -> str:
        t = s.replace("\n", " ").strip()
        if len(t) > limit:
            return t[:limit] + "..."
        return t

    def build_candidates(self, text: str):
        items = []
        for shift in range(26):
            plain = decrypt(text, shift)
            score = chi_square_score(plain)
            items.append((shift, score, plain))
        items.sort(key=lambda x: x[1])
        return items

    def update_candidates(self):
        text = self.get_input_text()
        if not text.strip():
            self._clear_candidates()
            return

        self._clear_candidates()

        items = self.build_candidates(text)
        shown = items[:10]

        for shift, score, plain in shown:
            row = ctk.CTkFrame(self.cand_frame, corner_radius=10)
            row.pack(fill="x", padx=6, pady=6)

            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, padx=10, pady=10)

            ctk.CTkLabel(info, text=f"Shift {shift} | Score {score:.2f}").pack(anchor="w")
            ctk.CTkLabel(info, text=self._preview_line(plain), text_color=("gray40", "gray70")).pack(anchor="w", pady=(2, 0))

            ctk.CTkButton(row, text="Apply", width=80, command=lambda s=shift: self.apply_candidate(s)).pack(
                side="right", padx=10, pady=10
            )

    def apply_candidate(self, shift: int):
        self.mode_seg.set("decrypt")
        self.shift_slider.set(shift)
        self.shift_value.configure(text=str(shift))
        self.update_all()

    def recommend_best(self):
        text = self.get_input_text()
        if not text.strip():
            return
        best_shift, _, _ = self.build_candidates(text)[0]
        self.apply_candidate(best_shift)

    def copy_output(self):
        out = self.output_box.get("1.0", "end-1c")
        if not out.strip():
            return
        self.clipboard_clear()
        self.clipboard_append(out)

    def clear_all(self):
        self.input_box.delete("1.0", "end")
        self.set_output_text("")
        self._clear_candidates()


def main():
    app = ShiftSleuthApp()
    app.mainloop()
