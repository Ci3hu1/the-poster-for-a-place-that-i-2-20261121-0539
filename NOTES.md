# Notes — the-poster-for-a-place-that-i-2-20261121-0539

## Top-10 study (live, 21 Nov 2026 ~13:10 WIB)

Source: GET /api/competitions/<slug>/live (performance view) and
/leaderboard?view=performance. Scores are dev-phase pairwise-judge
estimates (90% interval roughly ±45k); finals re-judge the top 80 afresh.

| Rank | Title | Live score |
| --- | --- | --- |
| 1 | NOCTARA (makegreat) | 802,665 |
| 2 | ORLUNE: The Ringed Tide | 769,564 |
| 3 | LUMISARA | 760,794 |
| 4 | LUMEN BAY — the bay where the water glows | 752,021 |
| 5 | SOLMERA — Geothermal Sea-Arch Baths | 743,189 |
| 6 | VELMARA — The City Above the Clouds | 740,246 |
| 7 | The Isle of Vellamora: dusk travel poster, spiral-conch lighthouse | 731,396 |
| 8 | PELAGIA — the garden under the sea | 731,396 |
| 9 | Velmara | 728,440 |
| 10 | SOLMARA | 728,440 |

- **All ten withhold source** (`source_withheld: true`, no repo URL, no
  clone URL). Their code and method cannot be studied — this study uses
  only what is visible: titles, live scores and output byte sizes.
  Nothing about their method is invented here.
- **Visible pattern:** every leader is maritime — bays, tides,
  sea-arch baths, gardens under the sea, lighthouses, glowing water.
  Names are invented single words, mostly ending in -ara / -ora /
  -elle / -ia (NOCTARA, ORLUNE, LUMISARA, SOLMERA, VELMARA, PELAGIA,
  SOLMARA), often with a subtitle naming the place's one feature
  ("The Ringed Tide", "the bay where the water glows", "Geothermal
  Sea-Arch Baths", "the garden under the sea").
- **Byte sizes:** 210,117–1,002,491 bytes — rich, detailed images, not
  flat minimal ones. #1 is 391,483 bytes.
- **What the judge rewards (brief, in order):** invented place + name
  in the picture; makes you want to go (weather, light, one landmark);
  distinct identity; legible intentional type; colour/composition
  leading the eye name → landmark → horizon. No quotes, star ratings
  or other copy. Clutter does not count.

## What we did differently (own recipe, world-class art)

The field is a sea. Ours is a desert of glass: VITRAEL, where the
desert is made of glass. Different terrain (desert, not coast),
different palette (amber/violet instead of blue/teal), different
landmark (a faceted glass spire instead of water), same scored
elements: invented name set large into the picture, one landmark,
golden-hour weather + light, a lone traveller as the promise of a
stay, legible intentional type, eye path name → spire → horizon.

## Verification done

- Image: 1024x1024, 230,217 bytes (gate: <= 1024x1024, <= 1,048,576).
- Viewed the render: name legible, subtitle clear of the sun, spire
  and dunes read as glass desert, traveller + shadow visible on the
  third ridge. One fix round: sun moved clear of the subtitle, murky
  tip-glow disc and cross facet line removed, dunes given irregular
  ridges + vertical gradient (first render read as ocean waves),
  traveller enlarged and shadow attached to its feet, subtitle rules
  removed.
- `main.py` is pure stdlib (copies bundled entry.png). Tests: 2/2 pass
  (`python3 tests/test_main.py`); clean-dir run verified byte-identical
  output, 1024x1024, mode 0644.
- Kit check: (filled in after the check run).
- Bundle: (filled in after the re-bundle).

## Live score / rank

- Not submitted yet — this build is reported for Joni's 'Setuju' first.
- After submit: record live score and rank here.
