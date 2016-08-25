package mlflexlite.core;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;

import mlflexlite.helper.ListUtilities;
import mlflexlite.helper.MiscUtilities;

/** This class is designed to store all data for a set of data instances. It provides methods that make it easier to create, retrieve, update, and delete data values for these instances.
 * @author Stephen Piccolo
 */
public class DataInstanceCollection implements Iterable<String>
{
    /** This value is placed at the end of a file that contains a serialized version of this object. It's used to verify that the entire file was stored properly. */
    public static String END_OF_FILE_MARKER = "[EOF]";
    private static String COMMA_REPLACE_STRING = "_comma_";
    
    private HashMap<String, CompactHashMap<Integer, String>> _instances;
    private CompactHashMap<String, Integer> _valueIndexMap;
    private int _intRefCount;

    /** Default constructor */
    public DataInstanceCollection()
    {
        _instances = new HashMap<String, CompactHashMap<Integer, String>>();
        _valueIndexMap  = new CompactHashMap<String, Integer>(COMPACT_TRANSLATOR_STR_INT);
        _intRefCount = Integer.MIN_VALUE;
    }

    /** Adds a data value for a given instance to this collection.
     *
     * @param dataPointName Data point name
     * @param instanceID Data instance ID
     * @param value Data value
     */
    public void Add(String dataPointName, String instanceID, String value)
    {
    	//if (MiscUtilities.IsMissing(value))
    	//	return;
    	
    	Integer intDataPointName = GetIntRef(MiscUtilities.FormatName(dataPointName));
    	instanceID = MiscUtilities.FormatName(instanceID);

    	if (!_instances.containsKey(instanceID))
    		_instances.put(instanceID, new CompactHashMap<Integer, String>(COMPACT_TRANSLATOR_INT_STR));

    	_instances.get(instanceID).put(intDataPointName, value);
    }
    
    public void Add(DataInstanceCollection newInstances)
    {
    	for (String dataPointName : newInstances.GetDataPointNames())
        	for (String instanceID : newInstances.GetInstanceIDs())
    			Add(dataPointName, instanceID, newInstances.GetDataPointValue(instanceID, dataPointName));
    }
    
    /** Indicates whether this collection contains the specified data instance.
     *
     * @param instanceID Query instance ID
     * @return Whether the collection contains the instance
     */
    public boolean Contains(String instanceID)
    {
        return _instances.containsKey(instanceID);
    }

    /** Gets a collection of data instances that match the specified data instance IDs.
    *
    * @param ids Query data instance IDs
    * @return Collection of data instances for specified data instance IDs
    */
   public DataInstanceCollection Get(ArrayList<String> instanceIDs)
   {
       DataInstanceCollection result = new DataInstanceCollection();
       
       result._valueIndexMap = _valueIndexMap;
       
       for (String instanceID : instanceIDs)
			result._instances.put(instanceID, _instances.get(instanceID));

       return result;
   }
    
    /** Gets a list of all data point names across all data instances in the collection.
    *
    * @return List of all data point names
    */
   public ArrayList<String> GetDataPointNames()
   {
       return ListUtilities.SortStringList(new ArrayList<String>(_valueIndexMap.keySet()));
   }

   /** Gets the data point value for specified instance and data point.
   *
   * @param instanceID Instance ID
   * @param name Data point name
   * @return Data point value
   */
   private String GetDataPointValue(String instanceID, Integer intDataPointName)
   {
	   return _instances.get(instanceID).get(intDataPointName);
	   
//	   CompactHashMap<Integer, String> instance = _instances.get(instanceID);
//	   //HashMap<Integer, String> instance = _instances.get(instanceID);
//	   
//	   if (instance == null)
//		   return Settings.MISSING_VALUE_STRING;
//	   
//	   String value = instance.get(intDataPointName);
//	   
//	   if (value == null)
//		   return Settings.MISSING_VALUE_STRING;
//	   
//	   return value;
   }
   
   public String GetDataPointValue(String instanceID, String dataPointName)
   {
	   return GetDataPointValue(instanceID, GetIntRef(dataPointName));
   }

	/** Gets the data point values across all data instances for the specified data point.
	 *
	 * @param dataPointName Query data point name
	 * @return Data values across all data instances
	 */
	public HashMap<String, String> GetDataPointValues(String dataPointName)
	{
	    HashMap<String, String> values = new HashMap<String, String>();
	
	    for (String instanceID : _instances.keySet())
	        values.put(instanceID, GetDataPointValue(instanceID, dataPointName));
	
	    return values;
	}
    
    /** Gets the data point values across all data instances for the specified data point.
    *
    * @param dataPointName Query data point name
    * @return Data values across all data instances
    */
    public ArrayList<String> GetDataPointValues(String instanceID, ArrayList<String> dataPointNames)
    {
       ArrayList<String> values = new ArrayList<String>();

       for (String dataPointName : dataPointNames)
       	   values.add(GetDataPointValue(instanceID, dataPointName));

       return values;
    }

    /** Gets a list of data instance IDs for the instances in this collection.
     *
     * @return List of all data instance IDs in this collection
     */
    public ArrayList<String> GetInstanceIDs()
    {
        return ListUtilities.SortStringList(new ArrayList<String>(_instances.keySet()));
    }
    
    private Integer GetIntRef(String key)
    {
    	Integer intKey = _valueIndexMap.get(key);

    	if (intKey == null)
    	{
    		intKey = new Integer(_intRefCount);
    		_intRefCount++;

    		_valueIndexMap.put(key, intKey);
    	}
    	
    	return intKey;
    }

