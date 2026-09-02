# Design QA — Project 04 跨境项目管理

- Reference: `docs/qa/01-reference.png` (selected editorial direction A, 1440 × 900)
- Implementation: `docs/qa/02-implementation.png` (local page, 1440 × 900)
- Comparison: `docs/qa/03-comparison.png`
- Additional states: `docs/qa/04-mobile-390.png`, `docs/qa/05-lightbox.png`
- Browser: Codex in-app browser

## Visual comparison

The implementation preserves the selected direction's warm editorial paper palette, oversized serif hierarchy, navy metadata, terracotta annotation, fine rules, asymmetrical hero, and restrained capsule stamps. Chinese content renders correctly in the implementation; the raw low-fidelity reference server displayed mojibake, so only its visible layout and art direction were used as the visual target.

## Responsive and interaction checks

- Desktop 1440 × 900: no horizontal overflow; primary KPI has safe right-edge spacing.
- Tablet 1024 × 768: evidence lightbox opens above page content and remains scrollable.
- Mobile 390 × 844: no horizontal overflow; navigation remains usable; hero stacks into one column.
- Both evidence screenshots open in the modal.
- Escape closes the modal and restores focus to the invoking button.
- Back links target `../index.html#timeline`.
- Reduced-motion behavior is present.

## Findings and resolution

- P1: Full-page capture appeared to duplicate sections. DOM count confirmed one instance per section; this was a scrolling screenshot stitching artifact. No code change required.
- P2: Desktop KPI sat too close to the right edge at the maximum type size. Reduced its maximum size from 118px to 106px. Resolved.
- P3: Existing project runtime reports a Tailwind CDN production warning from shared `assets/js/vendor.js`. This predates and sits outside the requested Project 04 page scope; no change made.

## Final result

final result: passed
