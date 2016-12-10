package shinylearner.core;

import java.util.ArrayList;

/** This class stores information about a prediction that has been for the dependent variable of a given data instance. It includes information not only about the predicted class but also about the probabilities assigned to each class.
 * @author Stephen Piccolo
 */
public class Prediction
{
    /** Data instance for which the prediction was made. */
    public String InstanceID;
    /** The dependent variable (class) value. */
    public String DependentVariableValue;
    /** The prediction that was made via classification. */
    public String Prediction;
    /** The posterior probability of each class. */
    public ArrayList<Double> ClassProbabilities;

    /** Constructor
     *
     * @param instanceID Data instance for which prediction was made
     * @param dependentVariableValue Actual dependent-variable value of the specified instance
     * @param prediction Predicted dependent-variable value of the specified instance
     * @param classProbabilities Probabilities of each possible dependent-variable value in the same order that the dependent-variable processor orders the possible dependent-variable values.
     */
    public Prediction(String instanceID, String dependentVariableValue, String prediction, ArrayList<Double> classProbabilities) throws Exception
    {
        InstanceID = instanceID;
        DependentVariableValue = dependentVariableValue;
        Prediction = prediction;
        ClassProbabilities = classProbabilities;
    }
}