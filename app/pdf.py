import pdfkit


def write_pdf(addresses, filename):
    html = """
        <!DOCTYPE HTML>
        <html>

        <head>
          <style>
            table {
              width: 100%;
              border-collapse: collapse;
            }
            table, th, td {
              border: 1px solid black;
            }
            tr {
             height: 80px;
            }
          </style>
        </head>

        <body>
            <table>
              <tr>
                <th>No</th>
                <th>Name</th>
                <th>Address</th>
                <th>Tracking No</th>
                <th>Comments</th>
                <th>Fee</th>
              </tr>
    """
    for i, address in enumerate(addresses):
        num = i + 1
        address_lines = address.split("  ")
        recipient = address_lines[0]
        place = "\n".join(adress_lines[1:])
        row = "<td>" + x + "</td>"
    
    html += "</table></body>"
    
    pdfkit.from_string(html, filename)

