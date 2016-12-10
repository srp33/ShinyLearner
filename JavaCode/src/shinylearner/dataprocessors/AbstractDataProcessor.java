package shinylearner.dataprocessors;


import shinylearner.core.DataInstanceCollection;

import java.util.ArrayList;

/** This abstract class coordinates all tasks required to parse raw data, transform the data, and describe the data. This class takes care of the generic functionality to accomplish these tasks yet allows the user to develop custom classes that inherit from this class.
 *
 * @author Stephen Piccolo
 */
public abstract class AbstractDataProcessor
{
	public String DataFilePath = null;

    public ArrayList<String> ParseInstanceIDs() throws Exception
    {
        throw new Exception("Not implemented");
    }

    public ArrayList<String> ParseDataPointNames(String dataPointNamePrefix) throws Exception
    {
        throw new Exception("Not implemented");
    }

    public void SaveData(DataInstanceCollection dataInstanceCollection, String dataPointNamePrefix) throws Exception
    {
        throw new Exception("Not implemented");
    }

    protected String PrefixDataPointName(String dataPointName, String prefix)
    {
        if (dataPointName.equals("Class") || dataPointName.equals("ID"))
            return dataPointName;
        else
            return prefix + dataPointName;
    }

    protected void PrefixDataPointNames(ArrayList<String> dataPointNames, String prefix)
    {
        if (prefix.equals(""))
            return;

        for (int i=0; i<dataPointNames.size(); i++)
            dataPointNames.set(i, PrefixDataPointName(dataPointNames.get(i), prefix));
    }
}