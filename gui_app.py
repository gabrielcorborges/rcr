"""Tkinter GUI for generating LATAM and Azul flight links."""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from typing import List

from flight_links import (
    IATAValidationError,
    export_csv,
    export_excel,
    export_json,
    generate_flight_links,
    results_to_dicts,
)


class FlightLinkApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Gerador de Links LATAM & Azul")
        self.geometry("900x700")

        self._build_form()
        self._build_results()

    def _build_form(self) -> None:
        form = ttk.Frame(self)
        form.pack(fill="x", padx=16, pady=12)

        ttk.Label(form, text="Origens (separadas por vírgula)").grid(row=0, column=0, sticky="w")
        self.origins_entry = ttk.Entry(form, width=50)
        self.origins_entry.grid(row=0, column=1, sticky="ew", padx=8)

        ttk.Label(form, text="Destino").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.destination_entry = ttk.Entry(form, width=10)
        self.destination_entry.grid(row=1, column=1, sticky="w", padx=8, pady=(8, 0))

        self.swap_button = ttk.Button(form, text="Inverter Origem/Destino", command=self._swap_routes)
        self.swap_button.grid(row=1, column=2, sticky="w", padx=8, pady=(8, 0))

        ttk.Label(form, text="Data ida (YYYY-MM-DD)").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.outbound_entry = ttk.Entry(form, width=15)
        self.outbound_entry.grid(row=2, column=1, sticky="w", padx=8, pady=(8, 0))

        ttk.Label(form, text="Data volta (YYYY-MM-DD)").grid(row=3, column=0, sticky="w", pady=(8, 0))
        self.inbound_entry = ttk.Entry(form, width=15)
        self.inbound_entry.grid(row=3, column=1, sticky="w", padx=8, pady=(8, 0))

        self.swap_dates_button = ttk.Button(form, text="Inverter Datas", command=self._swap_dates)
        self.swap_dates_button.grid(row=3, column=2, sticky="w", padx=8, pady=(8, 0))

        ttk.Label(form, text="Adultos").grid(row=4, column=0, sticky="w", pady=(8, 0))
        self.adults_spinbox = ttk.Spinbox(form, from_=1, to=9, width=5)
        self.adults_spinbox.set("1")
        self.adults_spinbox.grid(row=4, column=1, sticky="w", padx=8, pady=(8, 0))

        form.columnconfigure(1, weight=1)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=16, pady=8)
        ttk.Button(buttons, text="Gerar Links", command=self._generate_links).pack(side="left")
        ttk.Button(buttons, text="Exportar JSON", command=lambda: self._export("json")).pack(
            side="left", padx=8
        )
        ttk.Button(buttons, text="Exportar CSV", command=lambda: self._export("csv")).pack(
            side="left", padx=8
        )
        ttk.Button(buttons, text="Exportar Excel", command=lambda: self._export("excel")).pack(
            side="left", padx=8
        )

    def _build_results(self) -> None:
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=16, pady=12)

        self.result_text = tk.Text(container, wrap="none")
        self.result_text.pack(side="left", fill="both", expand=True)

        scroll_y = ttk.Scrollbar(container, orient="vertical", command=self.result_text.yview)
        scroll_y.pack(side="right", fill="y")
        self.result_text.configure(yscrollcommand=scroll_y.set)

    def _swap_routes(self) -> None:
        destination = self.destination_entry.get().strip().upper()
        origins_raw = self.origins_entry.get().strip()
        origins = [code.strip().upper() for code in origins_raw.split(",") if code.strip()]
        if not destination and not origins:
            return

        new_destination = origins[0] if origins else ""
        new_origins = [destination] + origins[1:] if destination else origins[1:]

        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, new_destination)
        self.origins_entry.delete(0, tk.END)
        self.origins_entry.insert(0, ", ".join([code for code in new_origins if code]))

    def _swap_dates(self) -> None:
        outbound = self.outbound_entry.get().strip()
        inbound = self.inbound_entry.get().strip()
        self.outbound_entry.delete(0, tk.END)
        self.inbound_entry.delete(0, tk.END)
        self.outbound_entry.insert(0, inbound)
        self.inbound_entry.insert(0, outbound)

    def _collect_inputs(self) -> List[str]:
        origins = [code.strip().upper() for code in self.origins_entry.get().split(",") if code.strip()]
        if not origins:
            raise ValueError("Informe pelo menos uma origem.")
        destination = self.destination_entry.get().strip().upper()
        if not destination:
            raise ValueError("Informe o destino.")
        outbound = self.outbound_entry.get().strip()
        inbound = self.inbound_entry.get().strip()
        adults = int(self.adults_spinbox.get())
        return [origins, destination, outbound, inbound, adults]

    def _generate_links(self) -> None:
        try:
            origins, destination, outbound, inbound, adults = self._collect_inputs()
            results = generate_flight_links(
                origins=origins,
                destination=destination,
                outbound_date=outbound,
                inbound_date=inbound,
                adults=adults,
            )
        except (ValueError, IATAValidationError) as exc:
            messagebox.showerror("Erro", str(exc))
            return

        data = results_to_dicts(results)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, json.dumps(data, ensure_ascii=False, indent=2))

    def _export(self, export_type: str) -> None:
        try:
            origins, destination, outbound, inbound, adults = self._collect_inputs()
            results = generate_flight_links(
                origins=origins,
                destination=destination,
                outbound_date=outbound,
                inbound_date=inbound,
                adults=adults,
            )
        except (ValueError, IATAValidationError) as exc:
            messagebox.showerror("Erro", str(exc))
            return

        if export_type == "json":
            path = filedialog.asksaveasfilename(defaultextension=".json")
            if path:
                export_json(results, Path(path))
        elif export_type == "csv":
            path = filedialog.asksaveasfilename(defaultextension=".csv")
            if path:
                export_csv(results, Path(path))
        elif export_type == "excel":
            path = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if path:
                try:
                    export_excel(results, Path(path))
                except RuntimeError as exc:
                    messagebox.showerror("Erro", str(exc))
                    return
        else:
            messagebox.showerror("Erro", "Tipo de exportação inválido.")
            return

        messagebox.showinfo("Sucesso", "Arquivo exportado com sucesso!")


if __name__ == "__main__":
    app = FlightLinkApp()
    app.mainloop()
