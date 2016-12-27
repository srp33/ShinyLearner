When performing benchmark comparisons across multiple algorithms and/or hyperparameters, it is important to exercise caution in interpreting those results. Below are some recommendations on performing benchmarks and interpreting results.

* If you apply multiple algorithms or hyperparameter combinations, you should always report those in any reports (e.g., journal articles) you publish based on those findings. It is poor form to report only the best results.
* After you have identified the best performing algorithm and/or hyperparameters, it is usually best to test those findings on a completely independent dataset that was not used in the benchmark comparison. We plan to implement this functionality within ShinyLearner. Please let us know if this is a feature you would like us to prioritize.
* Just because an algorithm (or hyperparameters) appears to work well in one setting doesn't necessarily mean that the same will be true in alternate settings.
