package shinylearner.dataprocessors;

import shinylearner.core.DataInstanceCollection;
import shinylearner.helper.BigFileReader;
import shinylearner.helper.ListUtilities;

import java.util.ArrayList;
import java.util.HashMap;

/** This class enables the user to import data directly from delimited (for example, by tabs or commas) text files. This class ignores the final column in the file (which it assumes contains the dependent variable values). The default delimiter is a tab.
 * @author Stephen Piccolo
 */
public class DelimitedDataProcessor extends AbstractDataProcessor
{
    private String _delimiter;

    public DelimitedDataProcessor(String filePath, String delimiter)
    {
        DataFilePath = filePath;
        _delimiter = delimiter;
    }

    @Override
    public ArrayList<String> ParseInstanceIDs() throws Exception
    {
        BigFileReader reader = new BigFileReader(DataFilePath);

        reader.ReadLine();

        ArrayList<String> instanceIDs = new ArrayList<String>();

        for (String line : reader)
            instanceIDs.add(line.trim().split(_delimiter)[0]);

        reader.Close();

        return instanceIDs;
    }

    @Override
    public ArrayList<String> ParseDataPointNames(String dataPointNamePrefix) throws Exception
    {
        BigFileReader reader = new BigFileReader(DataFilePath);

        ArrayList<String> dataPointNames = ListUtilities.CreateStringList(reader.ReadLine().split(_delimiter));

        reader.Close();

        // Remove name of first column because it should be ignored
        dataPointNames.remove(0);

        // Trim the last column name
        int lastIndex = dataPointNames.size() - 1;
        dataPointNames.set(lastIndex, dataPointNames.get(lastIndex).trim());

        PrefixDataPointNames(dataPointNames, dataPointNamePrefix);

        return dataPointNames;
    }

    @Override
    public void SaveData(DataInstanceCollection dataInstanceCollection, String dataPointNamePrefix) throws Exception
    {
        ArrayList<String> dataPointNames = ParseDataPointNames(dataPointNamePrefix);

        BigFileReader reader = new BigFileReader(DataFilePath);
        reader.ReadLine();

        HashMap<String, String> nameValueMap;
        for (String line : reader)
        {
            ArrayList<String> rowValues = ListUtilities.CreateStringList(line.trim().split(_delimiter));
            String instanceID = rowValues.remove(0);

            Integer masterInstanceIndex = dataInstanceCollection.GetIndexOfInstance(instanceID);

            if (masterInstanceIndex == null)
                continue;

            nameValueMap = new HashMap<String, String>();
            for (int i=0; i<rowValues.size(); i++)
                nameValueMap.put(dataPointNames.get(i), rowValues.get(i));

            dataInstanceCollection.SetValues(masterInstanceIndex, nameValueMap);
        }

        reader.Close();
    }
}