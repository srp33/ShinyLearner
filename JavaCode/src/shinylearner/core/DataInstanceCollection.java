package shinylearner.core;

import shinylearner.helper.ListUtilities;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

/** This class is designed to store all data for a set of data instances. It provides methods that make it easier to create, retrieve, update, and delete data values for these instances.
 * @author Stephen Piccolo
 */
public class DataInstanceCollection
{
	public ArrayList<String> DataPointNames;
	public ArrayList<String> InstanceIDs;
	private String[][] _data;
	private int _classIndex;

	private HashMap<String, Integer> _instanceIndexMap = new HashMap<String, Integer>();
	private HashMap<String, Integer> _dataPointNameIndexMap = new HashMap<String, Integer>();

	private HashSet<String> _missingOptions = new HashSet<String>();

	public DataInstanceCollection(ArrayList<String> instanceIDs, ArrayList<String> dataPointNames)
	{
		DataPointNames = dataPointNames;
		InstanceIDs = instanceIDs;

		_classIndex = DataPointNames.indexOf("Class");
		_data = new String[InstanceIDs.size()][DataPointNames.size()];

		for (int i=0; i<instanceIDs.size(); i++)
			_instanceIndexMap.put(InstanceIDs.get(i), i);
		for (int i = 0; i< DataPointNames.size(); i++)
			_dataPointNameIndexMap.put(DataPointNames.get(i), i);

		_missingOptions.add("?");
		_missingOptions.add("na");
		_missingOptions.add("null");
	}

	public void SetValues(int instanceIndex, HashMap<String, String> nameValueMap)
	{
		for (String dataPointName : nameValueMap.keySet())
		{
			String value = nameValueMap.get(dataPointName);

			if (_missingOptions.contains(value.toLowerCase()))
				value = "NA";

			_data[instanceIndex][_dataPointNameIndexMap.get(dataPointName)] = value;
		}
	}

	public Integer GetIndexOfInstance(String instanceID)
	{
		return _instanceIndexMap.get(instanceID);
	}

	public int GetIndexOfDataPoint(String dataPointName)
	{
		return _dataPointNameIndexMap.get(dataPointName);
	}

	public int GetNumInstances()
	{
		return InstanceIDs.size();
	}

	public int GetNumDataPoints()
	{
		return DataPointNames.size();
	}

	public ArrayList<String> GetDataPointNamesForAnalysis()
	{
		ArrayList<String> dataPointNames = ListUtilities.CreateStringList(DataPointNames);
		dataPointNames.remove("Class");

		return ListUtilities.SortStringList(dataPointNames);
	}

	// The last two arguments are used just for debugging purposes
	private String GetValue(int instanceIndex, int dataPointIndex, String instanceID, String dataPointName)
	{
		String value = _data[instanceIndex][dataPointIndex];

		if (value == null || value.equals("NA"))
		{
			if (Settings.IMPUTE)
			{
				value = "NA";
			}
			else
			{
				Log.Debug(value);
				Log.Debug(InstanceIDs);
				Log.Debug(DataPointNames);
				Log.Debug("No data value has been stored in internal data structure for instance [" + instanceID + "] and data point [" + dataPointName + "] at indices [" + instanceIndex + ", " + dataPointIndex + "].");
				Log.Info("A missing value was found, but imputation is not enabled. Please check the documentation for information on how to enable imputation.");
				Log.Exit(1);
			}
		}

		return value;
	}

	public ArrayList<String> GetValuesForInstance(String instanceID, ArrayList<String> dataPointNames)
	{
		int instanceIndex = GetIndexOfInstance(instanceID);
		ArrayList<String> values = new ArrayList<String>();

		for (String dataPointName : dataPointNames)
			values.add(GetValue(instanceIndex, GetIndexOfDataPoint(dataPointName), instanceID, dataPointName));

		return values;
	}

	public String GetClassValue(String instanceID)
	{
		return GetValue(GetIndexOfInstance(instanceID), _classIndex, instanceID, "Class");
	}

	public ArrayList<String> GetInstanceValuesForDataPoint(String dataPointName)
	{
		int dataPointIndex = GetIndexOfDataPoint(dataPointName);
		ArrayList<String> values = new ArrayList<String>();

		for (int i = 0; i< InstanceIDs.size(); i++)
			values.add(GetValue(i, dataPointIndex, InstanceIDs.get(i), dataPointName));

		return values;
	}

	public ArrayList<String> GetUniqueValuesForDataPoint(String dataPointName)
	{
		return GetUniqueValuesForDataPointByIndex(GetIndexOfDataPoint(dataPointName));
	}

	private ArrayList<String> GetUniqueValuesForDataPointByIndex(int dataPointIndex)
	{
		HashSet<String> values = new HashSet<>();

		for (int i = 0; i< InstanceIDs.size(); i++)
			values.add(GetValue(i, dataPointIndex, "", ""));

		return new ArrayList<String>(values);
	}

	public ArrayList<String> GetClassOptions()
	{
		return ListUtilities.SortStringList(GetUniqueValuesForDataPointByIndex(_classIndex));
	}
}
