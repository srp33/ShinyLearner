package mlflexlite.dataprocessors;

import java.util.ArrayList;

import mlflexlite.core.DataInstanceCollection;
import mlflexlite.helper.FileUtilities;
import mlflexlite.helper.ListUtilities;

/** This data processor class is designed to parse text files in the ARFF format.
 * @author Stephen Piccolo
 */
public class ArffDataProcessor extends AbstractDataProcessor
{
    private String _filePath;

    /** This constructor accepts a relative path to an ARFF file that will be parsed.
     * @param filePath Relative or absolute path where the file is located (under the InputData directory)
     */
    public ArffDataProcessor(String filePath)
    {
        _filePath = filePath;
    }

    @Override
    public DataInstanceCollection ParseInputData() throws Exception
    {
    	DataInstanceCollection dataInstances = new DataInstanceCollection();
    	
        int overallInstanceCount = 0;

        ArrayList<String> fileLines = FileUtilities.ReadLinesFromFile(_filePath, "%");

        ArrayList<String> metaRows = ListUtilities.GetValuesStartingWith(fileLines, "@");
        //ArrayList<String> dataRows = ListUtilities.RemoveAll(fileLines, metaRows);
        ArrayList<String> dataRows = ListUtilities.GetValuesNotStartingWith(fileLines, "@");
        metaRows = ListUtilities.Replace(metaRows, "\t", " ");

        if (dataRows.size() == 0)
            throw new Exception("No data rows could be identified in " + _filePath + ".");

        ArrayList<String> attributeNames = ParseAttributeNames(metaRows, _filePath);
        int idIndex = ListUtilities.ToLowerCase(attributeNames).indexOf("id");

        for (int i=0; i<dataRows.size(); i++) {
            overallInstanceCount++;

            ArrayList<String> dataRowItems = ListUtilities.CreateStringList(dataRows.get(i).trim().split(","));
            String instanceID = idIndex == -1 ? "Instance" + overallInstanceCount : dataRowItems.get(idIndex);

            for (int j = 0; j < dataRowItems.size(); j++)
                if (j != idIndex)
                    dataInstances.Add(attributeNames.get(j), instanceID, dataRowItems.get(j));
        }
        
        return dataInstances;
    }

    /** Parses attribute names from the metadata rows in an ARFF file.
     *
     * @param metaRows Metadata rows (those that start with @)
     * @param filePath Path where the ARFF file was stored
     * @return Attribute names
     * @throws Exception
     */
    public static ArrayList<String> ParseAttributeNames(ArrayList<String> metaRows, String filePath) throws Exception
    {
        ArrayList<String> attributeNames = new ArrayList<String>();

        for (String metaRow : metaRows)
        {
            ArrayList<String> metaRowItems = new ArrayList<String>();
            for (String item : ListUtilities.CreateStringList(metaRow.split(" ")))
            	if (item != " ")
            		metaRowItems.add(item);

            String descriptor = metaRowItems.get(0).toLowerCase();

            if (!descriptor.equals("@attribute"))
                continue;

            String attributeName = metaRowItems.get(1).trim();

            if (attributeName.equals("class"))
                attributeName = "Class";

            attributeNames.add(attributeName);
        }

        if (attributeNames.size() == 0 || (attributeNames.size() == 1 && attributeNames.get(0).toLowerCase().equals("id")))
            throw new Exception("No attributes could be identified in " + filePath + ".");

        return attributeNames;
    }
}