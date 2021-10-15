package shinylearner.core;

import java.util.ArrayList;

import shinylearner.helper.ListUtilities;
import shinylearner.helper.MiscUtilities;

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
		String dependentVariableOptions = ListUtilities.Join(AnalysisFileCreator.FormatClassValues(ListUtilities.SortStringList(Singletons.DependentVariableOptions)), ",");
		String parameters = "\"" + trainingFilePath + "\" \"" + testFilePath + "\" \"" + dependentVariableOptions + "\"";

		Log.Debug(Singletons.ExperimentItems.AlgorithmScriptFilePath + " " + parameters);
		//Log.Exit(1);

		return MiscUtilities.ExecuteShellCommand(Singletons.ExperimentItems.AlgorithmScriptFilePath + " " + parameters);
	}

	private static ArrayList<Prediction> ParsePredictions(String predictionOutput, ArrayList<String> testIDs) throws Exception
	{
		Log.Debug(predictionOutput);

		ArrayList<Prediction> predictions = new ArrayList<Prediction>();
		String[] predictionLines = predictionOutput.split("\n");

		Log.Debug(predictionLines.length);
		Log.Debug(testIDs.size());
		//System.exit(1);

		ArrayList<String> tempTestIDs = new ArrayList<String>();

		for (int i=0; i<predictionLines.length; i++)
		{
			if (tempTestIDs.size() == 0)
				tempTestIDs = ListUtilities.CreateStringList(testIDs);

			String[] lineItems = predictionLines[i].split("\t");

			String instanceID = tempTestIDs.remove(0);
			String actualClass = Singletons.DependentVariableInstances.get(instanceID);
			String prediction = lineItems[0];

			ArrayList<Double> probabilities = new ArrayList<Double>();
			for (int j=1; j<lineItems.length; j++)
				probabilities.add(Double.parseDouble(lineItems[j].trim()));

			predictions.add(new Prediction(instanceID, actualClass, prediction, probabilities));
		}
		
		if (tempTestIDs.size() > 0)
			Log.ExceptionFatal("The number of predictions [" + predictionLines.length + "] was not divisible by the number of test samples [" + testIDs.size() + "].\n\nAlgorithm output:\n" + predictionOutput);

		return predictions;
	}

	public static String GetOutputHeader()
	{
		String header = "Description\tAlgorithm\tInstanceID\tActualClass\tPredictedClass";

		for (String x : Singletons.DependentVariableOptions)
			header += "\t" + AnalysisFileCreator.UnformatClassValue(x);

		return header;
	}

	private static String GetPredictionOutput(ArrayList<Prediction> predictions) throws Exception
	{
		ArrayList<String> outLines = new ArrayList<String>();

		// Loop through the predictions and construct the output
		for (Prediction prediction : predictions)
		{
			ArrayList<String> outputVals = new ArrayList<String>();

			outputVals.add(Singletons.ExperimentItems.Description);
			outputVals.add(Singletons.ExperimentItems.AlgorithmScriptFilePath);
			outputVals.add(AnalysisFileCreator.UnformatName(prediction.InstanceID));
			outputVals.add(AnalysisFileCreator.UnformatClassValue(prediction.DependentVariableValue));
			outputVals.add(AnalysisFileCreator.UnformatClassValue(prediction.Prediction));

			for (double classProbability : prediction.ClassProbabilities)
				outputVals.add(String.valueOf(classProbability));

			outLines.add(ListUtilities.Join(outputVals, "\t"));
		}

		return ListUtilities.Join(outLines, "\n");
	}
}