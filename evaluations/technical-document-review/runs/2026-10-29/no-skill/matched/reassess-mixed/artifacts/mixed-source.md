# Batch source record

Synthetic authoritative facts for this exercise.

The pilot used the same 40 requests. A succeeded on 20; B on 24. Servers changed
as well as scheduler, so component effects cannot be isolated.

The admission example creates one task for each of 100 inputs, then awaits them
all. Each operation acquires a semaphore of four before starting its work.

Protocol revision 2 requires the service to include a receipt ID in every
successful response. The document adopts RFC 2119 and RFC 8174 requirement terms.

The sampling summary uses the median for resistance to outliers. "Robust" is a
technical characterization of that estimator, not a performance guarantee.
