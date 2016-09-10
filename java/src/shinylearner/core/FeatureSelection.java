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
		return "Description\tAlgorithmScript\tFeatures";
	}
	
	public static void SelectFeatures(String trainingFilePath) throws Exception
	{
		Log.PrintErr(Log.FormatText("Selecting features."));

		long startTime = System.nanoTime();

		String algorithmOutput = SelectFeaturesCommand(trainingFilePath);

		if (Settings.OUTPUT_BENCHMARK_FILE_PATH != "")
			FileUtilities.AppendLineToFile(Settings.OUTPUT_BENCHMARK_FILE_PATH, Benchmark.GetBenchmarkValues(startTime));
		
		if (!Settings.OUTPUT_FEATURES_FILE_PATH.equals(""))
			FileUtilities.AppendLineToFile(Settings.OUTPUT_FEATURES_FILE_PATH, GetOutput(algorithmOutput));
	}
	
    private static String SelectFeaturesCommand(String dataFilePath) throws Exception
    {
        String parameters = "\"" + dataFilePath + "\"";
        Log.Debug(Singletons.ExperimentItems.AlgorithmScriptFilePath + " " + parameters);
        //Log.Exit(1);
        return MiscUtilities.ExecuteShellCommand(Singletons.ExperimentItems.AlgorithmScriptFilePath + " " + parameters);
    }
    
    private static String GetOutput(String algorithmOutput) throws Exception
    {
    	StringBuffer output = new StringBuffer();

    	for (String outputLine : algorithmOutput.split("\n"))
    	{
    		if (outputLine.trim().length() == 0)
    			continue;

    		String[] outputLineItems = outputLine.split("\t");
    		String selectedFeatures = MiscUtilities.UnformatName(outputLineItems[0]);
		
    		ArrayList<String> outputVals = new ArrayList<String>();
    		outputVals.add(Singletons.ExperimentItems.Description);
    		outputVals.add(Singletons.ExperimentItems.AlgorithmScriptFilePath);
    		outputVals.add(selectedFeatures);

    		output.append(ListUtilities.Join(outputVals, "\t"));
    	}
    	
    	return output.toString();
    }
}
