#!/usr/bin/env python3
from pathlib import Path
from icalendar import Calendar, Event
from datetime import datetime, date
import pytz
import re

def read():
    root = Path('~/obsidian/primary/daily').expanduser()

    cal = Calendar()
    cal.add('prodid', '-//Export from obsidian-ical//j.yud.co.za//')
    cal.add('version', '2.0')
    for day in root.glob('*.md'):
        daily_date = date.fromisoformat(day.stem)
        lines = [
            line.strip() for line in day.read_text().splitlines()
            if line.strip()
        ]

        while lines and not lines[0].endswith('plan'):
            lines.pop(0)
        assert lines, 'Expected plan in %s' % day
        lines.pop(0)

        plan_item = re.compile(r'^- \[(?:x|X| )\] (.*)')
        tag_regex = re.compile(r'(?: |^)#([a-z0-9]+)\b')
        while lines and (match := plan_item.match(lines.pop(0))):
            entry = match.group(1)
            tags = tag_regex.findall(entry)
            if 'nocal' in tags:
                continue

            event = Event()
            event.add('summary', entry)
            event.add('dtstart', daily_date)
            cal.add_component(event)

    dest_path = Path('~/obsidian/cal.ical').expanduser()
    dest_path.write_bytes(cal.to_ical())
    print('File written to: %s' % dest_path)



if __name__ == '__main__':
    read()
