package shinylearner.core;

import java.util.ArrayList;

import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;
import shinylearner.helper.Log;
import shinylearner.helper.MiscUtilities;

public class FeatureSelection
{
	public static String GetOutputHeader()
	{
		return "Description\tAlgorithmScript\tParameterDescription\tFeatures";
	}
	
	public static void SelectFeatures(String trainingFilePath) throws Exception
	{
		Log.PrintErr(Log.FormatText("Getting ready to select features."));

		long startTime = System.nanoTime();

		String algorithmOutput = SelectFeaturesCommand(trainingFilePath);

		if (Settings.OUTPUT_BENCHMARK_FILE_PATH != "")
			FileUtilities.AppendLineToFile(Settings.OUTPUT_BENCHMARK_FILE_PATH, Benchmark.GetBenchmarkValues(startTime));
		
		if (!Settings.OUTPUT_FEATURES_FILE_PATH.equals(""))
			FileUtilities.AppendLineToFile(Settings.OUTPUT_FEATURES_FILE_PATH, GetOutput(algorithmOutput));

		Log.PrintErr(Log.FormatText("Done selecting features."));
	}
	
    private static String SelectFeaturesCommand(String dataFilePath) throws Exception
    {
        String parameters = "\"" + Settings.MAIN_DIR + "\" \"" + dataFilePath + "\" \"" + Settings.USE_DEFAULT_PARAMETERS + "\"";
        Log.Debug(Singletons.ExperimentItems.AlgorithmScriptFilePath + " " + parameters);
        Log.Exit(1);
        return MiscUtilities.ExecuteShellCommand(Singletons.ExperimentItems.AlgorithmScriptFilePath + " " + parameters);
    }
    
    private static String GetOutput(String algorithmOutput) throws Exception
    {
    	String[] outputLines = algorithmOutput.trim().split("\n");
    	String parameterDescription = outputLines[0];
		String selectedFeatures = MiscUtilities.UnformatName(outputLines[1]);
		
        ArrayList<String> outputVals = new ArrayList<String>();

        outputVals.add(Singletons.ExperimentItems.Description);
        outputVals.add(Singletons.ExperimentItems.AlgorithmScriptFilePath);
        outputVals.add(parameterDescription);
        outputVals.add(selectedFeatures);

        return ListUtilities.Join(outputVals, "\t");
    }
}
