#!/usr/bin/env python3
import re

def split_items(body):
    items, buf = [], []
    depth, quote, i = 0, False, 0
    while i < len(body):
        ch = body[i]
        if ch == "'":
            if quote and i + 1 < len(body) and body[i + 1] == "'":
                buf.extend([ch, body[i + 1]])
                i += 2
                continue
            quote = not quote
            buf.append(ch)
        elif not quote and ch == "(":
            depth += 1
            buf.append(ch)
        elif not quote and ch == ")":
            depth -= 1
            buf.append(ch)
        elif not quote and ch == "," and depth == 0:
            items.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
        i += 1
    if "".join(buf).strip():
        items.append("".join(buf).strip())
    return items

def first_constraint_pos(rest):
    upper = " " + rest.upper()
    tokens = [" PRIMARY KEY", " NOT NULL", " UNIQUE", " REFERENCES ", " DEFAULT ", " CHECK "]
    positions = [upper.find(tok) for tok in tokens if upper.find(tok) >= 0]
    return max(0, min(positions) - 1) if positions else len(rest)

def parse_schema(text):
    tables = {}
    for m in re.finditer(r"CREATE TABLE\s+([a-zA-Z0-9_]+)\s*\((.*?)\);", text, re.S | re.I):
        name, body = m.group(1), m.group(2)
        table = {"name": name, "columns": [], "pk": [], "fks": [], "uniques": [], "checks": [], "indexes": []}
        for item in split_items(body):
            compact = " ".join(item.split())
            upper = compact.upper()
            if upper.startswith("UNIQUE"):
                mm = re.search(r"UNIQUE\s*\((.*?)\)", compact, re.I)
                if mm:
                    table["uniques"].append([x.strip() for x in mm.group(1).split(",")])
                continue
            if upper.startswith("CHECK"):
                mm = re.search(r"CHECK\s*\((.*)\)$", compact, re.I | re.S)
                if mm:
                    table["checks"].append(mm.group(1).strip())
                continue
            if upper.startswith("PRIMARY KEY"):
                mm = re.search(r"PRIMARY KEY\s*\((.*?)\)", compact, re.I)
                if mm:
                    table["pk"].extend(x.strip() for x in mm.group(1).split(","))
                continue

            cm = re.match(r"([a-zA-Z0-9_]+)\s+(.+)$", compact, re.S)
            if not cm:
                raise ValueError("Cannot parse table item " + name + ": " + compact)
            col, rest = cm.groups()
            pos = first_constraint_pos(rest)
            sql_type = rest[:pos].strip()
            inline_pk = bool(re.search(r"\bPRIMARY KEY\b", rest, re.I))
            nullable = ("NOT NULL" not in upper) and (not inline_pk)
            default = None
            dm = re.search(r"\bDEFAULT\s+(.+?)(?=\s+CHECK\s|\s+UNIQUE\b|\s+REFERENCES\b|$)", rest, re.I)
            if dm:
                default = dm.group(1).strip()
            inline_unique = bool(re.search(r"\bUNIQUE\b", rest, re.I))

            fk = None
            fm = re.search(r"\bREFERENCES\s+([a-zA-Z0-9_]+)\s*\(([a-zA-Z0-9_]+)\)", rest, re.I)
            if fm:
                fk = {"column": col, "ref_table": fm.group(1), "ref_column": fm.group(2), "nullable": nullable}
                table["fks"].append(fk)

            checks = []
            for ck in re.finditer(r"\bCHECK\s*\((.*?)\)(?=\s*$|\s+)", rest, re.I | re.S):
                checks.append(ck.group(1).strip())
                table["checks"].append(ck.group(1).strip())

            if inline_unique:
                table["uniques"].append([col])
            if inline_pk:
                table["pk"].append(col)

            table["columns"].append({
                "name": col,
                "type": sql_type,
                "nullable": nullable,
                "default": default,
                "pk": inline_pk,
                "fk": fk,
                "unique": inline_unique,
                "checks": checks,
            })
        tables[name] = table

    index_re = re.compile(
        r"CREATE INDEX\s+([a-zA-Z0-9_]+)\s+ON\s+([a-zA-Z0-9_]+)"
        r"(?:\s+USING\s+([a-zA-Z0-9_]+))?\s*\((.*?)\)"
        r"(?:\s+WHERE\s+(.*?))?;",
        re.I | re.S,
    )
    for m in index_re.finditer(text):
        idx, table, method, cols, where = m.groups()
        if table not in tables:
            raise ValueError("Index references unknown table " + table)
        tables[table]["indexes"].append({
            "name": idx,
            "method": (method or "btree").upper(),
            "columns": " ".join(cols.split()),
            "where": " ".join(where.split()) if where else None,
        })

    raw = {
        "tables": len(re.findall(r"\bCREATE TABLE\b", text, re.I)),
        "primary_keys": len(re.findall(r"\bPRIMARY KEY\b", text, re.I)),
        "foreign_keys": len(re.findall(r"\bREFERENCES\b", text, re.I)),
        "unique_constraints": len(re.findall(r"\bUNIQUE\b", text, re.I)),
        "check_constraints": len(re.findall(r"\bCHECK\s*\(", text, re.I)),
        "indexes": len(re.findall(r"\bCREATE INDEX\b", text, re.I)),
        "postgis_extensions": len(re.findall(r"CREATE EXTENSION IF NOT EXISTS postgis", text, re.I)),
    }
    parsed = {
        "tables": len(tables),
        "primary_keys": sum(bool(t["pk"]) for t in tables.values()),
        "foreign_keys": sum(len(t["fks"]) for t in tables.values()),
        "unique_constraints": sum(len(t["uniques"]) for t in tables.values()),
        "check_constraints": sum(len(t["checks"]) for t in tables.values()),
        "indexes": sum(len(t["indexes"]) for t in tables.values()),
        "postgis_extensions": 1 if "CREATE EXTENSION IF NOT EXISTS postgis" in text else 0,
    }
    return tables, raw, parsed

def foreign_key_edges(tables, selected=None):
    allowed = set(selected) if selected else set(tables)
    edges = []
    for table in tables.values():
        if table["name"] not in allowed:
            continue
        for fk in table["fks"]:
            if fk["ref_table"] in allowed:
                edges.append({"child": table["name"], **fk})
    return edges
