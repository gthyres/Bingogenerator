"""
bingo_generator.py

Skapar 500 liggande A4-sidor med 6 bingospelplaner per sida.

Krav:
- 6 spelplaner per liggande A4
- varje spelplan: 9 kolumner x 3 rader
- varje rad: exakt 5 siffror och 4 tomma rutor
- på varje A4 finns varje siffra 1-90 exakt en gång
- inga dubbla siffror på samma A4
- kolumn 1: 1-9
- kolumn 2: 10-19
- kolumn 3: 20-29
- kolumn 4: 30-39
- kolumn 5: 40-49
- kolumn 6: 50-59
- kolumn 7: 60-69
- kolumn 8: 70-79
- kolumn 9: 80-90
- svartvitt, stora siffror, tjocka linjer
- spelplansnummer 000001-003000

Installera:
    pip install reportlab

Kör:
    python bingo_generator.py
"""

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import random
import itertools

OUTPUT_FILE = "bingo_500_A4_6_spelplaner.pdf"

TOTAL_PAGES = 500
TICKETS_PER_PAGE = 6
ROWS = 3
COLS = 9

PAGE_W, PAGE_H = landscape(A4)

COL_RANGES = [
    list(range(1, 10)),
    list(range(10, 20)),
    list(range(20, 30)),
    list(range(30, 40)),
    list(range(40, 50)),
    list(range(50, 60)),
    list(range(60, 70)),
    list(range(70, 80)),
    list(range(80, 91)),
]

COLUMN_TARGETS = [9, 10, 10, 10, 10, 10, 10, 10, 11]
ALL_ROW_PATTERNS = list(itertools.combinations(range(COLS), 5))


def make_page_masks():
    targets = COLUMN_TARGETS[:]
    rows = []

    for row_index in range(TICKETS_PER_PAGE * ROWS):
        rows_left_after = TICKETS_PER_PAGE * ROWS - row_index - 1
        possible = []

        for pattern in ALL_ROW_PATTERNS:
            new_targets = targets[:]
            ok = True

            for c in pattern:
                if new_targets[c] <= 0:
                    ok = False
                    break
                new_targets[c] -= 1

            if ok and all(x <= rows_left_after for x in new_targets):
                possible.append(pattern)

        if not possible:
            return make_page_masks()

        weights = [sum(targets[c] for c in pattern) for pattern in possible]
        chosen = random.choices(possible, weights=weights, k=1)[0]
        rows.append(chosen)

        for c in chosen:
            targets[c] -= 1

    if targets != [0] * COLS:
        return make_page_masks()

    masks = []
    index = 0

    for _ in range(TICKETS_PER_PAGE):
        ticket = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in rows[index]:
                ticket[r][c] = 1
            index += 1
        masks.append(ticket)

    return masks


def fill_numbers(masks):
    tickets = [[["" for _ in range(COLS)] for _ in range(ROWS)] for _ in range(TICKETS_PER_PAGE)]

    for c in range(COLS):
        nums = COL_RANGES[c][:]
        random.shuffle(nums)

        cells = []
        for t in range(TICKETS_PER_PAGE):
            for r in range(ROWS):
                if masks[t][r][c]:
                    cells.append((t, r))

        if len(cells) != len(nums):
            raise ValueError("Fel antal rutor i kolumn")

        for (t, r), n in zip(cells, nums):
            tickets[t][r][c] = str(n)

    return tickets


def check_page(tickets):
    numbers = []

    for ticket in tickets:
        for row in ticket:
            if sum(1 for x in row if x) != 5:
                return False
            numbers.extend(int(x) for x in row if x)

    return sorted(numbers) == list(range(1, 91))


def draw_ticket(pdf, grid, x0, y0, w, h, serial):
    header_h = 10 * mm
    grid_h = h - header_h
    cell_w = w / COLS
    cell_h = grid_h / ROWS

    pdf.setLineWidth(2.2)
    pdf.rect(x0, y0, w, h)

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(x0 + 2 * mm, y0 + h - 6 * mm, f"{serial:06d}")

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(x0 + w / 2, y0 + h - 8 * mm, "B I N G O")

    pdf.line(x0, y0 + grid_h, x0 + w, y0 + grid_h)

    for r in range(ROWS):
        for c in range(COLS):
            x = x0 + c * cell_w
            y = y0 + (ROWS - 1 - r) * cell_h

            pdf.setLineWidth(1.8)
            pdf.rect(x, y, cell_w, cell_h)

            value = grid[r][c]
            if value:
                pdf.setFont("Helvetica-Bold", 22)
                pdf.drawCentredString(x + cell_w / 2, y + cell_h / 2 - 3.5 * mm, value)


def draw_page(pdf, tickets, page_number, first_serial):
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(5 * mm, PAGE_H - 7 * mm, f"A4 {page_number:04d}")

    margin_x = 4 * mm
    margin_y = 4 * mm
    gap_x = 4 * mm
    gap_y = 4 * mm

    ticket_w = (PAGE_W - 2 * margin_x - gap_x) / 2
    ticket_h = (PAGE_H - 2 * margin_y - 2 * gap_y) / 3

    positions = []
    for row in range(3):
        for col in range(2):
            x = margin_x + col * (ticket_w + gap_x)
            y = PAGE_H - margin_y - (row + 1) * ticket_h - row * gap_y
            positions.append((x, y))

    for i, (x, y) in enumerate(positions):
        draw_ticket(pdf, tickets[i], x, y, ticket_w, ticket_h, first_serial + i)


def main():
    pdf = canvas.Canvas(OUTPUT_FILE, pagesize=landscape(A4))
    seen_pages = set()
    serial = 1

    for page_number in range(1, TOTAL_PAGES + 1):
        while True:
            masks = make_page_masks()
            tickets = fill_numbers(masks)

            if not check_page(tickets):
                continue

            key = tuple(tuple(tuple(row) for row in ticket) for ticket in tickets)
            if key not in seen_pages:
                seen_pages.add(key)
                break

        draw_page(pdf, tickets, page_number, serial)
        serial += TICKETS_PER_PAGE
        pdf.showPage()

        if page_number % 25 == 0:
            print(f"Skapade {page_number} av {TOTAL_PAGES} sidor")

    pdf.save()
    print(f"Klar: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
