import datetime
import os
import pathlib
import subprocess
import pdfkit


def generate_html(addresses, template_filename="template.html"):
    rows = ""

    for i, address in enumerate(addresses):
        num = i + 1
        address_lines = list(filter(None, address.split("\n")))
        recipient = address_lines[0]
        place = "<br>".join(address_lines[1:])
        row_str = ("<td>{num}</td>"
                   "<td>{recipient}</td>"
                   "<td>{place}</td>"
                   "<td></td>"
                   "<td></td>"
                   "<td></td>"
                   "<td></td>").format(
                       num=num,
                       recipient=recipient,
                       place=place
                   )
        rows += "<tr>" + row_str + "</tr>"

    with open(template_filename, "r") as template:
        html = template.read()
        return html.replace("{{ROWS}}", rows)

    return rows


def generate_pdf_file_name():
    directory = pathlib.Path.cwd() / "pdf"
    if not directory.exists():
        directory.mkdir()

    name_pattern = "wysyłka " + \
        datetime.date.today().isoformat() + " - {:02d}.pdf"
    counter = 0
    while True:
        counter += 1
        path = directory / name_pattern.format(counter)
        if not path.exists():
            return path.as_posix()


def write_and_open_addresses_pdf(addresses):
    pdf_file_name = generate_pdf_file_name()
    print("Writing file {}".format(pdf_file_name))

    html = generate_html(addresses)

    pdfkit.from_string(html, pdf_file_name)

    if os.name == 'nt':  # For Windows
        os.startfile(pdf_file_name)
    elif os.name == 'posix':  # For Linux, Mac, etc.
        subprocess.call(('xdg-open', pdf_file_name))
