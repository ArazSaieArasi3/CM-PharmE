"""Freeze deterministic real-source slices from HTTP Range responses."""
import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

raw_dir, out = map(Path, sys.argv[1:3])
out.mkdir(parents=True, exist_ok=True)
filename = "pharmacy_data_20260322_131416.csv"
url = "https://zenodo.org/records/19160825/files/" + filename + "?download=1"
prefix = (raw_dir / "cmpe-p1-prefix.bin").read_bytes()
header_bytes = prefix.split(b"\n", 1)[0] + b"\n"
header = next(csv.reader(io.StringIO(header_bytes.decode("utf-8"))))
expected = [0, 426009586, 852019172, 1278028758, 1650000000]
strata = []
for i, first in enumerate(expected):
    if i == 0:
        payload = prefix
        header_text = (raw_dir / "cmpe-range-headers.txt").read_text()
        n = 256
        pos = len(header_bytes)
    else:
        payload = (raw_dir / f"cmpe-p1-range-{i}.bin").read_bytes()
        header_text = (raw_dir / f"cmpe-range-{i}.headers").read_text()
        n = 128
        pos = payload.index(b"\n") + 1  # discard the partial first record
    assert "HTTP/2 206" in header_text
    match = re.search(r"content-range:\s*bytes\s+(\d+)-(\d+)/(\d+)", header_text, flags=re.I)
    assert match and (int(match[1]), int(match[2]), int(match[3])) == (first, first+len(payload)-1, 1704038344)
    selected = []
    rows = []
    row_offsets = []
    for _ in range(n):
        end = payload.find(b"\n", pos)
        assert end >= 0
        row_bytes = payload[pos:end+1]
        row = next(csv.DictReader(io.StringIO(header_bytes.decode("utf-8") + row_bytes.decode("utf-8"))))
        assert len(row) == 19 and None not in row
        selected.append(row_bytes)
        rows.append(row)
        row_offsets.append(first + pos)
        pos = end + 1
    file = out / f"nhif-p1-record19160825-stratum{i}-{n}.csv"
    file.write_bytes(header_bytes+b"".join(selected))
    strata.append({"stratum":i,"raw_range_filename":"cmpe-p1-prefix.bin" if i==0 else f"cmpe-p1-range-{i}.bin",
                   "raw_headers_filename":"cmpe-range-headers.txt" if i==0 else f"cmpe-range-{i}.headers",
                   "range_start":first,"range_end":first+len(payload)-1,
                   "range_bytes":len(payload),"range_sha256":hashlib.sha256(payload).hexdigest(),
                   "selection_rule":"first 256 complete data records after header" if i==0 else "discard partial first record; take first 128 complete data records",
                   "selected_file":file.name,"selected_file_bytes":file.stat().st_size,
                   "selected_file_sha256":hashlib.sha256(file.read_bytes()).hexdigest(),
                   "first_selected_source_byte_offset":row_offsets[0],
                   "last_selected_source_byte_offset":row_offsets[-1],
                   "selected_rows":len(rows),"selected_region_codes":sorted({r["region_num"] for r in rows}),
                   "selected_periods":sorted({r["period"] for r in rows}),
                   "selected_parts":sorted({r["part"] for r in rows})})
manifest={"source":"Zenodo record 19160825 / DOI 10.5281/zenodo.19160825",
          "record_url":"https://zenodo.org/records/19160825", "file_url":url,
          "published_filename":filename,"published_size_bytes":1704038344,
          "published_md5_from_Zenodo_metadata_unverified_locally":"b43fb62d3d44525de74f930f472d2f03",
          "source_license_id_from_Zenodo_API":"cc-by-4.0",
          "retrieved_local_date":"2026-10-09 Asia/Tehran",
          "source_contract_discrepancy":"W6 manifest expects nhif_outpatient_pharmacy_combined.csv, but record 19160825 publishes pharmacy_data_20260322_131416.csv; 19 required columns match this slice",
          "sampling_limit":"Five deterministic contiguous byte-range prefixes, deliberately not random or representative of the 7,266,074 source rows; whole 1.7 GB file was not downloaded or hashed locally.",
          "columns":header,"strata":strata,"selected_rows_total":sum(x["selected_rows"] for x in strata)}
assert manifest["selected_rows_total"] == 768
(out / "source-slice-manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"sample_rows":manifest["selected_rows_total"],"strata":[(x["stratum"],x["selected_rows"],x["selected_region_codes"],x["selected_periods"]) for x in strata]}))
