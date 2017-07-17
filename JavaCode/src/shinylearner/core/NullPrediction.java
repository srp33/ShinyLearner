package shinylearner.core;

import java.util.ArrayList;

/** This class stores information about a prediction that has been for the dependent variable of a given data instance. It includes information not only about the predicted class but also about the probabilities assigned to each class.
 * @author Stephen Piccolo
 */
public class NullPrediction extends AbstractPrediction
{
    /** Constructor
     *
     * @param instanceID Data instance for which prediction was made
     * @param dependentVariableValue Actual dependent-variable value of the specified instance
     */
    public NullPrediction(String instanceID, String dependentVariableValue) throws Exception
    {
        InstanceID = instanceID;
        DependentVariableValue = dependentVariableValue;
        Prediction = "ERROR";

        ClassProbabilities = new ArrayList<String>();
        for (String option : Singletons.Data.GetClassOptions())
            ClassProbabilities.add("NA");
    }
}