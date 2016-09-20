package shinylearner.core;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

import shinylearner.dataprocessors.AbstractDataProcessor;
import shinylearner.dataprocessors.ArffDataProcessor;
import shinylearner.dataprocessors.DelimitedDataProcessor;
import shinylearner.dataprocessors.TransposedDelimitedDataProcessor;
import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;
import shinylearner.helper.MiscUtilities;

/** This class provides convenience methods for accessing information about data instances that are used for machine-learning analyses.
 * @author Stephen Piccolo
 */
public class InstanceVault
{
    /** These are the dependent variable (class) instances. */
    public HashMap<String, String> DependentVariableInstances = new HashMap<String, String>();
    /** These are the unique dependent variable values. They are sorted. */
    public ArrayList<String> DependentVariableOptions = new ArrayList<String>();

    public DataInstanceCollection IndependentVariableInstances = null;

    public InstanceVault LoadDataInstances() throws Exception
    {
    	for (String dataFilePath : Settings.DATA_FILES)
    	{
    		AbstractDataProcessor dataProcessor = ParseDataProcessor(dataFilePath);
    		Log.Debug(dataProcessor.getClass().getName());
    		Log.Debug("Parsing input data from " + dataFilePath);

    		if (IndependentVariableInstances == null)
    			IndependentVariableInstances = dataProcessor.ParseInputData();
    		else
    			IndependentVariableInstances.Add(dataProcessor.ParseInputData());
    	}
    	
    	return this;
    }
    
    public void RefineDataInstances() throws Exception
    {
    	RemoveInstancesWithMissingValues();
    	
        // Look for any data point that contains class information
        ExtractDependentVariableValues(IndependentVariableInstances);
        Log.Debug(DependentVariableInstances.size() + " dependent variable instances");

        Log.Debug("Reconciling dependent variable values");
        HashSet<String> commonInstanceIDs = ListUtilities.Intersect(IndependentVariableInstances.GetInstanceIDsUnsorted(), DependentVariableInstances.keySet());
        
        for (String instanceID : IndependentVariableInstances.GetInstanceIDsUnsorted())
        	if (!commonInstanceIDs.contains(instanceID))
        		IndependentVariableInstances.RemoveInstance(instanceID);
        
        for (String instanceID : DependentVariableInstances.keySet())
        	if (!commonInstanceIDs.contains(instanceID))
        		DependentVariableInstances.remove(instanceID);
        
        if (IndependentVariableInstances.Size() == 0)
        	Log.ExceptionFatal("No independent variable instances were found.");
        if (IndependentVariableInstances.GetNumDataPoints() == 0)
        	Log.ExceptionFatal("No independent variables were found.");            
        if (DependentVariableInstances.size() == 0)
        	Log.ExceptionFatal("No dependent variable instances were found.");
    }
    
    private AbstractDataProcessor ParseDataProcessor(String dataFilePath) throws Exception
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
    
    public void RemoveInstancesWithMissingValues() throws Exception
    {
    	int currentNumInstances = IndependentVariableInstances.GetNumInstances();
    	HashSet<String> dataPointsToRemove = new HashSet<String>();
    	for (String dataPointName : IndependentVariableInstances.GetDataPointNamesSorted())
    		if (IndependentVariableInstances.GetNumValuesForDataPoint(dataPointName) != currentNumInstances)
    			dataPointsToRemove.add(dataPointName);

    	if (dataPointsToRemove.size() > 0)
    	{
    		for (String dataPointName : dataPointsToRemove)
    			IndependentVariableInstances.RemoveDataPointName(dataPointName);
    		
    		Log.Info("WARNING: The following data points were missing a value for at least one instance, so they were removed: " +  ListUtilities.Join(ListUtilities.SortStringList(ListUtilities.CreateStringList(dataPointsToRemove)), "; ") + ". Missing values are not supported at this time.");
    	}

    	int currentNumDataPoints = IndependentVariableInstances.GetNumDataPoints();
    	HashSet<String> instancesToRemove = new HashSet<String>();
    	for (String instanceID : IndependentVariableInstances.GetInstanceIDsUnsorted())
    		if (IndependentVariableInstances.GetNumValuesForInstance(instanceID) != currentNumDataPoints)
    			dataPointsToRemove.add(instanceID);
    	
    	if (instancesToRemove.size() > 0)
    	{
    		for (String instanceID : instancesToRemove)
    			IndependentVariableInstances.RemoveInstance(instanceID);
    		
    		Log.Info("WARNING: The following instances were missing a value for at least one data point, so they were removed: " + ListUtilities.Join(ListUtilities.SortStringList(ListUtilities.CreateStringList(instancesToRemove)), "; ") + ". Missing values are not supported at this time.");
    	}
    }

    /** This method looks in a data instance collection a data point that contains class information. If found, this information is extracted and stored separately.
    *
    * @param dataInstances Data instances that may contain class information
    * @throws Exception
    */
    private void ExtractDependentVariableValues(DataInstanceCollection dataInstances) throws Exception
    {
        if (!dataInstances.HasDataPoint(Settings.DEPENDENT_VARIABLE_NAME))
        	Log.ExceptionFatal("The input data does not contain a variable with the name " + Settings.DEPENDENT_VARIABLE_NAME + ". This is required.");

        for (String instanceID : dataInstances.GetInstanceIDsUnsorted())
        {
            String value = dataInstances.GetDataPointValue(instanceID, Settings.DEPENDENT_VARIABLE_NAME);

//            if (value.equals(Settings.MISSING_VALUE_STRING))
//            	continue;
            
            DependentVariableInstances.put(instanceID, MiscUtilities.FormatClassValue(value));
        }

        dataInstances.RemoveDataPointName(Settings.DEPENDENT_VARIABLE_NAME);
       
        DependentVariableOptions = ListUtilities.SortStringList(ListUtilities.GetUniqueValues(new ArrayList<String>(DependentVariableInstances.values())));
    }

	public HashMap<String, String> GetDependentVariableValues(ArrayList<String> ids)
	{
		HashMap<String, String> results = new HashMap<String, String>();
		
		for (String instanceID : ids)
			results.put(instanceID, DependentVariableInstances.get(instanceID));
		
		return results;
	}

	public void SaveOutputDataFile() throws Exception
	{
		new AnalysisFileCreator(Settings.OUTPUT_DATA_FILE_PATH, IndependentVariableInstances.GetInstanceIDsSorted(), IndependentVariableInstances.GetDataPointNamesSorted()).CreateTabDelimitedFile(true);
	}
}
