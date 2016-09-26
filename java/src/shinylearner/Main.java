package shinylearner;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;

import shinylearner.core.AnalysisFileCreator;
import shinylearner.core.Benchmark;
import shinylearner.core.Classification;
import shinylearner.core.ExperimentItems;
import shinylearner.core.FeatureSelection;
import shinylearner.core.InstanceManager;
import shinylearner.core.Log;
import shinylearner.core.Settings;
import shinylearner.core.Singletons;
import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;
import shinylearner.helper.MiscUtilities;

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
			Singletons.DatabaseReader = PalDB.createReader(new File(Singletons.DatabaseFilePath));
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

			//Log.PrintOut("Successfully completed!");
			
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
		SaveOutputHeaders();

		HashMap<String, String> trainingDataFileMap = new HashMap<String, String>();
		HashMap<String, String> testDataFileMap = new HashMap<String, String>();
		
		int lineNumber = 1;

		for (ArrayList<String> lineItems : FileUtilities.ParseDelimitedFile(Settings.EXPERIMENT_FILE))
		{
			Singletons.ExperimentItems = new ExperimentItems(lineNumber, lineItems);
			lineNumber++;
			
			CheckTrainTestAssignments(Singletons.ExperimentItems.TrainingIDs, Singletons.ExperimentItems.TestIDs);

			if (!trainingDataFileMap.containsKey(Singletons.ExperimentItems.UniqueKey))
			{
				trainingDataFileMap.put(Singletons.ExperimentItems.UniqueKey, AnalysisFileCreator.CreateFile(Singletons.ExperimentItems.AlgorithmDataFormat, Singletons.ExperimentItems.TrainingIDs, Singletons.ExperimentItems.DataPointsToUse, true));
				testDataFileMap.put(Singletons.ExperimentItems.UniqueKey, AnalysisFileCreator.CreateFile(Singletons.ExperimentItems.AlgorithmDataFormat, Singletons.ExperimentItems.TestIDs, Singletons.ExperimentItems.DataPointsToUse, false));
			}

			String trainingFilePath = trainingDataFileMap.get(Singletons.ExperimentItems.UniqueKey);
			String testFilePath = testDataFileMap.get(Singletons.ExperimentItems.UniqueKey);
			
			if (Singletons.ExperimentItems.AlgorithmType.equals("Classification"))
				Classification.Classify(trainingFilePath, testFilePath);
			else
				FeatureSelection.SelectFeatures(trainingFilePath);
		}
		
		for (String filePath : trainingDataFileMap.values())
			FileUtilities.DeleteFile(filePath);
		for (String filePath : testDataFileMap.values())
			FileUtilities.DeleteFile(filePath);
	}

	private static void SaveOutputHeaders() throws Exception
	{
		if (!Settings.OUTPUT_FEATURES_FILE_PATH.equals(""))
			FileUtilities.AppendLineToFile(Settings.OUTPUT_FEATURES_FILE_PATH, FeatureSelection.GetOutputHeader());
		
		if (!Settings.OUTPUT_PREDICTIONS_FILE_PATH.equals(""))
			FileUtilities.AppendLineToFile(Settings.OUTPUT_PREDICTIONS_FILE_PATH, Classification.GetOutputHeader());
		
		if (!Settings.OUTPUT_BENCHMARK_FILE_PATH.equals(""))
			FileUtilities.AppendLineToFile(Settings.OUTPUT_BENCHMARK_FILE_PATH, Benchmark.GetBenchmarkHeader());
	}
	
    public static void CheckTrainTestAssignments(ArrayList<String> trainIDs, ArrayList<String> testIDs) throws Exception
    {
        if (trainIDs.size() == 0 || testIDs.size() == 0)
            throw new Exception("No predictions can be made because the training and/or test set have no data.");

        // Make sure the training and test IDs are in the data set we are working with
//        ArrayList<String> overlappingTrainingIDs = ListUtilities.Intersect(ListUtilities.CreateStringList(Singletons.IndependentVariableInstances.GetInstanceIDsUnsorted()), trainIDs);
//        ArrayList<String> overlappingTestIDs = ListUtilities.Intersect(ListUtilities.CreateStringList(Singletons.IndependentVariableInstances.GetInstanceIDsUnsorted()), testIDs);

//        if (overlappingTrainingIDs.size() != trainIDs.size())
//        	Log.ExceptionFatal("At least one of the training IDs was not present in the input data set(s).");
//        if (overlappingTestIDs.size() != testIDs.size())
//        	Log.ExceptionFatal("At least one of the test IDs was not present in the input data set(s).");

        Log.Debug("Do a sanity check to make sure that no instances overlap between the training and test sets");
        if (ListUtilities.Intersect(trainIDs, testIDs).size() > 0)
        {
            String errorMessage = "The training and test sets overlap. ";
            errorMessage += "Training IDs: " + ListUtilities.Join(trainIDs, ", ");
            errorMessage += "Test IDs: " + ListUtilities.Join(testIDs, ", ") + ".";

            throw new Exception(errorMessage);
        }
    }
}