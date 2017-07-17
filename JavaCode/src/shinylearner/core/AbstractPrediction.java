package shinylearner.core;

import java.util.ArrayList;

/** This class stores information about a prediction that has been for the dependent variable of a given data instance. It includes information not only about the predicted class but also about the probabilities assigned to each class.
 * @author Stephen Piccolo
 */
abstract class AbstractPrediction
{
    /** Data instance for which the prediction was made. */
    public String InstanceID;
    /** The dependent variable (class) value. */
    public String DependentVariableValue;
    /** The prediction that was made via classification. */
    public String Prediction;
    /** The posterior probability of each class. */
    public ArrayList<String> ClassProbabilities;
}