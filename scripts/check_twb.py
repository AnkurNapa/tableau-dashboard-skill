#!/usr/bin/env python3
"""Structural check of a generated .twb against real workbooks saved by Tableau Desktop 2026.3.

It learns from the sample workbooks inside the Desktop app bundle: the child elements each element
may hold, their order plus the attributes it carries. Context is the parent tag plus its class
attribute (so a dashboard window and a worksheet window are told apart). Run it before opening any
generated file in Desktop, so no load error dialog reaches the screen.

The official XSD runs first; the sample comparison catches load rules the XSD cannot express.

Usage: python3 check_twb.py workbook.twb
Exit code 1 on any child or order problem. Unknown attributes are printed as warnings.
"""
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

APP = Path("/Applications/Tableau Desktop (Apple silicon) 2026.3.app/Contents")
# Elements whose children are free form text runs or data, not a fixed content model
ENUMS = {("mark", "class"), ("zone", "type-v2"), ("zone", "mode"), ("zoom", "type"), ("column-instance", "derivation"),
         ("table-calc", "ordering-type"), ("column", "datatype"), ("column", "role"), ("column", "type"), ("filter", "class")}
FREE = {"formatted-text", "run", "calculation", "dictionary", "groupfilter", "expression", "members", "aliases",
        "bucket", "map", "column-mapping", "cols", "metadata-records", "metadata-record", "attributes"}


def samples():
    for p in list(APP.glob("help/Workbooks/en_US/*.twbx")) + list(APP.glob("install/Performance/*.twb*")):
        if p.suffix == ".twbx":
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.endswith(".twb"):
                        yield ET.fromstring(z.read(n))
        else:
            yield ET.parse(p).getroot()


def ctx(el):
    return el.tag + (f"[{el.get('class')}]" if el.tag == "window" else "")


def learn():
    kids, order, attrs, first = {}, {}, {}, {}
    for root in samples():
        for el in root.iter():
            c = ctx(el)
            attrs.setdefault(el.tag, set()).update(el.attrib)
            for t, a in ENUMS:
                if el.tag == t and a in el.attrib:
                    attrs.setdefault((t, a), set()).add(el.get(a))
            seq = [k.tag for k in el]
            kids.setdefault(c, set()).update(seq)
            first.setdefault(c, set()).add(seq[0] if seq else None)
            for i, a in enumerate(seq):
                for b in seq[i + 1:]:
                    if a != b:
                        order.setdefault(c, set()).add((a, b))
    return kids, order, attrs, first


def check(path):
    kids, order, attrs, first = learn()
    root = ET.parse(path).getroot()
    errors, warns = [], set()
    for el in root.iter():
        c = ctx(el)
        for a in el.attrib:
            if a not in attrs.get(el.tag, set()):
                warns.add(f"attribute {a} on <{el.tag}> not seen in samples")
            elif (el.tag, a) in ENUMS and el.get(a) not in attrs.get((el.tag, a), set()):
                warns.add(f"value {a}='{el.get(a)}' on <{el.tag}> not seen in samples")
        if el.tag in FREE or c not in kids:
            if c not in kids and el.tag not in FREE:
                warns.add(f"element <{c}> not seen as a parent in samples")
            continue
        seq = [k.tag for k in el]
        if (seq[0] if seq else None) not in first[c]:
            errors.append(f"<{c}> starts with <{seq[0] if seq else 'nothing'}>, samples start with {sorted(map(str, first[c]))}")
        for t in seq:
            if t not in kids[c]:
                errors.append(f"<{t}> inside <{c}> never seen in samples")
        for i, a in enumerate(seq):
            for b in seq[i + 1:]:
                if (b, a) in order.get(c, set()) and (a, b) not in order.get(c, set()):
                    errors.append(f"order <{a}> before <{b}> inside <{c}> contradicts samples")
    return sorted(set(errors)), sorted(warns)


