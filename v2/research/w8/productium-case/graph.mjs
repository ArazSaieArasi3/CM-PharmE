// Small N-Triples reader for this fixed, URI/literal-only case fixture.
// It rejects unsupported syntax instead of silently omitting evidence.
const TRIPLE = /^<([^>]+)> <([^>]+)> (?:<([^>]+)>|"((?:[^"\\]|\\.)*)"(?:@[a-zA-Z-]+|\^\^<[^>]+>)?) \.$/;

export const TYPE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type';
export const SOURCE = 'http://purl.org/dc/terms/source';

export function parseCase(text) {
  const triples = text.split(/\r?\n/).filter(Boolean).map((line, i) => {
    const match = line.match(TRIPLE);
    if (!match) throw new Error(`Unsupported N-Triples line ${i + 1}`);
    return { subject: match[1], predicate: match[2], object: match[3] ?? match[4], literal: match[3] === undefined };
  });
  const entities = new Map();
  for (const triple of triples) {
    if (!entities.has(triple.subject)) entities.set(triple.subject, { id: triple.subject, types: [], sources: [], outgoing: [], incoming: [] });
    const entity = entities.get(triple.subject);
    if (triple.predicate === TYPE) entity.types.push(triple.object);
    else if (triple.predicate === SOURCE) entity.sources.push(triple.object);
    else entity.outgoing.push(triple);
  }
  for (const triple of triples) {
    if (!triple.literal && entities.has(triple.object) && triple.predicate !== TYPE && triple.predicate !== SOURCE) {
      entities.get(triple.object).incoming.push(triple);
    }
  }
  return { triples, entities };
}

export function label(iri) {
  if (iri.startsWith('urn:r033:cmpe-explorer:')) return iri.split(':').at(-1);
  return decodeURIComponent(iri.split(/[/#]/).at(-1) || iri);
}

export function search(graph, term = '') {
  const needle = term.trim().toLowerCase();
  return [...graph.entities.values()].filter(e => [e.id, ...e.types, ...e.sources].some(s => s.toLowerCase().includes(needle)))
    .sort((a, b) => label(a.id).localeCompare(label(b.id)));
}
