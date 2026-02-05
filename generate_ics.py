from __future__ import annotations
from datetime import date, datetime, timedelta, timezone

def is_leap_year(y: int) -> bool:
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

def day_of_year(d: date) -> int:
    return int(d.strftime("%j"))

def build_year_ics(year: int) -> str:
    total_days = 366 if is_leap_year(year) else 365
    start = date(year, 1, 1)

    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//year-progress//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]

    for i in range(total_days):
        d = start + timedelta(days=i)
        doy = i + 1
        pct = round(doy / total_days * 100.0, 2)

        dtstart = d.strftime("%Y%m%d")
        dtend = (d + timedelta(days=1)).strftime("%Y%m%d")

        # Stable UID per date so Apple Calendar does not duplicate events
        uid = f"year-progress-{year}-{dtstart}@github-pages"

        summary = f"Day {doy} ({pct:.2f}%)"

        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{dtstamp}",
            f"SUMMARY:{summary}",
            f"DTSTART;VALUE=DATE:{dtstart}",
            f"DTEND;VALUE=DATE:{dtend}",
            "TRANSP:TRANSPARENT",
            "END:VEVENT",
        ]

    lines += ["END:VCALENDAR", ""]
    return "\r\n".join(lines)

if __name__ == "__main__":
    today = date.today()
    year = today.year
    out = build_year_ics(year)
    with open("calendar.ics", "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print(f"Wrote calendar.ics for full year {year}")
