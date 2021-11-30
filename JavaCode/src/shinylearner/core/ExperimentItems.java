package shinylearner.core;

import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;

import java.util.ArrayList;

public class ExperimentItems implements Comparable<ExperimentItems>
{
	public String Description;
	public ArrayList<String> TrainingIDs;
	public ArrayList<String> TestIDs;
	public String AlgorithmScriptFilePath;
	public String AlgorithmType;
	public String AlgorithmDataFormat;
	public ArrayList<String> DataPointsToUse = null;
	public String Key;
	public boolean IsClassificationAnalysis;
	
	public ExperimentItems(int lineNumber, ArrayList<String> lineItems) throws Exception
	{
		Description = ParseItem(lineNumber, lineItems, 0);
		
		String rawTrainIDs = ParseItem(lineNumber, lineItems, 1);
		String rawTestIDs = ParseItem(lineNumber, lineItems, 2);

		TrainingIDs = ListUtilities.CreateStringList(rawTrainIDs.split(","));
		TrainingIDs = ListUtilities.Intersect(TrainingIDs, ListUtilities.CreateStringList(Singletons.Data.InstanceIDs));
		TrainingIDs = ListUtilities.SortStringList(TrainingIDs);
		
		TestIDs = ListUtilities.CreateStringList(rawTestIDs.split(","));
		TestIDs = ListUtilities.Intersect(TestIDs, ListUtilities.CreateStringList(Singletons.Data.InstanceIDs));
		TestIDs = ListUtilities.SortStringList(TestIDs);
		
		CheckTrainTestAssignments();

		AlgorithmScriptFilePath = ParseItem(lineNumber, lineItems, 3);

		//Log.Debug("Will use algorithm script file: " + AlgorithmScriptFilePath);
		
		if (!FileUtilities.FileExists(AlgorithmScriptFilePath))
			Log.ExceptionFatal("No algorithm script file exists at " + AlgorithmScriptFilePath + ".");
		
		String[] fileNameParts = AlgorithmScriptFilePath.split("/");
		AlgorithmType = fileNameParts[fileNameParts.length - 5];
		AlgorithmDataFormat = fileNameParts[fileNameParts.length - 4];

		if (!AlgorithmType.equals("Classification") && !AlgorithmType.equals("Classification_WrapperFS") && !AlgorithmType.equals("FeatureSelection"))
			Log.ExceptionFatal("Invalid algorithm type: " + AlgorithmType);

		if (!AnalysisFileCreator.AcceptedDataFormats.contains(AlgorithmDataFormat))
			Log.ExceptionFatal("Invalid data format: " + AlgorithmDataFormat);

		String rawDataPointsToUse = "";
		if (lineItems.size() > 4)
		{
			rawDataPointsToUse = lineItems.get(4);
			DataPointsToUse = ListUtilities.CreateStringList(rawDataPointsToUse.split(","));
		}
		
		//Key = AlgorithmType + "_" + rawTrainIDs + "_" + rawTestIDs + "_" + AlgorithmDataFormat + "_" + rawDataPointsToUse;
		Key = rawTrainIDs + "_" + rawTestIDs + "_" + AlgorithmDataFormat + "_" + rawDataPointsToUse;
		
		IsClassificationAnalysis = AlgorithmType.startsWith("Classification");
	}
	
	private String ParseItem(int lineNumber, ArrayList<String> lineItems, int index)
	{
		if (lineItems.size() <= index)
			Log.ExceptionFatal("Line " + Integer.toString(lineNumber) + " of " + Settings.EXPERIMENT_FILE + " is missing an entry in column " + Integer.toString(index + 1));
		
		return lineItems.get(index);
	}
	
    private void CheckTrainTestAssignments() throws Exception
    {
        if (TrainingIDs.size() == 0 || TestIDs.size() == 0)
            throw new Exception("No predictions can be made because the training and/or test set have no data.");

        // Make sure the training and test IDs are in the data set we are working with
//        ArrayList<String> overlappingTrainingIDs = ListUtilities.Intersect(ListUtilities.CreateStringList(Singletons.IndependentVariableInstances.GetInstanceIDsUnsorted()), trainIDs);
//        ArrayList<String> overlappingTestIDs = ListUtilities.Intersect(ListUtilities.CreateStringList(Singletons.IndependentVariableInstances.GetInstanceIDsUnsorted()), testIDs);

//        if (overlappingTrainingIDs.size() != trainIDs.size())
//        	Log.ExceptionFatal("At least one of the training IDs was not present in the input data set(s).");
//        if (overlappingTestIDs.size() != testIDs.size())
//        	Log.ExceptionFatal("At least one of the test IDs was not present in the input data set(s).");

        //Log.Debug("Do a sanity check to make sure that no instances overlap between the training and test sets");
        if (ListUtilities.Intersect(TrainingIDs, TestIDs).size() > 0)
        {
            String errorMessage = "The training and test sets overlap. ";
            errorMessage += "Training IDs: " + ListUtilities.Join(TrainingIDs, ", ");
            errorMessage += "Test IDs: " + ListUtilities.Join(TestIDs, ", ") + ".";

            throw new Exception(errorMessage);
        }
    }

	@Override
	public int compareTo(ExperimentItems compareObj)
	{
		return Key.compareTo(compareObj.Key);
	}
}
