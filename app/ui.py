import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

from app.engine import XPADIEngine


class XPADIProofUI:
    FONT = "Segoe UI"

    BG = "#040914"
    SURFACE = "#07111e"
    GLASS = "#0a1626"
    GLASS_2 = "#0d1b2f"
    GLASS_3 = "#0b1422"
    BORDER = "#1d3552"

    TEXT = "#eef6ff"
    MUTED = "#8fa9cc"
    DIM = "#6f86a7"

    BLUE = "#74b4ff"
    CYAN = "#59d8ff"
    GREEN = "#42e6a4"
    ORANGE = "#ffb45f"
    RED = "#ff7f7f"
    PURPLE = "#b591ff"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("XPADI — Survivability Proof")
        self.root.geometry("1600x980")
        self.root.minsize(1440, 900)
        self.root.configure(bg=self.BG)

        self.engine = XPADIEngine()
        self.selected_file = None
        self.recovered_file = None
        self.running = False

        self.test_state = tk.StringVar(value="Ready")
        self.recovery_state = tk.StringVar(value="No File Loaded")
        self.proof_outcome = tk.StringVar(value="Awaiting Test")

        self.step_vars = {
            "select": tk.StringVar(value="IDLE"),
            "protect": tk.StringVar(value="IDLE"),
            "attack": tk.StringVar(value="IDLE"),
            "recover": tk.StringVar(value="IDLE"),
            "verify": tk.StringVar(value="IDLE"),
        }

        self._build_ui()
        self._boot_logs()

    # --------------------------------------------------
    # BOOT
    # --------------------------------------------------
    def _boot_logs(self):
        self.log("XPADI Survivability Proof initialized", "SYSTEM")
        self.log("SAFE MODE ACTIVE — original source file will never be attacked", "SYSTEM")
        self.log("Controlled demo of attack simulation, recovery, and integrity verification", "SYSTEM")
        self.log("System ready for survivability test", "SYSTEM")

    # --------------------------------------------------
    # UI BUILD
    # --------------------------------------------------
    def _build_ui(self):
        self._build_background()
        self._build_header()
        self._build_body()
        self._build_footer()

    def _build_background(self):
        self.bg_canvas = tk.Canvas(self.root, bg=self.BG, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self._redraw_background)
        self._redraw_background()

    def _redraw_background(self, event=None):
        self.bg_canvas.delete("all")
        w = max(self.root.winfo_width(), 1200)
        h = max(self.root.winfo_height(), 800)

        self.bg_canvas.create_rectangle(0, 0, w, h, fill=self.BG, outline="")
        self.bg_canvas.create_oval(-180, -120, 520, 440, fill="#0a2240", outline="", stipple="gray25")
        self.bg_canvas.create_oval(w - 520, -140, w + 160, 360, fill="#0c2c42", outline="", stipple="gray25")
        self.bg_canvas.create_oval(w - 420, h - 300, w + 140, h + 120, fill="#17344c", outline="", stipple="gray25")
        self.bg_canvas.create_oval(-120, h - 220, 360, h + 120, fill="#12263b", outline="", stipple="gray25")

        step = 44
        for x in range(0, w, step):
            self.bg_canvas.create_line(x, 0, x, h, fill="#0a1828")
        for y in range(0, h, step):
            self.bg_canvas.create_line(0, y, w, y, fill="#0a1828")

        self.bg_canvas.tag_lower("all")

    def _build_header(self):
        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="x", padx=22, pady=(18, 10))

        wrap = self._glass_panel(outer)
        wrap.pack(fill="x")
        wrap.configure(padx=18, pady=14)

        left = tk.Frame(wrap, bg=self.GLASS)
        left.pack(side="left", fill="y")

        logo_wrap = tk.Frame(left, bg=self.GLASS)
        logo_wrap.pack(side="left", padx=(0, 14))

        logo = tk.Canvas(logo_wrap, width=62, height=62, bg=self.GLASS, highlightthickness=0)
        logo.pack()
        logo.create_rectangle(8, 8, 54, 54, fill="#0f2340", outline=self.BORDER)
        logo.create_text(31, 31, text="X", fill=self.TEXT, font=(self.FONT, 26, "bold"))

        title_wrap = tk.Frame(left, bg=self.GLASS)
        title_wrap.pack(side="left")

        tk.Label(
            title_wrap,
            text="XPADI — Survivability Proof",
            font=(self.FONT, 18, "bold"),
            bg=self.GLASS,
            fg=self.TEXT,
        ).pack(anchor="w")

        tk.Label(
            title_wrap,
            text="Controlled demo of attack simulation, recovery, and integrity verification",
            font=(self.FONT, 10),
            bg=self.GLASS,
            fg=self.MUTED,
        ).pack(anchor="w", pady=(4, 0))

        right = tk.Frame(wrap, bg=self.GLASS)
        right.pack(side="right")

        self._pill(right, "Proof Mode")
        self._pill(right, "Safe Mode Active")
        self._pill(right, "Offline-Capable Recovery")

    def _build_body(self):
        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True, padx=22, pady=(0, 10))

        left = tk.Frame(body, bg=self.BG, width=390)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        center = tk.Frame(body, bg=self.BG)
        center.pack(side="left", fill="both", expand=True, padx=8)

        right = tk.Frame(body, bg=self.BG, width=360)
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)

        self._build_left_column(left)
        self._build_center_column(center)
        self._build_right_column(right)

    def _build_left_column(self, parent):
        hero = self._glass_panel(parent)
        hero.pack(fill="x", pady=(0, 10))
        hero.configure(padx=18, pady=18)

        tk.Label(
            hero,
            text="XPADI — Survivability-Governed Data Systems",
            font=(self.FONT, 10, "bold"),
            bg=self.GLASS,
            fg=self.GREEN,
            wraplength=330,
            justify="left",
        ).pack(anchor="w")

        tk.Label(
            hero,
            text="Your file can be attacked.\nIt should still survive.",
            font=(self.FONT, 23, "bold"),
            justify="left",
            bg=self.GLASS,
            fg=self.TEXT,
            wraplength=330,
        ).pack(anchor="w", pady=(12, 10))

        tk.Label(
            hero,
            text="This proof application demonstrates how XPADI protects a file in survivability state, simulates a controlled attack on an internal protected copy, reconstructs the file, and verifies integrity.",
            font=(self.FONT, 10),
            justify="left",
            wraplength=330,
            bg=self.GLASS,
            fg=self.MUTED,
        ).pack(anchor="w")

        actions = tk.Frame(hero, bg=self.GLASS)
        actions.pack(fill="x", pady=(16, 0))

        self._action_button(actions, "Select File", self.select_file, self.BLUE, "#071018").pack(fill="x", pady=(0, 8))
        self._action_button(actions, "Run Survivability Test", self.run_full_proof, self.GREEN, "#071018").pack(fill="x", pady=(0, 8))
        self._action_button(actions, "Reset Session", self.reset_session, self.ORANGE, "#071018").pack(fill="x")

        flow = self._glass_panel(parent)
        flow.pack(fill="x", pady=(0, 10))
        flow.configure(padx=16, pady=16)

        tk.Label(
            flow,
            text="Proof Flow",
            font=(self.FONT, 12, "bold"),
            bg=self.GLASS,
            fg=self.TEXT,
        ).pack(anchor="w")

        tk.Label(
            flow,
            text="Follow the test from source selection to integrity verification.",
            font=(self.FONT, 9),
            bg=self.GLASS,
            fg=self.MUTED,
            wraplength=330,
            justify="left",
        ).pack(anchor="w", pady=(4, 12))

        steps = [
            ("select", "1. Select File"),
            ("protect", "2. Protect"),
            ("attack", "3. Simulate Attack"),
            ("recover", "4. Recover"),
            ("verify", "5. Verify"),
        ]
        for key, title in steps:
            self._flow_row(flow, title, self.step_vars[key]).pack(fill="x", pady=(0, 8))

        file_box = self._glass_panel(parent)
        file_box.pack(fill="x")
        file_box.configure(padx=16, pady=16)

        tk.Label(
            file_box,
            text="Selected Source File",
            font=(self.FONT, 12, "bold"),
            bg=self.GLASS,
            fg=self.TEXT,
        ).pack(anchor="w")

        self.file_label = tk.Label(
            file_box,
            text="No file selected",
            font=(self.FONT, 10),
            bg=self.GLASS,
            fg=self.CYAN,
            justify="left",
            wraplength=330,
        )
        self.file_label.pack(anchor="w", pady=(8, 0))

        tk.Label(
            file_box,
            text="Original remains untouched during Safe Mode testing",
            font=(self.FONT, 9),
            bg=self.GLASS,
            fg=self.MUTED,
            wraplength=330,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

    def _build_center_column(self, parent):
        proof = self._glass_panel(parent)
        proof.pack(fill="both", expand=True, pady=(0, 10))
        proof.configure(padx=16, pady=16)

        top = tk.Frame(proof, bg=self.GLASS)
        top.pack(fill="x")

        tk.Label(
            top,
            text="Proof Canvas",
            font=(self.FONT, 14, "bold"),
            bg=self.GLASS,
            fg=self.TEXT,
        ).pack(side="left")

        tk.Label(
            top,
            text="Live security-proof state surface",
            font=(self.FONT, 10),
            bg=self.GLASS,
            fg=self.MUTED,
        ).pack(side="right")

        canvas_wrap = tk.Frame(proof, bg=self.GLASS, highlightbackground=self.BORDER, highlightthickness=1)
        canvas_wrap.pack(fill="both", expand=True, pady=(12, 12))

        self.proof_canvas = tk.Canvas(
            canvas_wrap,
            bg=self.GLASS_3,
            highlightthickness=0,
            bd=0,
            relief="flat",
            height=390,
        )
        self.proof_canvas.pack(fill="both", expand=True)
        self.proof_canvas.bind("<Configure>", self._draw_proof_canvas)

        stats = tk.Frame(proof, bg=self.GLASS)
        stats.pack(fill="x")

        self._metric_card(stats, "Test State", self.test_state).pack(side="left", fill="both", expand=True, padx=(0, 8))
        self._metric_card(stats, "Recovery State", self.recovery_state).pack(side="left", fill="both", expand=True, padx=4)
        self._metric_card(stats, "Proof Outcome", self.proof_outcome).pack(side="left", fill="both", expand=True, padx=(8, 0))

        log_panel = self._glass_panel(parent)
        log_panel.pack(fill="both", expand=True)
        log_panel.configure(padx=16, pady=16)

        tk.Label(
            log_panel,
            text="Live Proof Log",
            font=(self.FONT, 13, "bold"),
            bg=self.GLASS,
            fg=self.TEXT,
        ).pack(anchor="w")

        tk.Label(
            log_panel,
            text="Readable event stream for proof, recovery, and integrity validation.",
            font=(self.FONT, 9),
            bg=self.GLASS,
            fg=self.MUTED,
        ).pack(anchor="w", pady=(4, 12))

        text_wrap = tk.Frame(log_panel, bg=self.GLASS_3, highlightbackground=self.BORDER, highlightthickness=1)
        text_wrap.pack(fill="both", expand=True)

        self.log_text = tk.Text(
            text_wrap,
            bg=self.GLASS_3,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            wrap="word",
            font=("Consolas", 10),
            padx=14,
            pady=14,
        )
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")

    def _build_right_column(self, parent):
        result = self._glass_panel(parent)
        result.pack(fill="x", pady=(0, 10))
        result.configure(padx=16, pady=16)

        tk.Label(
            result,
            text="Proof Result",
            font=(self.FONT, 14, "bold"),
            bg=self.GLASS,
            fg=self.TEXT,
        ).pack(anchor="w")

        self.result_desc = tk.Label(
            result,
            text="This demo proves whether a protected file can be recovered after controlled attack simulation.",
            font=(self.FONT, 10),
            bg=self.GLASS,
            fg=self.MUTED,
            wraplength=300,
            justify="left",
        )
        self.result_desc.pack(anchor="w", pady=(8, 12))

        inner = tk.Frame(result, bg=self.GLASS_3, highlightbackground=self.BORDER, highlightthickness=1)
        inner.pack(fill="x")
        inner.configure(padx=14, pady=14)

        tk.Label(
            inner,
            text="What this demo does",
            font=(self.FONT, 11, "bold"),
            bg=self.GLASS_3,
            fg=self.TEXT,
        ).pack(anchor="w")

        demo_lines = [
            "1. Keeps your original selected file untouched",
            "2. Creates an internal protected proof copy",
            "3. Simulates attack on protected state",
            "4. Reconstructs the file",
            "5. Verifies integrity by hash match",
        ]
        for line in demo_lines:
            tk.Label(
                inner,
                text=line,
                font=(self.FONT, 10),
                bg=self.GLASS_3,
                fg=self.MUTED,
                justify="left",
                wraplength=300,
            ).pack(anchor="w", pady=(4, 0))

        safe = self._glass_panel(parent)
        safe.pack(fill="x", pady=(0, 10))
        safe.configure(padx=16, pady=16)

        tk.Label(
            safe,
            text="Safe Mode Active",
            font=(self.FONT, 13, "bold"),
            bg=self.GLASS,
            fg=self.GREEN,
        ).pack(anchor="w")

        tk.Label(
            safe,
            text="Your selected source file is never attacked.\nThe test runs only on an internal protected copy.",
            font=(self.FONT, 10),
            bg=self.GLASS,
            fg=self.MUTED,
            wraplength=300,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        stages = self._glass_panel(parent)
        stages.pack(fill="both", expand=True)
        stages.configure(padx=16, pady=16)

        tk.Label(
            stages,
            text="Execution Stages",
            font=(self.FONT, 13, "bold"),
            bg=self.GLASS,
            fg=self.TEXT,
        ).pack(anchor="w")

        tk.Label(
            stages,
            text="Each stage explains what XPADI is proving during the run.",
            font=(self.FONT, 9),
            bg=self.GLASS,
            fg=self.MUTED,
            wraplength=300,
            justify="left",
        ).pack(anchor="w", pady=(4, 12))

        self.stage_labels = {}
        stage_titles = [
            "Source Selected",
            "Protected State Created",
            "Attack Simulated",
            "Recovery Completed",
            "Integrity Verified",
        ]
        for title in stage_titles:
            card = tk.Frame(stages, bg=self.GLASS_3, highlightbackground=self.BORDER, highlightthickness=1)
            card.pack(fill="x", pady=(0, 8))
            card.configure(padx=12, pady=10)

            tk.Label(
                card,
                text=title,
                font=(self.FONT, 10, "bold"),
                bg=self.GLASS_3,
                fg=self.TEXT,
            ).pack(anchor="w")

            val = tk.Label(
                card,
                text="Pending",
                font=(self.FONT, 9),
                bg=self.GLASS_3,
                fg=self.MUTED,
            )
            val.pack(anchor="w", pady=(4, 0))
            self.stage_labels[title] = val

    def _build_footer(self):
        footer = tk.Frame(self.root, bg=self.BG)
        footer.pack(fill="x", padx=22, pady=(0, 14))

        tk.Label(
            footer,
            text="XPADI does not prevent every attack. It proves that data can remain recoverable even after disruption.",
            font=(self.FONT, 9),
            bg=self.BG,
            fg=self.DIM,
        ).pack(anchor="w")

    # --------------------------------------------------
    # COMPONENTS
    # --------------------------------------------------
    def _glass_panel(self, parent):
        return tk.Frame(parent, bg=self.GLASS, highlightbackground=self.BORDER, highlightthickness=1)

    def _pill(self, parent, text):
        pill = tk.Frame(parent, bg=self.GLASS_2, highlightbackground=self.BORDER, highlightthickness=1)
        pill.pack(side="left", padx=5)
        tk.Label(
            pill,
            text=text,
            font=(self.FONT, 9, "bold"),
            bg=self.GLASS_2,
            fg=self.MUTED,
            padx=12,
            pady=9,
        ).pack()

    def _action_button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=(self.FONT, 11, "bold"),
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            relief="flat",
            bd=0,
            padx=16,
            pady=14,
            cursor="hand2",
        )

    def _metric_card(self, parent, title, var):
        card = tk.Frame(parent, bg=self.GLASS_3, highlightbackground=self.BORDER, highlightthickness=1)
        card.configure(padx=12, pady=12)

        tk.Label(
            card,
            text=title.upper(),
            font=(self.FONT, 9, "bold"),
            bg=self.GLASS_3,
            fg=self.MUTED,
        ).pack(anchor="w")

        tk.Label(
            card,
            textvariable=var,
            font=(self.FONT, 15, "bold"),
            bg=self.GLASS_3,
            fg=self.TEXT,
            wraplength=240,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))
        return card

    def _flow_row(self, parent, title, var):
        row = tk.Frame(parent, bg=self.GLASS_3, highlightbackground=self.BORDER, highlightthickness=1)
        row.configure(padx=12, pady=10)

        left = tk.Frame(row, bg=self.GLASS_3)
        left.pack(side="left", fill="x", expand=True)

        dot = tk.Canvas(left, width=16, height=16, bg=self.GLASS_3, highlightthickness=0)
        dot.pack(side="left", padx=(0, 10))
        dot.create_oval(3, 3, 13, 13, fill=self.CYAN, outline="")
        tk.Label(
            left,
            text=title,
            font=(self.FONT, 10, "bold"),
            bg=self.GLASS_3,
            fg=self.TEXT,
        ).pack(side="left")

        tk.Label(
            row,
            textvariable=var,
            font=(self.FONT, 9),
            bg=self.GLASS_3,
            fg=self.CYAN,
        ).pack(side="right")

        return row

    # --------------------------------------------------
    # PROOF CANVAS
    # --------------------------------------------------
    def _draw_proof_canvas(self, event=None):
        c = self.proof_canvas
        c.delete("all")

        w = max(c.winfo_width(), 500)
        h = max(c.winfo_height(), 300)

        c.create_rectangle(0, 0, w, h, fill=self.GLASS_3, outline="")

        # ambient shapes
        c.create_oval(-120, -80, 260, 220, fill="#0a2340", outline="", stipple="gray25")
        c.create_oval(w - 260, -60, w + 80, 200, fill="#103149", outline="", stipple="gray25")
        c.create_oval(w - 280, h - 180, w + 80, h + 80, fill="#17344a", outline="", stipple="gray25")

        # layout tuned to avoid clipping/overlap
        cx = w * 0.50
        cy = h * 0.46

        for r, color in [(140, "#0f2c42"), (98, "#12354d"), (62, "#17435c")]:
            c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, width=2)

        c.create_oval(cx - 34, cy - 34, cx + 34, cy + 34, fill="#0f2740", outline=self.CYAN, width=2)
        c.create_text(cx, cy, text="XPADI", fill=self.TEXT, font=(self.FONT, 12, "bold"))

        nodes = {
            "SELECT": (cx - 180, cy),
            "PROTECT": (cx - 320, cy),
            "ATTACK": (cx, cy + 130),
            "RECOVER": (cx + 180, cy),
            "VERIFY": (cx + 320, cy),
        }

        self._canvas_line(c, nodes["PROTECT"], nodes["SELECT"], self.BLUE)
        self._canvas_line(c, nodes["SELECT"], (cx - 62, cy), self.CYAN)
        self._canvas_line(c, (cx, cy + 62), nodes["ATTACK"], self.ORANGE)
        self._canvas_line(c, (cx + 62, cy), nodes["RECOVER"], self.GREEN)
        self._canvas_line(c, nodes["RECOVER"], nodes["VERIFY"], self.BLUE)

        for name, pos in nodes.items():
            self._canvas_node(c, pos[0], pos[1], name)

        c.create_text(
            cx,
            h - 34,
            text="Attack ≠ Data Loss",
            fill=self.TEXT,
            font=(self.FONT, 20, "bold")
        )

    def _canvas_line(self, c, p1, p2, color):
        c.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=3)

    def _canvas_node(self, c, x, y, label):
        c.create_oval(x - 42, y - 42, x + 42, y + 42, fill="#0d2036", outline=self.BORDER, width=2)
        c.create_text(x, y, text=label, fill=self.TEXT, font=(self.FONT, 9, "bold"))

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------
    def log(self, message: str, level: str = "INFO"):
        now = datetime.now().strftime("%H:%M:%S")
        line = f"[{now}] [{level}] {message}\n"

        self.log_text.configure(state="normal")
        self.log_text.insert("end", line)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

        self.root.update_idletasks()

    def _set_step(self, key, value):
        self.step_vars[key].set(value)

    def _set_stage(self, title, value, color=None):
        label = self.stage_labels[title]
        label.config(text=value)
        label.config(fg=color if color else self.MUTED)

    # --------------------------------------------------
    # ACTIONS
    # --------------------------------------------------
    def select_file(self):
        path = filedialog.askopenfilename(
            title="Select source file for XPADI proof",
            filetypes=[("All files", "*.*")]
        )
        if not path:
            return

        self.selected_file = path
        self.file_label.config(text=path)

        self.test_state.set("Ready")
        self.recovery_state.set("Source Selected")
        self.proof_outcome.set("Awaiting Test")

        self._set_step("select", "COMPLETE")
        self._set_stage("Source Selected", "Selected and safe", self.GREEN)

        self.log("Source file selected", "INFO")
        self.log("Safe Mode active — original file will remain untouched", "INFO")

    def protect_file(self):
        if not self.selected_file:
            messagebox.showwarning("XPADI", "Select a file first.")
            return

        self._set_step("protect", "RUNNING")
        self.test_state.set("Protecting")
        self.recovery_state.set("Protected State Creating")
        self.proof_outcome.set("In Progress")
        self.result_desc.config(
            text="XPADI is creating an internal protected proof copy and converting it into survivability state."
        )

        self.log("Internal proof copy created", "INFO")
        self.log("Protection workflow started", "INFO")

        self.engine.protect(self.selected_file)

        self._set_step("protect", "COMPLETE")
        self._set_stage("Protected State Created", "Protected state established", self.GREEN)
        self.test_state.set("Protected")
        self.recovery_state.set("Protected State Created")

        self.log("File fragmented into protected state", "INFO")
        self.log("Fragment protection established", "SUCCESS")

    def simulate_attack(self):
        if not self.engine.metadata:
            messagebox.showwarning("XPADI", "Protect a file first.")
            return

        self._set_step("attack", "RUNNING")
        self.test_state.set("Under Test")
        self.recovery_state.set("Attack Simulated")
        self.proof_outcome.set("In Progress")
        self.result_desc.config(
            text="A controlled attack simulation is running against the internal protected state, not the original selected file."
        )

        self.log("Controlled attack simulation executed on internal state", "WARN")
        self.engine.simulate_attack()

        self._set_step("attack", "COMPLETE")
        self._set_stage("Attack Simulated", "Controlled simulation completed", self.ORANGE)
        self.log("Original source file preserved", "SUCCESS")

    def recover_file(self):
        if not self.engine.metadata:
            messagebox.showwarning("XPADI", "No active protection session.")
            return

        self._set_step("recover", "RUNNING")
        self.test_state.set("Recovering")
        self.recovery_state.set("Reconstructing")
        self.proof_outcome.set("In Progress")
        self.result_desc.config(
            text="XPADI is reconstructing the protected file from internal survivability state."
        )

        self.log("Reconstruction started", "INFO")
        self.recovered_file = self.engine.recover()

        self._set_step("recover", "COMPLETE")
        self._set_stage("Recovery Completed", "Recovered output created", self.GREEN)
        self.test_state.set("Recovered")
        self.recovery_state.set("Recovery Completed")

        self.log(f"Recovery output created: {self.recovered_file}", "SUCCESS")

    def verify_recovery(self):
        if not self.recovered_file:
            messagebox.showwarning("XPADI", "Recover the file first.")
            return

        self._set_step("verify", "RUNNING")
        self.test_state.set("Verifying")
        self.recovery_state.set("Checking Integrity")
        self.proof_outcome.set("In Progress")
        self.result_desc.config(
            text="XPADI is verifying whether the recovered file matches original integrity."
        )

        self.log("Integrity verification started", "INFO")
        result = self.engine.verify_result(self.recovered_file)

        if result:
            self._set_step("verify", "COMPLETE")
            self._set_stage("Integrity Verified", "Hash match confirmed", self.GREEN)

            self.test_state.set("Proof Complete")
            self.recovery_state.set("Intact")
            self.proof_outcome.set("Attack ≠ Data Loss")
            self.result_desc.config(
                text="Recovery successful. The recovered file matches original integrity after controlled attack simulation."
            )

            self.log("Integrity verified by hash match", "SUCCESS")
            self.log("FINAL RESULT — ATTACK ≠ DATA LOSS", "SUCCESS")

            messagebox.showinfo(
                "XPADI Proof",
                "SUCCESS\n\nRecovered file matches original integrity.\n\nXPADI proved that the protected file remained recoverable after controlled attack simulation."
            )
        else:
            self._set_step("verify", "FAILED")
            self._set_stage("Integrity Verified", "Mismatch detected", self.RED)

            self.test_state.set("Mismatch")
            self.recovery_state.set("Compromised")
            self.proof_outcome.set("Verification Failed")
            self.result_desc.config(
                text="Recovery completed, but output does not match original integrity. Resilience conditions need tuning."
            )

            self.log("Integrity mismatch detected", "ERROR")

            messagebox.showerror(
                "XPADI Proof",
                "Recovery Incomplete\n\nRecovered output does not match original integrity.\n\nThe proof run completed, but resilience conditions need tuning before this attack mode can be considered successful."
            )

    def run_full_proof(self):
        if self.running:
            return

        if not self.selected_file:
            self.select_file()
            if not self.selected_file:
                return

        def task():
            self.running = True
            try:
                self.protect_file()
                self.simulate_attack()
                self.recover_file()
                self.verify_recovery()
            except Exception as e:
                self.log(f"Run failed: {e}", "ERROR")
                messagebox.showerror("XPADI Error", str(e))
            finally:
                self.running = False

        threading.Thread(target=task, daemon=True).start()

    def reset_session(self):
        self.engine = XPADIEngine()
        self.selected_file = None
        self.recovered_file = None

        self.file_label.config(text="No file selected")

        self.test_state.set("Ready")
        self.recovery_state.set("No File Loaded")
        self.proof_outcome.set("Awaiting Test")
        self.result_desc.config(
            text="This demo proves whether a protected file can be recovered after controlled attack simulation."
        )

        for key in self.step_vars:
            self._set_step(key, "IDLE")

        for title in self.stage_labels:
            self._set_stage(title, "Pending")

        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        self.log("Session reset", "SYSTEM")
        self.log("SAFE MODE ACTIVE — original source file will never be attacked", "SYSTEM")


def launch_ui():
    root = tk.Tk()
    app = XPADIProofUI(root)
    root.mainloop()