def duplicate_errors(path):
    """Each column name once per datasource or dependency block; no calc caption equal to a field name."""
    errs = []
    for el in ET.parse(path).getroot().iter():
        if el.tag not in ("datasource", "datasource-dependencies"):
            continue
        cols = [c for c in el if c.tag == "column"]
        names = [c.get("name") for c in cols]
        errs += [f"column {n} defined {names.count(n)} times in <{el.tag} {el.get('name') or el.get('datasource')}>"
                 for n in sorted(set(names)) if names.count(n) > 1]
        plain = {n.strip("[]") for n in names}
        errs += [f"calc caption '{c.get('caption')}' equals a field name in {el.get('name') or el.get('datasource')}"
                 for c in cols if c.find("calculation") is not None and c.get("caption") in plain and c.get("name") != f"[{c.get('caption')}]"
                 and el.get("name") != "Parameters"]
    return sorted(set(errs))


def metadata_errors(path):
    """Every <cols> map needs a column metadata-record with the same local-name and the map's relation as parent."""
    errs = []
    for ds in ET.parse(path).getroot().iter("datasource"):
        recs = {r.findtext("local-name"): r.findtext("parent-name") for r in ds.iter("metadata-record") if r.get("class") == "column"}
        for m in ds.iter("map"):
            if m.get("value", "").startswith("[") and "].[" in m.get("value", "") and ds.find("connection") is not None:
                parent = m.get("value").split("].[")[0] + "]"
                if m.get("key") not in recs:
                    errs.append(f"{ds.get('caption')}: no metadata-record for {m.get('key')}")
                elif recs[m.get("key")] != parent:
                    errs.append(f"{ds.get('caption')}: {m.get('key')} record parent {recs[m.get('key')]} but map says {parent}")
    return errs


def xsd_errors(path):
    """Validate against the official Tableau 2026.3 schema (github.com/tableau/tableau-document-schemas)."""
    from lxml import etree
    d = Path(__file__).parent / "schema"
    xsd = (d / "twb_2026.3.0.xsd").read_text(encoding="utf-8")
    xsd = xsd.replace('<xs:import namespace="http://www.tableausoftware.com/xml/user"/>',
                      f'<xs:import namespace="http://www.tableausoftware.com/xml/user" schemaLocation="{(d / "user_stub.xsd").as_uri()}"/>')
    xsd = xsd.replace('<xs:import namespace="http://www.w3.org/XML/1998/namespace"/>',
                      f'<xs:import namespace="http://www.w3.org/XML/1998/namespace" schemaLocation="{(d / "xml_stub.xsd").as_uri()}"/>')
    schema = etree.XMLSchema(etree.fromstring(xsd.encode("utf-8"), base_url=d.as_uri() + "/"))
    # Resolve feature flags the way Desktop does: keep the .true... form, drop the .false... form
    txt = Path(path).read_text(encoding="utf-8")
    txt = re.sub(r"<_\.fcp\.[A-Za-z_]+\.false\.\.\.([a-z-]+)\b.*?</_\.fcp\.[A-Za-z_]+\.false\.\.\.\1>", "", txt, flags=re.S)
    txt = re.sub(r"<_\.fcp\.[A-Za-z_]+\.false\.\.\.[^>]*/>", "", txt)
    txt = re.sub(r"(</?)_\.fcp\.[A-Za-z_]+\.true\.\.\.", r"\1", txt)
    txt = re.sub(r" _\.fcp\.[A-Za-z_]+\.true\.\.\.", " ", txt)
    doc = etree.fromstring(txt.encode("utf-8")).getroottree()
    # explain-data is required by the XSD yet absent from the Superstore sample Desktop itself ships
    return [] if schema.validate(doc) else [f"XSD line {e.line}: {e.message}" for e in schema.error_log
                                            if "explain-data" not in e.message]


if __name__ == "__main__":
    xs = xsd_errors(sys.argv[1])
    for e in xs[:40]:
        print("XSD:", e)
    print(f"{len(xs)} XSD errors")
    errs, warns = check(sys.argv[1])
    errs += xs + duplicate_errors(sys.argv[1]) + metadata_errors(sys.argv[1])
    for w in warns:
        print("warn:", w)
    for e in errs:
        print("ERROR:", e)
    print(f"{len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)
