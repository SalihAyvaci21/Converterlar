import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import threading
import warnings
import webbrowser
from PIL import Image, ImageOps
import numpy as np

# Uyarıları gizle
warnings.filterwarnings("ignore")

class SalihAtolyeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Salih'in Dijital Atölyesi v3.4 (Visual Edition)")
        self.root.geometry("1150x900")
        
        # --- TEMA AYARLARI ---
        self.setup_theme()

        # --- YENİ DİRENÇ VERİ YAPISI (Görsel Renk Kodlarıyla Beraber) ---
        # Hem hesaplama değerlerini hem de HEX renk kodlarını tek yapıda tutuyoruz.
        self.RES_DATA = {
            "Siyah":   {"val": 0, "mul": 1,         "tol": None, "hex": "#000000", "font": "white"},
            "Kahve":   {"val": 1, "mul": 10,        "tol": 1,    "hex": "#8B4513", "font": "white"},
            "Kırmızı": {"val": 2, "mul": 100,       "tol": 2,    "hex": "#FF0000", "font": "white"},
            "Turuncu": {"val": 3, "mul": 1000,      "tol": None, "hex": "#FFA500", "font": "black"},
            "Sarı":    {"val": 4, "mul": 10000,     "tol": None, "hex": "#FFFF00", "font": "black"},
            "Yeşil":   {"val": 5, "mul": 100000,    "tol": 0.5,  "hex": "#008000", "font": "white"},
            "Mavi":    {"val": 6, "mul": 1000000,   "tol": 0.25, "hex": "#0000FF", "font": "white"},
            "Mor":     {"val": 7, "mul": 10000000,  "tol": 0.1,  "hex": "#800080", "font": "white"},
            "Gri":     {"val": 8, "mul": None,      "tol": 0.05, "hex": "#808080", "font": "white"},
            "Beyaz":   {"val": 9, "mul": None,      "tol": None, "hex": "#FFFFFF", "font": "black"},
            "Altın":   {"val": None, "mul": 0.1,    "tol": 5,    "hex": "#FFD700", "font": "black"},
            "Gümüş":   {"val": None, "mul": 0.01,   "tol": 10,   "hex": "#C0C0C0", "font": "black"},
        }
        
        # Dropdown listeleri için anahtarlar
        self.keys_digit = [k for k, v in self.RES_DATA.items() if v['val'] is not None]
        self.keys_mult = [k for k, v in self.RES_DATA.items() if v['mul'] is not None]
        self.keys_tol = [k for k, v in self.RES_DATA.items() if v['tol'] is not None]

        # --- NOTA SÖZLÜĞÜ ---
        self.NOTE_MAP = {
            'sus': '0000', '.': '0000',
            'do': '4A8B', 'do#': '4676', 're': '426E', 're#': '3ECC',
            'mi': '3B2F', 'fa': '37F6', 'fa#': '34C9', 'sol': '31D3',
            'sol#': '2F07', 'a': '2C63', 'ad': '29E6', 'b': '2789',
            'c': '2558', 'cd': '233B', 'd': '2141', 'dd': '1F63',
            'e': '1D9F', 'f': '1BFA', 'fd': '1A64', 'g': '191B',
            'gd': '1788', 'a2': '162C', 'ad2': '14F3', 'b2': '13C4',
            'c2': '12A8', 'cd2': '119C', 'd2': '109F', 'dd2': '0FB1',
            'e2': '0ED0', 'f2': '0DFD', 'fd2': '0D36', 'g2': '0C7D',
            'gd2': '0BD1', 'a3': '0B2B'
        }
        self.HEX_TO_NOTE_MAP = {v: k for k, v in self.NOTE_MAP.items()}
        
        # --- ANA SEKME YAPISI ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Sekmeleri Oluştur
        self.create_converter_tab()    # 1. Dosya & Medya
        self.create_fpga_tab()         # 2. FPGA & Gömülü
        self.create_component_tab()    # 3. Komponent Hesaplayıcılar (YENİLENDİ)
        self.create_utils_tab()        # 4. STL & QR
        
        # --- ALT BİLGİ & İMZA ---
        self.create_footer()

    def setup_theme(self):
        self.bg_color = "#2b2b2b"
        self.root.configure(bg=self.bg_color)
        style = ttk.Style()
        style.theme_use('clam') 
        BG_COLOR, FG_COLOR, ACCENT_COLOR = "#2b2b2b", "#ffffff", "#00ced1"
        FRAME_BG, BTN_BG = "#333333", "#444444"
        style.configure(".", background=BG_COLOR, foreground=FG_COLOR, font=("Segoe UI", 10))
        style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", background="#444", foreground="white", padding=[15, 5], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", ACCENT_COLOR)], foreground=[("selected", "black")])
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabelframe", background=FRAME_BG, relief="flat")
        style.configure("TLabelframe.Label", background=FRAME_BG, foreground=ACCENT_COLOR, font=("Segoe UI", 11, "bold"))
        style.configure("TLabel", background=FRAME_BG, foreground=FG_COLOR)
        style.configure("TButton", background=BTN_BG, foreground="white", borderwidth=1, focuscolor="none")
        style.map("TButton", background=[('active', ACCENT_COLOR)], foreground=[('active', 'black')])
        style.configure("TEntry", fieldbackground="#555", foreground="white", insertcolor="white")
        style.configure("TRadiobutton", background=FRAME_BG, foreground="white", font=("Segoe UI", 10))
        # Custom style for result labels
        style.configure("Result.TLabel", font=("Consolas", 14, "bold"), foreground="#00ff00", background="#222")

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg=self.bg_color)
        footer_frame.pack(side="bottom", fill="x", padx=15, pady=5)
        
        version_text = f"Python: {sys.version.split()[0]} | System: {sys.platform}"
        tk.Label(footer_frame, text=version_text, bg=self.bg_color, fg="#666", font=("Arial", 8)).pack(side="left")
        
        credits_frame = tk.Frame(footer_frame, bg=self.bg_color)
        credits_frame.pack(side="right")
        tk.Label(credits_frame, text="Design by Salih Tekin Ayvacı", bg=self.bg_color, fg="white", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 15))

        def add_link(text, url, color):
            link = tk.Label(credits_frame, text=text, bg=self.bg_color, fg=color, cursor="hand2", font=("Segoe UI", 9, "bold"))
            link.pack(side="left", padx=5)
            link.bind("<Button-1>", lambda e: webbrowser.open(url))

        # --- LİNKLER ---
        add_link("GitHub", "https://github.com/SalihAyvaci21", "#cccccc")
        add_link("LinkedIn", "https://linkedin.com/in/salih-tekin-ayvaci", "#0077b5")
        add_link("Instagram", "https://instagram.com/salih_ayvaci21", "#e1306c")

    # =========================================================================
    # SEKME 1: DÖNÜŞTÜRÜCÜLER
    # =========================================================================
    def create_converter_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dönüştürücüler")
        tab.columnconfigure(0, weight=1); tab.columnconfigure(1, weight=1)

        # SOL: Belge
        frame_doc = ttk.LabelFrame(tab, text="Belge (Word/PDF)")
        frame_doc.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ttk.Button(frame_doc, text="Word -> PDF", command=lambda: self.run_doc_conversion("w2p")).pack(fill="x", padx=20, pady=5)
        ttk.Button(frame_doc, text="PDF -> Word", command=lambda: self.run_doc_conversion("p2w")).pack(fill="x", padx=20, pady=5)
        ttk.Separator(frame_doc, orient="horizontal").pack(fill="x", padx=10, pady=10)
        ttk.Button(frame_doc, text="Resim -> PDF Yap", command=self.img_to_pdf).pack(fill="x", padx=20, pady=5)
        self.lbl_doc_status = ttk.Label(frame_doc, text="Durum: Hazır", foreground="gray")
        self.lbl_doc_status.pack(pady=10)
        self.progress_doc = ttk.Progressbar(frame_doc, mode="indeterminate")

        # SAĞ: Medya
        frame_media = ttk.LabelFrame(tab, text="Medya (Resim/Video)")
        frame_media.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        sub_vid = ttk.Frame(frame_media); sub_vid.pack(fill="x", padx=10, pady=10)
        ttk.Label(sub_vid, text="Video -> GIF (FPS):").pack(side="left")
        self.entry_fps = ttk.Entry(sub_vid, width=5); self.entry_fps.insert(0, "10"); self.entry_fps.pack(side="left", padx=5)
        ttk.Button(sub_vid, text="Dönüştür", command=self.run_video_conversion).pack(side="right", fill="x", expand=True)
        ttk.Separator(frame_media, orient="horizontal").pack(fill="x", padx=10, pady=10)
        sub_img = ttk.Frame(frame_media); sub_img.pack(fill="x", padx=10, pady=10)
        self.combo_format = ttk.Combobox(sub_img, values=["png", "jpg", "webp", "bmp", "ico"], state="readonly", width=8); self.combo_format.set("png"); self.combo_format.pack(side="left", padx=5)
        ttk.Button(sub_img, text="Format Çevir", command=self.convert_image_format).pack(side="right", fill="x", expand=True)

    # =========================================================================
    # SEKME 2: FPGA & GÖMÜLÜ SİSTEMLER
    # =========================================================================
    def create_fpga_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="FPGA & Gömülü")
        tab.columnconfigure(0, weight=1); tab.columnconfigure(1, weight=1); tab.columnconfigure(2, weight=1)

        # KOLON 1
        col1 = ttk.Frame(tab); col1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame_base = ttk.LabelFrame(col1, text="Taban Çevirici"); frame_base.pack(fill="x", pady=5)
        self.var_dec = tk.StringVar(); self.var_hex = tk.StringVar(); self.var_bin = tk.StringVar()
        for lbl, var in [("DEC:", self.var_dec), ("HEX:", self.var_hex), ("BIN:", self.var_bin)]:
            f = ttk.Frame(frame_base); f.pack(fill="x", padx=5, pady=2)
            ttk.Label(f, text=lbl, width=5).pack(side="left")
            ttk.Entry(f, textvariable=var).pack(side="left", fill="x", expand=True)
        self.updating = False
        self.var_dec.trace_add("write", lambda *args: self.convert_base("dec"))
        self.var_hex.trace_add("write", lambda *args: self.convert_base("hex"))
        self.var_bin.trace_add("write", lambda *args: self.convert_base("bin"))
        ttk.Button(frame_base, text="Temizle", command=self.clear_bases).pack(pady=5)

        frame_timer = ttk.LabelFrame(col1, text="Timer Hesaplayıcı"); frame_timer.pack(fill="x", pady=5)
        ttk.Label(frame_timer, text="Sistem MHz:").pack(anchor="w", padx=5)
        self.entry_sys_clk = ttk.Entry(frame_timer); self.entry_sys_clk.insert(0, "27"); self.entry_sys_clk.pack(fill="x", padx=5)
        ttk.Label(frame_timer, text="Hedef Hz/Baud:").pack(anchor="w", padx=5)
        self.entry_target_freq = ttk.Entry(frame_timer); self.entry_target_freq.insert(0, "9600"); self.entry_target_freq.pack(fill="x", padx=5)
        ttk.Button(frame_timer, text="Hesapla", command=self.calc_timer).pack(pady=5)
        self.lbl_timer_res = ttk.Label(frame_timer, text="-", foreground="#00ced1"); self.lbl_timer_res.pack(pady=5)

        # KOLON 2
        col2 = ttk.Frame(tab); col2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        frame_imgh = ttk.LabelFrame(col2, text="Resim <-> Hex"); frame_imgh.pack(fill="x", pady=5)
        ttk.Button(frame_imgh, text="Resim -> Hex", command=self.img_to_hex).pack(fill="x", padx=10, pady=5)
        ttk.Button(frame_imgh, text="Hex -> Resim", command=self.hex_to_img).pack(fill="x", padx=10, pady=5)

        frame_note = ttk.LabelFrame(col2, text="Müzik Notası"); frame_note.pack(fill="both", expand=True, pady=5)
        self.txt_notes = scrolledtext.ScrolledText(frame_note, height=10, bg="#444", fg="white", insertbackground="white"); self.txt_notes.pack(fill="both", expand=True, padx=5, pady=5)
        ttk.Button(frame_note, text="Song.hex Oluştur", command=self.notes_to_hex).pack(fill="x", padx=5, pady=2)
        ttk.Button(frame_note, text="Hex Oku", command=self.hex_to_notes).pack(fill="x", padx=5, pady=2)

        # KOLON 3
        col3 = ttk.Frame(tab); col3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        frame_seg = ttk.LabelFrame(col3, text="7-Segment"); frame_seg.pack(fill="x", pady=5)
        self.seg_canvas = tk.Canvas(frame_seg, width=120, height=160, bg="#222", highlightthickness=0); self.seg_canvas.pack(pady=5)
        self.segments = {'A': [30, 15, 90, 25], 'B': [90, 25, 100, 75], 'C': [90, 85, 100, 135], 'D': [30, 135, 90, 145], 'E': [20, 85, 30, 135], 'F': [20, 25, 30, 75], 'G': [30, 75, 90, 85], 'DP': [105, 135, 115, 145]}
        self.seg_state = {k: False for k in self.segments}; self.seg_ids = {}
        for name, coords in self.segments.items():
            rect_id = self.seg_canvas.create_rectangle(coords, fill="#333", outline="#555", tags=name)
            self.seg_ids[name] = rect_id
            self.seg_canvas.tag_bind(rect_id, '<Button-1>', lambda e, n=name: self.toggle_segment(n))
        self.lbl_hex_ca = ttk.Label(frame_seg, text="CA: 0xFF", font=("Consolas", 9)); self.lbl_hex_ca.pack()
        self.lbl_hex_cc = ttk.Label(frame_seg, text="CC: 0x00", font=("Consolas", 9)); self.lbl_hex_cc.pack()

        frame_rgb = ttk.LabelFrame(col3, text="RGB565 Renk"); frame_rgb.pack(fill="x", pady=5)
        ttk.Button(frame_rgb, text="Renk Seç", command=self.open_color_picker).pack(pady=5)
        self.lbl_color_preview = tk.Label(frame_rgb, text="   ", bg="black", width=10); self.lbl_color_preview.pack()
        self.lbl_rgb565_hex = ttk.Label(frame_rgb, text="Hex: -", font=("Consolas", 10)); self.lbl_rgb565_hex.pack(pady=2)

    # =========================================================================
    # SEKME 3: KOMPONENTLER (YENİLENMİŞ GÖRSEL DİRENÇ)
    # =========================================================================
    def create_component_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Komponentler")
        tab.columnconfigure(0, weight=6) # Sol taraf geniş
        tab.columnconfigure(1, weight=4) # Sağ taraf

        # --- SOL TARAF: DİNAMİK DİRENÇ HESAPLAYICI ---
        frame_res = ttk.LabelFrame(tab, text="Görsel Direnç Hesaplayıcı (3-4-5 Bant)")
        frame_res.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # 1. Bant Sayısı Seçimi
        self.band_mode = tk.IntVar(value=3)
        frm_mode = ttk.Frame(frame_res)
        frm_mode.pack(pady=10)
        ttk.Label(frm_mode, text="Bant Sayısı:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        for m in [3, 4, 5]:
            ttk.Radiobutton(frm_mode, text=f"{m} Bant", variable=self.band_mode, value=m, 
                            command=self.update_resistor_ui).pack(side="left", padx=10)

        # 2. Canvas (Görsel Çizim)
        # Arka plan rengini frame ile uyumlu yapıyoruz (#333333)
        self.res_canvas = tk.Canvas(frame_res, width=500, height=150, bg="#333333", highlightthickness=0)
        self.res_canvas.pack(pady=15)
        
        # 3. Sonuç Ekranı
        self.lbl_res_result = ttk.Label(frame_res, text="---", style="Result.TLabel", anchor="center")
        self.lbl_res_result.pack(fill="x", padx=50, pady=10)

        # 4. Seçim Kutuları (Comboboxes)
        self.frm_combos = ttk.Frame(frame_res)
        self.frm_combos.pack(pady=10)

        labels = ["1. Bant", "2. Bant", "3. Bant", "Çarpan", "Tolerans"]
        self.res_combos = []
        self.res_frames = [] # Widgetları gizlemek için frame referansları

        for i, label_text in enumerate(labels):
            f = ttk.Frame(self.frm_combos)
            f.pack(side="left", padx=5)
            self.res_frames.append(f)
            
            ttk.Label(f, text=label_text, font=("Arial", 8)).pack()
            
            cb = ttk.Combobox(f, state="readonly", width=10)
            
            # İçerik Doldurma
            if i < 3: values = self.keys_digit # Rakamlar
            elif i == 3: values = self.keys_mult # Çarpan
            else: values = self.keys_tol # Tolerans
            
            cb['values'] = values
            # Varsayılanlar
            if i == 0: cb.set("Kahve")
            elif i == 1: cb.set("Siyah")
            elif i == 2: cb.set("Siyah")
            elif i == 3: cb.set("Kahve") # x10
            elif i == 4: cb.set("Altın") # %5

            cb.bind("<<ComboboxSelected>>", self.calculate_resistor)
            cb.pack()
            self.res_combos.append(cb)

        # İlk Başlatma
        self.draw_resistor_bg()
        self.update_resistor_ui()

        # --- SAĞ TARAF: SMD KOD ÇÖZÜCÜ ---
        frame_smd = ttk.LabelFrame(tab, text="SMD Kod Çözücü")
        frame_smd.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ttk.Label(frame_smd, text="SMD Direnç (Örn: 103, 4R7):").pack(pady=(20,5))
        self.entry_smd_res = ttk.Entry(frame_smd, font=("Consolas", 11)); self.entry_smd_res.pack(fill="x", padx=20)
        ttk.Button(frame_smd, text="Çöz", command=self.calc_smd_resistor).pack(pady=5)
        self.lbl_smd_res_result = ttk.Label(frame_smd, text="-", foreground="#00ced1", font=("Consolas", 12)); self.lbl_smd_res_result.pack(pady=5)

        ttk.Separator(frame_smd, orient="horizontal").pack(fill="x", pady=20, padx=10)

        ttk.Label(frame_smd, text="SMD Kapasitör (Örn: 104):").pack(pady=(5,5))
        self.entry_smd_cap = ttk.Entry(frame_smd, font=("Consolas", 11)); self.entry_smd_cap.pack(fill="x", padx=20)
        ttk.Button(frame_smd, text="Çöz", command=self.calc_smd_capacitor).pack(pady=5)
        self.lbl_smd_cap_result = ttk.Label(frame_smd, text="-", foreground="#00ced1", font=("Consolas", 12)); self.lbl_smd_cap_result.pack(pady=5)

    # --- DİRENÇ MANTIĞI & GÖRSELİ ---
    def draw_resistor_bg(self):
        """Direnç gövdesini ve tellerini çizer (Bantlar hariç)"""
        self.res_canvas.delete("bg") # Sadece arka planı sil
        # Tel
        self.res_canvas.create_line(20, 75, 480, 75, width=8, fill="#999", tags="bg")
        # Gövde (Hap şeklinde) - Bej renk
        self.res_canvas.create_line(100, 75, 400, 75, width=90, capstyle=tk.ROUND, fill="#e8c694", tags="bg")
        # Parlama efekti (Basit)
        self.res_canvas.create_line(100, 55, 400, 55, width=20, capstyle=tk.ROUND, fill="#f0dcb8", tags="bg")

    def update_resistor_ui(self):
        """Mod değişiminde arayüz elemanlarını gizler/gösterir"""
        mode = self.band_mode.get()
        
        # 3. Bant (Rakam) -> index 2
        # Tolerans -> index 4
        
        if mode == 3:
            self.res_frames[2].pack_forget() # 3. Rakam Yok
            self.res_frames[4].pack_forget() # Tolerans Yok (Sabit)
        elif mode == 4:
            self.res_frames[2].pack_forget() # 3. Rakam Yok
            self.res_frames[4].pack(side="left", padx=5) # Tolerans Var
        elif mode == 5:
            self.res_frames[2].pack(side="left", padx=5, before=self.res_frames[3]) # 3. Rakam Var
            self.res_frames[4].pack(side="left", padx=5) # Tolerans Var
            
        self.calculate_resistor()

    def calculate_resistor(self, event=None):
        mode = self.band_mode.get()
        
        c1 = self.res_combos[0].get()
        c2 = self.res_combos[1].get()
        c3 = self.res_combos[2].get()
        cmult = self.res_combos[3].get()
        ctol = self.res_combos[4].get()

        val1 = self.RES_DATA[c1]['val']
        val2 = self.RES_DATA[c2]['val']
        val3 = self.RES_DATA[c3]['val']
        multiplier = self.RES_DATA[cmult]['mul']
        
        resistance = 0
        tol_text = ""
        visual_colors = []

        if mode == 3:
            resistance = (val1 * 10 + val2) * multiplier
            tol_text = "±20%"
            visual_colors = [c1, c2, cmult]
            
        elif mode == 4:
            resistance = (val1 * 10 + val2) * multiplier
            t_val = self.RES_DATA[ctol]['tol']
            tol_text = f"±{t_val}%"
            visual_colors = [c1, c2, cmult, ctol]
            
        elif mode == 5:
            resistance = (val1 * 100 + val2 * 10 + val3) * multiplier
            t_val = self.RES_DATA[ctol]['tol']
            tol_text = f"±{t_val}%"
            visual_colors = [c1, c2, c3, cmult, ctol]

        # Sonuç Metni Formatlama
        if resistance >= 1e6: res_str = f"{resistance/1e6:g} MΩ"
        elif resistance >= 1e3: res_str = f"{resistance/1e3:g} kΩ"
        else: res_str = f"{resistance:g} Ω"
        
        self.lbl_res_result.config(text=f"{res_str} {tol_text}")

        # Görseli Güncelle
        self.update_resistor_visuals(mode, visual_colors)

    def update_resistor_visuals(self, mode, color_names):
        self.res_canvas.delete("band") # Eski bantları sil
        
        # Pozisyonlar (Canvas üzerinde x koordinatları)
        if mode == 3:
            positions = [130, 180, 250] # 3. renk biraz ayrık
        elif mode == 4:
            positions = [130, 170, 240, 360] # Tolerans en sağda
        else: # 5 bant
            positions = [120, 160, 200, 270, 370]
            
        for i, c_name in enumerate(color_names):
            hex_code = self.RES_DATA[c_name]['hex']
            x = positions[i]
            # Bant Çizimi (Dikey çizgi ama kalın)
            # Gövde y=75, kalınlık 90 -> y aralığı 30 ile 120
            self.res_canvas.create_line(x, 30, x, 120, width=15, fill=hex_code, tags="band")

    # =========================================================================
    # SEKME 4: ARAÇLAR (STL, QR, Lithophane)
    # =========================================================================
    def create_utils_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Araçlar")
        
        frame_stl = ttk.LabelFrame(tab, text="3D Araçlar (STL)")
        frame_stl.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ttk.Button(frame_stl, text="STL Dosyasını Görüntüle (PNG)", command=self.run_stl_to_png).pack(fill="x", padx=20, pady=10)
        ttk.Separator(frame_stl, orient="horizontal").pack(fill="x", padx=10, pady=5)
        ttk.Label(frame_stl, text="Resim -> STL (Lithophane)").pack(pady=5)
        ttk.Button(frame_stl, text="Resim Seç ve STL Yap", command=self.run_img_to_stl).pack(fill="x", padx=20, pady=10)

        frame_qr = ttk.LabelFrame(tab, text="QR Kod"); frame_qr.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        ttk.Label(frame_qr, text="Metin:").pack(); self.entry_qr_text = ttk.Entry(frame_qr); self.entry_qr_text.pack(fill="x", padx=10, pady=5)
        ttk.Button(frame_qr, text="QR Kaydet", command=self.run_qr_generator).pack(fill="x", padx=30, pady=10)

    # =========================================================================
    # LOGIC FUNCTIONS (DİĞERLERİ AYNI)
    # =========================================================================
    
    def calc_smd_resistor(self):
        c = self.entry_smd_res.get().upper()
        try:
            if 'R' in c: val = float(c.replace('R', '.'))
            else: val = int(c[:-1]) * (10**int(c[-1]))
            if val >= 1e6: s = f"{val/1e6:g} MΩ"
            elif val >= 1e3: s = f"{val/1e3:g} kΩ"
            else: s = f"{val:g} Ω"
            self.lbl_smd_res_result.config(text=s)
        except: self.lbl_smd_res_result.config(text="Hata")

    def calc_smd_capacitor(self):
        c = self.entry_smd_cap.get()
        try:
            pf = float(c) if len(c)<3 else int(c[:-1])*(10**int(c[-1]))
            if pf>=1e6: s=f"{pf/1e6:.2f} uF"
            elif pf>=1e3: s=f"{pf/1e3:.2f} nF"
            else: s=f"{pf:.0f} pF"
            self.lbl_smd_cap_result.config(text=s)
        except: self.lbl_smd_cap_result.config(text="Hata")

    # --- ESKİ FONKSİYONLARIN DEVAMI (Değişiklik Yok) ---
    def run_doc_conversion(self, mode):
        fp = filedialog.askopenfilename()
        if not fp: return
        self.lbl_doc_status.config(text="İşleniyor...", foreground="orange")
        self.progress_doc.start()
        threading.Thread(target=self.thread_doc_safe, args=(fp, mode), daemon=True).start()

    def thread_doc_safe(self, input_path, mode):
        try:
            if mode == "w2p":
                from docx2pdf import convert
                convert(input_path, os.path.splitext(input_path)[0] + ".pdf")
            else:
                from pdf2docx import Converter
                cv = Converter(input_path); cv.convert(os.path.splitext(input_path)[0] + ".docx"); cv.close()
            self.root.after(0, lambda: messagebox.showinfo("Bitti", "Dönüştürme Başarılı"))
            self.root.after(0, lambda: self.lbl_doc_status.config(text="Tamamlandı", foreground="#00ced1"))
        except Exception as e: self.root.after(0, lambda: messagebox.showerror("Hata", str(e)))
        finally: self.root.after(0, self.progress_doc.stop)

    def img_to_pdf(self):
        fp = filedialog.askopenfilename(filetypes=[("Resim", "*.jpg;*.png;*.bmp")])
        if not fp: return
        sp = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not sp: return
        try:
            img = Image.open(fp).convert('RGB')
            img.save(sp)
            messagebox.showinfo("Başarılı", "PDF Oluşturuldu")
        except Exception as e: messagebox.showerror("Hata", str(e))

    def run_video_conversion(self):
        fp = filedialog.askopenfilename(); 
        if not fp: return
        sp = filedialog.asksaveasfilename(defaultextension=".gif")
        if not sp: return
        threading.Thread(target=self.thread_video_safe, args=(fp, sp, int(self.entry_fps.get())), daemon=True).start()

    def thread_video_safe(self, fp, sp, fps):
        try:
            from moviepy.editor import VideoFileClip
            c = VideoFileClip(fp); c.write_gif(sp, fps=fps, logger=None); c.close()
            self.root.after(0, lambda: messagebox.showinfo("Bitti", "GIF Hazır"))
        except Exception as e: self.root.after(0, lambda: messagebox.showerror("Hata", str(e)))

    def convert_image_format(self):
        fp = filedialog.askopenfilename()
        if not fp: return
        try:
            img = Image.open(fp)
            t = self.combo_format.get()
            if t in ['jpg', 'jpeg']: img = img.convert('RGB')
            img.save(os.path.splitext(fp)[0] + "_new." + t)
            messagebox.showinfo("Bitti", "Resim Dönüştürüldü")
        except Exception as e: messagebox.showerror("Hata", str(e))

    def convert_base(self, source):
        if self.updating: return
        self.updating = True
        try:
            val = 0
            if source == "dec": val = int(self.var_dec.get())
            elif source == "hex": val = int(self.var_hex.get(), 16)
            elif source == "bin": val = int(self.var_bin.get(), 2)
            if source != "dec": self.var_dec.set(str(val))
            if source != "hex": self.var_hex.set(hex(val).upper().replace("0X", ""))
            if source != "bin": self.var_bin.set(bin(val).replace("0b", ""))
        except: pass
        finally: self.updating = False

    def clear_bases(self): self.updating = True; self.var_dec.set(""); self.var_hex.set(""); self.var_bin.set(""); self.updating = False

    def calc_timer(self):
        try:
            sys = float(self.entry_sys_clk.get()) * 1e6; target = float(self.entry_target_freq.get())
            if target > 0: cnt = int(sys/target); self.lbl_timer_res.config(text=f"Count: {cnt} (0x{cnt:X})")
        except: self.lbl_timer_res.config(text="Hata")

    def img_to_hex(self):
        fp = filedialog.askopenfilename(); 
        if not fp: return
        sp = filedialog.asksaveasfilename(defaultextension=".hex")
        if not sp: return
        try:
            img = Image.open(fp).resize((128,64)).convert('1'); px = img.load(); lines = []
            for r in range(1024):
                pg, cl = divmod(r, 128); val = 0
                for i in range(8):
                    if px[cl, pg*8+i]: val |= (1<<i)
                lines.append(f"{val:02x}")
            with open(sp, 'w') as f: f.write("\n".join(lines))
            messagebox.showinfo("Bitti", "Hex Oluşturuldu")
        except Exception as e: messagebox.showerror("Hata", str(e))

    def hex_to_img(self):
        fp = filedialog.askopenfilename(); 
        if not fp: return
        sp = filedialog.asksaveasfilename(defaultextension=".png")
        if not sp: return
        try:
            img = Image.new('1', (128,64)); px = img.load()
            with open(fp) as f: lines = [l.strip() for l in f if l.strip()]
            r = 0
            for l in lines:
                if r >= 1024: break
                val = int(l, 16); pg, cl = divmod(r, 128)
                for i in range(8):
                    if (val>>i)&1: px[cl, pg*8+i] = 1
                r+=1
            img.save(sp)
            messagebox.showinfo("Bitti", "Resim Oluşturuldu")
        except Exception as e: messagebox.showerror("Hata", str(e))
    
    def notes_to_hex(self):
        raw = self.txt_notes.get("1.0", "end").replace("\n", " ").replace(",", " ").split()
        out = [self.NOTE_MAP[n.lower()] for n in raw if n.lower() in self.NOTE_MAP]
        sp = filedialog.asksaveasfilename(defaultextension=".hex")
        if sp and out:
            with open(sp, 'w') as f: f.write("\n".join(out))
            messagebox.showinfo("Bitti", f"{len(out)} nota kaydedildi")

    def hex_to_notes(self):
        fp = filedialog.askopenfilename()
        if not fp: return
        try:
            with open(fp) as f: lines = [l.strip().upper() for l in f if l.strip()]
            dec = [self.HEX_TO_NOTE_MAP.get(h, f"[{h}??]") for h in lines]
            self.txt_notes.delete("1.0", "end"); self.txt_notes.insert("1.0", " ".join(dec))
        except: messagebox.showerror("Hata", "Dosya okunamadı")

    def toggle_segment(self, name):
        self.seg_state[name] = not self.seg_state[name]
        self.seg_canvas.itemconfig(self.seg_ids[name], fill="#00ced1" if self.seg_state[name] else "#333")
        val = 0
        bit = {'A':1, 'B':2, 'C':4, 'D':8, 'E':16, 'F':32, 'G':64, 'DP':128}
        for k, v in self.seg_state.items():
            if v: val |= bit[k]
        self.lbl_hex_cc.config(text=f"CC: 0x{val:02X}")
        self.lbl_hex_ca.config(text=f"CA: 0x{(~val)&0xFF:02X}")

    def open_color_picker(self):
        from tkinter import colorchooser
        c = colorchooser.askcolor()
        if c and c[0]:
            r,g,b = [int(x) for x in c[0]]
            self.lbl_color_preview.config(bg=c[1])
            rgb565 = ((r>>3)<<11) | ((g>>2)<<5) | (b>>3)
            self.lbl_rgb565_hex.config(text=f"Hex: 0x{rgb565:04X}")

    def run_stl_to_png(self):
        fp = filedialog.askopenfilename(filetypes=[("STL", "*.stl")])
        if not fp: return
        sp = filedialog.asksaveasfilename(defaultextension=".png")
        if not sp: return
        threading.Thread(target=self.thread_stl_safe, args=(fp, sp), daemon=True).start()

    def set_axes_equal(self, ax):
        try:
            import numpy as np
            x_limits = ax.get_xlim3d(); y_limits = ax.get_ylim3d(); z_limits = ax.get_zlim3d()
            x_range = abs(x_limits[1] - x_limits[0]); x_middle = np.mean(x_limits)
            y_range = abs(y_limits[1] - y_limits[0]); y_middle = np.mean(y_limits)
            z_range = abs(z_limits[1] - z_limits[0]); z_middle = np.mean(z_limits)
            plot_radius = 0.5 * max([x_range, y_range, z_range])
            ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
            ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
            ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
        except: pass

    def thread_stl_safe(self, fp, sp):
        try:
            from stl import mesh; from mpl_toolkits import mplot3d; import matplotlib.pyplot as plt; import numpy as np
            plt.switch_backend('Agg')
            ym = mesh.Mesh.from_file(fp)
            fig = plt.figure(figsize=(10,8)); fig.suptitle(f"STL: {os.path.basename(fp)}", fontsize=16)
            views = [{'pos': 221, 'title': 'Top', 'elev': 90, 'azim': -90}, {'pos': 222, 'title': 'Iso', 'elev': 30, 'azim': 45}, {'pos': 223, 'title': 'Front', 'elev': 0, 'azim': -90}, {'pos': 224, 'title': 'Side', 'elev': 0, 'azim': 0}]
            for v in views:
                ax = fig.add_subplot(v['pos'], projection='3d'); ax.set_title(v['title'])
                pc = mplot3d.art3d.Poly3DCollection(ym.vectors, facecolors='#00ced1', edgecolors='#00ced1', linewidths=0, alpha=1.0, shade=True)
                ax.add_collection3d(pc); s = ym.points.flatten(); ax.auto_scale_xyz(s, s, s); self.set_axes_equal(ax)
                ax.view_init(elev=v['elev'], azim=v['azim']); ax.set_axis_off()
            plt.tight_layout(); plt.savefig(sp, dpi=150); plt.close()
            self.root.after(0, lambda: messagebox.showinfo("Bitti", "STL Kaydedildi"))
        except Exception as e: err = str(e); print(err); self.root.after(0, lambda: messagebox.showerror("Hata", err))

    def run_img_to_stl(self):
        fp = filedialog.askopenfilename(filetypes=[("Resim", "*.jpg;*.png")])
        if not fp: return
        sp = filedialog.asksaveasfilename(defaultextension=".stl")
        if not sp: return
        threading.Thread(target=self.thread_img_to_stl, args=(fp, sp), daemon=True).start()

    def thread_img_to_stl(self, fp, sp):
        try:
            from stl import mesh
            width_mm = 100; thickness = 3; min_thick = 0.8
            img = Image.open(fp).convert('L'); img = ImageOps.invert(img)
            base_width = 200; w_percent = (base_width / float(img.size[0])); h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((base_width, h_size), Image.LANCZOS)
            img_array = np.array(img); height, width = img_array.shape
            z_heights = (img_array / 255.0) * (thickness - min_thick) + min_thick
            faces = []
            for y in range(height - 1):
                for x in range(width - 1):
                    x_scale = width_mm / width; y_scale = (width_mm * (height/width)) / height
                    v1 = [x * x_scale, y * y_scale, z_heights[y, x]]
                    v2 = [(x+1) * x_scale, y * y_scale, z_heights[y, x+1]]
                    v3 = [x * x_scale, (y+1) * y_scale, z_heights[y+1, x]]
                    v4 = [(x+1) * x_scale, (y+1) * y_scale, z_heights[y+1, x+1]]
                    faces.append([v1, v3, v2]); faces.append([v2, v3, v4])
            faces_np = np.array(faces)
            model_mesh = mesh.Mesh(np.zeros(faces_np.shape[0], dtype=mesh.Mesh.dtype)); model_mesh.vectors = faces_np
            model_mesh.save(sp)
            self.root.after(0, lambda: messagebox.showinfo("Başarılı", "Lithophane STL oluşturuldu!"))
        except Exception as e: err = str(e); self.root.after(0, lambda: messagebox.showerror("Hata", f"STL Hatası:\n{err}"))

    def run_qr_generator(self):
        d = self.entry_qr_text.get()
        if not d: return
        sp = filedialog.asksaveasfilename(defaultextension=".png")
        if not sp: return
        try:
            import qrcode; qr = qrcode.QRCode(box_size=10, border=4); qr.add_data(d); qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white"); img.save(sp)
            messagebox.showinfo("Bitti", "QR Oluşturuldu")
        except Exception as e: messagebox.showerror("Hata", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SalihAtolyeApp(root)
    root.mainloop()
