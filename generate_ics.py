from __future__ import annotations
from datetime import date, datetime, timedelta, timezone

def is_leap_year(y: int) -> bool:
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

def day_of_year(d: date) -> int:
    return int(d.strftime("%j"))

def build_ics(d: date) -> str:
    year = d.year
    total_days = 366 if is_leap_year(year) else 365
    doy = day_of_year(d)
    pct = round(doy / total_days * 100.0, 2)

    # Apple Calendar is happy with all-day events using DTSTART;VALUE=DATE / DTEND;VALUE=DATE
    # DTEND is exclusive, so add 1 day.
    dtstart = d.strftime("%Y%m%d")
    dtend = (d + timedelta(days=1)).strftime("%Y%m%d")

    # UID must be stable per day to avoid duplicates.
    uid = f"year-progress-{year}-{dtstart}@github-pages"

    # DTSTAMP in UTC
    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    summary = f"Day {doy} ({pct:.2f}%)"

    ics = "\r\n".join([
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//year-progress//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{dtstamp}",
        f"SUMMARY:{summary}",
        f"DTSTART;VALUE=DATE:{dtstart}",
        f"DTEND;VALUE=DATE:{dtend}",
        "TRANSP:TRANSPARENT",
        "END:VEVENT",
        "END:VCALENDAR",
        ""
    ])
    return ics

if __name__ == "__main__":
    today = date.today()
    out = build_ics(today)
    with open("calendar.ics", "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print(f"Wrote calendar.ics for {today.isoformat()}")
