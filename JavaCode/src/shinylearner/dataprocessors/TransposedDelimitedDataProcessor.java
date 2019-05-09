package shinylearner.dataprocessors;

import shinylearner.core.DataInstanceCollection;
import shinylearner.helper.BigFileReader;
import shinylearner.helper.ListUtilities;

import java.util.ArrayList;
import java.util.HashMap;

/** This class enables the user to import data directly from delimited (for example, by tabs or commas) text files. This class ignores the final column in the file (which it assumes contains the dependent variable values). The default delimiter is a tab.
 * @author Stephen Piccolo
 */
public class TransposedDelimitedDataProcessor extends AbstractDataProcessor
{
    private String _delimiter;

    public TransposedDelimitedDataProcessor(String filePath, String delimiter)
    {
        DataFilePath = filePath;
        _delimiter = delimiter;
    }

    @Override
    public ArrayList<String> ParseInstanceIDs() throws Exception
    {
        BigFileReader reader = new BigFileReader(DataFilePath);

        ArrayList<String> instanceIDs = ListUtilities.CreateStringList(reader.ReadLine().split(_delimiter));

        reader.Close();

        // Remove name of first column because it should be ignored
        instanceIDs.remove(0);

        // Trim the last column name
        int lastIndex = instanceIDs.size() - 1;
        instanceIDs.set(lastIndex, instanceIDs.get(lastIndex).trim());

        return instanceIDs;
    }

    @Override
    public ArrayList<String> ParseDataPointNames(String dataPointNamePrefix) throws Exception
    {
        BigFileReader reader = new BigFileReader(DataFilePath);

        reader.ReadLine();

        ArrayList<String> dataPointNames = new ArrayList<String>();

        for (String line : reader)
            dataPointNames.add(line.trim().split(_delimiter)[0]);

        reader.Close();

        PrefixDataPointNames(dataPointNames, dataPointNamePrefix);

        return dataPointNames;
    }

    @Override
    public void SaveData(DataInstanceCollection dataInstanceCollection, String dataPointNamePrefix) throws Exception
    {
        ArrayList<String> instanceIDs = ParseInstanceIDs();

        HashMap<String, String> nameValueMap;
        for (int i=0; i<instanceIDs.size(); i++)
        {
            String instanceID = instanceIDs.get(i);

            Integer instanceIndex = dataInstanceCollection.GetIndexOfInstance(instanceID);
            if (instanceIndex == null)
                continue;

            nameValueMap = new HashMap<String, String>();
            BigFileReader reader = new BigFileReader(DataFilePath);
            reader.ReadLine();

            for (String line : reader)
            {
                ArrayList<String> rowValues = ListUtilities.CreateStringList(line.trim().split(_delimiter));
                String dataPointName = PrefixDataPointName(rowValues.remove(0), dataPointNamePrefix);

                nameValueMap.put(dataPointName, rowValues.get(i));
            }

            reader.Close();

            dataInstanceCollection.SetValues(instanceIndex, nameValueMap);
        }
    }
}