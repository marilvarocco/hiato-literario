export function countWords(text) {
  const clean = text.trim();
  if (!clean) return 0;
  return (clean.match(/\S+/g) || []).length;
}

export function countCharacters(text) {
  return text.length;
}

export function countCharactersWithoutSpaces(text) {
  return text.replace(/\s/g, "").length;
}

export function countSentences(text) {
  const clean = text.trim();
  if (!clean) return 0;
  const matches = clean.match(/[^.!?]+[.!?]+|[^.!?]+$/g);
  return matches ? matches.length : 0;
}

export function countParagraphs(text) {
  const clean = text.trim();
  if (!clean) return 0;
  return clean.split(/\n\s*\n/).filter(Boolean).length;
}
