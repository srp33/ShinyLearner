package shinylearner.core;

import shinylearner.helper.FileUtilities;

import java.util.ArrayList;

public class OutputFileProcessor
{
	private static ArrayList<String> FeatureSelectionOutLines = new ArrayList<String>();
	private static ArrayList<String> PredictionOutLines = new ArrayList<String>();
	private static ArrayList<String> BenchmarkOutLines = new ArrayList<String>();
	
	public static void AddFeatureSelectionOutputLine(String output, boolean force) throws Exception
	{
		if (!Settings.OUTPUT_FEATURES_FILE_PATH.equals("") && !output.equals(""))
			FeatureSelectionOutLines.add(output);
		
		FlushToFile(Settings.OUTPUT_FEATURES_FILE_PATH, FeatureSelectionOutLines, force);
	}
	
	public static void AddPredictionOutputLine(String output, boolean force) throws Exception
	{
		if (!Settings.OUTPUT_PREDICTIONS_FILE_PATH.equals("") && !output.equals(""))
			PredictionOutLines.add(output);
		
		FlushToFile(Settings.OUTPUT_PREDICTIONS_FILE_PATH, PredictionOutLines, force);
	}
	
	public static void AddBenchmarkOutputLine(String output, boolean force) throws Exception
	{
		if (!Settings.OUTPUT_BENCHMARK_FILE_PATH.equals("") && !output.equals(""))
			BenchmarkOutLines.add(output);
		
		FlushToFile(Settings.OUTPUT_BENCHMARK_FILE_PATH, BenchmarkOutLines, force);
	}
	
	private static void FlushToFile(String outFilePath, ArrayList<String> outputLines, boolean force) throws Exception
	{
		if (outFilePath.equals(""))
			return;
		
		if (outputLines.size() == 0)
			return;

		if (force || outputLines.size() >= 100000)
		{
			FileUtilities.AppendLinesToFile(outFilePath, outputLines);
			outputLines = new ArrayList<String>();
		}
	}
	
	public static void DeleteExistingOutputFiles() throws Exception
	{
		if (!Settings.OUTPUT_FEATURES_FILE_PATH.equals("") && FileUtilities.FileExists(Settings.OUTPUT_FEATURES_FILE_PATH))
			FileUtilities.DeleteFile(Settings.OUTPUT_FEATURES_FILE_PATH);
		
		if (!Settings.OUTPUT_PREDICTIONS_FILE_PATH.equals("") && FileUtilities.FileExists(Settings.OUTPUT_PREDICTIONS_FILE_PATH))
			FileUtilities.DeleteFile(Settings.OUTPUT_PREDICTIONS_FILE_PATH);
		
		if (!Settings.OUTPUT_BENCHMARK_FILE_PATH.equals("") && FileUtilities.FileExists(Settings.OUTPUT_BENCHMARK_FILE_PATH))
			FileUtilities.DeleteFile(Settings.OUTPUT_BENCHMARK_FILE_PATH);
	}
}
