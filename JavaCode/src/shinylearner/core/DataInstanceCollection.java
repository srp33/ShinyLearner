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
	}

	public void SetValues(int instanceIndex, HashMap<String, String> nameValueMap)
	{
		for (String dataPointName : nameValueMap.keySet())
			_data[instanceIndex][_dataPointNameIndexMap.get(dataPointName)] = nameValueMap.get(dataPointName);
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

	private String GetValue(int instanceIndex, int dataPointIndex)
	{
		String value = _data[instanceIndex][dataPointIndex];

		if (value == null)
		{
			Log.Debug(InstanceIDs);
			Log.Debug(DataPointNames);
			Log.ExceptionFatal("No data value has been stored in internal data structure at indices " + instanceIndex + ", " + dataPointIndex);
		}

		return value;
	}

	public ArrayList<String> GetValuesForInstance(String instanceID, ArrayList<String> dataPointNames)
	{
		int instanceIndex = GetIndexOfInstance(instanceID);
		ArrayList<String> values = new ArrayList<String>();

		for (String dataPointName : dataPointNames)
			values.add(GetValue(instanceIndex, GetIndexOfDataPoint(dataPointName)));

		return values;
	}

	public String GetClassValue(String instanceID)
	{
		return GetValue(GetIndexOfInstance(instanceID), _classIndex);
	}

	public ArrayList<String> GetInstanceValuesForDataPoint(String dataPointName)
	{
		int dataPointIndex = GetIndexOfDataPoint(dataPointName);
		ArrayList<String> values = new ArrayList<String>();

		for (int i = 0; i< InstanceIDs.size(); i++)
			values.add(GetValue(i, dataPointIndex));

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
			values.add(GetValue(i, dataPointIndex));

		return new ArrayList<String>(values);
	}

	public ArrayList<String> GetClassOptions()
	{
		return ListUtilities.SortStringList(GetUniqueValuesForDataPointByIndex(_classIndex));
	}
}