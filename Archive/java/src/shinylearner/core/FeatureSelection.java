package shinylearner.core;

import java.util.ArrayList;

import shinylearner.helper.ListUtilities;
import shinylearner.helper.MiscUtilities;

public class FeatureSelection
{
	public static String GetOutputHeader()
	{
		return "Description\tAlgorithm\tFeatures";
	}
	
	public static void SelectFeatures(String trainingFilePath) throws Exception
	{
		Log.Debug("Selecting features.");

		long startTime = System.nanoTime();

		String algorithmOutput = SelectFeaturesCommand(trainingFilePath);
		Log.Debug(algorithmOutput);
		//Log.Exit(1);

		OutputFileProcessor.AddBenchmarkOutputLine(Benchmark.GetBenchmarkValues(startTime), false);
		OutputFileProcessor.AddFeatureSelectionOutputLine(GetOutput(algorithmOutput), false);
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
    		String selectedFeatures = AnalysisFileCreator.UnformatName(outputLineItems[0]);
		
    		ArrayList<String> outputVals = new ArrayList<String>();
    		outputVals.add(Singletons.ExperimentItems.Description);
    		outputVals.add(Singletons.ExperimentItems.AlgorithmScriptFilePath);
    		outputVals.add(selectedFeatures);

    		output.append(ListUtilities.Join(outputVals, "\t"));
    	}
    	
    	return output.toString();
    }
}
