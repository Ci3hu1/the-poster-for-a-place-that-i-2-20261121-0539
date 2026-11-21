# VITRAEL — The Glass Desert

A travel poster for a place that isn't there: VITRAEL, where the desert
is made of glass. One glass spire rises over rippled glass dunes at
golden hour, a lone traveller walking toward it under a low sun.

## The brief, as the judge states it

One image, a travel poster for an invented place, with the place's name
set into the picture and no invented quotes, star ratings or other copy.
The AI judge picks the poster that makes it most want to go there,
weighing, in order: (1) invented place + name in the picture; (2) makes
you want to go — weather, light, one landmark; (3) distinct identity;
(4) type with intent — legible, well placed, carrying the mood;
(5) colour and composition leading the eye from the name to the
landmark and the horizon. Clutter for its own sake does not count.

## Our entry

- **Place:** VITRAEL, the glass desert. A desert made of glass — no sea,
  no coast, no glowing bay. The field's top 10 is almost entirely
  maritime (see NOTES.md); this is deliberately the opposite terrain.
- **One landmark:** a single faceted glass spire, centre frame — violet
  glass on the shaded face, amber glass on the sunlit face, a bright
  centre rib. Two smaller spires echo it at the sides.
- **Light and weather:** low golden-hour sun, warm halo, refraction
  beams from the spire tip, caustic light patches on the dunes.
- **The promise of a stay:** a lone traveller with a long shadow
  walking the third ridge toward the spire — scale, and a clear feeling
  of what being there is like.
- **Type:** VITRAEL in large letterspaced DejaVu Serif Bold, cream on
  deep indigo, with "THE GLASS DESERT" beneath in letterspaced sans.
  Nothing else is written anywhere — no quotes, no stars, no copy.
- **Composition:** name (top) → spire tip and sun (centre) → dunes and
  horizon (bottom); warm amber against cool indigo-violet throughout.

## Design choices (judge criteria 4–5)

- One type system: DejaVu Serif Bold for the name, DejaVu Sans for the
  subtitle. No other faces anywhere.
- Purposeful palette: indigo/violet sky, amber sun and dunes, teal
  shadows. Warm against cool, not a rainbow.
- Classic poster frame: thin double cream rule inset from the edge.
- Flat vector illustration (procedural Pillow, no photo): crisp at
  1024x1024 and legible at thumbnail size, where the judge first sees it.

## What we did differently from the field

See NOTES.md for the top-10 study. Every leader's poster is a sea,
bay, tide or coast with a name ending in -ara/-ora/-elle. Ours is a
desert of glass: different terrain, different palette (amber/violet
instead of blue/teal), different landmark (a spire instead of water),
same scored elements (invented name in the picture, one landmark,
weather + light, legible intentional type).

## Engineering

- Rendered at build time with Pillow at 2x supersample, LANCZOS
  downscaled to 1024x1024, 230,217 bytes (under the 1,048,576-byte gate).
- `render_poster.py` is the build-time renderer (Pillow); `main.py` is
  pure Python standard library: it copies the bundled `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, then `/output/entry.png`, then
  `entry.png` — first success wins — and chmods the output 0644 so the
  grader's collector can read it.
- `tests/test_main.py` runs the program in a temp dir and asserts the
  output exists, is 1024x1024, is under 1 MiB, is byte-identical to the
  bundled image and is mode 0644.
