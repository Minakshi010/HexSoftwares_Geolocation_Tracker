import tkinter as tk
from tkinter import messagebox
import requests
import folium
import webbrowser
import os

def fetch_location():
    ip = entry_ip.get().strip()
    url = f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json/"

    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] != "success":
            messagebox.showerror("Error", "Invalid IP address or location not found")
            return

        lat, lon = data["lat"], data["lon"]
        city = data["city"]
        region = data["regionName"]
        country = data["country"]
        isp = data["isp"]

        lbl_ip.config(text=f"IP Address: {data['query']}")
        lbl_location.config(text=f"Location: {city}, {region}, {country}")
        lbl_isp.config(text=f"ISP: {isp}")

        # Create map
        user_map = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker(
            [lat, lon],
            popup=f"{city}, {region}, {country}",
            tooltip="Location"
        ).add_to(user_map)

        map_file = "ip_location_map.html"
        user_map.save(map_file)
        webbrowser.open("file://" + os.path.realpath(map_file))

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= GUI DESIGN ================= #

root = tk.Tk()
root.title("IP Geolocation Finder")
root.geometry("520x420")
root.configure(bg="#E8F0FE")
root.resizable(False, False)

# Main Card
card = tk.Frame(root, bg="white", bd=0, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=360)

# Title
tk.Label(
    card,
    text="🌍 IP Geolocation Finder",
    font=("Segoe UI", 18, "bold"),
    bg="white",
    fg="#1A73E8"
).pack(pady=15)

# Subtitle
tk.Label(
    card,
    text="Enter an IP address or leave blank",
    font=("Segoe UI", 10),
    bg="white",
    fg="gray"
).pack()

# IP Entry
entry_ip = tk.Entry(
    card,
    font=("Segoe UI", 12),
    width=30,
    bd=1,
    relief="solid"
)
entry_ip.pack(pady=15)

# Button
tk.Button(
    card,
    text="Find Location",
    font=("Segoe UI", 12, "bold"),
    bg="#1A73E8",
    fg="white",
    activebackground="#1558B0",
    activeforeground="white",
    bd=0,
    padx=20,
    pady=8,
    command=fetch_location
).pack(pady=10)

# Divider
tk.Frame(card, bg="#E0E0E0", height=1, width=380).pack(pady=10)

# Result Labels
lbl_ip = tk.Label(card, text="IP Address: ", font=("Segoe UI", 11), bg="white")
lbl_ip.pack(pady=5)

lbl_location = tk.Label(card, text="Location: ", font=("Segoe UI", 11), bg="white")
lbl_location.pack(pady=5)

lbl_isp = tk.Label(card, text="ISP: ", font=("Segoe UI", 11), bg="white")
lbl_isp.pack(pady=5)

# Footer
tk.Label(
    card,
    text="📌 IP-based location is approximate",
    font=("Segoe UI", 9),
    bg="white",
    fg="gray"
).pack(side="bottom", pady=10)

root.mainloop()
