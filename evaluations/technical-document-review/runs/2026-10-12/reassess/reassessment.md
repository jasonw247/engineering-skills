# Reassessment

No remaining material issues were found within the requested scope. Reviewed the complete `revised.md` against all four findings in `prior-findings.md` and the supplied `source-note.md`. This was an editorial and supplied-evidence review; inputs were not edited, and no external source audit or code execution was performed.

| Prior finding | Status and evidence in the revision |
| --- | --- |
| Percentage units and reranker attribution | Resolved in Pilot result. The revision reports 5 percentage points, gives the 70/100 and 75/100 results, identifies both configurations' reader and context cap, and states that the reranker's contribution is not isolated. |
| Proposed threshold reported as an achieved gain | Resolved in Next experiment. The study is described as planned, the five-percentage-point threshold as proposed, and results as unavailable. |
| Post-warmup timing labeled cold-start | Resolved in Runtime check. The text accurately describes one invocation after warmup and excludes startup and model loading. |
| Unsupported immediate production replacement | Resolved in Pilot result. The revision acknowledges missing uncertainty and latency measurements and states that the pilot alone does not establish a production promotion decision. |

No demonstrated regressions were found. The pressure limit is directly supported by P-17 revision B, §7; the self-contained exception is sufficient at 70 °C. The Compatibility note agrees with the supplied source.

The underlying experimental uncertainties remain, but the revision now represents them accurately. They are not remaining document defects, and no further prose changes are required by these findings.
