# p2d — frequently asked questions

*The questions agents, brokers, and sellers ask — answered the way p2d is actually built.*

## Trust

**Will it invent features my listing doesn't have?**
This is the problem p2d exists to solve. The copy may only draw from features you confirmed from the photos and facts from the record. An independent checker (not the writer) traces every line to its evidence; anything unsupported is softened before you see it; numbers are compared against the record digit-for-digit. The operating rule: *no claim without a pixel.*

**What does "auto-softened" mean?**
A claim that overreached its evidence was minimally weakened — "imported Carrara marble" becomes "stone countertops" — and the repaired line is re-verified. Softening can remove or weaken claims; it can never add one.

**Can a beautiful photo make it say "newly renovated"?**
No. Photo trust is deliberately asymmetric: photos can prove a negative ("needs work") but positive condition claims get cautious phrasing unless the record supports more. Staged and virtually-staged shots get extra discounting.

**Why should I believe the checking works?**
Because it's measured, not asserted. p2d's verifier is scored on frozen benchmark listings seeded with known "hallucination traps" — luxury features the homes don't have — and calibrated for high recall with a low false-alarm rate. Writer and checker are separate models; the writer never grades its own work.

**Who has final responsibility for what I publish?**
You — same as with a human copywriter. p2d hands you checked copy plus the receipt (**`How we checked this`**); the professional sign-off is yours.

## Compliance

**How does it handle Fair Housing?**
Three layers. The photo reader is structurally unable to output people, ethnicity, religion, school desirability, or steering language — those categories can't exist in its output format. The writer works only from that cleaned evidence. And a deterministic screening pass runs on **every** format before delivery — prohibited terms blocked, cautionary ones flagged. It's screening, not legal advice — but it's screening that runs every single time.

**Will the MLS remarks pass my board's review?**
They're generated to fit public-remarks conventions: length-limited and with agent contact information stripped (the most common rejection reason). Boards differ — a quick read against your board's rules is still wise.

## Privacy and ownership

**What happens to my photos?**
Processed in memory, not stored. p2d keeps the derived feature list (so later refines stay grounded), not your images.

**Who owns the copy?**
You do. p2d claims no ownership of your output; whatever rights exist are yours.

**Is my data used to train models?**
Your original inputs aren't used for training and aren't sold. Quality calibration uses de-identified aggregates and p2d's own generated outputs.

**Can I get my data out, or delete it?**
Both, from your account: export as portable JSON, or delete your account and its listings.

## Practical

**Do I need to know how to "prompt"?**
No. If you can pick photos and answer plain questions, you can use p2d. There is no prompt box to master — the craft is in the pipeline, not in your typing.

**How long does one listing take?**
About two minutes of machine time — photo reading (~30–45 s for a dozen shots) plus writing and checking — and a few minutes of your judgment at the confirm screen.

**How many photos should I upload?**
Your 12–15 strongest. Duplicates are auto-detected, and features only need one clear photo to count as evidence.

**What does it cost?**
A finished listing (all five formats) is 10 credits by default; AI refines are 1 credit with the first free per listing; manual edits are always free. Plans and packs: the pricing page in-app (**`Buy credits`**).

**Is it only for $5M+ listings?**
It's built and calibrated for the luxury tier — where a fabricated sentence costs the most and pedigree matters. That's where its checking, designer registry, and register options earn their keep.

**My listing has no MLS number yet.**
Enter facts by hand — pre-MLS is a common moment to prepare the campaign. Add the number later when it exists.

**I use ohm too — separate account?**
Same Sum28 account signs in to both. The description p2d writes is exactly what an ohm listing's visitor packet wants — see [ohm's lesson 5](../ohm/guide/05-listings-and-p2d.md).
