package shinylearner.core;

import java.util.ArrayList;
import java.util.HashSet;

import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;

/** This class is designed to store all data for a set of data instances. It provides methods that make it easier to create, retrieve, update, and delete data values for these instances.
 * @author Stephen Piccolo
 */
public class DataInstanceCollection
{
	/** This value is placed at the end of a file that contains a serialized version of this object. It's used to verify that the entire file was stored properly. */
	private static String COMMA_REPLACE_STRING = "_comma_";
	private static String KEY_DELIMITER = "__";

	private HashSet<String> _dataPointNames = new HashSet<String>();
	private HashSet<String> _instanceIDs = new HashSet<String>();

	/** Adds a data value for a given instance to this collection.
	 *
	 * @param dataPointName Data point name
	 * @param instanceID Data instance ID
	 * @param value Data value
	 */
	public void Add(String dataSource, String dataPointName, String instanceID, String value)
	{
		//if (MiscUtilities.IsMissing(value))
		//	return;
		
		if (dataPointName.equals(Settings.DEPENDENT_VARIABLE_NAME))
		{
			if (dataSource != null && Singletons.DependentVariableInstances.containsKey(instanceID))
				Log.ExceptionFatal("Multiple dependent-variable (class) values were detected in the input files for " + instanceID + ". Each instance (sample) may have only one class value.");
		
			Singletons.DependentVariableInstances.put(instanceID, value);
		}
		else
		{
			dataPointName = dataSource == null ? dataPointName : FileUtilities.GetFileName(dataSource) + KEY_DELIMITER + dataPointName;

			Singletons.DatabaseWriter.put(BuildKey(dataPointName, instanceID), value);
	
			_dataPointNames.add(dataPointName);
			_instanceIDs.add(instanceID);
		}
	}
	
	private String BuildKey(String dataPointName, String instanceID)
	{
		return dataPointName + KEY_DELIMITER + instanceID;
	}

	/** Gets a list of all data point names across all data instances in the collection.
	 *
	 * @return List of all data point names
	 */
	public ArrayList<String> GetDataPointNamesSorted()
	{
		return ListUtilities.SortStringList(new ArrayList<String>(_dataPointNames));
	}
	
//	/** Gets a list of all data point names across all data instances in the collection.
//	 *
//	 * @return List of all data point names
//	 */
//	public HashSet<String> GetDataPointNamesUnsorted()
//	{
//		return _dataPointNames;
//	}

	public String GetDataPointValue(String instanceID, String dataPointName)
	{
		return Singletons.DatabaseReader.get(BuildKey(dataPointName, instanceID));
	}

	public ArrayList<String> GetDataPointValues(String instanceID, ArrayList<String> dataPointNames)
	{
		ArrayList<String> values = new ArrayList<String>();

		for (String dataPointName : dataPointNames)
			values.add(GetDataPointValue(instanceID, dataPointName));

		return values;
	}

	/** Gets the data point values across all data instances for the specified data point.
	 *
	 * @param dataPointName Query data point name
	 * @return Data values across all data instances
	 */
	public int GetNumValuesForDataPoint(String dataPointName)
	{
		int num = 0;

		for (String instanceID : _instanceIDs)
			if (HasDataPointValue(instanceID, dataPointName))
				num++;

		return num;
	}

	public int GetNumValuesForInstance(String instanceID)
	{
		int num = 0;

		for (String dataPointName : _dataPointNames)
			if (HasDataPointValue(instanceID, dataPointName))
				num++;

		return num;
	}

	/** Gets a list of data instance IDs for the instances in this collection.
	 *
	 * @return List of all data instance IDs in this collection
	 */
	public ArrayList<String> GetInstanceIDsSorted()
	{
		return ListUtilities.SortStringList(new ArrayList<String>(_instanceIDs));
	}
	
	/** Gets a list of data instance IDs for the instances in this collection.
	 *
	 * @return List of all data instance IDs in this collection
	 */
	public HashSet<String> GetInstanceIDsUnsorted()
	{
		return _instanceIDs;
	}

	/** Indicates the number of data point names across all data instances in this collection.
	 *
	 * @return Number of data point names across all data instances in this collection
	 */
	public int GetNumDataPoints()
	{
		return _dataPointNames.size();
	}

	public int GetNumInstances()
	{
		return _instanceIDs.size();
	}

	/** Identifies all unique values for the specified data point, across all data instances in the collection. Null and missing values are ignored.
	 *
	 * @param dataPointName Query data point name
	 * @return List of all unique values for the specified data point
	 */
	public ArrayList<String> GetUniqueValues(String dataPointName)
	{
		HashSet<String> values = new HashSet<String>();

		for (String instanceID : _instanceIDs)
		{
			String value = GetDataPointValue(instanceID, dataPointName);

			//if (!MiscUtilities.IsMissing(value))
			values.add(value);
		}

		return new ArrayList<String>(values);
	}

	public boolean HasDataPoint(String dataPointName)
	{
		return _dataPointNames.contains(dataPointName);
	}
	
	public boolean HasDataPointValue(String instanceID, String dataPointName)
	{
		return GetDataPointValue(instanceID, dataPointName) != null;
	}
	
	public boolean HasInstance(String instanceID)
	{
		return _instanceIDs.contains(instanceID);
	}

	/** Removes the specified data point from all instances in the collection.
	 *
	 * @param dataPointName Data point to be removed
	 */
	public void RemoveDataPointName(String dataPointName)
	{
		_dataPointNames.remove(dataPointName);
	}

	/** Removes data instances that are in the specified list.
	 *
	 * @param ids List of data instance IDs to be removed
	 */
	public void RemoveInstances(ArrayList<String> ids)
	{
		for (String id : ids)
			RemoveInstance(id);
	}

	/** Removes the specified data instance.
	 *
	 * @param instanceID Data instance ID
	 */
	public void RemoveInstance(String instanceID)
	{
		_instanceIDs.remove(instanceID);
	}

	/** Indicates the number of data instances in this collection.
	 *
	 * @return Number of data instances in this collection
	 */
	public int Size()
	{
		return _instanceIDs.size();
	}

	/** Creates a String representation of this object in a format that can be used for debugging purposes.
	 *
	 * @return Short String representation of this object
	 */
	public String toShortString()
	{
		StringBuilder builder = new StringBuilder();

		ArrayList<String> instanceIDs = GetInstanceIDsSorted();

		for (int i = 0; i<5; i++)
		{
			String instanceID = instanceIDs.get(i);
			builder.append(instanceToString(instanceID) + "\n");
		}

		return builder.toString();
	}

	private String instanceToString(String instanceID)
	{
		StringBuilder output = new StringBuilder();
		output.append(instanceID + ":");

		ArrayList<String> dataPointNames = GetDataPointNamesSorted();

		int numPoints = dataPointNames.size() > 5 ? 5 : dataPointNames.size();

		for (int i=0; i<numPoints; i++)
		{
			String dataPointName = dataPointNames.get(i);
			String dataPointValue = GetDataPointValue(instanceID, dataPointName);

			if (dataPointValue == null)
				dataPointValue = "<null>";

				output.append(dataPointName + "=" + dataPointValue.replace(",", COMMA_REPLACE_STRING) + ",");
		}

		String str = output.toString();
		str = str.substring(0, str.length()-1);
		return str;
	}
}
