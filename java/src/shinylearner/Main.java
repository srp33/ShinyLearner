package shinylearner;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import shinylearner.core.AnalysisFileCreator;
import shinylearner.core.Benchmark;
import shinylearner.core.Classification;
import shinylearner.core.ExperimentItems;
import shinylearner.core.FeatureSelection;
import shinylearner.core.InstanceManager;
import shinylearner.core.Log;
import shinylearner.core.OutputFileProcessor;
import shinylearner.core.Settings;
import shinylearner.core.Singletons;
import shinylearner.helper.FileUtilities;
import shinylearner.helper.MiscUtilities;

import com.linkedin.paldb.api.Configuration;
import com.linkedin.paldb.api.PalDB;

/** This is the class that gets invoked when code begins to execute.
 * @author Stephen Piccolo
 */
public class Main
{
	/** This method is the first one invoked when code is run from the command line. It sets up an experiment, processes it, and handles exceptions at a high level.
	 *
	 * @param args Array of arguments that are passed to this application from the Java runtime
	 */
	public static void main(String[] args)
	{
		try
		{
			Log.Info("Parsing command line settings...");
			Settings.ParseCommandLineSettings(args);
			Settings.Check();
			
			Log.Info("Loading data from input files...");
			Singletons.DatabaseFilePath = Settings.TEMP_DIR + "/" + MiscUtilities.GetUniqueID() + ".db";			
			Singletons.DatabaseWriter = PalDB.createWriter(new File(Singletons.DatabaseFilePath));
			InstanceManager.LoadDataInstances();
			Singletons.DatabaseWriter.close();
			
			Log.Info("Refining data instances...");
			
			Configuration config = PalDB.newConfiguration();
			config.set(Configuration.COMPRESSION_ENABLED, "true");
			Singletons.DatabaseReader = PalDB.createReader(new File(Singletons.DatabaseFilePath), config);

			InstanceManager.RefineDataInstances();

			if (!Settings.OUTPUT_DATA_FILE_PATH.equals(""))
				InstanceManager.SaveOutputDataFile();
			
			if (!Settings.OUTPUT_PREDICTIONS_FILE_PATH.equals("") || !Settings.OUTPUT_FEATURES_FILE_PATH.equals("") || !Settings.OUTPUT_BENCHMARK_FILE_PATH.equals(""))
			{
				Log.Info("Starting analysis...");
				PerformAnalysis();
			}
			
			Singletons.DatabaseReader.close();
			
			FileUtilities.DeleteFile(Singletons.DatabaseFilePath);

			Log.PrintOut("Successfully completed!");
			
			System.exit(0); // Not sure if this is necessary, but keeping it just in case
		}
		catch (Exception ex)
		{
			Log.PrintOut(Log.GetStackTrace(ex));
			
			try
			{
				if (Singletons.DatabaseWriter != null)
					Singletons.DatabaseWriter.close();
			}
			catch (Exception ex2) {}

			try
			{
				if (Singletons.DatabaseReader != null)
					Singletons.DatabaseReader.close();
			}
			catch (Exception ex3) {}
			
			try
			{
				if (Singletons.DatabaseFilePath != null && FileUtilities.FileExists(Singletons.DatabaseFilePath))
					FileUtilities.DeleteFile(Singletons.DatabaseFilePath);
			}
			catch (Exception ex4) {}

			System.exit(1); // Not sure if this is necessary, but keeping it just in case
		}
	}

	private static void PerformAnalysis() throws Exception
	{
		OutputFileProcessor.DeleteExistingOutputFiles();
		OutputFileProcessor.AddFeatureSelectionOutputLine(FeatureSelection.GetOutputHeader(), false);
		OutputFileProcessor.AddPredictionOutputLine(Classification.GetOutputHeader(), false);
		OutputFileProcessor.AddBenchmarkOutputLine(Benchmark.GetBenchmarkHeader(), false);

		List<ExperimentItems> experimentItemsList = new ArrayList<ExperimentItems>();
		int lineNumber = 1;
		for (ArrayList<String> lineItems : FileUtilities.ParseDelimitedFile(Settings.EXPERIMENT_FILE))
		{
			experimentItemsList.add(new ExperimentItems(lineNumber, lineItems));
			lineNumber++;
		}
		
        Collections.sort(experimentItemsList);
        
        ExperimentItems previousExperimentItems = null;
        String trainingFilePath = null;
        String testFilePath = null;

        ArrayList<Integer> progressBarThresholds = GetProgressBarThresholds(experimentItemsList);

        for (int i=0; i<experimentItemsList.size(); i++)
        {
        	ExperimentItems experimentItems = experimentItemsList.get(i);

        	if (!Settings.DEBUG && progressBarThresholds.contains(i))
        		ShowProgress(progressBarThresholds, i);
        	
        	Singletons.ExperimentItems = experimentItems;

        	// Should only create test file if we are doing classification        	
        	if (previousExperimentItems == null || !experimentItems.Key.equals(previousExperimentItems.Key))
			{
        		// Delete any previous files that were created
        		if (trainingFilePath != null)
        			FileUtilities.DeleteFile(trainingFilePath);
        		
        		if (experimentItems.IsClassificationAnalysis && testFilePath != null)
        			FileUtilities.DeleteFile(testFilePath);
        		
        		trainingFilePath = AnalysisFileCreator.CreateFile(Singletons.ExperimentItems.AlgorithmDataFormat, Singletons.ExperimentItems.TrainingIDs, Singletons.ExperimentItems.DataPointsToUse, true);
        		
        		if (experimentItems.IsClassificationAnalysis)
        			testFilePath = AnalysisFileCreator.CreateFile(Singletons.ExperimentItems.AlgorithmDataFormat, Singletons.ExperimentItems.TestIDs, Singletons.ExperimentItems.DataPointsToUse, false);
			}
			
			if (experimentItems.IsClassificationAnalysis)
				Classification.Classify(trainingFilePath, testFilePath);
			else
				FeatureSelection.SelectFeatures(trainingFilePath);
			
			previousExperimentItems = experimentItems;
		}

        // Make sure all the output lines are flushed at the end
		OutputFileProcessor.AddFeatureSelectionOutputLine("", true);
		OutputFileProcessor.AddPredictionOutputLine("", true);
		OutputFileProcessor.AddBenchmarkOutputLine("", true);
	}

	private static ArrayList<Integer> GetProgressBarThresholds(List<ExperimentItems> experimentItemsList)
	{
		double progressBarStepSize = (double)experimentItemsList.size() / 100.0;
        ArrayList<Integer> progressBarThresholds = new ArrayList<Integer>();
        
        for (double x=0.0; x<=(double)experimentItemsList.size(); x+=progressBarStepSize)
        {
        	int step = (int)x;
        	
        	if (!progressBarThresholds.contains(step))
        		progressBarThresholds.add(step);
        }
        
		return progressBarThresholds;
	}

	private static void ShowProgress(ArrayList<Integer> progressBarThresholds, int i)
	{
		int thresholdIndex = progressBarThresholds.indexOf(i);
		int percent = (int)((float)progressBarThresholds.get(thresholdIndex) * 100.0 / progressBarThresholds.get(progressBarThresholds.size() - 1));
		
		String progressOutput = "Progress: " + Integer.toString(percent) + "% ";
		for (int j=0; j<=percent; j+=2)
			progressOutput += "#";

		if (percent < 100)
			System.out.print(progressOutput += "\r");
		else
			System.out.println(progressOutput + "                                                          ");

		System.out.flush();
	}
}