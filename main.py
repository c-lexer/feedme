"""
Webscraper to lookup lunch menus.
"""

from krall import Krall
from kurve import Kurve
from karli import Karli


kurve_menu = Kurve().get_menus()
krall_menu = Krall().get_menus()
karli_menu = Karli().get_menus()

f = open("index.html", "a")
f.write(
    """
<!DOCTYPE html>
<html>
<style>
table, th, td {
  border:1px solid black;
}
</style>
<body>
"""
)

for tag in ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]:
    f.write(
        """
    <h2>{}</h2>
    <table>
            <tr>
                <th>Kurve</th>
                <td>{}</td><td>{}</td>
            </tr>
            <tr>
                <th>Krall</th>
                <td>{}</td><td>{}</td>
            </tr>
            <tr>
                <th>Karli</th>
                <td>{}</td><td>{}</td><td>{}</td>
            </tr>
</table>
    """.format(
            tag,
            kurve_menu[tag][0],
            kurve_menu[tag][1],
            krall_menu[tag][0],
            krall_menu[tag][1],
            karli_menu[tag][0],
            karli_menu[tag][1],
            karli_menu[tag][2],
        )
    )


f.write(
    """
</body>
</html>
"""
)
f.close()
