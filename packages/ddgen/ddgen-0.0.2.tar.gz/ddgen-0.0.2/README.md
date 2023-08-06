# ddgen
Library of Python utilities that I needed so many times in the past


## Select RefSeq transcript with the highest priority

RefSeq transcripts have following categories: 
- `NM_`, `XM_`, `NR_`, `XR_`

If we have transcripts from multiple sources, we want to select the one coming from the source with highest priority.
> E.g. `NM_` has higher priority than `XM_`.

If we have multiple transcripts from a single source, we want to select the one with smaller integer.
> E.g. `NM_123.4` has higher priority than `NM_124.4`.

```python
from ddgen.utils import txs

# tx will be `NM_123.4`
tx = txs.prioritize_refseq_transcripts(['NM_123.4', 'NM_124.4', 'XM_100.1'])
```
