package shinylearner.dataprocessors;

import shinylearner.core.DataInstanceCollection;

/** This abstract class coordinates all tasks required to parse raw data, transform the data, and describe the data. This class takes care of the generic functionality to accomplish these tasks yet allows the user to develop custom classes that inherit from this class.
 *
 * @author Stephen Piccolo
 */
public abstract class AbstractDataProcessor
{
    /** When this method is executed, raw data is parsed and saved so it can be processed further. Classes that inherit from this class must implement this method if new data are being added.
     *
     * @throws Exception
     */
    public DataInstanceCollection ParseInputData() throws Exception
    {
        throw new Exception("Not implemented");
    }
}