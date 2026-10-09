import { parseCase, label, search } from './graph.mjs';

const $ = id => document.getElementById(id);
let graph;
let selected;

function link(value) {
  if (value.startsWith('https://github.com/ArazSaieArasi3/CM-PharmE/')) {
    const a = document.createElement('a'); a.href = value; a.textContent = 'CM-PharmE source snapshot'; a.target = '_blank'; a.rel = 'noopener noreferrer'; return a;
  }
  const span = document.createElement('span'); span.textContent = value; return span;
}
function relationRows(id, direction) {
  const body = $(id); body.replaceChildren();
  const relations = selected[direction];
  if (!relations.length) { const row = body.insertRow(); row.insertCell().textContent = 'No asserted links'; return; }
  for (const r of relations) {
    const row = body.insertRow(); row.insertCell().textContent = label(r.predicate);
    const cell = row.insertCell(); const target = direction === 'outgoing' ? r.object : r.subject;
    if (graph.entities.has(target)) {
      const button = document.createElement('button'); button.textContent = label(target); button.title = target;
      button.addEventListener('click', () => select(target)); cell.append(button);
    } else cell.textContent = label(target);
  }
}
function select(id) {
  selected = graph.entities.get(id);
  $('title').textContent = label(id); $('iri').textContent = id;
  $('types').textContent = selected.types.map(label).join(', ') || 'No asserted type';
  const sources = $('sources'); sources.replaceChildren();
  selected.sources.forEach((s, i) => { if (i) sources.append(', '); sources.append(link(s)); });
  if (!selected.sources.length) sources.textContent = 'No asserted source';
  relationRows('outgoing', 'outgoing'); relationRows('incoming', 'incoming');
  renderList();
}
function renderList() {
  const entities = search(graph, $('filter').value);
  $('status').textContent = `${entities.length} of ${graph.entities.size} typed case entities; ${graph.triples.length} asserted triples`;
  const list = $('entities'); list.replaceChildren();
  for (const e of entities) {
    const item = document.createElement('li'); const button = document.createElement('button');
    button.textContent = `${label(e.id)} · ${e.types.map(label).join(', ') || 'untyped'}`;
    button.setAttribute('aria-current', String(e === selected));
    button.addEventListener('click', () => select(e.id)); item.append(button); list.append(item);
  }
}
try {
  const response = await fetch('./data/CASE_INSTANCE_GRAPH.nt');
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  graph = parseCase(await response.text());
  $('filter').addEventListener('input', renderList);
  select([...graph.entities.keys()].find(id => id.endsWith('PROD-CMPE-EXPLORER')) ?? [...graph.entities.keys()][0]);
} catch (error) { $('status').textContent = `Cannot load fixture: ${error.message}. Serve this directory through a local HTTP server.`; }
