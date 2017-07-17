package shinylearner.dataprocessors;

import shinylearner.core.DataInstanceCollection;
import shinylearner.helper.BigFileReader;
import shinylearner.helper.ListUtilities;
import shinylearner.helper.MiscUtilities;

import java.util.ArrayList;
import java.util.HashMap;

/** This data processor class is designed to parse text files in the ARFF format.
 * @author Stephen Piccolo
 */
public class ArffDataProcessor extends AbstractDataProcessor
{
    /** This constructor accepts a relative path to an ARFF file that will be parsed.
     * @param filePath Relative or absolute path where the file is located (under the InputData directory)
     */
    public ArffDataProcessor(String filePath)
    {
        DataFilePath = filePath;
    }

    @Override
    public ArrayList<String> ParseInstanceIDs() throws Exception
    {
        int idIndex = ParseDataPointNames("").indexOf("ID");

        if (idIndex != -1)
        {
            BigFileReader reader = new BigFileReader(DataFilePath);

            ArrayList<String> instanceIDs = new ArrayList<String>();

            boolean data = false;
            for (String line : reader)
            {
                if (line.startsWith("%"))
                    continue;

                if (line.toUpperCase().startsWith("@DATA"))
                {
                    data = true;
                    continue;
                }

                if (data)
                    instanceIDs.add(ListUtilities.CreateStringList(line.trim().split(",")).get(idIndex));
            }

            reader.Close();

            return instanceIDs;
        }

        BigFileReader reader = new BigFileReader(DataFilePath);

        ArrayList<String> instanceIDs = null;

        for (String line : reader)
        {
            if (line.startsWith("%"))
                continue;

            if (line.toUpperCase().startsWith("@DATA"))
                instanceIDs = new ArrayList<String>();
            else
            {
                if (instanceIDs != null)
                    instanceIDs.add("Instance" + (instanceIDs.size() + 1));
            }
        }

        reader.Close();

        return instanceIDs;
    }

    @Override
    public ArrayList<String> ParseDataPointNames(String dataPointNamePrefix) throws Exception
    {
        BigFileReader reader = new BigFileReader(DataFilePath);

        ArrayList<String> dataPointNames = new ArrayList<String>();
        for (String line : reader)
        {
            if (line.toUpperCase().startsWith("@ATTRIBUTE"))
            {
                ArrayList<String> rowItems = new ArrayList<String>();
                for (String item : ListUtilities.CreateStringList(line.split(" ")))
                    if (item != " ")
                        rowItems.add(item);

                String dataPointName = rowItems.get(1).trim();
                dataPointName = MiscUtilities.trimSpecific(dataPointName, "'");

                if (dataPointName.toUpperCase().equals("ID"))
                    dataPointName = "ID";

                if (dataPointName.toUpperCase().equals("CLASS"))
                    dataPointName = "Class";

                dataPointNames.add(dataPointName);
            }
        }

        reader.Close();

        PrefixDataPointNames(dataPointNames, dataPointNamePrefix);

        return dataPointNames;
    }

    @Override
    public void SaveData(DataInstanceCollection dataInstanceCollection, String dataPointNamePrefix) throws Exception
    {
        ArrayList<String> dataPointNames = ParseDataPointNames(dataPointNamePrefix);
        ArrayList<String> instanceIDs = ParseInstanceIDs();

        BigFileReader reader = new BigFileReader(DataFilePath);

        int instanceCount = -1;

        HashMap<String, String> nameValueMap;
        for (String line : reader)
        {
            if (line.startsWith("%"))
                continue;

            if (line.toUpperCase().startsWith("@DATA"))
                instanceCount = 0;
            else
            {
                if (instanceCount > -1)
                {
                    String instanceID = instanceIDs.get(instanceCount);
                    instanceCount++;

                    int masterInstanceIndex = dataInstanceCollection.GetIndexOfInstance(instanceID);
                    if (masterInstanceIndex == -1)
                        continue;

                    ArrayList<String> rowValues = ListUtilities.CreateStringList(line.trim().split(","));

                    nameValueMap = new HashMap<String, String>();
                    for (int i=0; i<rowValues.size(); i++)
                    {
                        String dataPointName = dataPointNames.get(i);

                        if (dataPointName != "ID")
                            nameValueMap.put(dataPointNames.get(i), MiscUtilities.trimSpecific(rowValues.get(i), "'"));
                    }

                    dataInstanceCollection.SetValues(masterInstanceIndex, nameValueMap);
                }
            }
        }

        reader.Close();
    }
}