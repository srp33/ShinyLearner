package shinylearner.core;

import java.util.ArrayList;
import java.util.HashSet;

import shinylearner.dataprocessors.AbstractDataProcessor;
import shinylearner.dataprocessors.ArffDataProcessor;
import shinylearner.dataprocessors.DelimitedDataProcessor;
import shinylearner.dataprocessors.TransposedDelimitedDataProcessor;
import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;

/** This class provides convenience methods for accessing information about data instances that are used for machine-learning analyses.
 * @author Stephen Piccolo
 */
public class InstanceManager
{
    public static void LoadDataInstances() throws Exception
    {
    	ArrayList<AbstractDataProcessor> dataProcessors = new ArrayList<AbstractDataProcessor>();
    	for (String dataFilePath : Settings.DATA_FILES)
    		dataProcessors.add(ParseDataProcessor(dataFilePath));

    	if (dataProcessors.size() == 1)
    		dataProcessors.get(0).ParseInputData(null);
    	else
    		for (AbstractDataProcessor dataProcessor : dataProcessors)
    			dataProcessor.ParseInputData(dataProcessor.DataFilePath);
    }
    
    public static void RefineDataInstances() throws Exception
    {
    	CheckForMissingValues();
    	
        CheckDependentVariableValues(Singletons.IndependentVariableInstances);
        Log.Debug(Singletons.DependentVariableInstances.size() + " dependent variable instances");

        Log.Debug("Reconciling dependent variable values");
        
        ArrayList<String> instancesToRemove = new ArrayList<String>();
        for (String instanceID : Singletons.IndependentVariableInstances.GetInstanceIDsUnsorted())
        	if (!Singletons.DependentVariableInstances.keySet().contains(instanceID))
        	{
        		Log.Info("WARNING: Data for instance [" + instanceID + "] are excluded from this analysis because there is no dependent-variable (class) value for this instance.");
        		instancesToRemove.add(instanceID);
        	}
        
        for (String instanceID : instancesToRemove)
        	Singletons.IndependentVariableInstances.RemoveInstance(instanceID);
        
        instancesToRemove = new ArrayList<String>();
        for (String instanceID : Singletons.DependentVariableInstances.keySet())
        	if (!Singletons.IndependentVariableInstances.HasInstance(instanceID))
        	{
        		Log.Info("WARNING: Data for instance [" + instanceID + "] are excluded from this analysis because there is no independent-variable data for this instance.");
        		instancesToRemove.add(instanceID);
        	}
        
        for (String instanceID : instancesToRemove)
    		Singletons.DependentVariableInstances.remove(instanceID);

        if (Singletons.IndependentVariableInstances.Size() < 10)
        	Log.ExceptionFatal("An insufficient number of independent variable instances [" + Singletons.IndependentVariableInstances.Size() + "] was found.");
        if (Singletons.IndependentVariableInstances.GetNumDataPoints() == 0)
        	Log.ExceptionFatal("No independent variables were found.");            
        if (Singletons.DependentVariableInstances.size() < 10)
        	Log.ExceptionFatal("An insufficient number of dependent variable instances [" + Singletons.DependentVariableInstances.size() + "] was found.");
        
        Log.Info("After filtering, " + Singletons.DependentVariableInstances.size() + " instances and " + Singletons.IndependentVariableInstances.GetNumDataPoints() + " data points are available for the analysis.");
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
		return null;
    }
    
    public static void CheckForMissingValues() throws Exception
    {
    	int currentNumDataPoints = Singletons.IndependentVariableInstances.GetNumDataPoints();

    	HashSet<String> instancesMissingData = new HashSet<String>();
    	for (String instanceID : Singletons.IndependentVariableInstances.GetInstanceIDsUnsorted())
    		if (Singletons.IndependentVariableInstances.GetNumValuesForInstance(instanceID) != currentNumDataPoints)
    			instancesMissingData.add(instanceID);
    	
    	if (instancesMissingData.size() > 0)
    	{
    		for (String instanceID : instancesMissingData)
    		{
    			Singletons.IndependentVariableInstances.RemoveInstance(instanceID);
    			
    			if (Singletons.DependentVariableInstances.containsKey(instanceID))
    				Singletons.DependentVariableInstances.remove(instanceID);
    		}

    		Log.Info("WARNING: The following instances were missing a value for at least one data point, so they were excluded from the analysis: " + ListUtilities.Join(ListUtilities.SortStringList(ListUtilities.CreateStringList(instancesMissingData)), "; ") + ".");
    	}
    }

    /** This method looks in a data instance collection a data point that contains class information. If found, this information is extracted and stored separately.
    *
    * @param dataInstances Data instances that may contain class information
    * @throws Exception
    */
    private static void CheckDependentVariableValues(DataInstanceCollection dataInstances) throws Exception
    {
    	if (Singletons.DependentVariableInstances.size() == 0)
        	Log.ExceptionFatal("The input data does not contain any dependent-variable (class) values. This is required.");

        Singletons.DependentVariableOptions = ListUtilities.SortStringList(ListUtilities.GetUniqueValues(new ArrayList<String>(Singletons.DependentVariableInstances.values())));
    }

	public static void SaveOutputDataFile() throws Exception
	{
		new AnalysisFileCreator(Settings.OUTPUT_DATA_FILE_PATH, Singletons.IndependentVariableInstances.GetInstanceIDsSorted(), Singletons.IndependentVariableInstances.GetDataPointNamesSorted()).CreateTabDelimitedFile(true);
	}
}
