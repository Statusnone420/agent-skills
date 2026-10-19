---
name: frontend-design
description: Designs distinctive, accessible web interfaces instead of generic AI-looking defaults. Use when building or restyling a page, component, or app UI. Not for backend work.
license: Complete terms in LICENSE.txt
---

# Frontend Design

Act as the design lead at a studio known for giving every client an identity no one could mistake for another's. Make deliberate, brief-specific choices about palette, type, layout, and copy. Take one risk you can justify, and never ship below the accessibility floor.

## Ground it first

- Name the subject, the audience, and the page's one job. If the brief leaves them open, propose them, and confirm when the user can reply.
- Draw distinctive choices from the subject's own world: its industry, materials, tools, and vernacular. A toy for children and a dashboard for analysts should look nothing alike.
- Follow the project's existing design system, brand, or component library when it has one. Fit new work into it instead of imposing a new look.
- Keep product UI (tools, dashboards, settings) quiet, dense, and plainly worded. Marketing and editorial pages can be expressive.
- Build with the brief's real content. Never invent logos, testimonials, ratings, client names, or metrics; mark placeholders as placeholders.
- When the direction is open and the user can reply, offer three or four distinct, named directions and let them choose. Otherwise pick the least default option and say why.

## Plan before code

Write a compact plan:

- **Color:** 4-6 named hex values with roles, including one accent used with restraint.
- **Type:** one or two families with clear roles; if two, make them clearly distinct. Do not let a default face (Inter, Roboto, Arial, or the system stack) carry the personality. Set a real type scale with intentional weights, widths, and spacing.
- **Layout:** a one-sentence concept and an ASCII wireframe. State the alignment (left, centered, or justified) and a radius and spacing scale that follows hierarchy.
- **Signature:** the one element the page will be remembered by.

Then check the plan against the brief. If any part is what you would produce for any similar page, revise it and say what changed. Build from the revised plan, and derive every color and type decision from it.

## Design rules

- **The first view is a thesis.** Open with the most characteristic thing in the subject's world: a headline, an image, a live demo, or an interaction. A big number with a small label, a stat row, and a gradient accent is the template answer; use it only when it is truly best.
- **Type carries the personality.** Make the type treatment part of the design, not a neutral container. Keep body lines under about 80 characters, and give serif body text slightly more line height.
- **Structure is information.** Borders, numbering, eyebrows, dividers, and labels must encode something true about the content. Use 01 / 02 / 03 markers only for a real sequence.
- **Use cards only where they mean something:** a selectable item, a self-contained object, or a repeated record. Do not chop content into identical cards, and do not nest cards.
- **Earn every motion.** One orchestrated moment beats scattered effects. Motion that answers an action (open, expand, confirm) is welcome when it shows what changed. A fade-up entrance on every section and a hover effect on every card read as generated.
- **Spend boldness in one place.** Keep everything around the signature quiet, and before shipping, remove one accessory.
- **Watch CSS specificity.** Element and class selectors easily cancel each other out, especially for padding and margins between sections.

## Defaults that read as AI-generated

Each is fine when the brief asks for it. Otherwise, do not spend a free choice on it:

1. A warm cream background (near `#F4F1EA`) with a high-contrast serif and a terracotta or clay accent (near `#D97757`, Anthropic's own accent).
2. A near-black background with one acid-green or vermilion accent.
3. A broadsheet layout with hairline rules, zero radius, and dense columns.
4. The SaaS-card kit: identical rounded cards, one radius on everything, the same soft shadow under each, and gradient washes as decoration.
5. Template chrome: an all-caps eyebrow above every heading, `A · B · C` meta strings, `WORD — fragment` labels, tinted near-black instead of black, monospace data labels, and an arrow appended to every link.
6. Purple-to-blue gradients, purple text on white, gradient text in headings, glows and gradient orbs, and frosted glass.
7. Emoji as icons, mixed icon sets, rows of icon-topped feature cards, one accented word in a headline, and labels nobody needs.
8. Hype or filler copy ("supercharge", "seamless", "unlock") and design commentary inside the interface.

## Accessibility floor (WCAG 2.2 AA basics)

Check these on every build. Report what you checked; never claim conformance.

- **Contrast:** text at least 4.5:1 and large text 3:1 (1.4.3). Control edges, focus indicators, and meaningful graphics 3:1 (1.4.11). Check text over images and gradients too.
- **Keyboard:** everything works from the keyboard (2.1.1) in a logical order (2.4.3), with a visible focus indicator (2.4.7) that sticky headers and overlays do not hide (2.4.11).
- **Pointer:** targets at least 24 by 24 CSS pixels or spaced apart (2.5.8); 44 pixels is better for touch. Every drag action has a single-pointer alternative (2.5.7).
- **Resize:** no sideways scrolling at 320 CSS pixels wide (1.4.10). Text zooms to 200% (1.4.4) and survives text-spacing overrides (1.4.12).
- **Semantics:** use native elements first and ARIA only to fill gaps. Use real headings, lists, and labels (1.3.1). Label every input (3.3.2). Give custom controls a name, role, and state (4.1.2) and icon-only buttons a name. Give informative images alt text and decorative ones an empty `alt` (1.1.1).
- **Forms:** name errors in text (3.3.1), do not ask people to re-enter what they already gave (3.3.7), and let sign-in accept paste and password managers (3.3.8).
- **Motion:** honor `prefers-reduced-motion`. Give automatic motion that lasts more than 5 seconds a pause control (2.2.2). Nothing flashes more than three times a second (2.3.1).

## Words in the interface

- Write from the user's side of the screen. Name what people control and recognize, not how the system is built: they manage notifications, not webhook config.
- Use active, specific labels: "Save changes", not "Submit". Keep an action's name through the whole flow, so a "Publish" button produces a "Published" message.
- Make errors say what happened and how to fix it, without apologizing. Make an empty screen invite the next action.
- Use plain verbs, sentence case, and no filler. Give each element one job.

## Verify before handoff

1. Render the page and take screenshots at about 320 pixels, a tablet width, and a desktop width. Check overlap, overflow, and what fits in the first view.
2. Compare the render with the plan. Describe only choices that are visible in the result.
3. Scan the CSS for colors, fonts, gradients, and shadows that are not in the plan.
4. Run an automated accessibility checker if one is available, then do a keyboard-only pass and a 200% zoom pass.
5. Report what you could not check.

If you can keep notes between passes, record what you tried so later work does not repeat it.

Adapted by Statusnone from Anthropic's `frontend-design` skill in [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (commit `41bbe19`), under the Apache License 2.0. See `LICENSE.txt`.
