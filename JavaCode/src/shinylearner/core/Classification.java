package shinylearner.core;

import shinylearner.helper.ListUtilities;
import shinylearner.helper.MiscUtilities;

import java.util.ArrayList;

/** This class acts as a wrapper for performing classification tasks. It interprets parameters for executing these tasks, based on what has been configured.
 * @author Stephen Piccolo
 */
public class Classification
{
	public static void Classify(String trainingFilePath, String testFilePath) throws Exception
	{
		Log.Debug("Classifying.");

		long startTime = System.nanoTime();

		String predictionOutput = TrainTest(trainingFilePath, testFilePath);
		Log.Debug(predictionOutput);
		//Log.Exit(1);

		OutputFileProcessor.AddBenchmarkOutputLine(Benchmark.GetBenchmarkValues(startTime), false);
		OutputFileProcessor.AddPredictionOutputLine(GetPredictionOutput(ParsePredictions(predictionOutput, Singletons.ExperimentItems.TestIDs)), false);
	}

	private static String TrainTest(String trainingFilePath, String testFilePath) throws Exception
	{
		String dependentVariableOptions = ListUtilities.Join(AnalysisFileCreator.FormatClassValues(Singletons.Data.GetClassOptions()), ",");
		String parameters = "\"" + trainingFilePath + "\" \"" + testFilePath + "\" \"" + dependentVariableOptions + "\" " + Settings.NUM_CORES + " " + Settings.DEBUG;

		Log.Debug(Singletons.ExperimentItems.AlgorithmScriptFilePath + " " + parameters);
		//Log.Exit(1);

		return MiscUtilities.ExecuteShellCommand("\"" + Singletons.ExperimentItems.AlgorithmScriptFilePath + "\" " + parameters);
	}

	private static ArrayList<AbstractPrediction> ParsePredictions(String predictionOutput, ArrayList<String> testIDs) throws Exception
	{
		ArrayList<AbstractPrediction> predictions = new ArrayList<AbstractPrediction>();
		ArrayList<String> tempTestIDs = ListUtilities.CreateStringList(testIDs);

		for (String line : predictionOutput.split("\n"))
		{
			if (!line.startsWith(AnalysisFileCreator.CLASS_TEMP_PREFIX))
				continue;

			String[] lineItems = line.split("\t");

			String instanceID = tempTestIDs.remove(0);
			String actualClass = Singletons.Data.GetClassValue(instanceID);
			String prediction = lineItems[0];

			ArrayList<String> probabilities = new ArrayList<String>();
			for (int j=1; j<lineItems.length; j++)
				probabilities.add(lineItems[j].trim());

			predictions.add(new Prediction(instanceID, actualClass, prediction, probabilities));
			//Log.Debug(instanceID);
			//Log.Debug(actualClass);
			//Log.Debug(prediction);
			//Log.Debug(probabilities.size());
		}
		//Log.Debug("got here");
		//Log.Exit(1);
		
		if (tempTestIDs.size() > 0)
		{
			Log.Debug("An error occurred for " + Singletons.ExperimentItems.AlgorithmScriptFilePath + " and " + Singletons.ExperimentItems.Description + ".\n\nAlgorithm output:\n" + predictionOutput);

			predictions = new ArrayList<AbstractPrediction>();

			for (String testID : testIDs)
				predictions.add(new NullPrediction(testID, Singletons.Data.GetClassValue(testID)));
		}

		return predictions;
	}

	public static String GetOutputHeader()
	{
		String header = "Description\tAlgorithm\tInstanceID\tActualClass\tPredictedClass";

		for (String x : Singletons.Data.GetClassOptions())
			header += "\t" + AnalysisFileCreator.UnformatClassValue(x);

		return header;
	}

	private static String GetPredictionOutput(ArrayList<AbstractPrediction> predictions) throws Exception
	{
		ArrayList<String> outLines = new ArrayList<String>();

		// Loop through the predictions and construct the output
		for (AbstractPrediction prediction : predictions)
		{
			ArrayList<String> outputVals = new ArrayList<String>();

			outputVals.add(Singletons.ExperimentItems.Description);
			outputVals.add(Singletons.ExperimentItems.AlgorithmScriptFilePath);
			outputVals.add(AnalysisFileCreator.UnformatName(prediction.InstanceID));
			outputVals.add(AnalysisFileCreator.UnformatClassValue(prediction.DependentVariableValue));
			outputVals.add(AnalysisFileCreator.UnformatClassValue(prediction.Prediction));

			for (String classProbability : prediction.ClassProbabilities)
				outputVals.add(classProbability);

			outLines.add(ListUtilities.Join(outputVals, "\t"));
		}

		return ListUtilities.Join(outLines, "\n");
	}
}