    /** Indicates the number of data point names across all data instances in this collection.
     *
     * @return Number of data point names across all data instances in this collection
     */
    public int GetNumDataPoints()
    {
        return _valueIndexMap.size();
    }
    
    public int GetNumDataPoints(String instanceID)
    {
        return _instances.get(instanceID).size();
    }

    /** Identifies all unique values for the specified data point, across all data instances in the collection. Null and missing values are ignored.
     *
     * @param dataPointName Query data point name
     * @return List of all unique values for the specified data point
     */
    public ArrayList<String> GetUniqueValues(String dataPointName)
    {
        HashSet<String> values = new HashSet<String>();

        for (String instanceID : _instances.keySet())
        {
            String value = GetDataPointValue(instanceID, dataPointName);

            //if (!MiscUtilities.IsMissing(value))
            	values.add(value);
        }

        return new ArrayList<String>(values);
    }
    
	public boolean HasDataPoint(String dataPointName)
	{
		return _valueIndexMap.containsKey(dataPointName);
	}
    
    public boolean HasDataPoint(String instanceID, String dataPointName)
    {
    	if (!Contains(instanceID))
    		return false;
    	
    	String value = GetDataPointValue(instanceID, dataPointName);
    	
		return value != null;// && !value.equals(Settings.MISSING_VALUE_STRING);
    }

    /** Removes the specified data point from all instances in the collection.
     *
     * @param dataPointName Data point to be removed
     */
    public void RemoveDataPointName(String dataPointName)
    {
    	Integer intDataPointName = GetIntRef(dataPointName);
    	
        for (String instanceID : this)
        {
        	if (_instances.containsKey(instanceID))
                _instances.get(instanceID).remove(intDataPointName);
        }
        
        _valueIndexMap.remove(dataPointName);
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
    	_instances.remove(instanceID);
    }

    /** Indicates the number of data instances in this collection.
     *
     * @return Number of data instances in this collection
     */
    public int Size()
    {
        return _instances.size();
    }

    public Iterator<String> iterator()
    {
        return GetInstanceIDs().iterator();
    }
    
    /** Creates a String representation of this object in a format that can be used for debugging purposes.
    *
    * @return Short String representation of this object
    */
   public String toShortString()
   {
       StringBuilder builder = new StringBuilder();

       ArrayList<String> instanceIDs = GetInstanceIDs();
       
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
        
        ArrayList<String> dataPointNames = GetDataPointNames();

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
    
    // http://www.nayuki.io/res/compact-hash-map-java/CompactHashMapDemo.java
	private static final CompactMapTranslator<Integer, String> COMPACT_TRANSLATOR_INT_STR = new CompactMapTranslator<Integer, String>() {		
		public boolean isKeyInstance(Object obj) {
			return obj instanceof Integer;
		}
		
		public int getHash(Integer key) {
			return key.hashCode();
		}
		
		public byte[] serialize(Integer key, String value) {
			try {
				byte[] packed = value.getBytes("UTF-8");
				int off = packed.length;
				packed = Arrays.copyOf(packed, off + 4);
				int val = key;
				packed[off + 0] = (byte)(val >>> 24);
				packed[off + 1] = (byte)(val >>> 16);
				packed[off + 2] = (byte)(val >>>  8);
				packed[off + 3] = (byte)(val >>>  0);
				return packed;
			} catch (UnsupportedEncodingException e) {
				throw new AssertionError(e);
			}
		}

		public Integer deserializeKey(byte[] packed) {
			int n = packed.length;
			return (packed[n - 1] & 0xFF) | (packed[n - 2] & 0xFF) << 8 | (packed[n - 3] & 0xFF) << 16 | packed[n - 4] << 24;
		}
		
		public String deserializeValue(byte[] packed) {
			try {
				return new String(packed, 0, packed.length - 4, "UTF-8");
			} catch (UnsupportedEncodingException e) {
				throw new AssertionError(e);
			}
		}
	};

	//http://www.nayuki.io/res/compact-hash-map-java/CompactHashMapDemo.java
	private static final CompactMapTranslator<String,Integer> COMPACT_TRANSLATOR_STR_INT = new CompactMapTranslator<String,Integer>() {
		
		public boolean isKeyInstance(Object obj) {
			return obj instanceof String;
		}
		
		public int getHash(String key) {
			int state = 0;
			for (int i = 0; i < key.length(); i++) {
				state += key.charAt(i);
				for (int j = 0; j < 4; j++) {
					state *= 0x7C824F73;
					state ^= 0x5C12FE83;
					state = Integer.rotateLeft(state, 5);
				}
			}
			return state;
		}
		
		public byte[] serialize(String key, Integer value) {
			try {
				byte[] packed = key.getBytes("UTF-8");
				int off = packed.length;
				packed = Arrays.copyOf(packed, off + 4);
				int val = value;
				packed[off + 0] = (byte)(val >>> 24);
				packed[off + 1] = (byte)(val >>> 16);
				packed[off + 2] = (byte)(val >>>  8);
				packed[off + 3] = (byte)(val >>>  0);
				return packed;
			} catch (UnsupportedEncodingException e) {
				throw new AssertionError(e);
			}
		}
		
		public String deserializeKey(byte[] packed) {
			try {
				return new String(packed, 0, packed.length - 4, "UTF-8");
			} catch (UnsupportedEncodingException e) {
				throw new AssertionError(e);
			}
		}
		
		public Integer deserializeValue(byte[] packed) {
			int n = packed.length;
			return (packed[n - 1] & 0xFF) | (packed[n - 2] & 0xFF) << 8 | (packed[n - 3] & 0xFF) << 16 | packed[n - 4] << 24;
		}
	};
}
