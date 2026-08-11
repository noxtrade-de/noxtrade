#!/usr/bin/env python3
"""Schreibt den Zahlen-Block im README aus den echten Live-Daten neu.

    python3 tools/readme-zahlen.py            # aktualisieren
    python3 tools/readme-zahlen.py --zeigen   # nur anzeigen, nichts aendern

Warum es das gibt (11.08.2026): Ein Zahlen-Block im README veraltet lautlos.
Er sieht am Tag danach genauso vertrauenswuerdig aus wie am Tag der Messung —
und ausgerechnet in einem Text, dessen ganzes Versprechen Ehrlichkeit ist,
waere eine alte Zahl der teuerste Fehler. Deshalb wird er erzeugt und nicht
gepflegt.

Quelle ist der oeffentliche Endpunkt der Seite, nicht der Server: Das Skript
laeuft damit ueberall und braucht keinen Zugang.
"""
import argparse
import datetime
import json
import pathlib
import re
import sys
import urllib.request

QUELLE = "https://www.noxtrade.de/api/live"
README = pathlib.Path(__file__).resolve().parent.parent / "README.md"
ANFANG = "<!-- ZAHLEN-ANFANG (erzeugt von tools/readme-zahlen.py — nicht von Hand aendern) -->"
ENDE = "<!-- ZAHLEN-ENDE -->"

# Was der Live-Endpunkt NICHT liefert, weil es nicht auf dem Konto steht:
# die Trefferbilanz aus dem Handelsjournal. Von Hand gepflegt — mit Datum,
# damit ein alter Wert auffaellt statt zu verstauben. Siehe die Warnung unten.
#
# Die eigene API-Rechnung stand hier bis zum 11.08.2026 ebenfalls drin und ist
# auf Kevins Entscheidung wieder raus. Sie bleibt intern gemessen
# (`costs.jsonl` auf dem Server, Tagesbericht im Watchdog) — sie gehoert nur
# nicht auf die oeffentliche Seite. Wer sie wieder aufnimmt: es waren rund
# 31 $ ueber 42 Tage gegen ~2,42 $ Handelsgewinn, und die Zahl ist nahezu fix
# (sie skaliert mit der Zahl beobachteter Coins, nicht mit dem Kapital).
HANDGEPFLEGT = {
    "stand": "2026-08-06",
    "avg_gewinner_pct": 5.9,
    "avg_verlierer_pct": -4.1,
}
VERFALL_TAGE = 45


def hole(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def veraltet(h: dict, heute: datetime.date) -> int:
    """Wie viele Tage sind die handgepflegten Zahlen alt?"""
    return (heute - datetime.date.fromisoformat(h["stand"])).days


def block(d: dict, h: dict, heute: datetime.date) -> str:
    seit = datetime.date.fromisoformat(d["benchmark_since"][:10])
    cash = 100 * d["cash"] / d["total_value"] if d.get("total_value") else 0

    # Der handgepflegte Satz faellt RAUS, sobald er zu alt ist — er wird nicht
    # etwa mit altem Wert weiterveroeffentlicht. Eine Zahl, die niemand mehr
    # nachgerechnet hat, sieht im Text genauso vertrauenswuerdig aus wie eine
    # frische; das ist in einem Text ueber Ehrlichkeit der teuerste Fehler.
    # Lieber steht dort nichts als etwas Ungeprueftes.
    if veraltet(h, heute) > VERFALL_TAGE:
        geometrie = ""
    else:
        geometrie = (f"\n\nA {d['win_rate']:.0f} % hit rate is not a bug: average winner "
                     f"**{h['avg_gewinner_pct']:+.1f} %**, average loser "
                     f"**{h['avg_verlierer_pct']:+.1f} %**. The geometry has to carry it, "
                     f"and right now it barely does.")

    return f"""{ANFANG}
Real money, real Binance account, running since **{seit:%-d %B %Y}**. Numbers as of
**{heute:%-d %B %Y}**:

| | |
|---|---|
| Closed trades | **{d['total_trades']}** ({d['winning_trades']} winners — a **{d['win_rate']:.0f} %** hit rate) |
| Return on the traded capital | **{d['agent_trading_roi']:+.2f} %** |
| Holding BTC over the same window | {d['btc_hold_roi']:+.2f} % |
| Difference | **{d['alpha']:+.2f} pp** |
| Currently in cash | **{cash:.1f} %** |{geometrie}
{ENDE}"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--zeigen", action="store_true", help="nur anzeigen")
    a = p.parse_args()

    heute = datetime.date.today()
    alt = veraltet(HANDGEPFLEGT, heute)
    if alt > VERFALL_TAGE:
        print(f"WARNUNG: die handgepflegte Trefferbilanz ist {alt} Tage alt "
              f"(Grenze {VERFALL_TAGE}). Der Satz wurde deshalb aus dem README "
              f"ENTFERNT statt mit altem Wert weiterveroeffentlicht. Zum "
              f"Zurueckholen: Durchschnitt der Gewinner/Verlierer neu rechnen "
              f"und HANDGEPFLEGT anpassen.", file=sys.stderr)

    try:
        d = hole(QUELLE)
    except Exception as e:
        print(f"Live-Daten nicht erreichbar ({type(e).__name__}) — README bleibt, "
              f"wie es ist. Lieber ein alter Stand als ein erfundener.", file=sys.stderr)
        return 1
    if not d.get("available"):
        print("Endpunkt meldet 'available: false' — README bleibt unveraendert.",
              file=sys.stderr)
        return 1

    neu = block(d, HANDGEPFLEGT, heute)
    if a.zeigen:
        print(neu)
        return 0

    text = README.read_text(encoding="utf-8")
    muster = re.compile(re.escape(ANFANG) + r".*?" + re.escape(ENDE), re.S)
    if not muster.search(text):
        print(f"Markierungen nicht gefunden in {README}", file=sys.stderr)
        return 1
    if muster.sub(lambda _: neu, text) == text:
        print("unveraendert")
        return 0
    README.write_text(muster.sub(lambda _: neu, text), encoding="utf-8")
    print(f"README aktualisiert: {d['total_trades']} Trades, {d['win_rate']:.0f} % "
          f"Trefferquote, {d['agent_trading_roi']:+.2f} % gegen "
          f"{d['btc_hold_roi']:+.2f} % BTC-Hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
