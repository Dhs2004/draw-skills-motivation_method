# DAPO 示例说明

基于 Yu et al., [DAPO (2025)](https://arxiv.org/abs/2503.14476v1)。

## Scientific scope

Sections 2.3–2.4, 3.1–3.4 and Algorithm 1 provide the algorithmic basis. Section 4.1 provides the illustrated clipping and length settings.

The figures are mechanism schematics, not experimental result plots. Token bars, sequence lengths, group outcomes and probability bars are illustrative. In motivation, 0/1 denotes correctness; method shows the paper's +1/−1 correctness reward. The method table shows three illustrative completions, not the actual G=16 rollout group size. Soft length reward is added to correctness before group normalization. Dynamic sampling retains prompt groups whose correctness accuracy lies strictly between 0 and 1, and collects until the target batch is filled. This is not a filter on shaped rewards.

The displayed objective makes masking explicit: m(i,t) is one for a valid completion token and zero for padding or a truncated response. Numerator and denominator both use that mask, making the unmasked token-average objective of Eq. 12 consistent with the overlong loss masking described in Section 3.4. Advantages are shared over the valid tokens in each response. The compact diagram omits the outer expectation over sampled prompts and rollouts; it displays a sampled objective. A practical implementation must handle degenerate zero reward variance numerically.

The lower/upper clip settings are 0.20/0.28. These shape the surrogate objective and are not hard bounds on realized probability changes. The length penalty is zero up to 16,384 tokens, decreases linearly to −1 at 20,480 tokens, and is capped at −1 beyond that point; truncated responses have their policy-gradient loss masked. DAPO removes the reference-policy KL term and does not train a learned value critic.

Suggested captions:

**Motivation.** Four bottlenecks in long-chain-of-thought reinforcement learning motivate DAPO's asymmetric clipping, dynamic group sampling, token-level reduction, and overlong reward shaping. Bars and group outcomes are illustrative.

**Method.** DAPO samples response groups with an old-policy snapshot, combines correctness and length-aware rewards, retains mixed-correctness prompt groups, and optimizes a masked token-level clipped objective using group-relative advantages. The diagram shows the paper's clipping and length settings; the three-response table is schematic.

## Asset provenance

Entity icons use original-color cartoon artwork. OpenMoji assets are by OpenMoji contributors under CC BY-SA 4.0; retained licenses and source records are in the sibling `../icons/` directory; new DAPO icon records are in `icon-sources.json`. New seedling, basket, and ruler icons were downloaded from OpenMoji and rasterized/cropped without recoloring. The other assets are reused from the local drawing skills.

Flaticon assets: robot 4712109, snowflake 642000, checklist 2098402, trophy 3112946, scales 924954. Sources follow `https://cdn-icons-png.flaticon.com/512/{floor(id/1000)}/{id}.png`. The question icon is reused from the skill; its original attribution is unresolved. The Flaticon authors and applicable publication/redistribution licenses have not been verified. This folder does not grant additional rights to those assets; verify their licenses and attribution before publication.


The current method diagram uses a simplified layout: three schematic completions, a compact dynamic-sampling strip, and concise clipping, token-reduction and length-shaping panels. Detailed per-response length categories and duplicate ratio/reward equations are omitted.
