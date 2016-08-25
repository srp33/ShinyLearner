package mlflexlite.core;

public class Benchmark
{
	public static String GetBenchmarkHeader()
	{
		return "Description\tAlgorithmScript\tElapsedSeconds";
	}

	public static String GetBenchmarkValues(long startTime)
	{
		return Singletons.ExperimentItems.Description + "\t" +
				Singletons.ExperimentItems.AlgorithmScriptFilePath + "\t" +
				(float)(System.nanoTime() - startTime) / 1000000000.0;
	}
}
