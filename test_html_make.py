
from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("E:\study\Maker_DAT_BOT\DATMaker\BOXTemplate"))
template = environment.get_template("BOXTEMPLATE.data")

NTG = 0.9
PERM = 100
PERMZ = PERM / 10
PORO = 0.2

param = {"NTG": NTG,
         "PERM": PERM,
         "PERMZ": PERMZ,
         "PORO": PORO
        }

filename = f"output.inc"
content = template.render(param)

with open(filename, mode="w", encoding="utf-8") as message:
    message.write(content)
    print(f"... wrote {filename}")