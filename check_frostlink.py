
import frostlink, inspect

print("Loaded from:", getattr(frostlink, "__file__", "UNKNOWN"))
print("Exports:", [n for n in dir(frostlink) if n in ("read_sql","read_table","connect")])
