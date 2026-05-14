import re
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser as dt_parser


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s = s.lower().strip()

    # 1. Base Keywords
    if s == "today":
        return today
    if s == "tomorrow":
        return today + timedelta(days=1)
    if s == "yesterday":
        return today - timedelta(days=1)

    # 2. Next / Last Weekdays
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    weekday_match = re.match(r"(next|last)\s+([a-z]+)", s)
    if weekday_match:
        direction, day_name = weekday_match.groups()
        if day_name in weekdays:
            target_weekday = weekdays[day_name]
            current_weekday = today.weekday()
            days_ahead = target_weekday - current_weekday

            if direction == "next" and days_ahead <= 0:
                days_ahead += 7
            elif direction == "last" and days_ahead >= 0:
                days_ahead -= 7

            return today + timedelta(days=days_ahead)

    # 3. Relative complex dates (now supports "a" or "an" instead of digits)
    rel_pattern = r"(?:in\s+)?((?:(?:\d+|an?)\s+[a-z]+\s*(?:and\s+)?)+)\s*(ago|before|after|from)?\s*(.*)?"
    rel_match = re.search(rel_pattern, s)

    if rel_match and rel_match.group(1):
        quantities_str = rel_match.group(1)
        direction = rel_match.group(2) or ("after" if "in" in s else "ago")
        base_str = rel_match.group(3)

        # Determine the base date to add/subtract from
        base_date = today
        if base_str:
            base_str = base_str.strip()
            if base_str in ["today", "tomorrow", "yesterday"]:
                base_date = parse(base_str, today)  # recursive call for simple bases
            elif base_str and base_str != "now":
                # Fallback to dateutil parser for explicit dates
                base_date = dt_parser.parse(base_str).date()

        # Parse the delta
        years = months = weeks = days = 0
        units = re.findall(r"(\d+|an?)\s+(year|month|week|day)s?", quantities_str)

        for amount, unit in units:
            # Handle "a" or "an" as 1
            val = 1 if amount in ["a", "an"] else int(amount)

            if unit == "year":
                years += val
            elif unit == "month":
                months += val
            elif unit == "week":
                weeks += val
            elif unit == "day":
                days += val

        delta = relativedelta(years=years, months=months, weeks=weeks, days=days)

        if direction in ["ago", "before"]:
            return base_date - delta
        else:
            return base_date + delta

    # 4. Fallback
    try:
        return dt_parser.parse(s).date()
    except (dt_parser.ParserError, ValueError):
        raise ValueError(f"Could not parse date string: '{s}'")
