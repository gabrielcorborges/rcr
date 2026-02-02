"""Flight link generator for LATAM and Azul.

Provides utilities to validate IATA codes, generate search URLs, and export
results as JSON/CSV (Excel optional).
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Dict, Any, Optional, Sequence
from urllib import request

DEFAULT_AIRPORTS_PATH = Path(__file__).parent / "data" / "airports.json"


@dataclass(frozen=True)
class FlightLinkResult:
    index: int
    origin: str
    destination: str
    latam: Dict[str, str]
    azul: Dict[str, str]


class IATAValidationError(ValueError):
    """Raised when one or more IATA codes are invalid."""


def _load_airports_from_file(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"Airports file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        data = data.get("airports", [])
    if not isinstance(data, list):
        raise ValueError("Airports JSON must be a list or {airports: [...]} format.")
    return [str(item).upper() for item in data]


def _load_airports_from_api(api_url: str, api_key: Optional[str] = None) -> List[str]:
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = request.Request(api_url, headers=headers)
    with request.urlopen(req, timeout=20) as response:  # noqa: S310 - trusted API URL
        payload = json.loads(response.read().decode("utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("data", payload.get("airports", payload))
    if not isinstance(payload, list):
        raise ValueError("API response must be a list of airports.")
    iatas = []
    for item in payload:
        if isinstance(item, dict):
            code = item.get("iata") or item.get("iata_code")
        else:
            code = item
        if code:
            iatas.append(str(code).upper())
    return iatas


def load_airports(
    airports_path: Path = DEFAULT_AIRPORTS_PATH,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[str]:
    """Load IATA codes from a local JSON file or from a public API."""

    if api_url:
        return _load_airports_from_api(api_url, api_key)
    return _load_airports_from_file(airports_path)


def validate_iata_codes(codes: Iterable[str], airports: Sequence[str]) -> List[str]:
    airports_set = {code.upper() for code in airports}
    invalid = [code for code in codes if code.upper() not in airports_set]
    return invalid


def _format_azul_date(date_str: str) -> str:
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%m/%d/%Y")


def _build_latam_url(origin: str, destination: str, outbound: str, inbound: str, adults: int) -> str:
    return (
        "https://www.latamairlines.com/br/pt/oferta-voos?"
        f"origin={origin}&"
        f"outbound={outbound}T00%3A00%3A00.000Z&"
        f"destination={destination}&"
        f"inbound={inbound}T00%3A00%3A00.000Z&"
        f"adt={adults}&"
        "chd=0&inf=0&"
        "trip=RT&"
        "cabin=Economy&"
        "redemption=false"
    )


def _build_azul_url(origin: str, destination: str, outbound: str, inbound: str, adults: int) -> str:
    outbound_br = _format_azul_date(outbound)
    inbound_br = _format_azul_date(inbound)
    return (
        "https://www.voeazul.com.br/br/pt/home/selecao-voo?"
        f"c[0].ds={origin}&"
        f"c[0].std={outbound_br}&"
        f"c[0].as={destination}&"
        f"c[1].ds={destination}&"
        f"c[1].std={inbound_br}&"
        f"c[1].as={origin}&"
        "p[0].t=ADT&"
        f"p[0].c={adults}&"
        "p[0].cp=false&"
        "cc=BRL"
    )


def generate_flight_links(
    origins: Sequence[str],
    destination: str,
    outbound_date: str,
    inbound_date: str,
    adults: int = 1,
    airports_path: Path = DEFAULT_AIRPORTS_PATH,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[FlightLinkResult]:
    """Generate LATAM and Azul links for each origin airport.

    Raises:
        IATAValidationError: when any origin or destination is invalid.
    """

    airports = load_airports(airports_path=airports_path, api_url=api_url, api_key=api_key)
    codes_to_validate = list(origins) + [destination]
    invalid = validate_iata_codes(codes_to_validate, airports)
    if invalid:
        raise IATAValidationError(f"Invalid IATA codes: {', '.join(sorted(set(invalid)))}")

    results: List[FlightLinkResult] = []
    for idx, origin in enumerate(origins, start=1):
        origin_code = origin.upper()
        destination_code = destination.upper()
        latam_outbound = _build_latam_url(origin_code, destination_code, outbound_date, inbound_date, adults)
        latam_return = _build_latam_url(destination_code, origin_code, inbound_date, outbound_date, adults)
        azul_outbound = _build_azul_url(origin_code, destination_code, outbound_date, inbound_date, adults)
        azul_return = _build_azul_url(destination_code, origin_code, inbound_date, outbound_date, adults)
        results.append(
            FlightLinkResult(
                index=idx,
                origin=origin_code,
                destination=destination_code,
                latam={"ida": latam_outbound, "volta": latam_return},
                azul={"ida": azul_outbound, "volta": azul_return},
            )
        )
    return results


def results_to_dicts(results: Sequence[FlightLinkResult]) -> List[Dict[str, Any]]:
    return [
        {
            "index": item.index,
            "origem": item.origin,
            "destino": item.destination,
            "latam": item.latam,
            "azul": item.azul,
        }
        for item in results
    ]


def export_json(results: Sequence[FlightLinkResult], path: Path) -> None:
    data = results_to_dicts(results)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def export_csv(results: Sequence[FlightLinkResult], path: Path) -> None:
    data = results_to_dicts(results)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["index", "origem", "destino", "latam", "azul"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def export_excel(results: Sequence[FlightLinkResult], path: Path) -> None:
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError("pandas is required to export Excel files.") from exc

    data = results_to_dicts(results)
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)


def generateFlightLinks(  # noqa: N802 - keeping requested name
    origins: Sequence[str],
    destination: str,
    outbound_date: str,
    inbound_date: str,
    adults: int = 1,
    airports_path: Path = DEFAULT_AIRPORTS_PATH,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Wrapper matching the requested function name in the prompt."""

    results = generate_flight_links(
        origins=origins,
        destination=destination,
        outbound_date=outbound_date,
        inbound_date=inbound_date,
        adults=adults,
        airports_path=airports_path,
        api_url=api_url,
        api_key=api_key,
    )
    return results_to_dicts(results)


if __name__ == "__main__":
    sample = generateFlightLinks(
        origins=["JPA", "REC", "NAT", "MCZ"],
        destination="FOR",
        outbound_date="2024-10-15",
        inbound_date="2024-10-21",
        adults=1,
    )
    print(json.dumps(sample, ensure_ascii=False, indent=2))
