package shinylearner.core;

import shinylearner.dataprocessors.AbstractDataProcessor;
import shinylearner.dataprocessors.ArffDataProcessor;
import shinylearner.dataprocessors.DelimitedDataProcessor;
import shinylearner.dataprocessors.TransposedDelimitedDataProcessor;
import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;

import java.io.*;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.zip.GZIPOutputStream;

/** This class provides convenience methods for accessing information about data instances that are used for machine-learning analyses.
 * @author Stephen Piccolo
 */
public class InstanceManager
{
    public static void ParseRawInputData() throws Exception
	{
		if (Settings.RAW_DATA_FILES.size() == 1)
		{
			String dataFilePath = Settings.RAW_DATA_FILES.get(0);
			AbstractDataProcessor dataProcessor = ParseDataProcessor(dataFilePath);

			ArrayList<String> instanceIDs = dataProcessor.ParseInstanceIDs();
			ArrayList<String> dataPointNames = dataProcessor.ParseDataPointNames("");

			if (!dataPointNames.contains("Class"))
			{
				Log.Exception("The input file included no variable named 'Class'.");
				Log.Debug("Here are the top few variable names:");
				for (String dataPointName : dataPointNames)
				    Log.Debug(dataPointName);
				Log.ExceptionFatal("");
			}

			if (dataPointNames.contains("ID"))
				dataPointNames.remove("ID");

			Singletons.Data = new DataInstanceCollection(instanceIDs, dataPointNames);
			dataProcessor.SaveData(Singletons.Data, "");
		}
		else
		{
			HashSet<String> commonInstanceIDs = new HashSet<String>();
			HashSet<String> allDataPointNames = new HashSet<String>();

			for (int i = 0; i < Settings.RAW_DATA_FILES.size(); i++)
			{
				String dataFilePath = Settings.RAW_DATA_FILES.get(i);
				AbstractDataProcessor dataProcessor = ParseDataProcessor(dataFilePath);

				if (i == 0)
					commonInstanceIDs = new HashSet<String>(dataProcessor.ParseInstanceIDs());
				else
				{
					if (Settings.IMPUTE)
					{
						commonInstanceIDs.addAll(dataProcessor.ParseInstanceIDs());
					}
					else
					{
						commonInstanceIDs.retainAll(dataProcessor.ParseInstanceIDs());
					}
				}

				for (String dataPointName : dataProcessor.ParseDataPointNames(dataFilePath + "__"))
				{
					if (dataPointName.equals("Class"))
					{
						if (allDataPointNames.contains("Class"))
							Log.ExceptionFatal("The input files included multiple variables named 'Class.' This is not allowed.");
						else
							allDataPointNames.add("Class");
					}
					else
						allDataPointNames.add(dataPointName);
				}
			}

			if (!allDataPointNames.contains("Class"))
				Log.ExceptionFatal("None of the input files included a variable named 'Class.'");

			if (allDataPointNames.contains("ID"))
				allDataPointNames.remove("ID");

			Singletons.Data = new DataInstanceCollection(new ArrayList<String>(commonInstanceIDs), new ArrayList<String>(allDataPointNames));

			for (int i = 0; i < Settings.RAW_DATA_FILES.size(); i++)
				ParseDataProcessor(Settings.RAW_DATA_FILES.get(i)).SaveData(Singletons.Data, Settings.RAW_DATA_FILES.get(i) + "__");
		}

		if (Singletons.Data.GetNumDataPoints() <= 1)
			Log.ExceptionFatal("The input data contains no data points.");
    }

    private static AbstractDataProcessor ParseDataProcessor(String dataFilePath) throws Exception
    {
    	if (!FileUtilities.FileExists(dataFilePath))
    		Log.ExceptionFatal("A file could not be found at " + dataFilePath);
    	
    	if (dataFilePath.endsWith(".arff") || dataFilePath.endsWith(".arff.gz"))
    		return new ArffDataProcessor(dataFilePath);
    	if (dataFilePath.endsWith(".txt") || dataFilePath.endsWith(".tsv") || dataFilePath.endsWith(".txt.gz") || dataFilePath.endsWith(".tsv.gz"))
    		return new DelimitedDataProcessor(dataFilePath, "\t");
    	if (dataFilePath.endsWith(".csv") || dataFilePath.endsWith(".csv.gz"))
    		return new DelimitedDataProcessor(dataFilePath, ",");
    	if (dataFilePath.endsWith(".ttxt") || dataFilePath.endsWith(".ttsv") || dataFilePath.endsWith(".ttxt.gz") || dataFilePath.endsWith(".ttsv.gz"))
    		return new TransposedDelimitedDataProcessor(dataFilePath, "\t");
    	if (dataFilePath.endsWith(".tcsv") || dataFilePath.endsWith(".tcsv.gz"))
    		return new TransposedDelimitedDataProcessor(dataFilePath, ",");
    	
    	Log.ExceptionFatal("A suitable data processor could not be found for " + dataFilePath);
		return null; // This should never get called
    }
    
    public static void SaveRawInputDataToFile() throws Exception
    {
		PrintWriter printWriter = new PrintWriter(new BufferedWriter(new OutputStreamWriter(new GZIPOutputStream(new FileOutputStream(new File(Settings.ANALYSIS_DATA_FILE), true)), "UTF-8")));

		printWriter.write("\t" + ListUtilities.Join(Singletons.Data.DataPointNames, "\t") + "\n");

		int numInstances = 0;

		for (String instanceID : ListUtilities.SortStringList(Singletons.Data.InstanceIDs))
		{
			if (Singletons.Data.GetClassValue(instanceID).equals("NA"))
			{
				Log.Debug("No class value was specified for instance " + instanceID + ", so it has been excluded from the analysis.");
				continue;
			}

			printWriter.write((instanceID + "\t" + ListUtilities.Join(Singletons.Data.GetValuesForInstance(instanceID, Singletons.Data.DataPointNames), "\t") + "\n"));
			numInstances++;
		}

		printWriter.close();

		Log.Info("After filtering, data were available for " + numInstances + " instances and " + Singletons.Data.GetNumDataPoints() + " data points.");

		if (numInstances < 10)
			Log.ExceptionFatal("The input data contains too few instances [" + numInstances + "].");
    }

    public static void LoadAnalysisData() throws Exception
	{
		DelimitedDataProcessor dataProcessor = new DelimitedDataProcessor(Settings.ANALYSIS_DATA_FILE, "\t");
		ArrayList<String> instanceIDs = dataProcessor.ParseInstanceIDs();
		ArrayList<String> dataPointNames = dataProcessor.ParseDataPointNames("");

		Singletons.Data = new DataInstanceCollection(instanceIDs, dataPointNames);
		dataProcessor.SaveData(Singletons.Data, "");
	}
}
