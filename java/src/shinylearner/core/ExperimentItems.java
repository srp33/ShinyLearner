package shinylearner.core;

import java.util.ArrayList;

import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;
import shinylearner.helper.MiscUtilities;

public class ExperimentItems
{
	public String Description;
	public ArrayList<String> TrainingIDs;
	public ArrayList<String> TestIDs;
	public String AlgorithmScriptFilePath;
	public String AlgorithmType;
	public String AlgorithmDataFormat;
	public ArrayList<String> DataPointsToUse = null;
	public String UniqueKey;
	
	public ExperimentItems(int lineNumber, ArrayList<String> lineItems) throws Exception
	{
		Description = ParseItem(lineNumber, lineItems, 0);
		
		String rawTrainIDs = ParseItem(lineNumber, lineItems, 1);
		String rawTestIDs = ParseItem(lineNumber, lineItems, 2);

		TrainingIDs = MiscUtilities.FormatNames(ListUtilities.SortStringList(ListUtilities.CreateStringList(rawTrainIDs.split(","))));
		TestIDs = MiscUtilities.FormatNames(ListUtilities.SortStringList(ListUtilities.CreateStringList(rawTestIDs.split(","))));

		AlgorithmScriptFilePath = ParseItem(lineNumber, lineItems, 3);
		
		if (!FileUtilities.FileExists(AlgorithmScriptFilePath))
			Log.ExceptionFatal("No algorithm script file exists at " + AlgorithmScriptFilePath + ".");
		
		String[] fileNameParts = AlgorithmScriptFilePath.split("/");
		AlgorithmType = fileNameParts[fileNameParts.length - 5];
		AlgorithmDataFormat = fileNameParts[fileNameParts.length - 4];

		if (!AlgorithmType.equals("Classification") && !AlgorithmType.equals("FeatureSelection"))
			Log.ExceptionFatal("Invalid algorithm type: " + AlgorithmType);

		if (!AnalysisFileCreator.AcceptedDataFormats.contains(AlgorithmDataFormat))
			Log.ExceptionFatal("Invalid data format: " + AlgorithmDataFormat);

		String rawDataPointsToUse = "";
		if (lineItems.size() > 4)
		{
			rawDataPointsToUse = lineItems.get(4);
			DataPointsToUse = MiscUtilities.FormatNames(ListUtilities.CreateStringList(rawDataPointsToUse.split(",")));
		}
		
		UniqueKey = rawTrainIDs + "____" + rawTestIDs + "____" + AlgorithmDataFormat + "____" + rawDataPointsToUse;
	}
	
	private String ParseItem(int lineNumber, ArrayList<String> lineItems, int index)
	{
		if (lineItems.size() <= index)
			Log.ExceptionFatal("Line " + Integer.toString(lineNumber) + " of " + Settings.EXPERIMENT_FILE + " is missing an entry in column " + Integer.toString(index + 1));
		
		return lineItems.get(index);
	}
}
