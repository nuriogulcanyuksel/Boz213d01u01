import tkinter as tk, random as r
S = {"Savaşçı": (120, 20, 4), "Büyücü": (80, 80, 1), "Haydut": (100, 40, 3)}
D = [("Goblin", 30, 10, "green"), ("İskelet", 45, 12, "ivory"), ("Ejderha", 90, 14, "red")]
w = tk.Tk(); w.title("Zindan")
f = tk.Frame(w, padx=40, pady=40); f.pack()
tk.Label(f, text="Kahraman ismi:").pack()
e = tk.Entry(f); e.pack()
tk.Label(f, text="Sınıf seç:").pack()
c = tk.Canvas(w, width=600, height=360, bg="#222")
bt = tk.Frame(w)
sh = sw = 0
mesaj = ""

def basla(k):
    global ad, hp, mp, b, mh, mm, ik, oda, dh, mesaj
    ad = e.get() or "Kahraman"
    hp, mp, b = S[k]
    mh, mm, ik, oda = hp, mp, 3, 0
    dh = D[0][1]
    mesaj = "Goblin belirdi!"
    f.pack_forget(); c.pack(); bt.pack(); ciz()

def hamle(t):
    global hp, mp, ik, dh, oda, mesaj, sh, sw
    if hp <= 0 or oda >= len(D): return
    ac = D[oda][2]
    if t == 2:
        if ik == 0: return
        ik -= 1; hp = min(mh, hp + 40); mesaj = "İksir: +40 can"
    else:
        if t == 1:
            if mp < 10: mesaj = "Mana yok!"; ciz(); return
            mp -= 10
        z = r.randint(1, 20)
        if z == 20 or (z > 1 and z + b >= ac):
            x = r.randint(1, 8) + b if t == 0 else r.randint(2, 16) + b
            x *= 2 if z == 20 else 1
            dh -= x; sw = 10; sh = 8
            mesaj = f"Zar {z}: {x} hasar!"
        else:
            mesaj = f"Zar {z}: ıska!"
    if dh <= 0:
        oda += 1
        if oda >= len(D): mesaj = "KAZANDIN!"
        else: dh = D[oda][1]; mesaj += f" {D[oda][0]} geldi!"
    else:
        z = r.randint(1, 20)
        if z == 20 or (z > 1 and z + 2 + oda >= 13):
            x = r.randint(4, 9) + oda * 3
            hp -= x; sh = 10
            mesaj += f" | Düşman {x} vurdu"
        else:
            mesaj += " | Düşman ıskaladı"
        mp = min(mm, mp + 3)
        if hp <= 0: mesaj = "ÖLDÜN..."
    anim()

def anim():
    global sh, sw
    ciz()
    sh = max(0, sh - 1); sw = max(0, sw - 1)
    if sh or sw: w.after(30, anim)
    else: ciz()

def ciz():
    c.delete("all")
    ox, oy = r.randint(-sh, sh), r.randint(-sh, sh)
    def d(s, *a, **k):
        getattr(c, "create_" + s)(*[v + (ox, oy)[i % 2] for i, v in enumerate(a)], **k)
    d("rectangle", -20, -20, 620, 200, fill="#554", width=0)
    for i in range(0, 600, 50): d("line", i, 0, i, 200, fill="#332")
    for i in range(0, 200, 25): d("line", 0, i, 600, i, fill="#332")
    d("rectangle", -20, 200, 620, 380, fill="#321", width=0)
    d("rectangle", 100, 240, 140, 310, fill="royalblue", width=0)
    d("oval", 102, 205, 138, 241, fill="tan", width=0)
    d("line", 140, 270, 175, 215, fill="lightgray", width=5)
    n, mx, _, col = D[min(oda, len(D) - 1)]
    d("rectangle", 440, 230, 510, 310, fill=col, width=0)
    d("oval", 445, 190, 505, 240, fill=col, width=0)
    d("oval", 460, 205, 470, 215, fill="yellow"); d("oval", 480, 205, 490, 215, fill="yellow")
    if sw:
        x = 400 + (10 - sw) * 12
        d("line", x, 170, x - 70, 300, fill="white", width=6)
    d("rectangle", 10, 10, 210, 24, fill="#400")
    d("rectangle", 10, 10, 10 + 200 * max(hp, 0) / mh, 24, fill="red")
    d("rectangle", 10, 28, 210, 42, fill="#004")
    d("rectangle", 10, 28, 10 + 200 * mp / mm, 42, fill="dodgerblue")
    d("rectangle", 390, 10, 590, 24, fill="#400")
    d("rectangle", 390, 10, 390 + 200 * max(dh, 0) / mx, 24, fill="orange")
    d("text", 300, 335, text=f"{ad}  Can:{hp}  Mana:{mp}  İksir:{ik}", fill="white", font=("Arial", 12))
    d("text", 300, 355, text=mesaj, fill="yellow", font=("Arial", 11))

for k in S:
    tk.Button(f, text=k, command=lambda k=k: basla(k)).pack()
for i, t in enumerate(["Saldır", "Büyü (10 mana)", "İksir"]):
    tk.Button(bt, text=t, width=14, command=lambda i=i: hamle(i)).pack(side="left", padx=5, pady=5)
w.mainloop()
